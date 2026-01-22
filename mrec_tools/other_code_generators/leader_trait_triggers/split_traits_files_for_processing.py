""" Split up traits files into their own separate files sorted by source """
import re
from dataclasses import dataclass
from enum import Enum
import os
import argparse
from shutil import rmtree
import threading
import time
from multiprocessing import Process, TimeoutError
from leader_trait import (
    LEADER_MODIFIER_IDS,
    Scopes,
    LeaderClass,
    LeaderRarity,
    CustomNoneTypes,
    LeaderTrait,
    TraitGainedType,
    LeaderTier,
    TRAITS_TO_EXCLUDE,
)


# Find all leader classes allowed for the trait
leader_class_re = r'leader_class\s=\s{\s(?P<classnames>(?:\w+\s)+?)}'
leader_class_rx = re.compile(leader_class_re)

# grab the entire code block for leader_potential_add
# (?ms) are global flags that must go at the beginning of the regex
leader_potential_re = r'(?ms)^\t(leader_potential_add = {\n(?P<requirements>.*)^\t})\n\t'
leader_potential_rx = re.compile(leader_potential_re)

# a more generic, un-compiled regex for grabbing lines in any first-level block
def grab_block_contents_regex(word_identifier: str) -> str:
    # could be 'potential', 'triggered_self_modifier', etc.
    return r"(?ms)^\t(" + word_identifier + r" = {\n(?P<requirements>.*)^\t}\n)"

# look for 'leader_trait_blalbalb = {' and grab the trait name from that
trait_id_re = r'(?ms)^(?P<full_name>leader_trait_(?P<trait_series>\w+))\s=\s{'
trait_id_rx = re.compile(trait_id_re)

# trait_ruler_blabla
alt_trait_id_re = r'(?ms)^(?P<full_name>trait_ruler_(?P<trait_series>\w+))\s=\s{'
alt_trait_id_rx = re.compile(alt_trait_id_re)

# and then there's trait_imperial_heir lurking about
# breaking all the patterns
alt_trait_id_2_re = r'(?ms)^(?P<full_name>trait_(?P<trait_series>\w+))\s=\s{'
alt_trait_id_2_rx = re.compile(alt_trait_id_2_re)

# Not multiline
leader_class_from_script_re = r'CLASS = (\w+)'
leader_class_from_script_rx = re.compile(leader_class_from_script_re)

# scripted variable declaration
script_var_decl_re = r'(?ms)^\@(\w+)\s=\s.*$'
script_var_decl_rx = re.compile(script_var_decl_re)

# line breaks in the middle of a trait >_>
unwanted_line_breaks_re = r'(?ms)\n(?P<keepme>\n[\s+|\t+])'
unwanted_line_breaks_rx = re.compile(unwanted_line_breaks_re)

#
TRAITS_FILES_DEST = 'traits_files'
RAW_TRAITS_SUBFOLDER_NAME = 'raw'
PROCESSED_TRAITS_SUBFOLDER_NAME = 'processed'


class TraitNameNotFound(Exception):
    pass


######################


# ripped from https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

RED_DASH = f"{bcolors.FAIL}-{bcolors.ENDC}"
GREEN_PLUS = f"{bcolors.OKGREEN}+{bcolors.ENDC}"

######

def reset_traits_build_files(build_folder):

    RAW_TRAITS_SUBFOLDER_PATH = os.path.join(build_folder, TRAITS_FILES_DEST, RAW_TRAITS_SUBFOLDER_NAME)
    PROCESSED_TRAITS_PATH = os.path.join(build_folder, TRAITS_FILES_DEST, PROCESSED_TRAITS_SUBFOLDER_NAME)
    

    if os.path.exists(
        os.path.join(build_folder, TRAITS_FILES_DEST)
    ):
        rmtree(
            os.path.join(build_folder, TRAITS_FILES_DEST)
        )

    os.makedirs(RAW_TRAITS_SUBFOLDER_PATH, exist_ok=True)
    os.makedirs(PROCESSED_TRAITS_PATH, exist_ok=True)
    # Sort leader traits into these folders
    for leader_class in [lclass.value for lclass in LeaderClass]:
        os.makedirs(
            os.path.join(
                RAW_TRAITS_SUBFOLDER_PATH, leader_class
            ), 
            exist_ok=True
        )
        os.makedirs(
            os.path.join(
                PROCESSED_TRAITS_PATH, leader_class
            ), 
            exist_ok=True
        )
    print("Traits subfolder in build folder was cleaned up.")

def get_trait_name_from_raw_data(trait_raw_text: str) -> str:

    trait_name_matches = trait_id_rx.search(trait_raw_text)
    trait_name = None
    trait_name_match = trait_name_matches

    for name_match_option_rx in [
        trait_id_rx,
        alt_trait_id_rx,
        alt_trait_id_2_rx
    ]:
        if name_match := name_match_option_rx.search(trait_raw_text):
            trait_name = name_match.group('full_name')

    if not trait_name:
        raise
    return trait_name

def find_trait_name_in_data(trait_raw_text) -> str:
    trait_name_matches = trait_id_rx.search(trait_raw_text)
    trait_name = None
    trait_name_match = trait_name_matches

    for name_match_option_rx in [
        trait_id_rx,
        alt_trait_id_rx,
        alt_trait_id_2_rx
    ]:
        if name_match := name_match_option_rx.search(trait_raw_text):
            trait_name = name_match.group('full_name')

    if not trait_name:
        raise TraitNameNotFound(trait_raw_text)

    return trait_name


def split_traits_files_into_chunks(
    traits_file_path: str, build_folder: str, verbose: bool = False
):
    """ Do the main work of splitting up the big traits files """
    file_name_to_source_leader_class = {
        "general": "commander",
        "admiral": "commander",
        "governor": "official",
        "scientist": "scientist",
        "ambassador": "official",
        "delegate": "official",
    }

    known_leader_subclass_by_file_name = {
        "delegate": "subclass_official_delegate",
        "ambassador": "subclass_official_delegate",
    }

    RAW_TRAITS_SUBFOLDER_PATH = os.path.join(build_folder, TRAITS_FILES_DEST, RAW_TRAITS_SUBFOLDER_NAME)
    PROCESSED_TRAITS_PATH = os.path.join(build_folder, TRAITS_FILES_DEST, PROCESSED_TRAITS_SUBFOLDER_NAME)

    traits_saved = 0
    traits_skipped = 0

    with open(traits_file_path, 'r') as traits_file:

        entire_file = traits_file.read()
        # Take out the unexpected line breaks inside of traits
        entire_file = entire_file.replace('\n\n ','\n ').replace('\n\n\t','\n\t')

        trait_chunks = iter(
            entire_file.split('\n\n')
        )

        for tmp_trait_chunk in trait_chunks:

            tmp_chunk = tmp_trait_chunk.strip()

            if script_var_match := script_var_decl_rx.search(tmp_chunk):
                if verbose:
                    print(
                        f"{RED_DASH} Skipping what looks to be a scripted var: {tmp_chunk}"
                    )
                # breakpoint()
                continue

            if tmp_chunk.startswith('####') and tmp_chunk.endswith('####'):
                if verbose:
                    print(
                        f"{RED_DASH} Skipping what looks to be a comment: "
                        f"{tmp_chunk}"
                    )
                traits_skipped += 1
                continue

            try:
                trait_name = find_trait_name_in_data(tmp_chunk)
            except TraitNameNotFound:
                if tmp_chunk.strip().startswith('#leader_trait_'):
                    if verbose:
                        print(
                            f"{RED_DASH} Skipping commented trait: {trait_name}"
                        )
                    continue
                else:
                    print(
                        f"{RED_DASH} Broken trait? {tmp_chunk}"
                    )
                    traits_skipped += 1
                    continue

            # Must skip these, reasons are documented next to the object
            if TRAITS_TO_EXCLUDE.get(trait_name):
                if verbose:
                    print(
                        f"{RED_DASH} Skipping excluded trait: {trait_name}"
                    )
                traits_skipped += 1
                continue

            if 'script = trait/icon' not in tmp_chunk:
                if verbose:
                    print(
                        f"{RED_DASH} Skipping non-leader trait"
                    )
                    traits_skipped += 1
                continue

            # Now we can do skips because we have the trait name
            if 'is_machine_empire = no' in tmp_chunk:
                if verbose:
                    print(
                        f"{RED_DASH} Skipping non-machine empire trait: {trait_name}"
                    )
                traits_skipped += 1
                continue

            if 'leader_trait_type = negative' in tmp_chunk:
                if verbose:
                    print(
                        f"{RED_DASH} Skipping negative trait: {trait_name}"
                    )
                traits_skipped += 1
                continue

            if not leader_class_from_script_rx.search(tmp_chunk):
                # Might be a generic tier 1 starting trait
                if leader_classes_match := leader_class_rx.search(tmp_chunk):
                    if len(leader_classes_match.group(1)) > 1:
                        leader_class = 'leader'
                        # breakpoint()
                    else:
                        leader_class = leader_classes_match.group(1)[0]
                        # breakpoint()
            else:
                leader_class = leader_class_from_script_rx.search(tmp_chunk).group(1)

            dest_raw_file_name = f"{trait_name}.cwz"  # because it's Clausewitz, but still txt
            dest_raw_file_path = os.path.join(
                RAW_TRAITS_SUBFOLDER_PATH,
                leader_class,
                dest_raw_file_name
            )

            with open(dest_raw_file_path, 'w') as dest_file:
                dest_file.write(tmp_chunk)
            bytes_written = os.path.getsize(dest_raw_file_path)
            if verbose:
                print(
                    f"{GREEN_PLUS} Wrote {bytes_written} bytes of text to "
                    f"{dest_raw_file_name} in {leader_class} folder."
                )
            traits_saved += 1

    traits_file_name = traits_file_path.split(os.path.sep)[-1]
    print(
        f"\nFinished processing {traits_file_name}. {traits_saved} traits saved, {traits_skipped} traits skipped."
    )

if __name__ == "__main__":

    start_time = time.perf_counter()
    parser = argparse.ArgumentParser(
        prog="0xRetro M&RE Trait File Splitter",
        description="Separate all individual traits to their own files, from a single traits file"
    )
    parser.add_argument(
        '--traits_file_path',
        help='Location of one or more traits file to chop up. This can be a full path to a trait file in the Stellaris folder, or a trait file in a mod somewhere. If you just want to parse files in the Stellaris folder, better to use --stellaris_folder with --vanilla_traits_files',
        nargs="+",
    )
    parser.add_argument(
        '--stellaris_folder',
        help='Location of Stellaris folder. On Linux systems this is .local/share/Steam/steamapps/common/Stellaris',
        required=False
    )
    parser.add_argument(
        '--vanilla_traits_files',
        help="Name of one or more traits files in stellaris_folder/common/traits to process. Must give --stellaris_folder argument",
        required=False,
        nargs="+",
    )
    parser.add_argument(
        '--skip_clean',
        help='Use this flag to not erase the build_folder traits folder before processing.',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--build_folder',
        help="Location of mrec_tools/build, if it's not a subfolder of where this is being run",
        required=True
    )
    parser.add_argument(
        '--verbose',
        help="Print out extra information during processing",
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--multiproc',
        help="Run this Python code using multiprocessing (faster). Don't use this flag if you want to debug the script.",
        default=False,
        action="store_true"
    )
    args = parser.parse_args()
    if not os.path.exists(args.build_folder):
        sys.exit(
            f"Couldnt find {args.build_folder}. If you didn't specify its location, then "
            "just run this from the mrec_tools folder"
        )
    print(
        f"Let's chop some files."
    )
    if not args.skip_clean:
        reset_traits_build_files(args.build_folder)
    else:
        print("Skipping cleaning the build folder before starting.")
    
    # threads = []
    # # file_q = Queue()
    # max_processes = 4 if len(args.traits_file_paths) > 4 else len(args.traits_file_paths)

    # with Pool(processes=max_processes) as pool:
    procs = []

    file_paths_to_process = []

    # User has given one flag, but not the other
    if not (args.stellaris_folder and args.vanilla_traits_files):
        sys.exit(
            "Specify both --stellaris_folder and --vanilla_traits_files, not one or the other."
        )
    else:
        if not os.path.exists(args.stellaris_folder):
            sys.exit(f"Couldn't find where you said the Stellaris folder was: {args.stellaris_folder}")
        else:
            vanilla_files_to_process = [
                os.path.join(
                    args.stellaris_folder,
                    'common', 'traits', vanilla_trait_filename
                )
                for vanilla_trait_filename in args.vanilla_traits_files
            ]
            file_paths_to_process.extend(vanilla_files_to_process)

    # Respect any full trait file paths given in this arg
    if args.traits_file_path:
        for other_trait_file_path in args.traits_file_path:
            file_paths_to_process.append(other_trait_file_path)


    # Get to work
    for item in file_paths_to_process:

        if args.multiproc:
            proc = Process(
                target=split_traits_files_into_chunks,
                kwargs={
                    "traits_file_path": item,
                    "build_folder": args.build_folder,
                    "verbose": args.verbose
                }
            )
            procs.append(proc)
            proc.start()
        else:
            split_traits_files_into_chunks(
                traits_file_path=item,
                build_folder=args.build_folder,
                verbose=args.verbose
            )

    # Time for some Zro tea
    if args.multiproc:
        for proc in procs:
            proc.join()

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(
        f"Done in {str(execution_time)[:5]} seconds"
    )