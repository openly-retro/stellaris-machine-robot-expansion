from make_extractor_effects import do_all_work as make_scripted_effects
from make_extractor_special_projects import do_all_work as make_special_projects
from make_filler_deposits import do_all_work as make_deposits

import argparse
import os
from sys import exit


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="0xRetro Compulsory Consolidator DEPOSITS code",
    )
    parser.add_argument(
        "--feature-folder",
        dest="feature_folder",
        help="Absolute path to 'mrec_tools/features'. (Required)",
        required=True
    )
    if not os.path.abspath(
        'feature_folder'
    ):
        sys.exit(
            "Couldn't find the features folder where you said it was.\n"
            "Run with --feature-folder /home/users/you/location/of/feature_folder"
        )
    args = parser.parse_args()
    make_scripted_effects(args.feature_folder)
    make_special_projects(args.feature_folder)
    make_deposits(args.feature_folder)
