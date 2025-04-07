from mre_code_tools.pipeline.compile.mre_generate_councilor_editor_gui import gen_councilor_editor_traits_gui_code

def test_gen_councilor_editor_traits_gui_code__leader_trait_army_veteran_2():
    test_data = {
        "leader_trait_army_veteran_2": {
            "trait_name": "leader_trait_army_veteran_2",
            "leader_class": "official",
            "gfx": "GFX_leader_trait_army_veteran",
            "rarity": "common",
            "is_councilor_trait": True,
            "councilor_modifier": {
                "planet_army_build_speed_mult": 0.25,
                "armies_cost_mult": -0.1,
                "army_defense_damage_mult": 0.25
            },
            "requires_paragon_dlc": False
        }
    }
    expected = """
#regulatory #leader_trait_army_veteran_2 #common
containerWindowType = {
    name = "oxr_mdlc_councilor_editor_regulatory_traits_leader_trait_army_veteran_2"
    position = { x = @oxr_mdlc_councilor_editor_trait_position_column_1 y = @oxr_mdlc_councilor_editor_trait_position_row_1 }
    effectbuttonType = {
        name = "oxr_mdlc_councilor_editor_regulatory_traits_leader_trait_army_veteran_2_add_bg"
        position = { x = @oxr_mdlc_councilor_editor_traits_background_offset_width y = @oxr_mdlc_councilor_editor_traits_background_offset_height }
        spriteType = "GFX_xvcv_mdlc_leader_trait_background_green"
        effect = "oxr_mdlc_councilor_editor_regulatory_leader_trait_army_veteran_2_add_button_effect"
    }
    effectbuttonType = {
        name = "oxr_mdlc_councilor_editor_regulatory_traits_leader_trait_army_veteran_2_add"
        spriteType = "GFX_leader_trait_army_veteran"
        effect = "oxr_mdlc_councilor_editor_regulatory_leader_trait_army_veteran_2_add_button_effect"
    }
    effectbuttonType = {
        name = "oxr_mdlc_councilor_editor_regulatory_traits_leader_trait_army_veteran_2_remove_bg"
        position = { x = @oxr_mdlc_councilor_editor_traits_background_offset_width y = @oxr_mdlc_councilor_editor_traits_background_offset_height }
        spriteType = "GFX_xvcv_mdlc_leader_trait_background_red"
        effect = "oxr_mdlc_councilor_editor_regulatory_leader_trait_army_veteran_2_remove_button_effect"
    }
    effectbuttonType = {
        name = "oxr_mdlc_councilor_editor_regulatory_traits_leader_trait_army_veteran_2_remove"
        spriteType = "GFX_leader_trait_army_veteran"
        effect = "oxr_mdlc_councilor_editor_regulatory_leader_trait_army_veteran_2_remove_button_effect"
    }
}
"""
    actual = gen_councilor_editor_traits_gui_code(
        councilor_type="regulatory", trait_name="leader_trait_army_veteran_2",
        column_num=1, row_num=1, gfx_sprite_name="GFX_leader_trait_army_veteran",
        trait_type="common"
    )
    assert expected == actual

def test_gen_councilor_editor_traits_gui_code__leader_trait_adventurous_spirit_3():
    expected = """
#regulatory #leader_trait_cartographer_3 #veteran
containerWindowType = {
    name = "oxr_mdlc_councilor_editor_regulatory_traits_leader_trait_cartographer_3"
    position = { x = @oxr_mdlc_councilor_editor_trait_position_column_1 y = @oxr_mdlc_councilor_editor_trait_position_row_1 }
    effectbuttonType = {
        name = "oxr_mdlc_councilor_editor_regulatory_traits_leader_trait_cartographer_3_add_bg"
        position = { x = @oxr_mdlc_councilor_editor_traits_background_offset_width y = @oxr_mdlc_councilor_editor_traits_background_offset_height }
        spriteType = "GFX_xvcv_mdlc_leader_trait_background_veteran"
        effect = "oxr_mdlc_councilor_editor_regulatory_leader_trait_cartographer_3_add_button_effect"
    }
    effectbuttonType = {
        name = "oxr_mdlc_councilor_editor_regulatory_traits_leader_trait_cartographer_3_add"
        spriteType = "GFX_leader_trait_cartographer"
        effect = "oxr_mdlc_councilor_editor_regulatory_leader_trait_cartographer_3_add_button_effect"
    }
    effectbuttonType = {
        name = "oxr_mdlc_councilor_editor_regulatory_traits_leader_trait_cartographer_3_remove_bg"
        position = { x = @oxr_mdlc_councilor_editor_traits_background_offset_width y = @oxr_mdlc_councilor_editor_traits_background_offset_height }
        spriteType = "GFX_xvcv_mdlc_leader_trait_background_veteran_red"
        effect = "oxr_mdlc_councilor_editor_regulatory_leader_trait_cartographer_3_remove_button_effect"
    }
    effectbuttonType = {
        name = "oxr_mdlc_councilor_editor_regulatory_traits_leader_trait_cartographer_3_remove"
        spriteType = "GFX_leader_trait_cartographer"
        effect = "oxr_mdlc_councilor_editor_regulatory_leader_trait_cartographer_3_remove_button_effect"
    }
}
"""
    actual = gen_councilor_editor_traits_gui_code(
        councilor_type="regulatory", trait_name="leader_trait_cartographer_3",
        column_num=1, row_num=1, gfx_sprite_name="GFX_leader_trait_cartographer",
        trait_type="veteran"
    )
    assert expected == actual

def test_gen_councilor_editor_traits_gui_code__destiny_trait():
    expected = """
#regulatory #leader_trait_chainbreaker #paragon
containerWindowType = {
    name = "oxr_mdlc_councilor_editor_regulatory_traits_leader_trait_chainbreaker"
    position = { x = @oxr_mdlc_councilor_editor_trait_position_column_2 y = @oxr_mdlc_councilor_editor_trait_position_row_2 }
    effectbuttonType = {
        name = "oxr_mdlc_councilor_editor_regulatory_traits_leader_trait_chainbreaker_add_bg"
        position = { x = @oxr_mdlc_councilor_editor_traits_background_offset_width y = @oxr_mdlc_councilor_editor_traits_background_offset_height }
        spriteType = "GFX_xvcv_mdlc_leader_trait_background_destiny"
        effect = "oxr_mdlc_councilor_editor_regulatory_leader_trait_chainbreaker_add_button_effect"
    }
    effectbuttonType = {
        name = "oxr_mdlc_councilor_editor_regulatory_traits_leader_trait_chainbreaker_add"
        spriteType = "GFX_leader_trait_chainbreaker"
        effect = "oxr_mdlc_councilor_editor_regulatory_leader_trait_chainbreaker_add_button_effect"
    }
    effectbuttonType = {
        name = "oxr_mdlc_councilor_editor_regulatory_traits_leader_trait_chainbreaker_remove_bg"
        position = { x = @oxr_mdlc_councilor_editor_traits_background_offset_width y = @oxr_mdlc_councilor_editor_traits_background_offset_height }
        spriteType = "GFX_xvcv_mdlc_leader_trait_background_destiny_red"
        effect = "oxr_mdlc_councilor_editor_regulatory_leader_trait_chainbreaker_remove_button_effect"
    }
    effectbuttonType = {
        name = "oxr_mdlc_councilor_editor_regulatory_traits_leader_trait_chainbreaker_remove"
        spriteType = "GFX_leader_trait_chainbreaker"
        effect = "oxr_mdlc_councilor_editor_regulatory_leader_trait_chainbreaker_remove_button_effect"
    }
}
"""
    actual = gen_councilor_editor_traits_gui_code(
        councilor_type="regulatory", trait_name="leader_trait_chainbreaker",
        column_num=2, row_num=2, gfx_sprite_name="GFX_leader_trait_chainbreaker",
        trait_type="paragon"
    )
    assert expected == actual

