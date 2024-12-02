# Code generation workflow (The Good Stuff)

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

    python .\mre_code_tools\mre_propagate_loc_files.py --source-language english

