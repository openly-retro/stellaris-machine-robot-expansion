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
import time

import argparse
from json import load as json_load
from json import dump as json_dump

from stellaris_yaml_converter import (
    convert_stellaris_script_to_standard_yaml,
    validate_chopped_up_data
)
from mre_trait_cruncher import (
    read_and_write_traits_data
)
from mre_process_traits_for_codegen import (
    sort_and_filter_pipeline_files,
    write_sorted_filtered_data_to_json_files,
    qa_pipeline_files,
)
from generate_traits_gui_and_effects import (
    # run_codegen_process_for_leadermaking_feature,
    generate_mod_ready_code_files,
    pipeline_make_leader_start_button_code,
    pipeline_make_xvcv_mdlc_core_modifying_ruler_traits_trigger,
    pipeline_make_leader_making_clear_values_effect,
    pipeline_make_xvcv_mdlc_core_modifying_reset_traits_button_effect_lines,
    pipeline_make_core_modifying_subclasses_gui_code,
)
from mre_translation_key_normalizer import do_all_work as do_uppercase_modifier_mapping_work

from mre_common_vars import (
    BUILD_FOLDER,
    LEADER_CLASSES,
    BASE_TRAIT_FILES,
    PIPELINE_OUTPUT_FILES,
    UNICORN,
    INPUT_FILES_FOR_CODEGEN,
)

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
    generated_files = []
    buffer = ''
    for base_file in BASE_TRAIT_FILES:
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
    from mre_process_traits_for_codegen import (
        trickle_up_subclass_requirements
    )
    
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
        sorted_beautiful_data = sorted(output[leader_class], key=lambda x: [*x][0]) 
        # It just feels better having subclasses populated at the end of all this
        output[leader_class] = trickle_up_subclass_requirements(
            sorted_beautiful_data, for_class=leader_class
        )
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

# def generate_leadermaking_feature_code():
#     """ TODO: Deposit localisation and button effects directly into their game code files """
#     for input_file in INPUT_FILES_FOR_CODEGEN:
#         for generated_code_type in ["effects","gui","tooltips"]:
#             run_codegen_process_for_leadermaking_feature(
#                 input_file, generated_code_type=generated_code_type
#             )

def sort_and_write_filtered_trait_data():
    all_traits_processed_data = sort_and_filter_pipeline_files()
    write_sorted_filtered_data_to_json_files(all_traits_processed_data)


if __name__=="__main__":
    start_time = time.perf_counter()
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
    if not os.path.exists(
        os.path.join(
            os.getcwd(),
            'common'
        )
    ):
        sys.exit(
            "!Whoops! Run this script from the mod root folder, not in the mre_code_tools folder,"
            "because it will write to some of the mod files directly."
        )
    sys.stdout.write("***************************************************************\n")
    sys.stdout.write("**** Phase 1 starting! ... ****\n")
    sys.stdout.write("** Resetting the build folder (_boom_)**\n")
    clean_up_build_folder()
    sys.stdout.write("** Reading base Stellaris files & gleefully chopping them up **\n")
    base_files_processed_to_yaml = batch_process_base_files_into_yaml(args.stellaris_path)
    sys.stdout.write("** Sauteeing & serving chopped-up data **\n")
    # Here, we switch from fake YAML to dumping data to JSON, a reliable data standard
    useful_traits_json_files = crunch_trait_data_from_processed_yaml(base_files_processed_to_yaml)
    sys.stdout.write("** Sorting traits data & writing files **\n")
    just_three_traits_files = sort_merge_traits_files(useful_traits_json_files)
    sys.stdout.write("**** Mm mm, delicious, sane, predictable data! ****\n")
    sys.stdout.write("** Doing a QA check on our shiny new datafiles ... **\n")
    qa_pipeline_files()
    sys.stdout.write("***************************************************************\n")
    sys.stdout.write("**** Phase 2 starting! ... ****\n")
    sys.stdout.write("** Sorting, filtering, and getting data ready for code gen scripts ... **\n")
    sort_and_write_filtered_trait_data()
    sys.stdout.write("** Side quest: some modifier loc keys are in uppercase! Fixing ... **\n")
    do_uppercase_modifier_mapping_work(args.stellaris_path)
    sys.stdout.write("***************************************************************\n")
    sys.stdout.write("**** Phase 3 starting! ... Wait, what? there's a Phase 3?? ****\n")
    sys.stdout.write("** Jumpin' jumpgates, time to finally crank out some working mod code! **\n")
    generate_mod_ready_code_files()
    sys.stdout.write("**** Making copy/pasta for dinner! ****\n")
    sys.stdout.write("** Making lines of EFFECTS code for xvcv_mdlc_leader_making_start_button_effect ... **\n")
    pipeline_make_leader_start_button_code()
    sys.stdout.write("** Making lines of TRIGGER code for xvcv_mdlc_core_modifying_ruler_traits_trigger ... **\n")
    pipeline_make_xvcv_mdlc_core_modifying_ruler_traits_trigger()
    sys.stdout.write("** Making lines of EFFECTS code for xvcv_mdlc_leader_making_clear_values_effect ... **\n")
    pipeline_make_leader_making_clear_values_effect()
    sys.stdout.write("** Making lines of EFFECTS code for core_modifying_reset_traits_button_effect ... **\n")
    pipeline_make_xvcv_mdlc_core_modifying_reset_traits_button_effect_lines()
    sys.stdout.write("** Making lines of GUI code for core_modifying subclasses_gui_code ... **\n")
    pipeline_make_core_modifying_subclasses_gui_code()

    sys.stdout.write(
        "\n*burp* We just cranked out a TON of mod code! A lot of it should be in place now.\n"
        "Button effects and localisation files don't need fixing. But go check that the contents look sane.\n"
        "Also, GUI CODE NEEDS TO BE COPIED BY HAND INTO THE .GUI FILES IN THE INTERFACE FOLDER.\n"
        "Look in the build folder for the files starting with 86 and ending in _gui.txt..\n"
    )
    print("** TO DO by humans **")
    print("""
- Look in all build files beginning with 85_. They have code to be copy-pasted to certain effects.
  The file name tells in which effect/place they go where they go.
- Copy/paste from 86_mre_autogenerated_core (or leader) into the 6 gui files. (core modifying and leader making)
""")
    sys.stdout.write("There's still more automation to be done. Till then -- \n")

    print(UNICORN)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    sys.stdout.write(
        f"\nDone in {str(execution_time)[:5]} seconds"
    )