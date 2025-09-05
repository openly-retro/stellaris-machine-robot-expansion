#!/usr/bin/env python
""" Load & transform base Stellaris traits files for use in the Machines & Robots Expansion mod """

__author__ = "0xRetro (openly-retro)"
__license__ = "GPLv3"
__version__ = "2.0"

from random import randint
from shutil import rmtree
import os
import sys
import time

import argparse

from pipeline.compile.copy_fx_and_triggers import copy_effects_to_common, copy_triggers_to_common
from pipeline.extract.main import (
    batch_convert_traits_files_into_json,
    read_and_sort_extracted_traits,
)
from pipeline.transform.sort_and_filter import (
    sort_and_filter_pipeline_files,
    write_sorted_filtered_data_to_json_files,
    qa_pipeline_files,
)
from pipeline.compile.main import (
    # run_codegen_process_for_leadermaking_feature,
    generate_fx_tooltips_interfaces_for_all_guis,
    pipeline_make_leader_start_button_code,
    pipeline_stitch_xvcv_mdlc_leader_making_start_button_effect,
    pipeline_make_xvcv_mdlc_core_modifying_ruler_traits_trigger,
    pipeline_make_leader_making_clear_values_effect,
    pipeline_make_xvcv_mdlc_core_modifying_reset_traits_button_effect_lines,
    pipeline_make_core_modifying_subclasses_gui_code,
    pipeline_make_xvcv_mdlc_core_modifying_still_has_subclass_traits_picked,
)
from pipeline.extract.mre_translation_key_normalizer import do_all_work as do_uppercase_modifier_mapping_work
from pipeline.extract.harvest_machine_tooltips import do_all_work as harvest_machine_tooltips
from pipeline.compile.councilor_editor_gui import do_all_work as generate_councilor_editor_gui
from pipeline.compile.councilor_editor_scripted_triggers import do_all_work as generate_councilor_editor_scripted_triggers
from pipeline.compile.councilor_editor_button_effects import do_all_work as generate_councilor_editor_button_effects
from pipeline.compile.councilor_editor_button_effects_extra import do_all_work as generate_councilor_gui_traits_limits_effects
from pipeline.compile.core_modifying_button_effects_extra import do_all_work as generate_ruler_limits_scripted_effect
from pipeline.compile.mre_stitch_gui_files import stitch_gui_files_and_write_to_game_folder

from pipeline.mre_common_vars import (
    BUILD_EFFECTS_FOLDER,
    BUILD_FOLDER,
    BUILD_TEMPLATE_FOLDER,
    BUILD_TRIGGERS_FOLDER,
    COMPILE_FOLDER,
    UNICORN,
    EXTRACT_FOLDER,
)

def clean_up_build_folder():
    if os.path.exists(BUILD_FOLDER):
        rmtree(BUILD_FOLDER)
    os.makedirs(BUILD_FOLDER, exist_ok=True)
    os.makedirs(EXTRACT_FOLDER, exist_ok=True)
    os.makedirs(COMPILE_FOLDER, exist_ok=True)
    os.makedirs(BUILD_TRIGGERS_FOLDER, exist_ok=True)
    os.makedirs(BUILD_EFFECTS_FOLDER, exist_ok=True)
    os.makedirs(BUILD_TEMPLATE_FOLDER, exist_ok=True)

def sort_and_write_filtered_trait_data():
    all_traits_processed_data = sort_and_filter_pipeline_files()
    write_sorted_filtered_data_to_json_files(all_traits_processed_data)

horiz = f"{'*'*64}"

def sanity_check():
    return f"Sanity levels at {randint(15,115)}% of normal."

def print_stars(text, level: int = 4):
    print(f"{'*'*level} {text} {'*'*level}")


if __name__=="__main__":
    start_time = time.perf_counter()
    parser = argparse.ArgumentParser(
        prog="0xRetro M&RE Trait Data Pipeline",
        description="Read and process base game traits files, generate scripted effects, tooltips, and GUI button effects for custom in-game content"
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
    print(
        f"Starting the M&RE Trait Data pipeline. Code by 0xRetro. {sanity_check()}"
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
    print(horiz)
    print_stars("Phase 1: EXTRACT: Reset build folder and crunch base files into JSON")
    clean_up_build_folder()

    # CALL STUFF FROM 'EXTRACT'
    # New steps:
    # 1. Crunch trait files into individual files named the same as the source, into a tmp folder
    print_stars("Reading Clausewitz Traits files and mapping to JSON ..",2)
    # Print files to 'extract'
    extracted_files = batch_convert_traits_files_into_json(args.stellaris_path)
    # 2. For each LEADER trait in each json file, place a copy into a dict tracking traits by class
    # 3. Save them to commander/scientist/official
    print_stars("Reducing multiple traits files to 3 ..",2)
    # Sorted files are 10_*.json in 'build/extract'
    sorted_files = read_and_sort_extracted_traits(extracted_files)

    print_stars("Mm mm, delicious, sane, predictable data! (mostly)",2)
    print(horiz)
    print_stars("** Doing a QA check on our shiny new datafiles ... ",2)
    print(horiz)
    qa_pipeline_files(sorted_files)

    print(horiz)
    print_stars("Phase 2: TRANSFORM: Sorting, filtering, and getting data ready for code gen scripts ...")
    sort_and_write_filtered_trait_data()
    print_stars("Side quest: some modifier loc keys are in uppercase! Fixing ... ",2)
    do_uppercase_modifier_mapping_work(args.stellaris_path)
    print(horiz)

    print_stars("Phase 3: COMPILE: Create effects, triggers, and GUI code")
    harvest_machine_tooltips(args.stellaris_path)
    generate_fx_tooltips_interfaces_for_all_guis()  # This writes fx and triggers files directly to common
    generate_councilor_editor_gui()                 # generate gui files for stitching later
    generate_councilor_editor_scripted_triggers()
    generate_councilor_editor_button_effects()      # Traits effects in-place, other needs copy
    generate_councilor_gui_traits_limits_effects()
    generate_ruler_limits_scripted_effect()

    print_stars("Making lines of EFFECTS code for xvcv_mdlc_leader_making_start_button_effect ... ",2)
    pipeline_make_leader_start_button_code()
    print_stars("Making lines of TRIGGER code for xvcv_mdlc_core_modifying_ruler_traits_trigger ... ",2)
    pipeline_make_xvcv_mdlc_core_modifying_ruler_traits_trigger()
    print_stars("Making lines of EFFECTS code for xvcv_mdlc_leader_making_clear_values_effect ... ",2)
    pipeline_make_leader_making_clear_values_effect()
    print_stars("Making lines of EFFECTS code for core_modifying_reset_traits_button_effect ... ",2)
    pipeline_make_xvcv_mdlc_core_modifying_reset_traits_button_effect_lines()
    print_stars("Making lines of EFFECTS code for core_modifying_still_has_subclass_traits_picked", 2)
    pipeline_make_xvcv_mdlc_core_modifying_still_has_subclass_traits_picked()
    print_stars("Making lines of GUI code for core_modifying subclasses_gui_code ... ",2)
    pipeline_make_core_modifying_subclasses_gui_code()

    print_stars("Phase 4: STITCH & COPY: Automatically gluing and moving files. Bio-forms can relax now.")
    print_stars("Stitching GUI files together ... ",2)
    stitch_gui_files_and_write_to_game_folder()

    print_stars("Copying generated effects and triggers to common ... ",2)
    copy_effects_to_common()
    copy_triggers_to_common()

    print_stars("Stitching other files (button effects, etc)...",2)
    pipeline_stitch_xvcv_mdlc_leader_making_start_button_effect()

    print(horiz)
    print_stars("TO DO by humans",2)
    print("run 'mre_propagate_loc_files.py' ")
    print(
        "*** GOOD LUCK BIO BRAIN ***\n"
        f"Is tired. {sanity_check()}"
    )

    print(UNICORN)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(
        f"Done in {str(execution_time)[:5]} seconds"
    )
