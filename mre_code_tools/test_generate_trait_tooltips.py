from tempfile import NamedTemporaryFile

from generate_trait_tooltips import (
    create_tooltip_for_leader,
    load_modifier_keys_in_uppercase,
    detect_trait_modifier_permutation
)
from yaml import safe_load
from json import dump as json_dump
from mre_common_vars import (
    BUILD_FOLDER,
)

"""
We do encode on the trait output to stop pytest from expanding \n
"""

def test_leader_trait_private_mines_2():
    # Common trait
    stellaris_script = """

"""
    expected_output = """

 leader_trait_private_mines_2:0 "$leader_trait_private_mines$ II"
 leader_trait_private_mines_2_desc:0 "$leader_trait_private_mines_desc$"
"""
    pass

def test_generate_leader_trait_naturalist_2():
    trait_dict = {
        "leader_trait_naturalist_2": {
            "trait_name": "leader_trait_naturalist_2",
            "leader_class": "official",
            "gfx": "GFX_leader_trait_naturalist",
            "rarity": "veteran",
            "planet_modifier": {
                "deposit_blockers_natural_unity_produces_add": 6
            },
            "sector_modifier": {
                "deposit_blockers_natural_unity_produces_add": 3
            },
            "requires_paragon_dlc": False
        }
    }
    trait_output = create_tooltip_for_leader(
        trait_dict, "official", feature="leader_making"
    )
    expected_output = """
#leader_making #official #leader_trait_naturalist_2
xvcv_mdlc_leader_making_tooltip_official_leader_trait_naturalist_2:0 "§H$leader_trait_naturalist$ II§!$add_xvcv_mdlc_leader_making_traits_costs_desc_alt$\\n$governing_planet_effect$\\n$t$$mod_deposit_blockers_natural_unity_produces_add$: §G+6§!\\n$governing_sector_effect$\\n$t$$mod_deposit_blockers_natural_unity_produces_add$: §G+3§!\\n--------------\\n§L$leader_trait_naturalist_desc$§!"
"""

    assert expected_output.encode('utf-8') == trait_output.encode('utf-8')

def test_leader_trait_aggressive_2_fleet_modifier():
    """ This also tests our ability to check the 'uppercase localisation key map'
    to see if we need to prepend the key with mre_ """
    trait_data = {
        "leader_trait_aggressive_2": {
            "trait_name": "leader_trait_aggressive_2",
            "leader_class": "commander",
            "gfx": "GFX_leader_trait_aggressive",
            "rarity": "common",
            "fleet_modifier": {
                "ship_fire_rate_mult": 0.05,
                "ship_weapon_damage": 0.05
            },
            "requires_paragon_dlc": False
        }
    }
    expected_output = """
#leader_making #commander #leader_trait_aggressive_2
xvcv_mdlc_leader_making_tooltip_commander_leader_trait_aggressive_2:0 "§H$leader_trait_aggressive$ II§!$add_xvcv_mdlc_leader_making_traits_costs_desc$\\n$commanding_navy_effect$\\n$t$$mre_mod_ship_fire_rate_mult$: §G+5%§!\\n$t$$mre_mod_ship_weapon_damage$: §G+5%§!\\n--------------\\n§L$leader_trait_aggressive_desc$§!"
"""
    actual = create_tooltip_for_leader(trait_data, leader_class="commander")
    # breakpoint()
    assert expected_output.encode('utf-8') == actual.encode('utf-8')

def test_leadermaking_tooltip_leader_trait_generator_focus_3():
    """ Check mre_ gets substituted in front of mod_ in certain cases """
    test_data = {
        "leader_trait_generator_focus_3": {
            "trait_name": "leader_trait_generator_focus_3",
            "leader_class": "commander",
            "gfx": "GFX_leader_trait_financial",
            "rarity": "veteran",
            "planet_modifier": {
                "planet_jobs_energy_produces_mult": 0.45
            },
            "sector_modifier": {
                "planet_jobs_energy_produces_mult": 0.225
            },
            "requires_paragon_dlc": False,
            "custom_tooltip": "only_one_governor_focus"
        }
    }
    expected = """
#leader_making #commander #leader_trait_generator_focus_3
xvcv_mdlc_leader_making_tooltip_commander_leader_trait_generator_focus_3:0 "§H$leader_trait_generator_focus$ III§!$add_xvcv_mdlc_leader_making_traits_costs_desc_alt$\\n$governing_planet_effect$\\n$t$$mod_planet_jobs_energy_produces_mult$: §G+45%§!\\n$governing_sector_effect$\\n$t$$mod_planet_jobs_energy_produces_mult$: §G+22%§!\\n--------------\\n§L$leader_trait_generator_focus_desc$§!"
"""
    actual = create_tooltip_for_leader(test_data, leader_class="commander")
    assert expected.encode('utf-8') == actual.encode('utf-8')

def test_loading_uppercase_keys_from_files():
    megacorp_tmpfile = NamedTemporaryFile(delete=False)
    megacorp_data = {"MOD_BRANCH_OFFICE_VALUE_MULT": 1, "MOD_EMPIRE_SIZE_PENALTY_MULT":1}
    modifiers_tmpfile = NamedTemporaryFile(delete=False)
    modifiers_data = {"MOD_FEDERATION_EXPERIENCE_ADD": 1, "MOD_FEDERATION_COHESION_ADD": 1}
    paragon_tmpfile = NamedTemporaryFile(delete=False)
    paragon_data = {"MOD_PLANET_COMBAT_WIDTH_ADD": 1, "MOD_CREATE_DEBRIS_CHANCE": 1}
    with open(megacorp_tmpfile.name, "w+t") as mtmp:
        json_dump(megacorp_data, mtmp)
    with open(modifiers_tmpfile.name, "w+t") as mtmp:
        json_dump(modifiers_data, mtmp)
    with open(paragon_tmpfile.name, "w+t") as mtmp:
        json_dump(paragon_data, mtmp)
    # This test is brittle because it depends on files in the build folder
    sorted_data = load_modifier_keys_in_uppercase([
        megacorp_tmpfile.name, modifiers_tmpfile.name, paragon_tmpfile.name
    ])
    assert "MOD_BRANCH_OFFICE_VALUE_MULT" in sorted_data
    assert "MOD_FEDERATION_EXPERIENCE_ADD" in sorted_data
    assert "MOD_PLANET_COMBAT_WIDTH_ADD" in sorted_data

def test_detect_wrong_word_order_modifier_key():
    """ Sometimes the words in the modifier arent the same order as the actual tooltip key,
    so test that we can detect these funky word orders """

    """
     = {
	replace_traits = { "leader_trait_roamer" }
	inline_script = {
		script = trait/icon
		CLASS = scientist
		ICON = "GFX_leader_trait_roamer"
		RARITY = common
		COUNCIL = no
		TIER = 2
	}
	modifier = {
		science_ship_survey_speed = 0.20
	}
	leader_class = { scientist }
	opposites = {
		leader_trait_neurotic
		leader_trait_neurotic_2
	}
	ai_weight = 100
}"""
    test_data = {
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
    expected = """
#leader_making #scientist #leader_trait_roamer_2
xvcv_mdlc_leader_making_tooltip_scientist_leader_trait_roamer_2:0 "§H$leader_trait_roamer$ II§!$add_xvcv_mdlc_leader_making_traits_costs_desc$\\n$t$$MOD_SHIP_SCIENCE_SURVEY_SPEED$: §G+20%§!\\n--------------\\n§L$leader_trait_roamer_desc$§!"
"""
    actual = create_tooltip_for_leader(test_data, leader_class="scientist")
    assert expected.encode('utf-8') == actual.encode('utf-8')

def test_detect_permutation_of_trait_modifier_in_localisation():
    """ Check for a match of a permutation of a trait name in localisation keys """
    modifier_name = "species_leader_exp_gain"
    uppercase_localisation_keys = {
        "MOD_LEADER_SPECIES_EXP_GAIN": 1,
    }
    expected_permutation_detection = "MOD_LEADER_SPECIES_EXP_GAIN"
    actual = detect_trait_modifier_permutation(
        modifier_name,
        uppercase_key_store=uppercase_localisation_keys
    )
    assert expected_permutation_detection == actual


def test_detect_modifier_permutation__adventurous_spirit_3():
    trait_data = {
        "leader_trait_adventurous_spirit_3": {
            "trait_name": "leader_trait_adventurous_spirit_3",
            "leader_class": "commander",
            "gfx": "GFX_leader_trait_adventurous_spirit",
            "rarity": "veteran",
            "triggered_self_modifier": {
                "leaders_upkeep_mult": -0.25,
                "species_leader_exp_gain": 0.1
            },
            "requires_paragon_dlc": False,
            "custom_tooltip": "leader_trait_adventurous_spirit_effect"
        }
    }

    expected = """
#leader_making #commander #leader_trait_adventurous_spirit_3
xvcv_mdlc_leader_making_tooltip_commander_leader_trait_adventurous_spirit_3:0 "§H$leader_trait_adventurous_spirit$ III§!$add_xvcv_mdlc_leader_making_traits_costs_desc_alt$\\n$t$$mod_leaders_upkeep_mult$: §G-25%§!\\n$t$$MOD_LEADER_SPECIES_EXP_GAIN$: §G+10%§!\\n--------------\\n§L$leader_trait_adventurous_spirit_desc$§!"
"""
    actual = create_tooltip_for_leader(trait_data, leader_class="commander")
    assert expected == actual


def test_core_modifying_tooltip__adventurous_spirit_3():
    trait_data = {
        "leader_trait_adventurous_spirit_3": {
            "trait_name": "leader_trait_adventurous_spirit_3",
            "leader_class": "commander",
            "gfx": "GFX_leader_trait_adventurous_spirit",
            "rarity": "veteran",
            "triggered_self_modifier": {
                "leaders_upkeep_mult": -0.25,
                "species_leader_exp_gain": 0.1
            },
            "requires_paragon_dlc": False,
            "custom_tooltip": "leader_trait_adventurous_spirit_effect"
        }
    }

    expected = """
#core_modifying #commander #leader_trait_adventurous_spirit_3
xvcv_mdlc_core_modifying_tooltip_add_commander_leader_trait_adventurous_spirit_3:0 "§H$leader_trait_adventurous_spirit$ III§!$add_xvcv_mdlc_core_modifying_traits_costs_desc_alt$\\n$t$$mod_leaders_upkeep_mult$: §G-25%§!\\n$t$$MOD_LEADER_SPECIES_EXP_GAIN$: §G+10%§!\\n--------------\\n§L$leader_trait_adventurous_spirit_desc$§!"
xvcv_mdlc_core_modifying_tooltip_remove_commander_leader_trait_adventurous_spirit_3:0 "§RRemove§! Trait: §H$leader_trait_adventurous_spirit$ III§!$remove_xvcv_mdlc_core_modifying_traits_costs_desc_alt$\\n$t$$mod_leaders_upkeep_mult$: §G-25%§!\\n$t$$MOD_LEADER_SPECIES_EXP_GAIN$: §G+10%§!\\n--------------\\n§L$leader_trait_adventurous_spirit_desc$§!"
"""
    actual = create_tooltip_for_leader(trait_data, leader_class="commander", feature="core_modifying")
    assert expected.encode('utf-8') == actual.encode('utf-8')

def test_core_modifying_tooltip__leader_trait_roamer_2():
    test_data = {
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
    expected = """
#core_modifying #scientist #leader_trait_roamer_2
xvcv_mdlc_core_modifying_tooltip_add_scientist_leader_trait_roamer_2:0 "§H$leader_trait_roamer$ II§!$add_xvcv_mdlc_core_modifying_traits_costs_desc$\\n$t$$MOD_SHIP_SCIENCE_SURVEY_SPEED$: §G+20%§!\\n--------------\\n§L$leader_trait_roamer_desc$§!"
xvcv_mdlc_core_modifying_tooltip_remove_scientist_leader_trait_roamer_2:0 "§RRemove§! Trait: §H$leader_trait_roamer$ II§!$remove_xvcv_mdlc_core_modifying_traits_costs_desc$\\n$t$$MOD_SHIP_SCIENCE_SURVEY_SPEED$: §G+20%§!\\n--------------\\n§L$leader_trait_roamer_desc$§!"
"""
    actual = create_tooltip_for_leader(test_data, leader_class="scientist", feature="core_modifying")
    assert expected.encode('utf-8') == actual.encode('utf-8')
