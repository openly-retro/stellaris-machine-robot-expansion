# Code generation workflow (The Good Stuff)

Things like button effects, custom GUI code, and trait tooltips need to be automated. It is too punishing to require 1 human brain to update everything by hand. To this end, I created a number of Python scripts that generate some of the code for this mod.

What does the Python code pipeline do?

1. Collect base game trait files and reformat the PDX Script into something sane and predictable
2. Trim down trait data, sort it, dump it to JSON for organizing
3. Sort and order all the traits into three output files, deciding which traits are for each of the 3 custom GUI types
4. Look at the base game to find the correct capitalizations for modifiers
5. Find Machine-specific tooltips and trait names
6. A whole lot of miscellaneous stuff for solving headaches, corner cases, and dealing with inconsistencies
7. Generate button effects for all custom GUIs and place into `common/scripted_effects/`
8. Generate tooltips for all custom GUIs and place into `localisation/english/` folder
9. Stitch together custom GUI files and place them in `interface/` folder

Run: 

`python .\run_mre_trait_pipeline.py --stellaris_path <YOUR_STEAM_FOLDER>\steamapps\common\Stellaris\`


## What to do after running the pipeline

### Copy scripted effects and triggers in-place

- 40_oxr_mdlc_councilor_editor_check_can_use_reset_button.txt
- 50_oxr_mdlc_councilor_editor_reset_traits_button_effect.txt
- 40_oxr_mdlc_councilor_editor_deduct_points_picks_for_existing_traits.txt
- 50_oxr_mdlc_core_modifying_check_existing_traits_on_gui_open_effect.txt
- 85_leader_making_start_button_effect.txt
- 85_core_modifying_modifying_ruler_trait_trigger.txt
- 85_leader_making_clear_values_effect.txt
- 85_core_modifying_reset_traits_button_effect.txt
- 85_core_modifying_subclasses_gui_code.txt

### Copy localisation files

    python .\mrec_tools\mre_propagate_loc_files.py --source-language english

