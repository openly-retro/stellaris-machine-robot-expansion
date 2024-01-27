# Python code to help generate all the leader-making traits code
"""


"""

def gen_leader_making_trait_code(
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
            gfx_sprite_name = f"{GFX}_{trait_without_level}"
        else:
            gfx_sprite_name = f"{GFX}_{trait_name}"  # There will be exceptions
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

def gen_core_modifying_trait_code(
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
    }
    effectbuttonType = {{
        name = "xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_add"
        spriteType = "{gfx_sprite_name}"
        effect = "xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_add_button_effect"
    }
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