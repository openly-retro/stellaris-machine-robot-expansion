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
#trait_ruler_feedback_loop_2
xvcv_mdlc_core_modifying_traits_official_trait_ruler_feedback_loop_2_add_button_effect = {
    potential = {
        #has_paragon_dlc = no
        ruler = { NOT = { has_trait = trait_ruler_feedback_loop_2 } }
    }
    allow = {
        custom_tooltip = xvcv_mdlc_core_modifying_tooltip_add_official_trait_ruler_feedback_loop_2
        #xvcv_mdlc_core_modifying_requires_ruler_subclass_or_focus_trigger = { CLASS = official ID = None }
        xvcv_mdlc_core_modifying_trait_cost_trigger = yes
        xvcv_mdlc_core_modifying_trait_points_trigger = yes
        #xvcv_mdlc_core_modifying_trait_skill_level_alt_trigger = yes
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
        #has_paragon_dlc = no
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
    assert trait_ruler_feedback_loop_2_code == expected_effect_trait_ruler_feedback_2


def test_gen_core_modifying_button_effects_code__veteran_trait():

    leader_trait_frontier_spirit_3_code = gen_core_modifying_button_effects_code(
        "official", "leader_trait_frontier_spirit_3", is_veteran_trait=True,
        needs_paragon_dlc=True, required_subclass="subclass_official_diplomacy_councilor"
    )

    expected_effects_code = """
#leader_trait_frontier_spirit_3 #veteran trait
xvcv_mdlc_core_modifying_traits_official_leader_trait_frontier_spirit_3_add_button_effect = {
    potential = {
        has_paragon_dlc = yes
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
        has_paragon_dlc = yes
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

    assert leader_trait_frontier_spirit_3_code == expected_effects_code
