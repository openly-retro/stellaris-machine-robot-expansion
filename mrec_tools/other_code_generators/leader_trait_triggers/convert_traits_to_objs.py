""" Make Python objects from Clausewitz traits files """
from argparse import ArgumentParser
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
# leader_potential_re = r'(?ms)^\t+leader_potential_add\s=\s{\s*(?P<contents>(?:.)+?)^\t}'
leader_potential_re = r'(?ms)^\t(leader_potential_add = {\n(?P<requirements>.*)^\t}\n)'
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
    leader_classes_list_raw = leader_class_rx.search(raw_trait_text).group('classnames').strip().split(' ')
    leader_classes_list = [
        LeaderClass(class_name) for class_name in leader_classes_list_raw
    ]
    custom_tooltip_with_modifiers = None
    leader_potential_add = ''

    if leader_potential_add_match := leader_potential_rx.search(raw_trait_text):
        leader_potential_add = leader_potential_add_match.group('requirements')
    # if 'leader_potential_add' in raw_trait_text:
    #     breakpoint()

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
            else:
                breakpoint()
            

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

    leader_trait_json = {
        "identifier": trait_name,
        "leader_class_identifier": leader_class,
        "leader_class_list": leader_classes_list_raw,
        "leader_potential_add": leader_potential_add,
        "icon": trait_icon,
        "rarity": trait_rarity,
        "allowed_for_councilor": allowed_for_councilor,
        "allowed_for_ruler": allowed_for_ruler,
        "tier": trait_tier,
        "custom_tooltip_with_modifiers": custom_tooltip_with_modifiers,
        "modifiers": modifiers,
        "force_councilor_trait": 'force_councilor_trait = yes' in raw_trait_text
    }

    return (leader_trait_object, leader_trait_json)


def pickle_trait(LeaderTrait) -> bytes:
    1



def unpickle_trait(pickled_file_contents) -> LeaderTrait:
    1


def process_files_in_folder(subfolder):

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
            trait_as_obj, trait_as_json = make_trait_obj_from_raw_text(
                raw_trait_text=trait_file_obj.read(),
                leader_class=leader_class,
                trait_name=trait_name
            )

        # Close file
        target_trait_obj_file_name = f"{trait_name}.pickle"
        target_trait_json_file_name = f"{trait_name}.json"

        # CUSTOM
        target_trait_obj_file_path = os.path.join(
            dest_folder,
            leader_class,
            target_trait_obj_file_name
        )
        with open(target_trait_obj_file_path, 'wb') as target_trait_file:
             pickle.dump(trait_as_obj, target_trait_file)

        # JSON
        target_trait_json_file_path = os.path.join(
            dest_folder,
            leader_class,
            target_trait_json_file_name
        )
        # breakpoint()
        with open(target_trait_json_file_path, 'w') as target_trait_file:
             json.dump(trait_as_json, target_trait_file, indent=4)

        # Quick QA test
        with open(target_trait_obj_file_path, 'rb') as target_trait_file:
            trait_data = pickle.load(target_trait_file)
            assert trait_data.identifier == trait_as_obj.identifier
            # print(f"= OK: {target_trait_obj_file_path}")
        # Done
        print(
            f'+ Processed {trait_name} into the {leader_class} data folder'
        )
        num_files += 1

    print(f"++ Done with {num_files} traits in {leader_class} folder")


if __name__ == "__main__":

    start_time = time.perf_counter()
    parser = argparse.ArgumentParser(
        prog="0xRetro M&RE Trait File Processor",
        description="Load raw trait texts and pickle them into LeaderTrait objects"
    )
    parser.add_argument(
        '--pickle',
        help='Export data from Clausewitz traits text to a serialized Python format',
        action="store_true",
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
        # proc = Process(
        #     target=process_files_in_folder,
        #     args=[subfolder,]
        # )
        # procs.append(proc)
        # proc.start()
        process_files_in_folder(subfolder)

    # for proc in procs:
    #     proc.join()

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(
        f"Done in {str(execution_time)[:5]} seconds"
    )
