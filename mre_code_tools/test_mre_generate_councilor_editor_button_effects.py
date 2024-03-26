from mre_generate_councilor_editor_button_effects import (
    gen_councilor_editor_traits_button_effects_code,
)

def test_gen_councilor_editor_btn_fx_code__leader_trait_spycraft_2():
    expected = """
#regulatory #leader_trait_army_veteran_2 #common
oxr_mdlc_councilor_editor_regulatory_leader_trait_army_veteran_2_add_button_effect = {
	potential = {
		event_target:oxr_mdlc_councilor_editor_target = { NOT = { has_trait = leader_trait_army_veteran_2 } }
	}
	allow = {
		oxr_mdlc_councilor_editor_check_trait_resources_cost_common = yes
		event_target:oxr_mdlc_councilor_editor_target = {
			oxr_mdlc_councilor_editor_check_trait_points_cost_common = yes
			oxr_mdlc_councilor_editor_check_trait_picks = yes
		}
        
	}
	effect = {
		custom_tooltip = oxr_mdlc_councilor_editor_show_trait_total_cost_common
		event_target:oxr_mdlc_councilor_editor_target = {
			oxr_mdlc_councilor_editor_remove_tier_1_or_2_traits_effect = { TRAIT_NAME = leader_trait_army_veteran }
			add_trait_no_notify = leader_trait_army_veteran_2
		}
		hidden_effect = {
			oxr_mdlc_councilor_editor_deduct_trait_resources_cost_common = yes
			event_target:oxr_mdlc_councilor_editor_target = {
				oxr_mdlc_councilor_editor_deduct_trait_points_cost_common = yes
				oxr_mdlc_councilor_editor_deduct_trait_pick = yes
			}
		}
	}
}
oxr_mdlc_councilor_editor_regulatory_leader_trait_army_veteran_2_remove_button_effect = {
    potential = {
		event_target:oxr_mdlc_councilor_editor_target = { has_trait = leader_trait_army_veteran_2 }
    }
    allow = { always = yes }
    effect = {
        custom_tooltip = xvcv_mdlc_core_modifying_tooltip_remove_official_leader_trait_army_veteran_2
        hidden_effect = {
			event_target:oxr_mdlc_councilor_editor_target = {
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
