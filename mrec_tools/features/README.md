# Machine & Robots Expansion: Continued - Features

Keep the mod organized with "Features" (*audience gasp*)

Think of each feature as a very tiny sub-mod of the main mod.

Each has its own common, events, gfx, localistion, etc, folders.

The code pertaining to that feature, whether small or large, is developed in once place.

Make changes to the code in features/your_awesome_feature/, then run the command to sync the feature files into the main mod.

It adds a little bit of overhead, because for each tweak to a feature, a modder has to run the command to sync the files.

# Setting up a feature

1. Create a new sub folder in `features`, using underscores for spaces (snake case), name it whatever you like
2. Add an entry in `features_list.yml` file with some info about the thing you're working on
4. Add a `common` subfolder and work there; add other sub-folders as needed

# File naming standards

    <author tag>_mdlc_<name of the folder it's in>_<feature name>_<some sort of identifier>

Leading to good filenames like

    scripted_effects/oxr_mdlc_scripted_effects_mamp_main.txt
    traits/rikk_mdlc_species_traits_extended.txt

Some files that are already in the code base are named slightly differently, they all get a free pass and also free Zro ice cream on Saturdays.

# Development workflow

1. Make some changes to the files in features/your_awesome_feature
2. Commit the changes
3. Sync the files from your feature to the main mod
4. Test out the changes
5. If this is for a fix or update to something that's live, you can commit the changes to both your feature folder and the main mod
5.1. If this is for something brand new and it's not ready for prime time, remove the files in the main mod that were synced there

# How to sync

You will need **rsync** on your system for this. https://rsync.samba.org/ 

The below Python script will call rsync, which is ultra fast and reliable.

Sync all features:

    python mrec_tools/features/sync.py

Sync one feature (in this example, `mamp`):
 
    python mrec_tools/features/sync.py --features mamp

Sync multiple:

    python mrec_tools/features/sync.py --features mamp bio_mech_worlds

No prompt will be given, it will sync automatically. If you didn't want to sync, use `git restore` to clean up the synced files (don't accidentally restore the files in your features folder!)

# Cleanup

If you are testing a feature that isn't ready for prime time yet, **after you commit your code in your feature folder** clean up the working tree like so:

    git clean -d

It will tell you to use the `-f` parameter (force). Make sure you committed your code changes in your features folder.

# Remember ..!

1. Have fun!!
2. Name your files consistently
3. Save and commit files often
4. Remember it's modding, we are doing this for making awesome Machine and Robots related content, it's not a day job and perfectly fine to take a break, or work on something else that's more enticing, literally at any time .. 
