#!/usr/bin/env python
""" Load & transform base Stellaris traits files for use in the Machines & Robots Expansion mod """

__author__ = "0xRetro (openly-retro)"
__license__ = "GPLv3"
__version__ = "1.0"

import os
from shutil import rmtree
import sys
from operator import itemgetter
from random import randint

import argparse
from json import load as json_load
from json import dump as json_dump

from stellaris_yaml_converter import (
    convert_stellaris_script_to_standard_yaml,
    validate_chopped_up_data
)
from stellaris_trait_cruncher import (
    read_and_write_traits_data
)

BUILD_FOLDER = os.path.join(
    os.getcwd(),
    'build'
)

LEADER_CLASSES = [
    "commander", "official", "scientist"
]

def clean_up_build_folder():
    if os.path.exists(BUILD_FOLDER):
        rmtree(BUILD_FOLDER)
    os.makedirs(BUILD_FOLDER, exist_ok=True)

def make_converted_filename(base_filename):
    without_ext = base_filename.split('.')[0]
    updated_name = f"{without_ext}_as_yaml.txt"
    return os.path.join(
        BUILD_FOLDER, updated_name
    )

def batch_process_base_files_into_yaml(stellaris_path: str) -> list:
    base_traits_files = [
        "00_admiral_traits.txt",
        "00_general_traits.txt",
        "00_generic_leader_traits.txt",
        "00_governor_traits.txt",
        "00_scientist_traits.txt",
        "00_starting_ruler_traits.txt"
    ]
    generated_files = []
    buffer = ''
    for base_file in base_traits_files:
        base_file_path = os.path.join(
            stellaris_path, 'common', 'traits', base_file
        )
        if not os.path.exists(base_file_path):
            sys.exit(
                f"Couldnt find {base_file_path}. Check that you entered the correct "
                "base path for Stellaris (the folder with \\common\\ in it)"
            )
        with open(base_file_path, "r") as base_traits_file:
            buffer = convert_stellaris_script_to_standard_yaml(
                base_traits_file.read()
            )
            validate_chopped_up_data(buffer)
        target_converted_file_name = make_converted_filename(base_file)
        generated_files.append(target_converted_file_name)
        with open(target_converted_file_name, "w") as dest_file:
            dest_file.write(buffer)
            sys.stdout.write(
                f"Chopped up base file {base_file} successfully. Written to {dest_file.name}\n"
            )
    return generated_files

def crunch_trait_data_from_processed_yaml(generated_files_list: list):
    # Iterate each pseudo-yaml file, trim traits, sort into leader classes, write to JSON
    base_files_as_sorted_trimmed_json = []
    for source_yaml_file in generated_files_list:
        _buffer = ''
        sorted_data = ''
        base_filename = source_yaml_file.split('_as_yaml.txt')[0]
        target_filename = os.path.join(
            BUILD_FOLDER, f"{base_filename}_useful_traits.json"
        )
        read_and_write_traits_data(
            source_yaml_file, target_filename, format="json"
        )
        base_files_as_sorted_trimmed_json.append(target_filename)
    return base_files_as_sorted_trimmed_json

def sort_merge_traits_files(useful_yaml_traits_files):
    """ From several Stellaris traits files we mangled & filtered, merge & sort all data """
    output = {
        "commander": [],
        "scientist": [],
        "official": []
    }
    buffer = ''
    for file in useful_yaml_traits_files:
        with open(file, "r") as input_file:
            buffer = json_load(input_file)
        for leader_class in LEADER_CLASSES:
            # breakpoint()
            output[leader_class] = output[leader_class] + buffer[leader_class]

    # Now, sort all traits per class
    for leader_class in LEADER_CLASSES:
        # breakpoint()
        output[leader_class] = sorted(output[leader_class], key=lambda x: [*x][0]) 

    # Now, write each classes' traits to a file
    target_filenames = []
    for leader_class in LEADER_CLASSES:
        newfile_name = f"00_mre_{leader_class}_traits.json"
        newfilepath = os.path.join(BUILD_FOLDER, newfile_name)
        with open(newfilepath, "w") as traitsfile:
            json_dump(output[leader_class], traitsfile, indent=4)
            print(f"Wrote {leader_class} data to {newfilepath}")
            target_filenames.append(newfilepath)
    return target_filenames

if __name__=="__main__":
    parser = argparse.ArgumentParser(
        prog="0xRetro M&RE Trait Data Pipeline",
        description="Scrape base traits files, convert to yaml-ish format, trim & sort trait data that we want for processing later"
    )
    parser.add_argument(
        '--stellaris_path',
        help='Location of base Stellaris game files',
        required=True
    )
    args = parser.parse_args()
    if not os.path.exists(args.stellaris_path):
        sys.exit(
            f"Couldnt find {args.stellaris_path}. Check that you entered the correct "
            "base path for Stellaris (the folder with \\common\\ in it)"
        )
    sys.stdout.write(
        "Starting the M&RE Trait Data pipeline, phase 1: Make trait data fun to play with!\n"
        f"Code by 0xRetro. Sanity levels at {randint(15,115)}% of normal.\n"
    )
    sys.stdout.write("** Resetting the build folder **\n")
    clean_up_build_folder()
    sys.stdout.write("** Reading base files & chopping them up **\n")
    base_files_processed_to_yaml = batch_process_base_files_into_yaml(args.stellaris_path)
    sys.stdout.write("** Crunching & filtering chopped-up data **\n")
    # Here, we switch from fake YAML to dumping data to JSON, a reliable data standard
    useful_traits_json_files = crunch_trait_data_from_processed_yaml(base_files_processed_to_yaml)
    sys.stdout.write("** Sorting traits data & writing files **\n")
    just_three_traits_files = sort_merge_traits_files(useful_traits_json_files)
    sys.stdout.write("**** Mm mm, delicious, sane, predictable data! ****\n")
    sys.stdout.write(
        "Let's see how we did! Inspect these files in the build folder for errors:\n"
    )
    sys.stdout.write(
        "\n".join([f"00_mre_{leader_class}_traits.json" for leader_class in LEADER_CLASSES])
    )
