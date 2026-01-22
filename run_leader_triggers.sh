python mrec_tools/other_code_generators/leader_trait_triggers/split_traits_files_for_processing.py \
--stellaris_folder ~/modding/stellaris \
--vanilla_traits_files \
"00_generic_leader_traits.txt" \
"00_admiral_traits.txt" \
"00_general_traits.txt" \
"00_governor_traits.txt" \
"00_scientist_traits.txt" \
"00_starting_ruler_traits.txt" \
"100_ambassador_traits.txt" \
"100_delegate_traits.txt" \
"12_astral_planes_traits.txt" \
"14_grand_archive_traits.txt" \
--build_folder mrec_tools/build/

python mrec_tools/other_code_generators/leader_trait_triggers/convert_traits_to_objs.py --build_folder mrec_tools/build/

python mrec_tools/other_code_generators/leader_trait_triggers/create_leader_triggers.py --build_folder mrec_tools/build/ --mod_folder . --multiproc
