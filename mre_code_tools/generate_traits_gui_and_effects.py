# Python code to help generate all the leader-making traits code
"""


"""

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
    alt_trigger_name = "alt_" if is_veteran_trait else ""
    alt_trigger_name = "alt_2_" if is_destiny_trait else ""
    # Comment out the 'requires_leader_subclass_trigger` if it's not a veteran trait'
    requires_subclass_trigger = "" if is_veteran_trait else "#"
    # commend out skill level trigger if it's not a veteran trait
    requires_skill_lvl_trigger = "" if is_veteran_trait or is_destiny_trait else "#"
    return f"""
# {leader_class}: {trait_name}
xvcv_mdlc_leader_making_trait_{trait_name}_add_button_effect = {{
    potential = {{ xvcv_mdlc_leader_making_{leader_class}_subclass_traits = no }}
    allow = {{
        xvcv_mdlc_leader_making_trait_pick_trigger = {{ CLASS = {leader_class} ID = {trait_name} }}
        {requires_subclass_trigger} xvcv_mdlc_leader_making_requires_leader_subclass_trigger = {{ CLASS = {leader_class} ID = {required_subclass} }}
        xvcv_mdlc_leader_making_trait_cost_{alt_trigger_name}trigger = yes
        xvcv_mdlc_leader_making_trait_points_{alt_trigger_name}trigger = yes
        {requires_skill_lvl_trigger} xvcv_mdlc_leader_making_trait_skill_level_{alt_trigger_name}trigger = yes
        xvcv_mdlc_leader_making_trait_max_number_trigger = yes
        xvcv_mdlc_leader_making_picked_class_official_trigger = yes
        has_paragon_dlc = {needs_paragon_dlc}
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
    use_alt_trigger = "alt_" if is_veteran_trait or is_destiny_trait else ""
    # Comment out the 'requires_leader_subclass_trigger` if it's not a veteran trait'
    requires_subclass_trigger = "" if is_veteran_trait or is_destiny_trait or required_subclass == "any" else "#"
    # commend out skill level trigger if it's not a veteran trait
    requires_skill_lvl_trigger = "" if is_veteran_trait or is_destiny_trait else "#"
    veteran_trait_comment = " #veteran trait" if is_veteran_trait else ""

    return f"""
#{trait_name}{veteran_trait_comment}
xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_add_button_effect = {{
    potential = {{
        {comment_out_paragon_dlc}has_paragon_dlc = {has_paragon_dlc_answer}
        ruler = {{ NOT = {{ has_trait = {trait_name} }} }}
    }}
    allow = {{
        custom_tooltip = xvcv_mdlc_core_modifying_tooltip_add_{leader_class}_{trait_name}
        {requires_subclass_trigger}xvcv_mdlc_core_modifying_requires_ruler_subclass_or_focus_trigger = {{ CLASS = {leader_class} ID = {required_subclass} }}
        xvcv_mdlc_core_modifying_trait_cost_{use_alt_trigger}trigger = yes
        xvcv_mdlc_core_modifying_trait_points_{use_alt_trigger}trigger = yes
        {requires_skill_lvl_trigger}xvcv_mdlc_core_modifying_trait_skill_level_alt_trigger = yes
        xvcv_mdlc_core_modifying_trait_max_number_trigger = yes
        {comment_out_paragon_dlc}has_paragon_dlc = {has_paragon_dlc_answer}
    }}
    effect = {{
        {needs_remove_tier_num_trait_effect}xvcv_mdlc_core_modifying_remove_tier_1_or_2_traits_effect = {{ ID = {trait_name_no_tier} }}
        xvcv_mdlc_core_modifying_trait_pick_effect = {{ CLASS = {leader_class} ID = {trait_name} }}
		hidden_effect = {{ xvcv_mdlc_core_modifying_trait_add_{use_alt_trigger}effect = yes }}
    }}
}}
xvcv_mdlc_core_modifying_traits_{leader_class}_{trait_name}_remove_button_effect = {{
    potential = {{
        {comment_out_paragon_dlc}has_paragon_dlc = {has_paragon_dlc_answer}
        ruler = {{ has_trait = {trait_name} }}
    }}
    allow = {{ always = yes }}
    effect = {{
        custom_tooltip = xvcv_mdlc_core_modifying_tooltip_remove_{leader_class}_{trait_name}
		hidden_effect = {{
            ruler = {{ remove_trait = {trait_name} }}
            xvcv_mdlc_core_modifying_trait_remove_{use_alt_trigger}effect = yes
		}}
    }}
}}
"""
