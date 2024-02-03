This is an attempt to bring XVCV's "Machines & Robot Expansion" mod for Stellaris up to date, to be compatible with Stellaris version 3.10.*, and potentially carry on maintaining it.

The original author has abandoned the work and is no longer available for contact.

# Welcome

I (openly-retro) am a web developer by day, and a fan of Stellaris. Just cleared 1k hours with the game.. yay?

I invite you to collaborate, but I also want you to know I'm not desperate for help and this mod will live again even if you just stop by to say hi.

## Communicating

Chat with me about this mod in the [Stellaris Modding Den](https://discord.gg/vKwNs93g ) discord! Look for `mag-sanchusa#4206 (openlyretro)`. We can discuss this mod in the `xvcv_mods` channel.

I will also respond to comments in the Github wiki for this project.

## Contributing

Please visit the Github repo wiki for this project: [https://github.com/openly-retro/stellaris-machine-robot-expansion/wiki](https://github.com/openly-retro/stellaris-machine-robot-expansion/wiki)

Also please protect your sanity. Clausewitz Syntax (what base Stellaris traits files are written in) is UNPREDICTABLE and MAKES UP ITS OWN RULES.

After working on Clausewitz Syntax script, your mind may be forever altered.

# Code generation workflow (The Good Stuff)

Phase 1: Transform base game traits data into useful data
Phase 2: Automatically make GUI, effects, and tooltips code for this mod

## PHASE 1

1. Collect base game trait files and reformat the PDX Script into something sane and predictable
2. Trim down trait data, sort it, dump it to YAML for organizing
3. Sort and order all the traits into three output files which will (eventually) be fed to more Python code generation scripts that actually make GUI, effects, and tooltips code for this mod.

Run:

`python .\run_mre_trait_pipeline.py --stellaris_path <YOUR_STEAM_FOLDER>\steamapps\common\Stellaris\`

This will make a `build` folder with a bunch of text files.

Look for: `00_mre_commander_traits.yml`, `00_mre_official_traits.yml`, `00_mre_scientist_traits.yml`

These files have sanely organized data for breakfast, lunch, dinner, or just a snack.

**Note that LOTS OF TRAIT DATA WILL BE MISSING AND ONLY TRAIT DATA THAT'S USEFUL FOR THIS MOD WILL BE IN THOSE FILES**

The sections below are for documentation. You don't have to follow those commands, because the pipeline script does all that. The doc below is for posterity.

## Collect base game traits files and convert the data to something we can iterate over (WIP)
The traits files we will process for this mod are in base Stellaris, under `\common\traits`:
- 00_admiral_traits.txt
- 00_general_traits.txt
- 00_generic_leader_traits.txt
- 00_governor_traits.txt
- 00_scientist_traits.txt
- 00_starting_ruler_traits.txt

Open your favorite terminal. Make sure Python 3.12+, `pyyaml` are installed

1. Convert a Stellaris Clausewitz *traits* file to "something resembling YAML"

If you use this converter on anything but a traits file, expect to get useless garbage back.

`python .\mre_code_tools\stellaris_yaml_converter.py --infile <STEAM_INSTALL_FOLDER>\steamapps\common\Stellaris\common\traits\00_governor_traits.txt -o "00_governor_traits_parsed.txt"`

We'll do this for each traits file.

### Further trim down and sort data into a simple format we can later iterate over to generate GUI code, effects code, and tooltips (WIP)

2. Crunch the traits in this converted file: 
- Trim down the trait data to just the values we care about
- Sort traits into the three classes
- Duplicate common traits if a trait can be applied to more than one type of leader class
- Output as YAML for smaller file size

`python .\mre_code_tools\stellaris_trait_cruncher.py --infile .\00_governor_traits_parsed.txt --outfile 00_useful_governor_traits.yaml`

### Sort and merge files

There isn't a script for this, there is a method in the pipeline script.


## Phase 2

Auto-generate mod code from files.