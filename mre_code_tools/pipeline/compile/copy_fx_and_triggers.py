import os
from shutil import copyfile
import glob

from pipeline.mre_common_vars import (
    BUILD_FOLDER,
    BUILD_EFFECTS_FOLDER,
    BUILD_TRIGGERS_FOLDER,
)

def copy_effects_to_common():

    effects_files_to_copy = glob.iglob(
        os.path.join(
            BUILD_EFFECTS_FOLDER, '*.txt'
        )
    )
    for src_file in effects_files_to_copy:

        destfile = os.path.join(
            'common', 'scripted_effects', os.path.basename(src_file)
        )
        copyfile(src_file, destfile)
        print(f"+ Installing scripted effects:\n+ {os.path.basename(src_file)}")


def copy_triggers_to_common():

    effects_files_to_copy = glob.iglob(
        os.path.join(
            BUILD_TRIGGERS_FOLDER, '*.txt'
        )
    )
    for src_file in effects_files_to_copy:
        destfile = os.path.join(
            'common', 'scripted_triggers', os.path.basename(src_file)
        )
        copyfile(src_file, destfile)
        print(f"+ Installing scripted triggers: {os.path.basename(src_file)}")
