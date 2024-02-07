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

Warnings about working with Clausewitz syntax (what base Stellaris traits files are written in)

- It MAKES UP ITS OWN RULES
- IT MAY NOT FOLLOW THE RULES IT MAKES
- It wiLL DaNcE On yOuR SaNiTy
- You may lose yourself to possession of a psionic avatar if you stare too long or try to apply your ideas of "rules" and "well this could be standardized pretty easily"



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

Look for:

    build\00_mre_commander_traits.json
    build\00_mre_official_traits.json
    build\00_mre_scientist_traits.json

These files have sanely organized data for breakfast, lunch, dinner, or just a snack.

**Note that LOTS OF TRAIT DATA WILL BE MISSING AND ONLY TRAIT DATA THAT'S USEFUL FOR THIS MOD WILL BE IN THOSE FILES**

### Phase 1, part 2

Next up, some more data massaging before we can feed it to phase 2 scripts.

Run:

`python .\mre_mod_trait_organizer.py --sort_filter_all`

This will look in the build folder for the above 3 files, sort them by rarity and pick the highest tier trait in a series, discarding lower tier ones.

Look for:

    build\99_mre_commander_traits_for_codegen.json
    build\99_mre_commander_traits_for_codegen.json
    build\99_mre_commander_traits_for_codegen.json

## Phase 2 (WIP)

Auto-generate mod code from files.

WIP WIP WIP WIP

Run: 

`python .\generate_traits_gui_and_effects.py --infile .\build\99_mre_commander_traits_for_codegen.json --tooltips`

`python .\generate_traits_gui_and_effects.py --infile .\build\99_mre_commander_traits_for_codegen.json --effects`

In gui_auto, there will be interface GUI code for commander traits, just for the leader-making feature so far. 

WIP WIP WIP WIP
