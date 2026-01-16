""" Split up traits files into their own separate files sorted by source """
import re
from dataclasses import dataclass
from enum import Enum
from typing import Union, List
import os
import argparse
from shutil import rmtree

# Find all leader classes allowed for the trait
leader_class_re = r'leader_class\s=\s{\s(?P<classnames>(?:\w+\s)+?)}'
leader_class_rx = re.compile(leader_class_re)

# grab the entire code block for leader_potential_add
# (?ms) are global flags that must go at the beginning of the regex
leader_potential_re = r'(?ms)^\t(leader_potential_add = {\n(?P<requirements>.*)^\t}\n)'

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


######################

# This is a dict for faster searching
LEADER_MODIFIER_IDS = {
    "army_modifier": 1,
    "background_planet_modifier": 1,
    "councilor_modifier": 1,
    "federation_modifier": 1,
    "fleet_modifier": 1,
    "galcom_modifier": 1,
    "modifier": 1,
    "planet_modifier": 1,
    "sector_modifier": 1,
    "self_modifier": 1,
    "system_modifier": 1,
    "triggered_army_modifier": 1,
    "triggered_background_planet_modifier": 1,
    "triggered_councilor_modifier": 1,
    "triggered_federation_modifier": 1,
    "triggered_fleet_modifier": 1,
    "triggered_galcom_modifier": 1,
    "triggered_modifier": 1,
    "triggered_planet_modifier": 1,
    "triggered_sector_modifier": 1,
    "triggered_self_modifier": 1,
    "triggered_system_modifier": 1,
}

# If any of these keys are present in the trait, grab them, and save them
# because we will need them to build the trigger to check if the trait can
# be added


# A few scopes that may be used when creating the 'can we add this trait' trigger
class Scopes(Enum):

    COUNTRY = 'country',
    LEADER = 'leader',
    RULER = 'ruler',
    SPECIES = 'species',
    OWNER = 'owner'

TRAIT_ADD_REQUIREMENTS_KEYS_AND_SCOPES = {
    "leader_potential_add": Scopes.LEADER,
    "requires_traits": Scopes.LEADER,
    "requires_governments": Scopes.OWNER,
    "prerequisites": Scopes.OWNER,
    "opposites": Scopes.LEADER,
}

# The values that are allowed for leader classes
class LeaderClass(Enum):

    SCIENTIST = 'scientist'
    COMMANDER = 'commander'
    OFFICIAL = 'official'
    MIXED = 'leader'

class LeaderRarity(Enum):

    COMMON = 'common'
    VETERAN = 'veteran'
    PARAGON = 'paragon'
    FREE = 'free_or_veteran'

# There are some values that would go in place of an int, but have no
# Use like  " 'none' in CustomNoneTypes "
class CustomNoneTypes(Enum):

    NONE_STR = 'none'

# Let's try to stay organized by using this
@dataclass
class LeaderTrait:
    identifier: str  # the trait name
    leader_class_identifier: LeaderClass  # comes from inline_script
    leader_class_list: List[LeaderClass]  # comes from leader_class = { x y z }
    icon: str
    rarity: LeaderRarity
    allowed_for_councilor: bool
    allowed_for_ruler: bool
    tier: Union[int,CustomNoneTypes]
    custom_tooltip_with_modifiers: str
    modifiers: dict
    force_councilor_trait: bool = False


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


def split_traits_files_into_chunks(traits_file_path: str, build_folder: str):
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

        # Split up the file by double line ending
        # We will take comments out later
        # trait_chunks = re.finditer(
        #     r'(?ms)\n\n{.*}', traits_file.read()
        # )
        def trim_newlines(re_match):
            # breakpoint()
            return re_match.group()[1:]

        whole_damn_file = traits_file.read()
        # re.sub(
        #     unwanted_line_breaks_re,
        #     trim_newlines,
        #     whole_damn_file
        # )
        # breakpoint()
        whole_damn_file = whole_damn_file.replace('\n\n ','\n ').replace('\n\n\t','\n\t')

        trait_chunks = iter(
            whole_damn_file.split('\n\n')
        )

        for tmp_trait_chunk in trait_chunks:

            tmp_chunk = tmp_trait_chunk.strip()
            trait_name_matches = trait_id_rx.search(tmp_chunk)
            trait_name = None

            # "quick" cleanup
            if found_unwanted_line_breaks := unwanted_line_breaks_rx.search(tmp_chunk):
                re.sub(
                    unwanted_line_breaks_re,
                    found_unwanted_line_breaks.group(1),
                    tmp_chunk
                )
                breakpoint()

            if script_var_match := script_var_decl_rx.search(tmp_chunk):
                print(
                    f"- Skipping what looks to be a scripted var: {tmp_chunk}"
                )
                # breakpoint()
                continue

            trait_name_match = trait_name_matches

            for name_match_option_rx in [
                trait_id_rx,
                alt_trait_id_rx,
                alt_trait_id_2_rx
            ]:
                if name_match := name_match_option_rx.search(tmp_chunk):
                    trait_name = name_match.group('full_name')

            if not trait_name:
                if tmp_chunk.startswith('####') and tmp_chunk.endswith('####'):
                    print(
                        "- Skipping what looks to be a comment: "
                        # f"{tmp_chunk}"
                    )
                    traits_skipped += 1
                    continue

            if 'leader_trait_type = negative' in tmp_chunk:
                print(
                    f"- Skipping negative trait: {trait_name}"
                )
                traits_skipped += 1
                continue

            if not leader_class_from_script_rx.search(tmp_chunk):
                breakpoint()
            leader_class = leader_class_from_script_rx.search(tmp_chunk).group(1)

            dest_raw_file_name = f"{trait_name}.cwz"  # because it's Clausewitz, but still txt
            dest_raw_file_path = os.path.join(
                RAW_TRAITS_SUBFOLDER_PATH,
                leader_class,
                dest_raw_file_name
            )

            # breakpoint()

            with open(dest_raw_file_path, 'w') as dest_file:
                dest_file.write(tmp_chunk)
            bytes_written = os.path.getsize(dest_raw_file_path)
            print(
                f"+ Wrote {bytes_written} bytes of text to "
                f"{dest_raw_file_name} in {leader_class} folder."
            )
            traits_saved += 1

    traits_file_name = traits_file_path.split(os.path.sep)[-1]
    print(
        f"\nFinished processing {traits_file_name}. {traits_saved} traits saved, {traits_skipped} traits skipped."
    )

if __name__ == "__main__":

    # start_time = time.perf_counter()
    parser = argparse.ArgumentParser(
        prog="0xRetro M&RE Trait File Splitter",
        description="Separate all individual traits to their own files, from a single traits file"
    )
    parser.add_argument(
        '--traits_file',
        help='Location of one or more traits file to chop up',
        required=True,
        nargs="+",
        dest="traits_file_paths"
    )
    parser.add_argument(
        '--skip_clean',
        help='Use this flag to not erase the build_folder traits folder before processing.',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--build_folder',
        help="Location of mrec_tools/build, if it's not a subfolder of where this is being run"
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
    for item in args.traits_file_paths:
        split_traits_files_into_chunks(
            traits_file_path=item,
            build_folder=args.build_folder
        )
