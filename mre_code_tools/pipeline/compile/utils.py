import sys
from pipeline.mre_common_vars import (
    BUILD_TRIGGERS_FOLDER,
)

import os

def write_build_scripted_trigger(file_contents, file_name, feature_text):
    outfile_path = os.path.join(
        BUILD_TRIGGERS_FOLDER, file_name
    )
    with open(outfile_path, "w") as trigger_file_output:
        sys.stdout.write(f"Writing {feature_text} trigger code to {outfile_path}\n")
        trigger_file_output.write(
            file_contents
        )

def write_build_file(
    file_contents,
    file_name,
    file_folder,
    log_text,
):
    outfile_path = os.path.join(
        file_folder, file_name
    )
    with open(outfile_path, "w") as file_output:
        sys.stdout.write(f"Writing {log_text} code to {file_name}\n")
        file_output.write(file_contents)

