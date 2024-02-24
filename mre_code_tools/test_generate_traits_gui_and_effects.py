# Unit tests
from tempfile import NamedTemporaryFile
from json import dump as json_dump
from generate_traits_gui_and_effects import (
    gen_leader_making_button_effects_code,
    gen_core_modifying_trait_gui_code,
    gen_core_modifying_button_effects_code,
    gen_leader_making_trait_gui_code,
    gen_xvcv_mdlc_core_modifying_ruler_traits_trigger,
    gen_xvcv_mdlc_leader_making_clear_values_effect,
    gen_xvcv_mdlc_core_modifying_reset_traits_button_effect_lines,
    gen_core_modifying_leader_subclass_gui_code,
    gen_xvcv_mdlc_leader_making_start_button_effect,
)

def test_gen_core_modifying_button_effects_code__common_trait():

    trait_ruler_feedback_loop_2_code = gen_core_modifying_button_effects_code(
        "official", "trait_ruler_feedback_loop_2"
    )
    
    expected_effect_trait_ruler_feedback_2 = """
#trait_ruler_feedback_loop_2 #common trait
xvcv_mdlc_core_modifying_traits_official_trait_ruler_feedback_loop_2_add_button_effect = {
    potential = {
        ruler = { NOT = { has_trait = trait_ruler_feedback_loop_2 } }
    }
    allow = {
        custom_tooltip = xvcv_mdlc_core_modifying_tooltip_add_official_trait_ruler_feedback_loop_2
        #xvcv_mdlc_core_modifying_requires_ruler_subclass_or_focus_trigger = { CLASS = official ID = None }
        xvcv_mdlc_core_modifying_trait_cost_trigger = yes
        xvcv_mdlc_core_modifying_trait_points_trigger = yes
        #xvcv_mdlc_core_modifying_trait_skill_level_trigger = yes
        xvcv_mdlc_core_modifying_trait_max_number_trigger = yes
        #has_paragon_dlc = no
    }
    effect = {
        xvcv_mdlc_core_modifying_remove_tier_1_or_2_traits_effect = { ID = trait_ruler_feedback_loop }
        xvcv_mdlc_core_modifying_trait_pick_effect = { CLASS = official ID = trait_ruler_feedback_loop_2 }
        hidden_effect = { xvcv_mdlc_core_modifying_trait_add_effect = yes }
    }
}
xvcv_mdlc_core_modifying_traits_official_trait_ruler_feedback_loop_2_remove_button_effect = {
    potential = {
        ruler = { has_trait = trait_ruler_feedback_loop_2 }
    }
    allow = { always = yes }
    effect = {
        custom_tooltip = xvcv_mdlc_core_modifying_tooltip_remove_official_trait_ruler_feedback_loop_2
        hidden_effect = {
            ruler = { remove_trait = trait_ruler_feedback_loop_2 }
            xvcv_mdlc_core_modifying_trait_remove_effect = yes
        }
    }
}
"""
    assert expected_effect_trait_ruler_feedback_2 == trait_ruler_feedback_loop_2_code


def test_gen_core_modifying_button_effects_code__veteran_trait():

    leader_trait_frontier_spirit_3_code = gen_core_modifying_button_effects_code(
        "official", "leader_trait_frontier_spirit_3", is_veteran_trait=True,
        needs_paragon_dlc=True, required_subclass="subclass_official_diplomacy_councilor"
    )

    expected_effects_code = """
#leader_trait_frontier_spirit_3 #veteran trait
xvcv_mdlc_core_modifying_traits_official_leader_trait_frontier_spirit_3_add_button_effect = {
    potential = {
        ruler = { NOT = { has_trait = leader_trait_frontier_spirit_3 } }
    }
    allow = {
        custom_tooltip = xvcv_mdlc_core_modifying_tooltip_add_official_leader_trait_frontier_spirit_3
        xvcv_mdlc_core_modifying_requires_ruler_subclass_or_focus_trigger = { CLASS = official ID = subclass_official_diplomacy_councilor }
        xvcv_mdlc_core_modifying_trait_cost_alt_trigger = yes
        xvcv_mdlc_core_modifying_trait_points_alt_trigger = yes
        xvcv_mdlc_core_modifying_trait_skill_level_alt_trigger = yes
        xvcv_mdlc_core_modifying_trait_max_number_trigger = yes
        has_paragon_dlc = yes
    }
    effect = {
        xvcv_mdlc_core_modifying_remove_tier_1_or_2_traits_effect = { ID = leader_trait_frontier_spirit }
        xvcv_mdlc_core_modifying_trait_pick_effect = { CLASS = official ID = leader_trait_frontier_spirit_3 }
        hidden_effect = { xvcv_mdlc_core_modifying_trait_add_alt_effect = yes }
    }
}
xvcv_mdlc_core_modifying_traits_official_leader_trait_frontier_spirit_3_remove_button_effect = {
    potential = {
        ruler = { has_trait = leader_trait_frontier_spirit_3 }
    }
    allow = { always = yes }
    effect = {
        custom_tooltip = xvcv_mdlc_core_modifying_tooltip_remove_official_leader_trait_frontier_spirit_3
        hidden_effect = {
            ruler = { remove_trait = leader_trait_frontier_spirit_3 }
            xvcv_mdlc_core_modifying_trait_remove_alt_effect = yes
        }
    }
}
"""

    assert expected_effects_code == leader_trait_frontier_spirit_3_code

def test_gen_core_modifying_button_effects_code__destiny_trait():
    
    leader_trait_bellicose_code = gen_core_modifying_button_effects_code(
        "commander", "leader_trait_bellicose", is_destiny_trait=True,
        required_subclass="subclass_commander_general", needs_paragon_dlc=True
    )

    expected_code = """
#leader_trait_bellicose #destiny trait
xvcv_mdlc_core_modifying_traits_commander_leader_trait_bellicose_add_button_effect = {
    potential = {
        ruler = { NOT = { has_trait = leader_trait_bellicose } }
    }
    allow = {
        custom_tooltip = xvcv_mdlc_core_modifying_tooltip_add_commander_leader_trait_bellicose
        xvcv_mdlc_core_modifying_requires_ruler_subclass_or_focus_trigger = { CLASS = commander ID = subclass_commander_general }
        xvcv_mdlc_core_modifying_trait_cost_alt_2_trigger = yes
        xvcv_mdlc_core_modifying_trait_points_alt_2_trigger = yes
        xvcv_mdlc_core_modifying_trait_skill_level_alt_2_trigger = yes
        xvcv_mdlc_core_modifying_trait_max_number_trigger = yes
        has_paragon_dlc = yes
    }
    effect = {
        #xvcv_mdlc_core_modifying_remove_tier_1_or_2_traits_effect = { ID = leader_trait_bellicose }
        xvcv_mdlc_core_modifying_trait_pick_effect = { CLASS = commander ID = leader_trait_bellicose }
        hidden_effect = { xvcv_mdlc_core_modifying_trait_add_alt_2_effect = yes }
    }
}
xvcv_mdlc_core_modifying_traits_commander_leader_trait_bellicose_remove_button_effect = {
    potential = {
        ruler = { has_trait = leader_trait_bellicose }
    }
    allow = { always = yes }
    effect = {
        custom_tooltip = xvcv_mdlc_core_modifying_tooltip_remove_commander_leader_trait_bellicose
        hidden_effect = {
            ruler = { remove_trait = leader_trait_bellicose }
            xvcv_mdlc_core_modifying_trait_remove_alt_2_effect = yes
        }
    }
}
"""
    assert expected_code == leader_trait_bellicose_code

def test_gen_leadermaking_effects_code__adventurous_spirit_3():
    adventurous_spirit_effects_code = gen_leader_making_button_effects_code(
        leader_class="commander", trait_name="leader_trait_adventurous_spirit_3",
        is_veteran_trait=True
    )
    expected = """
#commander #leader_trait_adventurous_spirit_3 #veteran trait
xvcv_mdlc_leader_making_trait_commander_leader_trait_adventurous_spirit_3_add_button_effect = {
    potential = { always = yes }
    allow = {
        xvcv_mdlc_leader_making_trait_pick_trigger = { CLASS = commander ID = leader_trait_adventurous_spirit_3 }
        xvcv_mdlc_leader_making_trait_cost_alt_trigger = yes
        xvcv_mdlc_leader_making_trait_points_alt_trigger = yes
        xvcv_mdlc_leader_making_trait_skill_level_alt_trigger = yes
        xvcv_mdlc_leader_making_trait_max_number_trigger = yes
        xvcv_mdlc_leader_making_picked_class_commander_trigger = yes
    }
    effect = {
        xvcv_mdlc_leader_making_trait_pick_effect = { CLASS = commander ID = leader_trait_adventurous_spirit_3 }
        hidden_effect = { xvcv_mdlc_leader_making_trait_count_points_costs_alt_effect = yes }
    }
}
"""
    assert expected == adventurous_spirit_effects_code


def test_gen_xvcv_mdlc_core_modifying_ruler_traits_trigger():
    traits_json_file = NamedTemporaryFile(delete=False)
    traits_dict = {
        "core_modifying_traits": {
            "common": [
                {
                "leader_trait_roamer_2": {
                    "trait_name": "leader_trait_roamer_2",
                    "leader_class": "scientist",
                    "gfx": "GFX_leader_trait_roamer",
                    "rarity": "common",
                    "modifier": {
                        "science_ship_survey_speed": 0.2
                    },
                    "requires_paragon_dlc": False,
                }
            }
            ]
        }
    }
    with open(traits_json_file.name, "w+t") as mtmp:
        json_dump(traits_dict, mtmp)
    test_input_files_list = [traits_json_file.name]
    expected = """
xvcv_mdlc_core_modifying_ruler_traits_trigger = {
    optimize_memory
    OR = {
        has_trait = leader_trait_roamer_2
        has_trait = subclass_commander_admiral
        has_trait = subclass_commander_councilor
        has_trait = subclass_commander_general
        has_trait = subclass_commander_governor
        has_trait = subclass_official_delegate
        has_trait = subclass_official_diplomacy_councilor
        has_trait = subclass_official_economy_councilor
        has_trait = subclass_official_governor
        has_trait = subclass_scientist_councilor
        has_trait = subclass_scientist_explorer
        has_trait = subclass_scientist_governor
        has_trait = subclass_scientist_scholar
    }
}
"""
    actual = gen_xvcv_mdlc_core_modifying_ruler_traits_trigger(test_input_files_list)
    traits_json_file.close()
    assert expected == actual

def test_gen_xvcv_mdlc_core_modifying_reset_traits_button_effect_lines():
    1

def test_iterate_core_modifying_leader_subclass_gui_code():
    # test_data = "subclass_official_economy_councilor"
    expected_result = """
#official #subclass_official_economy_councilor #advisor
containerWindowType = {
    name = "xvcv_mdlc_core_modifying_traits_official_subclass_official_economy_councilor"
    position = { x = @xvcv_mdlc_core_modifying_trait_position_column_1 y = @xvcv_mdlc_core_modifying_trait_position_row_1 }
    effectbuttonType = {
        name = "xvcv_mdlc_core_modifying_traits_official_subclass_official_economy_councilor_add"
        position = { x = @xvcv_mdlc_core_modifying_subclass_traits_offset_width y = @xvcv_mdlc_core_modifying_subclass_traits_offset_height }
        spriteType = "GFX_leader_subclass_official_economy_councilor_medium"
        effect = "xvcv_mdlc_core_modifying_traits_official_subclass_official_economy_councilor_add_button_effect"
    }
    effectbuttonType = {
        name = "xvcv_mdlc_core_modifying_traits_official_subclass_official_economy_councilor_remove"
        position = { x = @xvcv_mdlc_core_modifying_subclass_traits_offset_width y = @xvcv_mdlc_core_modifying_subclass_traits_offset_height }
        spriteType = "GFX_leader_subclass_official_economy_councilor_medium_red"
        effect = "xvcv_mdlc_core_modifying_traits_official_subclass_official_economy_councilor_remove_button_effect"
    }
}
"""
    actual = gen_core_modifying_leader_subclass_gui_code(
        "subclass_official_economy_councilor", 1, 1
    )
    assert expected_result == actual

def test_gen_xvcv_mdlc_leader_making_start_button_effect():
    mock_json_data_from_file = {
        "leader_making_traits": {
            "common": [
                {
                "leader_trait_roamer_2": {
                    "trait_name": "leader_trait_roamer_2",
                    "leader_class": "official",
                    "gfx": "GFX_leader_trait_roamer",
                    "rarity": "common",
                    "modifier": {
                        "science_ship_survey_speed": 0.2
                    },
                    "requires_paragon_dlc": False,
                }
            }
            ]
        }
    }
    expected = """
#official
event_target:xvcv_mdlc_leader_making_target = {
    if = { limit = { prev = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_roamer_2 } } add_trait_no_notify = leader_trait_roamer_2 }
    if = { limit = { prev = { has_country_flag = xvcv_mdlc_leader_official_subclass_official_economy_councilor } } add_trait_no_notify = subclass_official_economy_councilor }
    if = { limit = { prev = { has_country_flag = xvcv_mdlc_leader_official_subclass_official_diplomacy_councilor } } add_trait_no_notify = subclass_official_diplomacy_councilor }
    if = { limit = { prev = { has_country_flag = xvcv_mdlc_leader_official_subclass_official_governor } } add_trait_no_notify = subclass_official_governor }
    if = { limit = { prev = { has_country_flag = xvcv_mdlc_leader_official_subclass_official_delegate } } add_trait_no_notify = subclass_official_delegate }
    if = { limit = { prev = { has_country_flag = xvcv_mdlc_leader_official_xvcv_mdlc_leader_trait_memory_backup } } add_trait_no_notify = xvcv_mdlc_leader_trait_memory_backup }
    if = { limit = { prev = { has_country_flag = xvcv_mdlc_leader_official_xvcv_mdlc_leader_trait_shared_memory } } add_trait_no_notify = xvcv_mdlc_leader_trait_shared_memory }
}
"""
    actual = gen_xvcv_mdlc_leader_making_start_button_effect(mock_json_data_from_file, for_class="official")
    assert expected == actual

def test_generate_dlc_dependency_from_prerequisites():
    """ Translate prereqs from a known dict of DLC reqs """
    mock_json_data_from_file = {
        "leader_making_traits": {
            "veteran": {
                "leader_trait_explorer_cloaking_focus_3": {
                    "trait_name": "leader_trait_explorer_cloaking_focus_3",
                    "gfx": "GFX_leader_trait_explorer_cloaking_focus",
                    "leader_class": "scientist",
                    "rarity": "veteran",
                    "requires_paragon_dlc": False,
                    "modifier": {
                        "ship_cloaking_strength_add": 2
                    },
                    "prerequisites": [ "tech_cloaking_1" ],
                    "custom_tooltip": "leader_trait_explorer_cloaking_focus_3_tt"
                }
            }
        }
    }
    # Leader-making, since this isn't a ruler trait
    leader_trait_explorer_cloaking_focus_3_code = gen_leader_making_button_effects_code(
        leader_class="commander", trait_name="leader_trait_sweaty_palmfronds_3",
        is_veteran_trait=True, prerequisites=["tech_cloaking_1"]
    )
    expected = """
#commander #leader_trait_sweaty_palmfronds_3 #veteran trait
xvcv_mdlc_leader_making_trait_commander_leader_trait_sweaty_palmfronds_3_add_button_effect = {
    potential = { always = yes }
    allow = {
        xvcv_mdlc_leader_making_trait_pick_trigger = { CLASS = commander ID = leader_trait_sweaty_palmfronds_3 }
        xvcv_mdlc_leader_making_trait_cost_alt_trigger = yes
        xvcv_mdlc_leader_making_trait_points_alt_trigger = yes
        xvcv_mdlc_leader_making_trait_skill_level_alt_trigger = yes
        xvcv_mdlc_leader_making_trait_max_number_trigger = yes
        xvcv_mdlc_leader_making_picked_class_commander_trigger = yes
        has_technology = tech_cloaking_1
    }
    effect = {
        xvcv_mdlc_leader_making_trait_pick_effect = { CLASS = commander ID = leader_trait_sweaty_palmfronds_3 }
        hidden_effect = { xvcv_mdlc_leader_making_trait_count_points_costs_alt_effect = yes }
    }
}
"""
    assert expected == leader_trait_explorer_cloaking_focus_3_code
