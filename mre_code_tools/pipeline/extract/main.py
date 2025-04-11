""" Operations regarding reading Stellaris traits files and sorting them for processing """

import os
import sys
import glob
from json import load as json_load, dump as json_dump, dumps

from pipeline.mre_common_vars import (
    BASE_TRAIT_FILES,
    BUILD_FOLDER,
    EXTRACT_FOLDER,
    LEADER_CLASSES,
)
from cz2json.converter import input_cz_output_json
from pipeline.transform.main import (
    trickle_up_subclass_requirements
)


def make_converted_filename_2(base_filename):
    without_ext = base_filename.split('.')[0]
    return f"{without_ext}.json"

def batch_convert_traits_files_into_json(stellaris_path: str) -> list:
    """ New 2.0 pipeline method """
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
            # breakpoint()
            print(f"Parsing {base_file}...")
            buffer = input_cz_output_json(base_traits_file.read())
                
        extracted_file_name = make_converted_filename_2(base_file)

        # Write to file in 'extract' folder
        target_file_path = os.path.join(
            EXTRACT_FOLDER, extracted_file_name
        )
        generated_files.append(target_file_path)
        with open(target_file_path, "w") as dest_file:
            # dest_file.write(json_dump(buffer))
            try:
                json_dump(buffer, dest_file, indent=4)
            except Exception as ex:
                with open(f"{base_file}_parse_err.txt", "w") as dumpfile:
                    dumpfile.write(str(buffer))
                    sys.exit(f"There was a problem parsing {base_file}")
            print(
                f"Chopped up base file {base_file} successfully. Written to {target_file_path}"
            )
    return generated_files

def read_and_sort_extracted_traits(list_of_extracted_files: list) -> list:
    """ Load up the traits from the extracted file data, sort them, save only 3 files
    The list of extracted files will already have the pathname in it
    Return the list of 3 files expected to be in the base build/ folder
    TODO: move the 3 exported files to a sub folder in build?
    """
    output = {
        "commander": [],
        "scientist": [],
        "official": []
    }

    for traits_src_json_path in list_of_extracted_files:
        with open(traits_src_json_path) as traits_src_json_file:
            # breakpoint()
            buffer = json_load(traits_src_json_file)
            for trait in buffer:
                if "commander" in trait['leader_class']:
                    output['commander'].append(trait)
                if "scientist" in trait['leader_class']:
                    output['scientist'].append(trait)
                if "official" in trait['leader_class']:
                    output['official'].append(trait)
    # Finished reading files, now dump to 3 json files
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
