""" Make Python objects from Clausewitz traits files """
from argparse import ArgumentParser
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from shutil import rmtree
from split_traits_files_for_processing import get_trait_name_from_raw_data
from typing import Union, List
import argparse
import os
import re
import threading
import time
from pathlib import Path
import pickle
import time
from multiprocessing import Process, TimeoutError
import json

from leader_trait import (
    LEADER_MODIFIER_IDS,
    Scopes,
    LeaderClass,
    LeaderRarity,
    CustomNoneTypes,
    LeaderTrait,
    TraitGainedType,
    LeaderTier,
    trait_obj_to_json,
)
import sys

TRAITS_FILES_DEST = 'traits_files'
RAW_TRAITS_SUBFOLDER_NAME = 'raw'
PROCESSED_TRAITS_SUBFOLDER_NAME = 'processed'
RAW_TRAIT_EXT = ".cwz"

#########################

# Find all leader classes allowed for the trait
leader_class_re = r'leader_class\s=\s{\s(?P<classnames>(?:\w+\s)+?)}'
leader_class_rx = re.compile(leader_class_re)

# grab the entire code block for leader_potential_add
# (?ms) are global flags that must go at the beginning of the regex
# leader_potential_re = r'(?ms)^\t(leader_potential_add = {\n(?P<requirements>.*)^\t})\n\t'
# leader_potential_re = r'(?m)^\t(leader_potential_add = {\n(?P<requirements>\t\t.*\n)+)\t}\n'
leader_potential_re = r'(?ms)^\t+leader_potential_add\s=\s{\s*(?P<contents>(?:.)+?)^\t}'
leader_potential_rx = re.compile(leader_potential_re)

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

rarity_from_script_re = r'RARITY = (\w+)'
rarity_from_script_rx = re.compile(rarity_from_script_re)

icon_from_script_re = r'ICON = \"{0,1}(\w+)\"{0,1}'
icon_from_script_rx = re.compile(icon_from_script_re)

tier_from_script_re = r'TIER = (\w+|\d)'
tier_from_script_rx = re.compile(tier_from_script_re)

council_from_script_re = r'COUNCIL = (yes|no)'
council_from_script_rx = re.compile(council_from_script_re)

custom_tooltip_re = r'custom_tooltip_with_modifiers = (\w+)'
custom_tooltip_rx = re.compile(custom_tooltip_re)

# allowed origins is typically on one line
# Find all leader classes allowed for the trait
allowed_origins_re = r'allowed_origins\s=\s{\s(?P<origins>(?:\w+\s)+?)}'
allowed_origins_rx = re.compile(allowed_origins_re)

# A few ways to determine if the trait can be added to the ruler

permit_ruler_by_potential_re = r'is_ruler = yes'
permit_ruler_by_starting_re = r'starting_ruler_trait = yes'
# and ofc, ruler name is in the trait name

LEADER_MODIFIER_IDS_KEYS = LEADER_MODIFIER_IDS.keys()

########

def reset_traits_files(build_folder):

    PROCESSED_TRAITS_PATH = os.path.join(
        build_folder,
        TRAITS_FILES_DEST,
        PROCESSED_TRAITS_SUBFOLDER_NAME
    )
    

    if os.path.exists(PROCESSED_TRAITS_PATH):
        rmtree(PROCESSED_TRAITS_PATH)

    os.makedirs(PROCESSED_TRAITS_PATH, exist_ok=True)
    # Sort leader traits into these folders
    for leader_class in [lclass.value for lclass in LeaderClass]:
        os.makedirs(
            os.path.join(
                PROCESSED_TRAITS_PATH, leader_class
            ), 
            exist_ok=True
        )
    print("Traits subfolder in build folder was cleaned up.")

def extract_code_for_named_block(block_name: str, raw_trait_text: str) -> str:
    block_parts = []

    target_block_detected = False
    trait_as_lines = raw_trait_text.split('\n')
    for line in trait_as_lines:
        if block_name in line and target_block_detected == False:
            target_block_detected = True
            continue
        if line == "\t}":
            target_block_detected = False
        if target_block_detected:
            block_parts.append(line)
    return "\n".join(block_parts)


def make_trait_obj_from_raw_text(
    raw_trait_text: str,
    leader_class: LeaderClass,
    trait_name: str,
):

    trait_rarity = rarity_from_script_rx.search(raw_trait_text).group(1)
    try:
        trait_rarity_checked = LeaderRarity(trait_rarity)
    except Exception as ex:
        breakpoint()
    if trait_icon_match := icon_from_script_rx.search(raw_trait_text):
        trait_icon = trait_icon_match.group(1)
    else:
        breakpoint()
    trait_tier = tier_from_script_rx.search(raw_trait_text).group(1)
    if leader_class_list_raw_matches := leader_class_rx.search(raw_trait_text):
        leader_class_list_raw = leader_class_rx.search(raw_trait_text).group('classnames').strip().split(' ')
        leader_classes_list = [
            LeaderClass(class_name) for class_name in leader_class_list_raw
        ]
    else:
        breakpoint()
    custom_tooltip_with_modifiers = None
    leader_potential_add = ''

    # if 'leader_potential_add' in raw_trait_text:
    if leader_potential_add_match := leader_potential_rx.search(raw_trait_text):
        leader_potential_add = leader_potential_add_match.group('contents')
        # breakpoint()

    allowed_for_councilor = 'COUNCIL = yes' in raw_trait_text or 'force_councilor_trait = yes' in raw_trait_text
    allowed_for_ruler = any([
        'is_ruler = yes' in raw_trait_text,
        'starting_ruler_trait = yes' in raw_trait_text,
        'ruler' in trait_name
    ])

    if custom_tooltip_match := custom_tooltip_rx.search(raw_trait_text):
        custom_tooltip_with_modifiers = custom_tooltip_match.group(1)

    
    modifiers = {}
    # Look for any blocks that have modifiers pertaining to the leader, and store them
    modifiers_to_fetch = [
        leader_modifier_key
        for leader_modifier_key in LEADER_MODIFIER_IDS_KEYS
        if re.search(r'\b' + leader_modifier_key + r'\b', raw_trait_text)
    ]
    if len(modifiers_to_fetch):
        for leader_modifier in modifiers_to_fetch:
            # Create a custom regex capturing the contents of 'leader_modifier = { <lines> }'
            leader_modifier_re = r'(?ms)^\t+' + re.escape(leader_modifier) + r'\s=\s{\s*(?P<contents>(?:.)+?)^\t}'
            if modifier_block_match := re.findall(leader_modifier_re, raw_trait_text):
                # Store the raw text as the contents of the named modifier for processing later
                modifiers[leader_modifier] = modifier_block_match

            # If the block/modifier isn't found, that's fine

            # else:
            #     breakpoint()
            # leader_modifier_code = extract_code_for_named_block(
            #     leader_modifier, raw_trait_text
            # )
            # modifiers[leader_modifier] = leader_modifier_code

    # catch some outliers that would not be picked up correctly by the above
    if 'allowed_origins' in raw_trait_text:
        allowed_origins_matches = allowed_origins_rx.search(raw_trait_text)
        allowed_origins_raw = allowed_origins_matches.group('origins').strip()
        allowed_origins_list = allowed_origins_raw.split(' ')
        modifiers['allowed_origins'] = allowed_origins_list

    leader_trait_object = LeaderTrait(
        identifier=trait_name,
        leader_class_identifier=LeaderClass(leader_class),
        leader_class_list=leader_classes_list,
        leader_potential_add=leader_potential_add,
        icon=trait_icon,
        rarity=LeaderRarity(trait_rarity),
        allowed_for_councilor=allowed_for_councilor,
        allowed_for_ruler=allowed_for_ruler,
        tier=LeaderTier(trait_tier),
        custom_tooltip_with_modifiers=custom_tooltip_with_modifiers,
        modifiers=modifiers,
        force_councilor_trait='force_councilor_trait = yes' in raw_trait_text
    )

    # leader_trait_json = {
    #     "identifier": trait_name,
    #     "leader_class_identifier": leader_class,
    #     "leader_class_list": leader_class_list_raw,
    #     "leader_potential_add": leader_potential_add,
    #     "icon": trait_icon,
    #     "rarity": trait_rarity,
    #     "allowed_for_councilor": allowed_for_councilor,
    #     "allowed_for_ruler": allowed_for_ruler,
    #     "tier": trait_tier,
    #     "custom_tooltip_with_modifiers": custom_tooltip_with_modifiers,
    #     "modifiers": modifiers,
    #     "force_councilor_trait": 'force_councilor_trait = yes' in raw_trait_text
    # }

    return leader_trait_object


def copy_trait_for_class(trait_as_obj: LeaderTrait, target_class: LeaderClass) -> LeaderTrait:
    changed_trait = LeaderTrait(
        identifier=trait_as_obj.identifier,  # the trait name
        leader_class_identifier=target_class,  # comes from inline_script
        leader_class_list=[target_class],  # comes from leader_class = { x y z }
        leader_potential_add=trait_as_obj.leader_potential_add,
        icon=trait_as_obj.icon,
        rarity=trait_as_obj.rarity,
        allowed_for_councilor=trait_as_obj.allowed_for_councilor,
        allowed_for_ruler=trait_as_obj.allowed_for_ruler,
        tier=trait_as_obj.tier,
        custom_tooltip_with_modifiers=trait_as_obj.custom_tooltip_with_modifiers,
        modifiers=trait_as_obj.modifiers,
        force_councilor_trait=trait_as_obj.force_councilor_trait,
    )
    return changed_trait


def write_pickle_and_json(trait_as_obj: LeaderTrait, verbose=False) -> None:
    """ Write data and json files to the folder corresponding to the trait's class """
    target_trait_obj_file_name = f"{trait_as_obj.identifier}.pickle"
    trait_as_json = trait_obj_to_json(trait_as_obj)
    # breakpoint()
    target_trait_json_file_name = f"{trait_as_obj.identifier}.json"

    # CUSTOM
    target_trait_obj_file_path = os.path.join(
        dest_folder,
        trait_as_obj.leader_class_identifier,
        target_trait_obj_file_name
    )
    # breakpoint()
    with open(target_trait_obj_file_path, 'wb') as target_trait_file:
         pickle.dump(trait_as_obj, target_trait_file)

    # JSON
    target_trait_json_file_path = os.path.join(
        dest_folder,
        trait_as_obj.leader_class_identifier,
        target_trait_json_file_name
    )
    with open(target_trait_json_file_path, 'w') as target_trait_file:
         json.dump(trait_as_json, target_trait_file, indent=4)

    # Quick QA test
    with open(target_trait_obj_file_path, 'rb') as target_trait_file:
        trait_data = pickle.load(target_trait_file)
        assert trait_data.identifier == trait_as_obj.identifier
        # print(f"= OK: {target_trait_obj_file_path}")
    # Done
    if verbose:
        print(
            f'+ Processed {trait_as_obj.identifier} into the {trait_as_json['leader_class_identifier']} data folder'
        )


def process_files_in_folder(subfolder, verbose=False):

    leader_class = subfolder.split(
        os.path.sep
    )[-1]

    file_list = Path(subfolder).glob(f'**/*{RAW_TRAIT_EXT}')
    num_files = 0

    for trait_file_name in file_list:

        trait_as_obj = None
        trait_as_json = {}
        # breakpoint()

        trait_name = str(trait_file_name).split(os.path.sep)[-1].split('.')[0]
        with open(trait_file_name, 'r') as trait_file_obj:
            trait_as_obj = make_trait_obj_from_raw_text(
                raw_trait_text=trait_file_obj.read(),
                leader_class=leader_class,
                trait_name=trait_name
            )
            # Close file

        # Does this trait get copied to the other leader class folders,
        # because it has multiple classes?

        for leader_class_obj in trait_as_obj.leader_class_list:

            trait_restricted_to_one_class = copy_trait_for_class(
                trait_as_obj=trait_as_obj,
                target_class=leader_class_obj.value,
            )
            # Create the json for this and write it alongside the pickled object
            write_pickle_and_json(trait_restricted_to_one_class, verbose=verbose)

        num_files += 1

    print(f"++ Done with {num_files} traits in {leader_class} folder")


if __name__ == "__main__":

    start_time = time.perf_counter()
    parser = argparse.ArgumentParser(
        prog="0xRetro M&RE Trait File Processor",
        description="Load raw trait texts and pickle them into LeaderTrait objects"
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
        help="Run this script with multiprocessing (faster)",
        action="store_true",
        default=False
    )
    args = parser.parse_args()
    if not os.path.exists(args.build_folder):
        sys.exit(
            f"Couldnt find {args.build_folder}. If you didn't specify its location, then "
            "just run this from the mrec_tools folder"
        )
    traits_build_folder = os.path.join(
        args.build_folder,
        TRAITS_FILES_DEST
    )
    if not os.path.exists(traits_build_folder):
        sys.exit(
            "Didn't see the 'traits_files' folder in the build folder. Did you run "
            "extract/split_traits_files_for_processing ?"
        )

    print(
        f"Let's nibble some files."
    )
    source_folder = os.path.join(
        traits_build_folder,
        'raw'
    )
    dest_folder = os.path.join(
        traits_build_folder,
        PROCESSED_TRAITS_SUBFOLDER_NAME
    )
    leader_class_subfolders = [ f.path for f in os.scandir(source_folder) if f.is_dir() ]
    print(
        f"Going to process traits in {leader_class_subfolders}"
    )
    reset_traits_files(args.build_folder)

    procs = []
    for subfolder in leader_class_subfolders:
        # We know the name of the trait already by reading the file name
        # and we know the class by which folder it's in
        if args.multiproc:
            proc = Process(
                target=process_files_in_folder,
                args=[subfolder,args.verbose]
            )
            procs.append(proc)
            proc.start()
        else:
            process_files_in_folder(subfolder)

    if args.multiproc:
        for proc in procs:
            proc.join()

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(
        f"Done in {str(execution_time)[:5]} seconds"
    )
