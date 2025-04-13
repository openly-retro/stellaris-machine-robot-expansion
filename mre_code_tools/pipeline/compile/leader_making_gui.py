from mre_code_tools.pipeline.compile.generate_traits_gui_and_effects import gui_footer, gui_header
from mre_code_tools.pipeline.mre_common_vars import RARITIES


from datetime import datetime


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


def iterate_traits_make_leadermaking_gui_code(organized_traits_dict, for_class: str) -> str:
    """ going thru a file like 99_mre_scientist_traits_for_codegen.json 
        and create code which we copy/paste into the interface/gui files
    """
    header_classname_spaced = ' '.join([char for char in for_class])
    header = gui_header.format(
        classname=header_classname_spaced,
        now=str(datetime.now())
    )
    footer = gui_footer.format(
        classname=header_classname_spaced
    )
    leader_making_code_bloblist = [header,]
    # 10 columns, 8 rows
    trait_column_num = 3  # There are 2 custom traits already coded in to the gui file
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