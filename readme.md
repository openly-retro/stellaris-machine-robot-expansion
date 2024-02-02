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

# Maintenance / update guidelines

- Avoid renaming files
- Avoid renaming custom variables where possible

# Resources

Graphics: Use paint.net
Code: VSCode with cwtools extension

# Code generation workflow (The Good Stuff)

## Collect base game traits files and convert the data to something we can iterate over (WIP)
The traits files we will process for this mod are in base Stellaris, under `\common\traits`:
- 00_admiral_traits.txt
- 00_general_traits.txt
- 00_generic_leader_traits.txt
- 00_governor_traits.txt
- 00_scientist_traits.txt
- 00_starting_ruler_traits.txt

Open your favorite terminal. Make sure Python 3.12+, `pyyaml` are installed

1. Convert a Stellaris ClauseScript *traits* file to "something resembling YAML"

If you use this converter on anything but a traits file, expect to get useless garbage back.

`python .\mre_code_tools\stellaris_yaml_converter.py --infile <STEAM_INSTALL_FOLDER>\steamapps\common\Stellaris\common\traits\00_governor_traits.txt -o "00_governor_traits_parsed.txt"`

We'll do this for each traits file. (TODO: Automate this part!)

## Further trim down and sort data into a simple format we can later iterate over to generate GUI code, effects code, and tooltips (WIP)

2. Crunch the traits in this converted file: 
- Trim down the trait data to just the values we care about
- Sort traits into the three classes
- Duplicate common traits if a trait can be applied to more than one type of leader class

`python .\mre_code_tools\stellaris_trait_cruncher.py --infile .\00_governor_traits_parsed.txt --outfile 00_useful_governor_traits.yaml`

TODO: automate all this for the files in part 1
