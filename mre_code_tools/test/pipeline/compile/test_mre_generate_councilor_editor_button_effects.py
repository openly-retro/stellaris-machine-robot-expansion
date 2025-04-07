from mre_code_tools.pipeline.compile.mre_generate_councilor_editor_button_effects import (
    gen_councilor_editor_traits_button_effects_code,
)

def test_gen_councilor_editor_btn_fx_code__leader_trait_spycraft_2():
    expected = """
#regulatory #leader_trait_army_veteran_2 #common
oxr_mdlc_councilor_editor_regulatory_leader_trait_army_veteran_2_add_button_effect = {
	potential = {
		event_target:oxr_mdlc_councilor_editor_target_@root_0 = { NOT = { has_trait = leader_trait_army_veteran_2 } }
	}
	allow = {
		custom_tooltip = xvcv_mdlc_core_modifying_tooltip_add_official_leader_trait_army_veteran_2
		oxr_mdlc_councilor_editor_check_trait_resources_cost_common = yes
		event_target:oxr_mdlc_councilor_editor_target_@root_0 = {
			oxr_mdlc_councilor_editor_check_trait_points_cost_common = yes
			oxr_mdlc_councilor_editor_check_trait_picks = yes
			#oxr_mdlc_councilor_editor_check_leader_has_required_subclass = { CLASS = official SUBCLASS = None }
		}
		
	}
	effect = {
		custom_tooltip = oxr_mdlc_councilor_editor_show_trait_total_cost_common
		event_target:oxr_mdlc_councilor_editor_target_@root_0 = {
			oxr_mdlc_councilor_editor_remove_tier_1_or_2_traits_effect = { TRAIT_NAME = leader_trait_army_veteran }
			add_trait_no_notify = leader_trait_army_veteran_2
		}
		hidden_effect = {
			oxr_mdlc_councilor_editor_deduct_trait_resources_cost_common = yes
			event_target:oxr_mdlc_councilor_editor_target_@root_0 = {
				oxr_mdlc_councilor_editor_deduct_trait_points_cost_common = yes
				oxr_mdlc_councilor_editor_deduct_trait_pick = yes
			}
		}
	}
}
oxr_mdlc_councilor_editor_regulatory_leader_trait_army_veteran_2_remove_button_effect = {
	potential = {
		event_target:oxr_mdlc_councilor_editor_target_@root_0 = { has_trait = leader_trait_army_veteran_2 }
	}
	allow = { always = yes }
	effect = {
		custom_tooltip = xvcv_mdlc_core_modifying_tooltip_remove_official_leader_trait_army_veteran_2
		hidden_effect = {
			event_target:oxr_mdlc_councilor_editor_target_@root_0 = {
				remove_trait = leader_trait_army_veteran_2
				oxr_mdlc_councilor_editor_refund_trait_points_cost_common = yes
				oxr_mdlc_councilor_editor_refund_trait_pick = yes
			}
			oxr_mdlc_councilor_editor_refund_trait_resources_cost_common = yes
		}
	}
}
"""
    actual = gen_councilor_editor_traits_button_effects_code(
        councilor_type="regulatory", trait_name="leader_trait_army_veteran_2",
        rarity="common"
    )
    assert expected == actual


def test_gen_councilor_editor_btn_fx_code__veteran_trait():
    test_data = {
		"leader_trait_armada_logistician_3": {
			"trait_name": "leader_trait_armada_logistician_3",
			"leader_class": "commander",
			"gfx": "GFX_leader_trait_armada_logistician",
			"rarity": "veteran",
			"is_councilor_trait": True,
			"councilor_modifier": {
				"ship_orbit_upkeep_mult": -0.1,
				"country_naval_cap_mult": 0.075
			},
			"requires_paragon_dlc": True,
			"required_subclass": "subclass_commander_councilor"
		}
	}
    expected = """
#legion #leader_trait_armada_logistician_3 #veteran
oxr_mdlc_councilor_editor_legion_leader_trait_armada_logistician_3_add_button_effect = {
	potential = {
		event_target:oxr_mdlc_councilor_editor_target_@root_0 = { NOT = { has_trait = leader_trait_armada_logistician_3 } }
	}
	allow = {
		custom_tooltip = xvcv_mdlc_core_modifying_tooltip_add_commander_leader_trait_armada_logistician_3
		oxr_mdlc_councilor_editor_check_trait_resources_cost_veteran = yes
		event_target:oxr_mdlc_councilor_editor_target_@root_0 = {
			oxr_mdlc_councilor_editor_check_trait_points_cost_veteran = yes
			oxr_mdlc_councilor_editor_check_trait_picks = yes
			oxr_mdlc_councilor_editor_check_leader_has_required_subclass = { CLASS = commander SUBCLASS = subclass_commander_councilor }
		}
		
	}
	effect = {
		custom_tooltip = oxr_mdlc_councilor_editor_show_trait_total_cost_veteran
		event_target:oxr_mdlc_councilor_editor_target_@root_0 = {
			oxr_mdlc_councilor_editor_remove_tier_1_or_2_traits_effect = { TRAIT_NAME = leader_trait_armada_logistician }
			add_trait_no_notify = leader_trait_armada_logistician_3
		}
		hidden_effect = {
			oxr_mdlc_councilor_editor_deduct_trait_resources_cost_veteran = yes
			event_target:oxr_mdlc_councilor_editor_target_@root_0 = {
				oxr_mdlc_councilor_editor_deduct_trait_points_cost_veteran = yes
				oxr_mdlc_councilor_editor_deduct_trait_pick = yes
			}
		}
	}
}
oxr_mdlc_councilor_editor_legion_leader_trait_armada_logistician_3_remove_button_effect = {
	potential = {
		event_target:oxr_mdlc_councilor_editor_target_@root_0 = { has_trait = leader_trait_armada_logistician_3 }
	}
	allow = { always = yes }
	effect = {
		custom_tooltip = xvcv_mdlc_core_modifying_tooltip_remove_commander_leader_trait_armada_logistician_3
		hidden_effect = {
			event_target:oxr_mdlc_councilor_editor_target_@root_0 = {
				remove_trait = leader_trait_armada_logistician_3
				oxr_mdlc_councilor_editor_refund_trait_points_cost_veteran = yes
				oxr_mdlc_councilor_editor_refund_trait_pick = yes
			}
			oxr_mdlc_councilor_editor_refund_trait_resources_cost_veteran = yes
		}
	}
}
"""
    actual = gen_councilor_editor_traits_button_effects_code(
        councilor_type="legion",
        trait_name="leader_trait_armada_logistician_3",
        rarity="veteran", required_subclass="subclass_commander_councilor"
    )
    assert expected == actual

def test_gen_councilor_editor_btn_fx_code__destiny_trait():
    pass

def test_gen_councilor_editor_btn_fx_code__trait_requires_subclass():
    pass
