# Unit tests

from generate_traits_gui_and_effects import (
    gen_leader_making_button_effects_code,
    gen_core_modifying_trait_gui_code,
    gen_core_modifying_button_effects_code,
    gen_leader_making_trait_gui_code
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
        has_paragon_dlc = yes
    }
    effect = {
        xvcv_mdlc_leader_making_trait_pick_effect = { CLASS = commander ID = leader_trait_adventurous_spirit_3 }
        hidden_effect = { xvcv_mdlc_leader_making_trait_count_points_costs_alt_effect = yes }
    }
}
"""
    assert expected == adventurous_spirit_effects_code
