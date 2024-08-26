This is an attempt to keep XVCV's "Machines & Robot Expansion" mod compatible with current Stellaris versions, and carry on maintaining it and adding new content.

The original author has abandoned the work and is no longer available for contact.

# Welcome

I (openly-retro) am a web developer by day, and a fan of Stellaris.

I invite you to collaborate, but I also want you to know I'm not desperate for help and this mod will live again even if you just stop by to say hi.

## Communicating

Chat with me about this mod in the [Stellaris Modding Den](https://discord.gg/vKwNs93g ) discord! Look for `mag-sanchusa#4206 (openlyretro)`. We can discuss this mod in the `machines-robots-expac` channel.

I will also respond to comments in the Github wiki for this project.

## Contributing

Please visit the Github repo wiki for this project: [https://github.com/openly-retro/stellaris-machine-robot-expansion/wiki](https://github.com/openly-retro/stellaris-machine-robot-expansion/wiki)

Warnings about working with Clausewitz syntax (what base Stellaris traits files are written in)

- It MAKES UP ITS OWN RULES
- IT MAY NOT FOLLOW THE RULES IT MAKES
- It wiLL DaNcE On yOuR SaNiTy
- You may lose yourself to possession of a psionic avatar if you stare too long or try to apply your ideas of "rules" and "well this could be standardized pretty easily"

## Translations

Welcome translators!! I am very happy to have you here.

If you would like to submit a translation, please go ahead and create a pull request from a fork of this repo.

The translation files should go in:

`localisation/<language>/replace`

So if you are translating Korean files, the changes should go in `localisation/korean/replace/` because I have a language copy tool which copies all changes from English to all other languge folders.

If you place the files in `localisation/<language>` and not in `localisation/<language>/replace` then the files will be overwritten.

If they are in the `replace` folder then your correctly translated files will always take precedence over the English version. If your translation files are missing any keys then the missing keys will show up in English.

This way, players will never see only the localisation key with no content if there are translations missing.

### Patches

I do updates using the concept of patches. A patch consists of:

1. A group of bug fixes or small features, OR
2. A large feature

Workflow:

1. Create a branch for the patch, following the next in the series at https://github.com/openly-retro/stellaris-machine-robot-expansion/tags (if 2.3.2 is the latest then the next is 2.3.3), named `patch-#.#.#` where #.#.# is the patch version
2. Do some work in your feature or bug branch and then make a pull request to the patch branch

# Art Credits

- https://pixabay.com/illustrations/water-technology-sci-fi-futuristic-7547817/ by [https://pixabay.com/users/joker39-30858803/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=7547817](Melvyn Thevenin) from [https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=7547817"](Pixabay) , used for World Machine planetary deposits and other artworks
- https://pixabay.com/illustrations/futuristic-architecture-wallpaper-6694976/ by  <a href="https://pixabay.com/users/tommyvideo-3092371/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=6694976">Tomislav Jakupec</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=6694976">Pixabay</a>, used for World Machine technology art
- https://pixabay.com/illustrations/blueprint-engineering-technology-6944719/ by Image by <a href="https://pixabay.com/users/xresch-7410129/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=6944719">Reto Scheiwiller</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=6944719">Pixabay</a>, used for World Machine event art


- [https://www.deviantart.com/xxaries1970xx/art/Digital-Circuit-936780185](Digital Circuit, by XxAries1970xX) , used for the Source Code Reprogramming event-related banners and other artworks.

# Code generation workflow (The Good Stuff)

Phase 1: Transform base game traits data into useful data
Phase 2: Automatically make GUI, effects, and tooltips code for this mod

Run: 

`python .\run_mre_trait_pipeline.py --stellaris_path <YOUR_STEAM_FOLDER>\steamapps\common\Stellaris\`

It does:

A LOT SO FAR: All the way up to "Make JSON maps of capitalized tooltips"!

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

`python .\mre_process_traits_for_codegen.py --sort_filter_all`

This will look in the build folder for the above 3 files, sort them by rarity and pick the highest tier trait in a series, discarding lower tier ones.

Look for:

    build\99_mre_commander_traits_for_codegen.json
    build\99_mre_official_traits_for_codegen.json
    build\99_mre_scientist_traits_for_codegen.json

## Phase 2 (WIP)

Auto-generate mod code from files.

### Deal with uppercase modifier names in base stellaris

Some auto-created modifier translation keys, like "ship_speed_mult" would have its tooltip key automatically set to `mod_ship_speed_mult` by our peaceful, ordinary, sane logic. But in base Stellaris, the translation key is actually `MOD_SHIP_SPEED_MULT` AND CAPITALIZATION MATTERS. And capitalization is unpredictable! Rock.. paper.. scissors, it's `random.choice('CAPITALIZED', 'not capitalized')`

But there is a way around this. If we make translation keys like:

`mre_mod_ship_speed_mult:0 "$MOD_SHIP_SPEED_MULT$"` we can set ourselves up to never have to deal with capitalization again. (Hahaha famous last words!) And in the auto-generation of the tooltip, prepend mre_, fill up a whole yml file in localisation\english.yml ... 

For a more clear picture of what this workflow should do, go look at `xvcv_mdlc_l_uppercase_modifiers.yml`

To fill/update that file, run

`python .\mre_translation_key_normalizer.py --infile <STEAM_LIBRARY>\steamapps\common\Stellaris\localisation\english\modifiers_l_english.yml --outfile modifiers_l_upper_map.txt`

`python .\mre_translation_key_normalizer.py --infile <STEAM_LIBRARY>\steamapps\common\Stellaris\localisation\english\megacorp_l_english.yml --outfile megacorp_upper_map.txt`

`python .\mre_translation_key_normalizer.py --infile <STEAM_LIBRARY>\steamapps\common\Stellaris\localisation\english\paragon_2_l_english.yml --outfile paragon_2_upper_map.txt`

Copy paste the contents of these output files into `xvcv_mdlc_l_english_uppercase_modifiers.yml`. You can delete the txt files after.

### Make JSON maps of capitalized tooltips, so when we make our tooltips, we know when to append mre_

Note: run_mre_trait_pipeline does up to and including this section of work.

I know, right? so much stuff to do. If only PDX devs could have made all their data consistently one case.

`python .\mre_translation_key_normalizer.py --infile <STEAM_LIBRARY>\steamapps\common\Stellaris\localisation\english\modifiers_l_english.yml --outfile .\build\modifiers_l_upper.json --list_keys`

`python .\mre_translation_key_normalizer.py --infile <STEAM_LIBRARY>\steamapps\common\Stellaris\localisation\english\megacorp_l_english.yml --outfile .\build\megacorp_upper.json --list_keys`

`python .\mre_translation_key_normalizer.py --infile <STEAM_LIBRARY>\steamapps\common\Stellaris\localisation\english\paragon_2_l_english.yml --outfile .\build\paragon_2_upper.json --list_keys`

Now that these three JSON files are in place, our tooltip generator will look in them and know when to use our custom reference vs when it's OK to use the sanely concatenated one.

### Auto generate GUI code, and button effects code

For both leadermaking and core-modifying, the button effects code which are not automatically generated, like for subclasses, and the custom traits, those stay together in either `xvcv_mdlc_button_effects_core_modifying_main_customgui.txt` or `xvcv_mdlc_button_effects_leader_making_main_customgui.txt`

These scripts will auto generate button effects code for the 3 separate classes.

Each class' autogenerated code goes in their own separate file, so it's easier to update things in the future.

The plan is to run the scripts, and then copy the output into their respective button effects files, without touching the stuff that isn't autogenerated.

Run: 

`python .\generate_traits_gui_and_effects.py --infile .\build\99_mre_commander_traits_for_codegen.json --tooltips`

`python .\generate_traits_gui_and_effects.py --infile .\build\99_mre_commander_traits_for_codegen.json --effects`

WIP WIP WIP

### Auto-generate trait tooltip localisation data

Already in pipeline..

### Generate triggers / effects that track trait clicks in leader & core modifying GUI

There are scripted trigger and effects for clearing/resetting/counting traits selected via GUI


Generate xvcv_mdlc_core_modifying_ruler_traits_trigger:

    python .\mre_code_tools\generate_traits_gui_and_effects.py --core_trigger

Generate xvcv_mdlc_leader_making_clear_values_effect

    python .\mre_code_tools\generate_traits_gui_and_effects.py --leader_fx1


## Councilor editor stuff

Generate GUI TRAITS CODE in the build folder starting with 30_ for each councilor node

    python.exe .\mre_code_tools\mre_generate_councilor_editor_gui.py

Generate BUTTON EFFECTS CODE in the .\common\button_effects\ folder

    python .\mre_code_tools\mre_generate_councilor_editor_button_effects.py

Generate SCRIPTED TRIGGERS in the build folder starting with 40_

    python .\mre_code_tools\mre_generate_councilor_editor_scripted_triggers.py

Generate GUI RESET BUTTON SCRIPTED TRIGGER in the build folder starting with 50_

    python .\mre_code_tools\mre_generate_councilor_editor_button_effects.py --reset-effect

Generate SCRIPTED EFFECT (DETECT TRAIT PICKS) in the build folder starting with 40_

    python.exe .\mre_code_tools\mre_generate_gui_traits_limits_effects.py

## Localisation files

Copy all english loc to other folders:

    python .\mre_code_tools\mre_propagate_loc_files.py --source-language english
