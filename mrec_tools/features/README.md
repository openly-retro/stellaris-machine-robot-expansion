# Machine & Robots Expansion: Continued - Features

Keep the mod organized with "Features" (*audience gasp*)

Think of each feature as a very tiny sub-mod of the main mod.

Each has its own common, events, gfx, localistion, etc, folders.

The code pertaining to that feature, whether small or large, stays in once place.

Make changes to the code in features/your_awesome_feature/, then run the command to sync the feature files into the main mod.

It adds a little bit of overhead, because for each tweak to a feature, a modder has to run the command to sync the files.

# Setting up a feature

1. Create a new sub folder, using underscores for spaces (snake case), name it whatever you like
2. Add an empty `__init__.py` file
3. Add a `feature.yml` file with an `author tag:` like
    author tag: oxr
4. Add a `common` subfolder and work there; add other sub-folders as needed
    
# How to sync

Use rsync:

    rsync -rvuz mrec_tools/features/<your_feature_folder>/ ./

This syncs any folders found in your sub-folder, like ones named `common`, `events`, etc, to the main mod.


<!-- # Synced files are automatically renamed

The files will be synced from the feature folder into the main mod, using the following naming strategy:

    <author_tag>_mdlc_<feature_folder_name>_(destination folder with filename)

For example:

    features/bio_mech_worlds/common/scripted_effects/main_scripted_effects.txt

gets synced to the main folder like

    common/scripted_effects/oxr_mdlc_f_bio_mech_worlds_main_scripted_effects.txt

- Author tag is auto-inserted at the beginning, followed by `mdlc`
- The `f` is inserted to say, "this file was compiled from the features folder"
- The name of the feature folder was added into the filename
 -->
