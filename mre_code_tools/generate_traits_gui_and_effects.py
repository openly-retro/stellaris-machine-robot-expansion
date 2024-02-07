# Python code to help generate all the leader-making traits code
import argparse
import time
import sys
from json import load as json_load

from trait_tooltip_generator import create_tooltip_for_leader

RARITIES = ("common", "veteran", "paragon")

def gen_leader_making_trait_gui_code(
        leader_class, trait_name, column_num, row_num,
        gfx_sprite_name=None,
        is_xvcv_custom_trait=False, is_veteran_trait=False, is_destiny_trait=False
):
    """ Create code to display a trait in the xvcv_mdlc_leader_making_custom_gui.gui file """
    if not gfx_sprite_name:
        # Guess GFX name from trait name
        ends_in_num = trait_name[-1].isdigit()
        if ends_in_num:
            trait_without_level = trait_name.rsplit('_', 1)
            gfx_sprite_name = f"GFX_{trait_without_level}"
        else:
            gfx_sprite_name = f"GFX_{trait_name}"  # There will be exceptions
    effect_button_background_gfx = "GFX_xvcv_mdlc_leader_trait_background_green"
    if is_xvcv_custom_trait:
        effect_button_background_gfx = "GFX_xvcv_mdlc_leader_trait_background_blue"
    elif is_veteran_trait:
        effect_button_background_gfx = "GFX_xvcv_mdlc_leader_trait_background_veteran"
    elif is_destiny_trait:
        effect_button_background_gfx = "GFX_xvcv_mdlc_leader_trait_background_destiny"
    return f"""
# {leader_class}: {trait_name}
containerWindowType = {{
    name = "xvcv_mdlc_leader_making_trait_{leader_class}_{trait_name}"
    position = {{ x = @xvcv_mdlc_leader_making_trait_position_column_{column_num} y = @xvcv_mdlc_leader_making_trait_position_row_{row_num} }}
    effectbuttonType = {{
        name = "xvcv_mdlc_leader_making_trait_{leader_class}_{trait_name}_add_bg"
        position = {{ x = @xvcv_mdlc_leader_making_traits_background_offset_width y = @xvcv_mdlc_leader_making_traits_background_offset_height }}
        spriteType = "{effect_button_background_gfx}"
        effect = "xvcv_mdlc_leader_making_trait_{leader_class}_{trait_name}_add_button_effect"
    }}
    effectbuttonType = {{
        name = "xvcv_mdlc_leader_making_trait_{leader_class}_{trait_name}_add"
        spriteType = "{gfx_sprite_name}"
        effect = "xvcv_mdlc_leader_making_trait_{leader_class}_{trait_name}_add_button_effect"
    }}
}}
"""

def gen_core_modifying_trait_gui_code(
    leader_class, trait_name, column_num, row_num,
    gfx_sprite_name,
    is_xvcv_custom_trait=False, is_veteran_trait=False, is_destiny_trait=False
):
    root_gfx_name = "GFX_xvcv_mdlc_leader_trait_background_"
    effect_button_background_gfx = f"{root_gfx_name}_green"
    effect_button_background_gfx_red = f"{root_gfx_name}_red"
    if is_veteran_trait:
        effect_button_background_gfx = "GFX_xvcv_mdlc_leader_trait_background_veteran"
        effect_button_background_gfx_red = f"{effect_button_background_gfx}_red"
    elif is_destiny_trait:
        effect_button_background_gfx = "GFX_xvcv_mdlc_leader_trait_background_destiny"
        effect_button_background_gfx_red = f"{effect_button_background_gfx}_red"
    return f"""
# {leader_class}: {trait_name}
containerWindowType = {{
    name = "xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}"
    position = {{ x = @xvcv_mdlc_core_modifying_trait_position_width_{column_num} y = @xvcv_mdlc_core_modifying_trait_position_height_{row_num} }}
    effectbuttonType = {{
        name = "xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_add_bg"
        position = {{ x = @xvcv_mdlc_core_modifying_traits_background_offset_width y = @xvcv_mdlc_core_modifying_traits_background_offset_height }}
        spriteType = "{effect_button_background_gfx}"
        effect = "xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_add_button_effect"
    }}
    effectbuttonType = {{
        name = "xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_add"
        spriteType = "{gfx_sprite_name}"
        effect = "xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_add_button_effect"
    }}
    effectbuttonType = {{
        name = "xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_remove_bg"
        position = {{ x = @xvcv_mdlc_core_modifying_traits_background_offset_width y = @xvcv_mdlc_core_modifying_traits_background_offset_height }}
        spriteType = "{effect_button_background_gfx_red}"
        effect = "xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_remove_button_effect"
    }}
    effectbuttonType = {{
        name = "xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_remove"
        spriteType = "{gfx_sprite_name}"
        effect = "xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_remove_button_effect"
    }}
}}
"""

def gen_leader_making_button_effects_code(
    leader_class, trait_name,
    is_veteran_trait=False, is_destiny_trait=False,
    required_subclass=None
):
    # This can be used for each leader class
    # \common\button_effects\xvcv_mdlc_button_effects_leader_making_<LEADER_CLASS>_customgui.txt
    needs_paragon_dlc = "yes" if is_veteran_trait or is_destiny_trait else "no"
    # Veteran & destinty traits need slightly altered trigger names
    alt_trigger_name = ""
    if is_veteran_trait:
        alt_trigger_name = "alt_"
    if is_destiny_trait:
        alt_trigger_name = "alt_2_"
    # Comment out the 'requires_leader_subclass_trigger` if it's not a veteran trait'
    requires_subclass_trigger = "" if required_subclass else "#"
    # commend out skill level trigger if it's not a veteran trait
    requires_skill_lvl_trigger = "" if is_veteran_trait or is_destiny_trait else "#"
    show_veteran_comment = f"#veteran trait" if is_veteran_trait else ''
    return f"""
#{leader_class} #{trait_name} {show_veteran_comment}
xvcv_mdlc_leader_making_trait_{leader_class}_{trait_name}_add_button_effect = {{
    potential = {{ always = yes }}
    allow = {{
        xvcv_mdlc_leader_making_trait_pick_trigger = {{ CLASS = {leader_class} ID = {trait_name} }}
        {requires_subclass_trigger}xvcv_mdlc_leader_making_requires_leader_subclass_trigger = {{ CLASS = {leader_class} ID = {required_subclass} }}
        xvcv_mdlc_leader_making_trait_cost_{alt_trigger_name}trigger = yes
        xvcv_mdlc_leader_making_trait_points_{alt_trigger_name}trigger = yes
        {requires_skill_lvl_trigger}xvcv_mdlc_leader_making_trait_skill_level_{alt_trigger_name}trigger = yes
        xvcv_mdlc_leader_making_trait_max_number_trigger = yes
        xvcv_mdlc_leader_making_picked_class_{leader_class}_trigger = yes
    }}
    effect = {{
        xvcv_mdlc_leader_making_trait_pick_effect = {{ CLASS = {leader_class} ID = {trait_name} }}
        hidden_effect = {{ xvcv_mdlc_leader_making_trait_count_points_costs_{alt_trigger_name}effect = yes }}
    }}
}}
"""

def gen_core_modifying_button_effects_code(
    leader_class, trait_name, needs_paragon_dlc=False, 
    is_veteran_trait=False, is_destiny_trait=False,
    required_subclass=None, gfx_name=None
):
    # This needs to generate two effects: add, and remove
    # xvcv_mdls_button_effects_core_modifying_traits_<LEADER_CLASS>_customgui.txt
    has_paragon_dlc_answer = "yes" if needs_paragon_dlc else "no"
    comment_out_paragon_dlc = "" if needs_paragon_dlc else "#"
    trait_ends_in_num = trait_name[-1].isdigit()
    needs_remove_tier_num_trait_effect = "" if trait_ends_in_num else "#"
    if trait_ends_in_num:
        trait_name_no_tier = trait_name.rsplit('_',1)[0]
    else:
        trait_name_no_tier = trait_name
    # Veteran & destinty traits need slightly altered trigger names
    alt_trigger_name = ""
    if is_veteran_trait:
        alt_trigger_name = "alt_"
    elif is_destiny_trait:
        alt_trigger_name = "alt_2_"
    # Comment out the 'requires_leader_subclass_trigger` if it's not a veteran trait'
    requires_subclass_trigger = "" if is_veteran_trait or is_destiny_trait or required_subclass == "any" else "#"
    # commend out skill level trigger if it's not a veteran trait
    requires_skill_lvl_trigger = "" if is_veteran_trait or is_destiny_trait else "#"
    trait_class = "common"
    if is_veteran_trait:
        trait_class = "veteran"
    elif is_destiny_trait:
        trait_class = "destiny"
    trait_comment = f"#{trait_class} trait"

    return f"""
#{trait_name} {trait_comment}
xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_add_button_effect = {{
    potential = {{
        ruler = {{ NOT = {{ has_trait = {trait_name} }} }}
    }}
    allow = {{
        custom_tooltip = xvcv_mdlc_core_modifying_tooltip_add_{leader_class}_{trait_name}
        {requires_subclass_trigger}xvcv_mdlc_core_modifying_requires_ruler_subclass_or_focus_trigger = {{ CLASS = {leader_class} ID = {required_subclass} }}
        xvcv_mdlc_core_modifying_trait_cost_{alt_trigger_name}trigger = yes
        xvcv_mdlc_core_modifying_trait_points_{alt_trigger_name}trigger = yes
        {requires_skill_lvl_trigger}xvcv_mdlc_core_modifying_trait_skill_level_{alt_trigger_name}trigger = yes
        xvcv_mdlc_core_modifying_trait_max_number_trigger = yes
        {comment_out_paragon_dlc}has_paragon_dlc = {has_paragon_dlc_answer}
    }}
    effect = {{
        {needs_remove_tier_num_trait_effect}xvcv_mdlc_core_modifying_remove_tier_1_or_2_traits_effect = {{ ID = {trait_name_no_tier} }}
        xvcv_mdlc_core_modifying_trait_pick_effect = {{ CLASS = {leader_class} ID = {trait_name} }}
		hidden_effect = {{ xvcv_mdlc_core_modifying_trait_add_{alt_trigger_name}effect = yes }}
    }}
}}
xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_remove_button_effect = {{
    potential = {{
        ruler = {{ has_trait = {trait_name} }}
    }}
    allow = {{ always = yes }}
    effect = {{
        custom_tooltip = xvcv_mdlc_core_modifying_tooltip_remove_{leader_class}_{trait_name}
		hidden_effect = {{
            ruler = {{ remove_trait = {trait_name} }}
            xvcv_mdlc_core_modifying_trait_remove_{alt_trigger_name}effect = yes
		}}
    }}
}}
"""

def iterate_traits_make_leadermaking_gui_code(organized_traits_dict, for_class: str) -> str:
    """ going thru a file like 99_mre_scientist_traits_for_codegen.json 
        and create code which we copy/paste into the interface/gui files
    """
    header_classname_spaced = ' '.join([char for char in for_class])
    header = f"""
##########################################################
#       START COPY/PASTE GENERATED GUI TRAITS CODE FOR:  #
#					{header_classname_spaced}						 #
##########################################################
"""
    footer = f"""
##########################################################
#       END COPY/PASTE GENERATED GUI TRAITS CODE FOR:  #
#					{header_classname_spaced}						 #
##########################################################
"""
    leader_making_code_bloblist = [header,]
    # 10 columns, 8 rows
    trait_column_num = 1
    trait_row_num = 1
    for rarity_level in RARITIES:
        for leader_making_trait in organized_traits_dict['leader_making_traits'][rarity_level]:
            trait_name = [*leader_making_trait][0]
            root = leader_making_trait[trait_name]
            trait_gui_code = gen_leader_making_trait_gui_code(
                trait_name=trait_name,
                leader_class=root['leader_class'],
                column_num=trait_column_num, row_num=trait_row_num,
                is_veteran_trait=(root['rarity']=="veteran"),
                is_destiny_trait=(root['rarity']=="paragon"),
                gfx_sprite_name=root['gfx']
            )
            trait_column_num = trait_column_num + 1
            if trait_column_num > 10:
                trait_column_num = 1
                trait_row_num = trait_row_num + 1
            leader_making_code_bloblist.append(trait_gui_code)
    leader_making_code_bloblist.append(footer)
    return ''.join(leader_making_code_bloblist)


def iterate_traits_make_leadermaking_effects_code(organized_traits_dict, for_class):
    leader_making_effects_copypaste_blob = []
    for rarity_level in RARITIES:
        for leader_making_trait in organized_traits_dict['leader_making_traits'][rarity_level]:
            trait_name = [*leader_making_trait][0]
            root = leader_making_trait[trait_name]
            leadermaking_effects_code_for_trait = gen_leader_making_button_effects_code(
                leader_class=for_class,
                trait_name=trait_name,
                is_veteran_trait=(root.get('rarity')=="veteran"),
                is_destiny_trait=(root.get('rarity')=="paragon"),
                required_subclass=root.get('required_subclass', None)
            )
            leader_making_effects_copypaste_blob.append(leadermaking_effects_code_for_trait)
    return '\n'.join(leader_making_effects_copypaste_blob)


def iterate_traits_make_leadermaking_tooltips_code(organized_traits_dict, for_class):
    leader_making_tooltips_copypaste_blob = []
    for rarity_level in RARITIES:
        for leader_making_trait in organized_traits_dict['leader_making_traits'][rarity_level]:
            # trait_name = [*leader_making_trait][0]
            # root = leader_making_trait[trait_name]
            tooltip_code_for_leadermaking_trait = create_tooltip_for_leader(
                trait_dict=leader_making_trait, leader_class=for_class, feature="leader_making"
            )
            leader_making_tooltips_copypaste_blob.append(tooltip_code_for_leadermaking_trait)
    return ''.join(leader_making_tooltips_copypaste_blob)

if __name__ == "__main__":
    start_time = time.time()
    parser = argparse.ArgumentParser(
        prog="0xRetro Machine & Robot Expansion Mod Codegen Tools",
        description="Automatically spew out mod code"
    )
    parser.add_argument(
        '--infile',
        help='A traits JSON file that we processed, like 99_mre_commander_traits_for_codegen.json, created from mre_mod_trait_organizer.py.',
        required=True
    )
    parser.add_argument(
        '--tooltips',
        help="Generate M&RE trait tooltips, given a traits JSON file that was processed by mre_mod_trait_organizer",
        action="store_true",
        required=False
    )
    parser.add_argument(
        '--effects',
        help="Generate effects code from trait files",
        action="store_true",
        required=False
    )
    parser.add_argument(
        '--process_all',
        help="The Big One. Generate M&RE tooltips, GUI code, button effects code, assuming all traits files were processed by mre_mod_trait_organizer"
    )
    args = parser.parse_args()
    buffer = ''
    infile_no_ext = args.infile.rsplit('.',1)[0]
    with open(args.infile) as organized_traits_file:
        buffer = json_load(organized_traits_file)
    if args.tooltips:
        detected_leader_class = args.infile.split('_')[2]
        tooltips_blob_for_writing = iterate_traits_make_leadermaking_tooltips_code(
            buffer, for_class=detected_leader_class)
        with open(f"{infile_no_ext}_leadermaking_tooltips.txt", "wb") as leadermaking_effects_output:
            sys.stdout.write(f"Writing leadermaking tooltips code to {leadermaking_effects_output.name}\n")
            leadermaking_effects_output.write(
                tooltips_blob_for_writing.encode('utf-8')
            )
            sys.exit()
    if args.effects:
        detected_leader_class = args.infile.split('_')[2]
        effects_blob_for_writing = iterate_traits_make_leadermaking_effects_code(
            buffer, for_class=detected_leader_class)
        with open(f"{infile_no_ext}_leadermaking_effects.txt", "wb") as leadermaking_effects_output:
            sys.stdout.write(f"Writing leadermaking effects code to {leadermaking_effects_output.name}\n")
            leadermaking_effects_output.write(
                effects_blob_for_writing.encode('utf-8')
            )
            sys.exit()
    gui_code = iterate_traits_make_leadermaking_gui_code(buffer, for_class="commander")
    leadermaking_effects_code = iterate_traits_make_leadermaking_effects_code(buffer, for_class="commander")
    
    with open(f"{infile_no_ext}_leadermaking_gui.txt", "w") as leadermaking_gui_output:
        sys.stdout.write(f"Writing leadermaking GUI code to {leadermaking_gui_output.name}\n")
        leadermaking_gui_output.write(gui_code)
    with open(f"{infile_no_ext}_leadermaking_effects.txt", "w") as leadermaking_effects_output:
        sys.stdout.write(f"Writing leadermaking effects code to {leadermaking_effects_output.name}\n")
        leadermaking_effects_output.write(leadermaking_effects_code)
