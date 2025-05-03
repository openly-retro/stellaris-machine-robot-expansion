from tempfile import NamedTemporaryFile
from pytest import fixture as pytest_fixture
from pipeline.compile.generate_trait_tooltips import (
    create_tooltip_for_leader,
    load_modifier_keys_in_uppercase,
    detect_trait_modifier_permutation
)
# from yaml import safe_load
from json import dump as json_dump
from pipeline.mre_common_vars import (
    BUILD_FOLDER,
)

@pytest_fixture
def make_uppercase_mapping_files():
    megacorp_tmpfile = NamedTemporaryFile(delete=False)
    megacorp_data = {"MOD_BRANCH_OFFICE_VALUE_MULT": 1, "MOD_EMPIRE_SIZE_PENALTY_MULT":1}
    modifiers_tmpfile = NamedTemporaryFile(delete=False)
    modifiers_data = {
        "MOD_FEDERATION_EXPERIENCE_ADD": 1,
        "MOD_FEDERATION_COHESION_ADD": 1,
        "MOD_SHIP_FIRE_RATE_MULT": 1,
        "MOD_SHIP_WEAPON_DAMAGE": 1,
        "MOD_SHIP_SCIENCE_SURVEY_SPEED": 1,
        "MOD_SHIP_HULL_MULT":1,
        "MOD_CREATE_DEBRIS_CHANCE":1,
    }
    paragon_tmpfile = NamedTemporaryFile(delete=False)
    paragon_data = {"MOD_PLANET_COMBAT_WIDTH_ADD": 1, "MOD_CREATE_DEBRIS_CHANCE": 1}
    with open(megacorp_tmpfile.name, "w+t") as mtmp:
        json_dump(megacorp_data, mtmp)
    with open(modifiers_tmpfile.name, "w+t") as mtmp:
        json_dump(modifiers_data, mtmp)
    with open(paragon_tmpfile.name, "w+t") as mtmp:
        json_dump(paragon_data, mtmp)
    yield [megacorp_tmpfile.name, modifiers_tmpfile.name, paragon_tmpfile.name]
    megacorp_tmpfile.close()
    modifiers_tmpfile.close()
    paragon_tmpfile.close() 

"""
We do encode on the trait output to stop pytest from expanding \n
"""

def test_generate_leader_trait_naturalist_2(make_uppercase_mapping_files):
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
        trait_dict, "official", feature="leader_making",
        uppercase_map_files=make_uppercase_mapping_files
    )
    expected_output = """
  #leader_making #official #leader_trait_naturalist_2
  xvcv_mdlc_leader_making_tooltip_official_leader_trait_naturalist_2:0 "§H$leader_trait_naturalist$ II§!$add_xvcv_mdlc_leader_making_traits_costs_desc_alt$\\n$governing_planet_effect$\\n$t$$mod_deposit_blockers_natural_unity_produces_add$: §G+6§!\\n$governing_sector_effect$\\n$t$$mod_deposit_blockers_natural_unity_produces_add$: §G+3§!\\n--------------\\n§L$leader_trait_naturalist_desc$§!"
"""

    assert expected_output.encode('utf-8') == trait_output.encode('utf-8')

def test_leader_trait_aggressive_2_fleet_modifier(make_uppercase_mapping_files):
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
    actual = create_tooltip_for_leader(
        trait_data, leader_class="commander", uppercase_map_files=make_uppercase_mapping_files
    )
    assert expected_output.encode('utf-8') == actual.encode('utf-8')

def test_leadermaking_tooltip_leader_trait_generator_focus_3(make_uppercase_mapping_files):
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
    actual = create_tooltip_for_leader(
        test_data, leader_class="commander", uppercase_map_files=make_uppercase_mapping_files
    )
    assert expected.encode('utf-8') == actual.encode('utf-8')

def test_loading_uppercase_keys_from_files(make_uppercase_mapping_files):

    # This test is brittle because it depends on files in the build folder
    sorted_data = load_modifier_keys_in_uppercase(make_uppercase_mapping_files)
    assert "MOD_BRANCH_OFFICE_VALUE_MULT" in sorted_data
    assert "MOD_FEDERATION_EXPERIENCE_ADD" in sorted_data
    assert "MOD_PLANET_COMBAT_WIDTH_ADD" in sorted_data

def test_detect_wrong_word_order_modifier_key(make_uppercase_mapping_files):
    """ Sometimes the words in the modifier arent the same order as the actual tooltip key,
    so test that we can detect these funky word orders """

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
    actual = create_tooltip_for_leader(
        test_data, leader_class="scientist", uppercase_map_files=make_uppercase_mapping_files
    )
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


def test_detect_modifier_permutation__adventurous_spirit_3(make_uppercase_mapping_files):
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
        }
    }

    expected = """
  #leader_making #commander #leader_trait_adventurous_spirit_3
  xvcv_mdlc_leader_making_tooltip_commander_leader_trait_adventurous_spirit_3:0 "§H$leader_trait_adventurous_spirit$ III§!$add_xvcv_mdlc_leader_making_traits_costs_desc_alt$\\n$t$$mod_leaders_upkeep_mult$: §G-25%§!\\n$t$$MOD_LEADER_SPECIES_EXP_GAIN$: §G+10%§!\\n--------------\\n§L$leader_trait_adventurous_spirit_desc$§!"
"""
    actual = create_tooltip_for_leader(
        trait_data, leader_class="commander", uppercase_map_files=make_uppercase_mapping_files
    )
    assert expected == actual


def test_core_modifying_tooltip__adventurous_spirit_3(make_uppercase_mapping_files):
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
        }
    }

    expected = """
  #core_modifying #commander #leader_trait_adventurous_spirit_3
  xvcv_mdlc_core_modifying_tooltip_add_commander_leader_trait_adventurous_spirit_3:0 "§H$leader_trait_adventurous_spirit$ III§!$add_xvcv_mdlc_core_modifying_traits_costs_desc_alt$\\n$t$$mod_leaders_upkeep_mult$: §G-25%§!\\n$t$$MOD_LEADER_SPECIES_EXP_GAIN$: §G+10%§!\\n--------------\\n§L$leader_trait_adventurous_spirit_desc$§!"
  xvcv_mdlc_core_modifying_tooltip_remove_commander_leader_trait_adventurous_spirit_3:0 "§RRemove§! Trait: §H$leader_trait_adventurous_spirit$ III§!$remove_xvcv_mdlc_core_modifying_traits_costs_desc_alt$\\n$t$$mod_leaders_upkeep_mult$: §G-25%§!\\n$t$$MOD_LEADER_SPECIES_EXP_GAIN$: §G+10%§!\\n--------------\\n§L$leader_trait_adventurous_spirit_desc$§!"
"""
    actual = create_tooltip_for_leader(
        trait_data, leader_class="commander", feature="core_modifying",
        uppercase_map_files=make_uppercase_mapping_files
    )
    assert expected.encode('utf-8') == actual.encode('utf-8')

def test_core_modifying_tooltip__leader_trait_roamer_2(make_uppercase_mapping_files):
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
    actual = create_tooltip_for_leader(
        test_data, leader_class="scientist", feature="core_modifying",
        uppercase_map_files=make_uppercase_mapping_files
    )
    assert expected.encode('utf-8') == actual.encode('utf-8')

def test_remove_garbage_modifiers_from_trait(make_uppercase_mapping_files):
    test_data = {
        "leader_trait_expertise_new_worlds_3": {
            "trait_name": "leader_trait_expertise_new_worlds_3",
            "leader_class": "scientist",
            "gfx": "GFX_leader_trait_expertise_new_worlds",
            "rarity": "veteran",
            "councilor_modifier": {
                "category_new_worlds_research_speed_mult": 0.35,
                "category_new_worlds_draw_chance_mult": 0.75,
                "inline_script": None,
                "script": "traits/technocracy_expertise_effects",
                "FIELD": "society",
                "TIER": 3
            },
            "requires_paragon_dlc": True,
            "is_councilor_trait": True,
            "required_subclass": "subclass_scientist_councilor"
        }
    }
    expected = """
  #core_modifying #scientist #leader_trait_expertise_new_worlds_3
  xvcv_mdlc_core_modifying_tooltip_add_scientist_leader_trait_expertise_new_worlds_3:0 "§H$leader_trait_expertise_new_worlds$ III§!$add_xvcv_mdlc_core_modifying_traits_costs_desc_alt$\\n$councilor_trait$\\n$t$$mod_category_new_worlds_draw_chance_mult$: §G+75%§!\\n$t$$mod_category_new_worlds_research_speed_mult$: §G+35%§!\\n--------------\\n§L$leader_trait_expertise_new_worlds_desc$§!"
  xvcv_mdlc_core_modifying_tooltip_remove_scientist_leader_trait_expertise_new_worlds_3:0 "§RRemove§! Trait: §H$leader_trait_expertise_new_worlds$ III§!$remove_xvcv_mdlc_core_modifying_traits_costs_desc_alt$\\n$councilor_trait$\\n$t$$mod_category_new_worlds_draw_chance_mult$: §G+75%§!\\n$t$$mod_category_new_worlds_research_speed_mult$: §G+35%§!\\n--------------\\n§L$leader_trait_expertise_new_worlds_desc$§!"
"""
    actual = create_tooltip_for_leader(
        test_data, leader_class="scientist", feature="core_modifying",
        uppercase_map_files=make_uppercase_mapping_files
    )
    assert expected == actual

def test_find_and_map_abberant_modifiers(make_uppercase_mapping_files):
    test_data = {
        "leader_trait_overseer_3": {
            "trait_name": "leader_trait_overseer_3",
            "leader_class": "official",
            "gfx": "GFX_leader_trait_overseer",
            "rarity": "veteran",
            "is_councilor_trait": True,
            "councilor_modifier": {
                "monthly_loyalty_from_subjects": 0.5
            },
            "requires_paragon_dlc": False,
            "required_subclass": "subclass_official_diplomacy_councilor"
        }
    }
    expected = """
  #core_modifying #scientist #leader_trait_overseer_3
  xvcv_mdlc_core_modifying_tooltip_add_scientist_leader_trait_overseer_3:0 "§H$leader_trait_overseer$ III§!$add_xvcv_mdlc_core_modifying_traits_costs_desc_alt$\\n$councilor_trait$\\n$t$$MOD_MONTHLY_LOYALTY_GAIN_FROM_SUBJECTS$: §G+50%§!\\n--------------\\n§L$leader_trait_overseer_desc$§!"
  xvcv_mdlc_core_modifying_tooltip_remove_scientist_leader_trait_overseer_3:0 "§RRemove§! Trait: §H$leader_trait_overseer$ III§!$remove_xvcv_mdlc_core_modifying_traits_costs_desc_alt$\\n$councilor_trait$\\n$t$$MOD_MONTHLY_LOYALTY_GAIN_FROM_SUBJECTS$: §G+50%§!\\n--------------\\n§L$leader_trait_overseer_desc$§!"
"""
    actual = create_tooltip_for_leader(
        test_data, leader_class="scientist", feature="core_modifying",
        uppercase_map_files=make_uppercase_mapping_files
    )
    assert expected == actual

def test_find_trait_with_machine_variant_tooltip(make_uppercase_mapping_files):
    traits_with_machine_desc = {
        "leader_trait_overseer": 1,
    }
    test_data = {
        "leader_trait_overseer_3": {
            "trait_name": "leader_trait_overseer_3",
            "leader_class": "official",
            "gfx": "GFX_leader_trait_overseer",
            "rarity": "veteran",
            "is_councilor_trait": True,
            "councilor_modifier": {
                "monthly_loyalty_from_subjects": 0.5
            },
            "requires_paragon_dlc": False,
            "required_subclass": "subclass_official_diplomacy_councilor"
        }
    }
    expected = """
  #core_modifying #scientist #leader_trait_overseer_3
  xvcv_mdlc_core_modifying_tooltip_add_scientist_leader_trait_overseer_3:0 "§H$leader_trait_overseer_machine$ III§!$add_xvcv_mdlc_core_modifying_traits_costs_desc_alt$\\n$councilor_trait$\\n$t$$MOD_MONTHLY_LOYALTY_GAIN_FROM_SUBJECTS$: §G+50%§!\\n--------------\\n§L$leader_trait_overseer_machine_desc$§!"
  xvcv_mdlc_core_modifying_tooltip_remove_scientist_leader_trait_overseer_3:0 "§RRemove§! Trait: §H$leader_trait_overseer_machine$ III§!$remove_xvcv_mdlc_core_modifying_traits_costs_desc_alt$\\n$councilor_trait$\\n$t$$MOD_MONTHLY_LOYALTY_GAIN_FROM_SUBJECTS$: §G+50%§!\\n--------------\\n§L$leader_trait_overseer_machine_desc$§!"
"""
    actual = create_tooltip_for_leader(
        test_data, leader_class="scientist", feature="core_modifying",
        uppercase_map_files=make_uppercase_mapping_files,
        machine_localisations_map=traits_with_machine_desc
    )
    assert expected == actual

def test_use_custom_tt_replacement_string(make_uppercase_mapping_files):
    traits_with_machine_desc = {
        "leader_trait_overseer": 1,
    }
    test_data = {
        "leader_trait_prospector_3": {
            "trait_name": "leader_trait_prospector_3",
            "leader_class": "scientist",
            "gfx": "GFX_leader_trait_prospector",
            "rarity": "veteran",
            "requires_paragon_dlc": False,
            "custom_tooltip": "leader_trait_prospector_3_effect",
            "required_subclass": "subclass_scientist_explorer"
        }
    }
    expected = """
  #core_modifying #scientist #leader_trait_prospector_3
  xvcv_mdlc_core_modifying_tooltip_add_scientist_leader_trait_prospector_3:0 "§H$leader_trait_prospector$ III§!$add_xvcv_mdlc_core_modifying_traits_costs_desc_alt$\\n$leader_trait_prospector_3_effect$\\n--------------\\n§L$leader_trait_prospector_desc$§!"
  xvcv_mdlc_core_modifying_tooltip_remove_scientist_leader_trait_prospector_3:0 "§RRemove§! Trait: §H$leader_trait_prospector$ III§!$remove_xvcv_mdlc_core_modifying_traits_costs_desc_alt$\\n$leader_trait_prospector_3_effect$\\n--------------\\n§L$leader_trait_prospector_desc$§!"
"""
    actual = create_tooltip_for_leader(
        test_data, leader_class="scientist", feature="core_modifying",
        uppercase_map_files=make_uppercase_mapping_files,
        machine_localisations_map=traits_with_machine_desc
    )
    assert expected == actual


def test_custom_tt_with_modifiers_appended(make_uppercase_mapping_files):
    traits_with_machine_desc = {
        "leader_trait_juryrigger": 1,
    }
    test_data = {
        "leader_trait_juryrigger_3": {
            "trait_name": "leader_trait_juryrigger_3",
            "leader_class": "commander",
            "gfx": "GFX_leader_trait_juryrigger",
            "rarity": "veteran",
            "fleet_modifier": {
                "create_debris_chance": -1,
                "ship_hull_mult": 0.1
            },
            "requires_paragon_dlc": False,
            "custom_tooltip_with_modifiers": "leader_trait_juryrigger_2_effect",
            "required_subclass": "subclass_commander_admiral"
        }
    }
    expected = """
  #leader_making #commander #leader_trait_juryrigger_3
  xvcv_mdlc_leader_making_tooltip_commander_leader_trait_juryrigger_3:0 "§H$leader_trait_juryrigger_machine$ III§!$add_xvcv_mdlc_leader_making_traits_costs_desc_alt$\\n$commanding_navy_effect$\\n$t$$mre_mod_create_debris_chance$: §G-100%§!\\n$t$$mre_mod_ship_hull_mult$: §G+10%§!\\n$leader_trait_juryrigger_2_effect$\\n--------------\\n§L$leader_trait_juryrigger_machine_desc$§!"
"""
    actual = create_tooltip_for_leader(
        test_data, leader_class="commander", feature="leader_making",
        uppercase_map_files=make_uppercase_mapping_files,
        machine_localisations_map=traits_with_machine_desc
    )
    assert expected == actual

def test_expanding_variables_into_brackets(make_uppercase_mapping_files):
    """ @somevar should be inside of [] """
    traits_with_machine_desc = {
        "leader_trait_surveyor": 1,
    }
    test_data = {
        "leader_trait_surveyor": {
            "trait_name": "leader_trait_surveyor",
            "leader_class": "commander",
            "destiny_trait": True,
            "gfx": "GFX_leader_trait_surveyor",
            "rarity": "paragon",
            "planet_modifier": {
                "planet_technician_physics_research_produces_add": "@trait_surveyor_amt",
                "planet_farmers_society_research_produces_add": "@trait_surveyor_amt",
                "planet_miners_engineering_research_produces_add": "@trait_surveyor_amt"
            },
            "sector_modifier": {
                "planet_technician_physics_research_produces_add": "@trait_surveyor_sector_amt",
                "planet_farmers_society_research_produces_add": "@trait_surveyor_sector_amt",
                "planet_miners_engineering_research_produces_add": "@trait_surveyor_sector_amt"
            },
            "requires_paragon_dlc": False,
            "leader_potential_add": {
                "has_paragon_dlc": "yes",
                "has_governor_subclass": "yes"
            }
        }
    }
    expected = """
  #leader_making #commander #leader_trait_surveyor
  xvcv_mdlc_leader_making_tooltip_commander_leader_trait_surveyor:0 "§H$leader_trait_surveyor_machine$ §!$add_xvcv_mdlc_leader_making_traits_costs_desc_alt_2$\\n$governing_planet_effect$\\n$t$$mod_planet_farmers_society_research_produces_add$: §G+[@trait_surveyor_amt]§!\\n$t$$mod_planet_miners_engineering_research_produces_add$: §G+[@trait_surveyor_amt]§!\\n$t$$mod_planet_technician_physics_research_produces_add$: §G+[@trait_surveyor_amt]§!\\n$governing_sector_effect$\\n$t$$mod_planet_farmers_society_research_produces_add$: §G+[@trait_surveyor_sector_amt]§!\\n$t$$mod_planet_miners_engineering_research_produces_add$: §G+[@trait_surveyor_sector_amt]§!\\n$t$$mod_planet_technician_physics_research_produces_add$: §G+[@trait_surveyor_sector_amt]§!\\n--------------\\n§L$leader_trait_surveyor_machine_desc$§!"
"""
    actual = create_tooltip_for_leader(
        test_data, leader_class="commander", feature="leader_making",
        uppercase_map_files=make_uppercase_mapping_files,
        machine_localisations_map=traits_with_machine_desc
    )
    assert expected == actual
