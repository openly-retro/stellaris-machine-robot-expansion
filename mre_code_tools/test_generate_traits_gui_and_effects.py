# Unit tests

from generate_traits_gui_and_effects import (
    gen_leader_making_button_effects_code,
    gen_core_modifying_trait_gui_code,
    gen_core_modifying_button_effects_code,
    gen_leader_making_trait_gui_code,
    gen_xvcv_mdlc_core_modifying_ruler_traits_trigger,
    gen_xvcv_mdlc_leader_making_clear_values_effect,
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
        #xvcv_mdlc_leader_making_requires_leader_subclass_trigger = { CLASS = commander ID = None }
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
    actual = gen_xvcv_mdlc_core_modifying_ruler_traits_trigger(traits_dict)
    assert expected == actual


def test_gen_xvcv_mdlc_leader_making_clear_values_effect():
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
    expected = """
xvcv_mdlc_leader_making_clear_values_effect = {
    optimize_memory
    if = {
        limit = { xvcv_mdlc_leader_making_picked_any_skill_level_trigger = yes }
        xvcv_mdlc_leader_making_clear_skill_levels_effect = yes
    }

    #commander
    if = {
        limit = { has_country_flag = xvcv_mdlc_leader_class_set_to_commander }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_xvcv_mdlc_leader_trait_memory_backup } remove_country_flag = xvcv_mdlc_leader_commander_xvcv_mdlc_leader_trait_memory_backup }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_xvcv_mdlc_leader_trait_shared_memory } remove_country_flag = xvcv_mdlc_leader_commander_xvcv_mdlc_leader_trait_shared_memory }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_xvcv_mdlc_subclass_commander_none } remove_country_flag = xvcv_mdlc_leader_commander_xvcv_mdlc_subclass_commander_none }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_adaptable_2 } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_adaptable_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_armada_logistician_3 } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_armada_logistician_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_armorer } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_armorer }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_aturion_organizer } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_aturion_organizer }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_border_guard_3 } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_border_guard_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_crew_trainer_3 } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_crew_trainer_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_defence_engineer_2 } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_defence_engineer_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_educator } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_educator }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_emotional_support_pet } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_emotional_support_pet }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_fleet_organizer_2 } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_fleet_organizer_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_gale_speed_3 } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_gale_speed_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_gifted_2 } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_gifted_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_guardian_3 } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_guardian_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_home_guard_3 } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_home_guard_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_intimidator_3 } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_intimidator_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_master_bureaucrat } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_master_bureaucrat }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_maven_of_war } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_maven_of_war }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_military_overseer } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_military_overseer }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_peacekeeper } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_peacekeeper }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_politician_2 } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_politician_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_resilient_2 } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_resilient_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_leader_trait_skirmisher_2 } remove_country_flag = xvcv_mdlc_leader_commander_leader_trait_skirmisher_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_trait_ruler_battleship_focus } remove_country_flag = xvcv_mdlc_leader_commander_trait_ruler_battleship_focus }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_trait_ruler_champion_of_the_people_2 } remove_country_flag = xvcv_mdlc_leader_commander_trait_ruler_champion_of_the_people_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_trait_ruler_charismatic_2 } remove_country_flag = xvcv_mdlc_leader_commander_trait_ruler_charismatic_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_trait_ruler_corvette_focus } remove_country_flag = xvcv_mdlc_leader_commander_trait_ruler_corvette_focus }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_trait_ruler_cruiser_focus } remove_country_flag = xvcv_mdlc_leader_commander_trait_ruler_cruiser_focus }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_trait_ruler_destroyer_focus } remove_country_flag = xvcv_mdlc_leader_commander_trait_ruler_destroyer_focus }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_trait_ruler_eye_for_talent_2 } remove_country_flag = xvcv_mdlc_leader_commander_trait_ruler_eye_for_talent_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_trait_ruler_feedback_loop_2 } remove_country_flag = xvcv_mdlc_leader_commander_trait_ruler_feedback_loop_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_trait_ruler_fortifier_3 } remove_country_flag = xvcv_mdlc_leader_commander_trait_ruler_fortifier_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_trait_ruler_from_the_ranks_3 } remove_country_flag = xvcv_mdlc_leader_commander_trait_ruler_from_the_ranks_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_trait_ruler_logistic_understanding_2 } remove_country_flag = xvcv_mdlc_leader_commander_trait_ruler_logistic_understanding_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_trait_ruler_military_pioneer_3 } remove_country_flag = xvcv_mdlc_leader_commander_trait_ruler_military_pioneer_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_trait_ruler_recruiter_3 } remove_country_flag = xvcv_mdlc_leader_commander_trait_ruler_recruiter_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_commander_trait_ruler_warlike_2 } remove_country_flag = xvcv_mdlc_leader_commander_trait_ruler_warlike_2 }
        remove_country_flag = xvcv_mdlc_leader_class_set_to_commander
    }
    #official
    if = {
        limit = { has_country_flag = xvcv_mdlc_leader_class_set_to_official }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_xvcv_mdlc_leader_trait_memory_backup } remove_country_flag = xvcv_mdlc_leader_official_xvcv_mdlc_leader_trait_memory_backup }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_xvcv_mdlc_leader_trait_shared_memory } remove_country_flag = xvcv_mdlc_leader_official_xvcv_mdlc_leader_trait_shared_memory }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_xvcv_mdlc_subclass_official_none } remove_country_flag = xvcv_mdlc_leader_official_xvcv_mdlc_subclass_official_none }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_adaptable_2 } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_adaptable_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_army_veteran_2 } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_army_veteran_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_cartographer_3 } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_cartographer_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_consul_general_3 } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_consul_general_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_courtroom_training_3 } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_courtroom_training_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_cultural_focus_3 } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_cultural_focus_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_educator } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_educator }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_emotional_support_pet } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_emotional_support_pet }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_expeditionist_3 } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_expeditionist_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_frontier_spirit_3 } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_frontier_spirit_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_gifted_2 } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_gifted_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_master_bureaucrat } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_master_bureaucrat }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_master_diplomat } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_master_diplomat }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_overseer_3 } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_overseer_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_peacekeeper } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_peacekeeper }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_politician_2 } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_politician_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_principled_2 } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_principled_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_reformer_3 } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_reformer_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_resilient_2 } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_resilient_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_retired_fleet_officer_2 } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_retired_fleet_officer_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_shadow_broker_3 } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_shadow_broker_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_shipwright_2 } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_shipwright_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_spycraft_2 } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_spycraft_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_spymaster } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_spymaster }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_supreme_organizer } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_supreme_organizer }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_leader_trait_totalitarian } remove_country_flag = xvcv_mdlc_leader_official_leader_trait_totalitarian }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_trait_ruler_architectural_sense_3 } remove_country_flag = xvcv_mdlc_leader_official_trait_ruler_architectural_sense_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_trait_ruler_champion_of_the_people_2 } remove_country_flag = xvcv_mdlc_leader_official_trait_ruler_champion_of_the_people_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_trait_ruler_charismatic_2 } remove_country_flag = xvcv_mdlc_leader_official_trait_ruler_charismatic_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_trait_ruler_deep_connections_3 } remove_country_flag = xvcv_mdlc_leader_official_trait_ruler_deep_connections_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_trait_ruler_eye_for_talent_2 } remove_country_flag = xvcv_mdlc_leader_official_trait_ruler_eye_for_talent_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_trait_ruler_feedback_loop_2 } remove_country_flag = xvcv_mdlc_leader_official_trait_ruler_feedback_loop_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_trait_ruler_fertility_preacher_2 } remove_country_flag = xvcv_mdlc_leader_official_trait_ruler_fertility_preacher_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_trait_ruler_frontier_spirit } remove_country_flag = xvcv_mdlc_leader_official_trait_ruler_frontier_spirit }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_trait_ruler_industrialist_2 } remove_country_flag = xvcv_mdlc_leader_official_trait_ruler_industrialist_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_trait_ruler_investor_3 } remove_country_flag = xvcv_mdlc_leader_official_trait_ruler_investor_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_official_trait_ruler_logistic_understanding_2 } remove_country_flag = xvcv_mdlc_leader_official_trait_ruler_logistic_understanding_2 }
        remove_country_flag = xvcv_mdlc_leader_class_set_to_official
    }
    #scientist
    if = {
        limit = { has_country_flag = xvcv_mdlc_leader_class_set_to_scientist }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_xvcv_mdlc_leader_trait_memory_backup } remove_country_flag = xvcv_mdlc_leader_scientist_xvcv_mdlc_leader_trait_memory_backup }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_xvcv_mdlc_leader_trait_shared_memory } remove_country_flag = xvcv_mdlc_leader_scientist_xvcv_mdlc_leader_trait_shared_memory }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_xvcv_mdlc_subclass_scientist_none } remove_country_flag = xvcv_mdlc_leader_scientist_xvcv_mdlc_subclass_scientist_none }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_adaptable_2 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_adaptable_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_army_veteran_2 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_army_veteran_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_brilliant_shipwright } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_brilliant_shipwright }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_cartographer_3 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_cartographer_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_educator } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_educator }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_emotional_support_pet } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_emotional_support_pet }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_archaeostudies_3 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_archaeostudies_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_biology_3 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_biology_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_computing_3 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_computing_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_field_manipulation_3 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_field_manipulation_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_industry_3 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_industry_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_materials_3 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_materials_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_military_theory_3 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_military_theory_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_new_worlds_3 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_new_worlds_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_particles_3 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_particles_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_propulsion_3 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_propulsion_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_psionics_3 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_psionics_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_statecraft_3 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_statecraft_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_voidcraft_3 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_expertise_voidcraft_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_gifted_2 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_gifted_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_great_researcher } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_great_researcher }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_inquisitive_3 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_inquisitive_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_knowledge_for_the_masses } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_knowledge_for_the_masses }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_maniacal_3 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_maniacal_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_master_bureaucrat } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_master_bureaucrat }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_percussive_maintainer } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_percussive_maintainer }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_politician_2 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_politician_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_resilient_2 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_resilient_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_retired_fleet_officer_2 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_retired_fleet_officer_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_science_communicator_3 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_science_communicator_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_leader_trait_spark_of_genius_2 } remove_country_flag = xvcv_mdlc_leader_scientist_leader_trait_spark_of_genius_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_trait_ruler_champion_of_the_people_2 } remove_country_flag = xvcv_mdlc_leader_scientist_trait_ruler_champion_of_the_people_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_trait_ruler_charismatic_2 } remove_country_flag = xvcv_mdlc_leader_scientist_trait_ruler_charismatic_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_trait_ruler_expansionist_3 } remove_country_flag = xvcv_mdlc_leader_scientist_trait_ruler_expansionist_3 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_trait_ruler_eye_for_talent_2 } remove_country_flag = xvcv_mdlc_leader_scientist_trait_ruler_eye_for_talent_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_trait_ruler_feedback_loop_2 } remove_country_flag = xvcv_mdlc_leader_scientist_trait_ruler_feedback_loop_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_trait_ruler_home_in_the_sky } remove_country_flag = xvcv_mdlc_leader_scientist_trait_ruler_home_in_the_sky }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_trait_ruler_industrialist_2 } remove_country_flag = xvcv_mdlc_leader_scientist_trait_ruler_industrialist_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_trait_ruler_logistic_understanding_2 } remove_country_flag = xvcv_mdlc_leader_scientist_trait_ruler_logistic_understanding_2 }
        if = { limit = { has_country_flag = xvcv_mdlc_leader_scientist_trait_ruler_space_miner } remove_country_flag = xvcv_mdlc_leader_scientist_trait_ruler_space_miner }
        remove_country_flag = xvcv_mdlc_leader_class_set_to_scientist
    }
    xvcv_mdlc_leader_making_clear_traits_variables_effect = yes
}
"""
    actual = gen_xvcv_mdlc_leader_making_clear_values_effect()
    # print(actual)
    assert expected == actual
