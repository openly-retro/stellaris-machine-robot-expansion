import os
from shutil import rmtree
import sys

import argparse
from yaml import safe_load, safe_dump

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

def clean_up_build_folder():
    if os.path.exists(BUILD_FOLDER):
        rmtree(BUILD_FOLDER)
    else:
        os.makedirs(BUILD_FOLDER)

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
        with open(target_converted_file_name, "w+") as dest_file:
            dest_file.write(buffer)
            sys.stdout.write(
                f"Chopped up base file {base_file} successfully. Written to {dest_file}"
            )
    return generated_files

def crunch_trait_data_from_processed_yaml(generated_files_list: list):
    # Iterate each pseudo-yaml file, trim traits, sort into leader classes, write to real yaml
    base_files_as_sorted_trimmed_yaml = []
    for source_yaml_file in generated_files_list:
        _buffer = ''
        sorted_data = ''
        base_filename = source_yaml_file.split('_as_yaml.txt')[0]
        target_filename = os.path.join(
            BUILD_FOLDER, f"{base_filename}_useful_traits.yaml"
        )
        read_and_write_traits_data(
            source_yaml_file, target_filename
        )
        base_files_as_sorted_trimmed_yaml.append(target_filename)
    return base_files_as_sorted_trimmed_yaml

def sort_merge_traits_files(useful_yaml_traits_files):
    """ From several Stellaris traits files we mangled & filtered, merge & sort all data """
    output = {
        "commander": [],
        "scientist": [],
        "official": []
    }
    for file in useful_yaml_traits_files:
        buffer = safe_load(file)
        for leader_class in ["official", "scientist", "commander"]:
            output[leader_class] = [*output[leader_class], *buffer[leader_class]]

    # Now, sort all traits per class
    for leader_class in ["official", "scientist", "commander"]:
        output[leader_class] = sorted(output[leader_class], key=lambda t: t['trait_name']) 
    
    # Now, write each classes' traits to a file

    for leader_class in ["official", "scientist", "commander"]:
        newfile_name = f"00_mre_{leader_class}_traits.yml"
        newfilepath = os.path.join(BUILD_FOLDER, newfile_name)
        with open(newfilepath, "w+") as traitsfile:
            traitsfile.write(
                safe_dump(output[leader_class])
            )
            print(f"Wrote {leader_class} data to {newfilepath}")

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
    clean_up_build_folder()
    base_files_processed_to_yaml = batch_process_base_files_into_yaml(args.stellaris_path)
    useful_traits_yaml_files = crunch_trait_data_from_processed_yaml(base_files_processed_to_yaml)
    just_three_traits_files = sort_merge_traits_files(useful_traits_yaml_files)
    sys.stdout.write(
        f"Let's see how we did! Inspect {just_three_traits_files} for errors."
    )
