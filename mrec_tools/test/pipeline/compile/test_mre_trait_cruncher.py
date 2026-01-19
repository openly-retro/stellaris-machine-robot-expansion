from pipeline.transform.mre_trait_cruncher import (
    filter_trait_info,
    # sort_traits_by_leader_class,
    sort_traits_asc,
)
# from yaml import safe_load

def test_filter_trait_info():
    # The YAML is loaded into a Python dict, so we will work with dict objects
    parsed_trait = {
        'leader_trait_bureaucrat_2': {
            'replace_traits': 'leader_trait_bureaucrat',
            'inline_script': {
                'script': 'trait/icon',
                'CLASS': 'official',
                'ICON': 'GFX_leader_trait_bureaucrat',
                'RARITY': 'common', 'COUNCIL': False,
                'TIER': 2
            },
            'triggered_planet_modifier': {
                'potential': {'always': True},
                'planet_bureaucrats_unity_produces_mult': 0.05
            },
            'triggered_sector_modifier': {
                'potential': {'always': True},
                'planet_bureaucrats_unity_produces_mult': 0.025
            },
            'triggered_desc': {
                'exclusive_trigger': {'always': True},
                'text': 'leader_trait_bureaucrat_2_tt'
            },
            'leader_class': ['official', 'commander', 'scientist']
        }
    }
    filtered_info = filter_trait_info(parsed_trait, for_class="official")
    expected_info = {
        "trait_name": "leader_trait_bureaucrat_2",
        "leader_class": 'official',
        "gfx": "GFX_leader_trait_bureaucrat",
        "rarity": "common",
        "triggered_planet_modifier": {
            'planet_bureaucrats_unity_produces_mult': 0.05
        },
        "triggered_sector_modifier": {
            'planet_bureaucrats_unity_produces_mult': 0.025
        },
        "requires_paragon_dlc": False,
        "custom_tooltip": "leader_trait_bureaucrat_2_tt"
    }
    assert expected_info == filtered_info

def test_crunch__trait_ruler_architectural_sense_3():
    # Councilor traits are good candidate for core-modifying ruler traits
    test_data = {
        "trait_ruler_architectural_sense_3": {
            "leader_trait_type": "veteran",
            "replace_traits": "trait_ruler_architectural_sense_2",
            "inline_script": {
                "script": "trait/icon",
                "CLASS": "official",
                "ICON": "GFX_leader_trait_architectural_sense",
                "RARITY": "veteran",
                "COUNCIL": True,
                "TIER": 3
            },
            "councilor_modifier": {
                "planet_buildings_cost_mult": -0.1,
                "planet_districts_cost_mult": -0.1,
                "planet_buildings_upkeep_mult": -0.05,
                "planet_districts_upkeep_mult": -0.05,
                "planet_building_build_speed_mult": 0.25
            },
            "leader_trait_type": "veteran",
            "leader_potential_add": {
                "has_paragon_dlc": True
            },
            "leader_class": [
                "official"
            ]
        }
    }
    actual = filter_trait_info(test_data)
    expected = {
        "trait_name": "trait_ruler_architectural_sense_3",
        "leader_class": "official",
        "gfx": "GFX_leader_trait_architectural_sense",
        "rarity": "veteran",
        "councilor_modifier": {
            "planet_buildings_cost_mult": -0.1,
            "planet_districts_cost_mult": -0.1,
            "planet_buildings_upkeep_mult": -0.05,
            "planet_districts_upkeep_mult": -0.05,
            "planet_building_build_speed_mult": 0.25
        },
        "is_councilor_trait": True,
        "requires_paragon_dlc": True,
        "leader_potential_add": {
            "has_paragon_dlc": True
        },
    }
    assert expected == actual

def test_crunch__leader_trait_reformer():
    """ Test picking out just the data we want from a standard trait blob """
    test_data = {
        "leader_trait_reformer": {
            "inline_script": {
                "script": "trait/icon",
                "CLASS": "official",
                "ICON": "GFX_leader_trait_reformer",
                "RARITY": "free_or_veteran",
                "COUNCIL": True,
                "TIER": 1
            },
            "leader_potential_add": {
                "is_gestalt": "no",
                "OR": {
                    "has_paragon_dlc": "no",
                    "has_trait": ["subclass_official_economy_councilor"]
                }
            },
            "councilor_modifier": {
                "country_unity_produces_mult": 0.05,
                "pop_government_ethic_attraction": 0.35
            },
            "leader_trait_type": "veteran",
            "leader_class": [
                "official"
            ],
            "selectable_weight": {
                "inline_script": "paragon/subclass_free_trait_weight"
            }
        }
    }
    actual = filter_trait_info(test_data)
    expected = {
        "trait_name": "leader_trait_reformer",
        "leader_class": ["official"],
        "gfx": "GFX_leader_trait_reformer",
        "rarity": "free_or_veteran",
        "is_councilor_trait": True,
        "councilor_modifier": {
            "country_unity_produces_mult": 0.05,
            "pop_government_ethic_attraction": 0.35
        },
        "requires_paragon_dlc": False,
        "required_subclass": "subclass_official_economy_councilor"
    }

def test_crunch__leader_trait_arbiter():
    # Destiny trait
    test_data = {
        "leader_trait_arbiter": {
            "leader_trait_type": "destiny",
            "inline_script": {
                "script": "trait/icon",
                "CLASS": "commander",
                "ICON": "GFX_leader_trait_arbiter",
                "RARITY": "paragon",
                "COUNCIL": False,
                "TIER": "none"
            },
            "leader_potential_add": {
                "has_paragon_dlc": True,
                "has_subclass_trait": ["subclass_commander_governor"]
            },
            "planet_modifier": {
                "planet_jobs_worker_produces_mult": 0.5,
                "planet_jobs_slave_produces_mult": 0.5,
                "planet_pops_upkeep_mult": -0.35,
                "pop_happiness": -0.1,
                "pop_growth_speed_reduction": 0.05
            },
            "sector_modifier": {
                "planet_jobs_worker_produces_mult": 0.25,
                "planet_jobs_slave_produces_mult": 0.25,
                "planet_pops_upkeep_mult": -0.175,
                "pop_happiness": -0.05,
                "pop_growth_speed_reduction": 0.025
            },
            "leader_class": [
                "commander"
            ],
            "selectable_weight": {
                "weight": "var_subclass_trait_weight",
                "inline_script": "paragon/governor_weight_mult"
            },
            "background_icon": "GFX_leader_background_destiny_1"
        }
    }
    actual = filter_trait_info(test_data)
    expected = {
        "trait_name": "leader_trait_arbiter",
        "destiny_trait": True,
        "leader_class": "commander",
        "gfx": "GFX_leader_trait_arbiter",
        "rarity": "paragon",
        "planet_modifier": {
            "planet_jobs_worker_produces_mult": 0.5,
            "planet_jobs_slave_produces_mult": 0.5,
            "planet_pops_upkeep_mult": -0.35,
            "pop_happiness": -0.1,
            "pop_growth_speed_reduction": 0.05
        },
        "sector_modifier": {
            "planet_jobs_worker_produces_mult": 0.25,
            "planet_jobs_slave_produces_mult": 0.25,
            "planet_pops_upkeep_mult": -0.175,
            "pop_happiness": -0.05,
            "pop_growth_speed_reduction": 0.025
        },
        "requires_paragon_dlc": True,
        "required_subclass": "subclass_commander_governor",
        "leader_potential_add": {
            "has_paragon_dlc": True,
            "has_subclass_trait": ["subclass_commander_governor"]
        },
    }
    assert expected == actual

def test_crunch__leader_trait_scout():
    """ An example which has TWO potential subclasses """
    test_data = {
        "leader_trait_scout": {
            "leader_trait_type": "veteran",
            "inline_script": {
                "script": "trait/icon",
                "CLASS": "leader",
                "ICON": "GFX_leader_trait_scout",
                "RARITY": "free_or_veteran",
                "COUNCIL": False,
                "TIER": 1
            },
            "leader_potential_add": {
                "OR": {
                    "has_paragon_dlc": "no",
                    "has_subclass_trait": [
                        "subclass_commander_admiral",
                        "subclass_scientist_explorer",
                        "subclass_scientist_councilor"
                    ]
                }
            },
            "modifier": {
                "ship_speed_mult": 0.05,
                "ship_hyperlane_range_add": 2,
                "fleet_mia_time_mult": -0.1
            },
            "triggered_modifier": {
                "ship_cloaking_strength_add": 1
            },
            "leader_class": [
                "commander",
                "scientist"
            ],
            "selectable_weight": {
                "inline_script": {
                    "script": "paragon/dual_subclass_weight_mult",
                    "SUBCLASS_1": "commander_admiral",
                    "SUBCLASS_2": "scientist_explorer"
                }
            }
        }
    }
    # First test, process the commander version
    expected_commander_trait_data = {
        "trait_name": "leader_trait_scout",
        "leader_class": "commander",
        "gfx": "GFX_leader_trait_scout",
        "rarity": "free_or_veteran",
        "modifier": {
            "ship_speed_mult": 0.05,
            "ship_hyperlane_range_add": 2,
            "fleet_mia_time_mult": -0.1
        },
        "requires_paragon_dlc": False,
        "required_subclass": "subclass_commander_admiral",
        "leader_potential_add": {
            "OR": {
                "has_paragon_dlc": "no",
                "has_subclass_trait": [
                    "subclass_commander_admiral",
                    "subclass_scientist_explorer",
                    "subclass_scientist_councilor"
                ]
            }
        },
    }
    actual_commander_trait_data = filter_trait_info(
        test_data, for_class="commander")
    assert expected_commander_trait_data == actual_commander_trait_data

    expected_scientist_trait_data = {
        "trait_name": "leader_trait_scout",
        "leader_class": "scientist",
        "gfx": "GFX_leader_trait_scout",
        "rarity": "free_or_veteran",
        "modifier": {
            "ship_speed_mult": 0.05,
            "ship_hyperlane_range_add": 2,
            "fleet_mia_time_mult": -0.1
        },
        "requires_paragon_dlc": False,
        "required_subclass": "subclass_scientist_explorer",
        "leader_potential_add": {
            "OR": {
                "has_paragon_dlc": "no",
                "has_subclass_trait": [
                    "subclass_commander_admiral",
                    "subclass_scientist_explorer",
                    "subclass_scientist_councilor"
                ]
            }
        },
    }
    actual_scientist_trait_data = filter_trait_info(
        test_data, for_class="scientist"
    )
    assert expected_scientist_trait_data == actual_scientist_trait_data

# def test_sort_traits_by_leader_class():

#     test_data = {
#         "trait_foo1": {
#             "trait_name": "trait_foo1",
#             "leader_class": ["official"]
#         },
#         "trait_foo2": {
#             "trait_name": "trait_foo2",
#             "leader_class": ["commander", "official", "scientist"]
#         },
#         "trait_foo3": {
#             "trait_name": "trait_foo3",
#             "leader_class": ["commander", "scientist"]
#         }
#     }
#     actual = sort_traits_by_leader_class(test_data)
#     expected = {
#         "official": [
#             {
#                 "trait_name": "trait_foo1",
#                 "leader_class": "official"
#             },
#             {
#                 "trait_name": "trait_foo2",
#                 "leader_class": "official"
#             }
#         ],
#         "commander": [
#             {
#                 "trait_name": "trait_foo2",
#                 "leader_class": "commander"
#             },
#             {
#                 "trait_name": "trait_foo3",
#                 "leader_class": "commander"
#             }
#         ],
#         "scientist": [
#             {
#                 "trait_name": "trait_foo2",
#                 "leader_class": "scientist"
#             },
#             {
#                 "trait_name": "trait_foo3",
#                 "leader_class": "scientist"
#             }
#         ]
#     }
#     assert expected == actual

def test_sort_traits_asc():
    test_data = [
            {
                "trait_name": "trait_foo4",
                "leader_class": "official"
            },
            {
                "trait_name": "trait_foo3",
                "leader_class": "official"
            },
            {
                "trait_name": "trait_foo2",
                "leader_class": "official"
            },
            {
                "trait_name": "trait_foo1",
                "leader_class": "official"
            },
        ]
    expected = [
            {
                "trait_name": "trait_foo1",
                "leader_class": "official"
            },
            {
                "trait_name": "trait_foo2",
                "leader_class": "official"
            },
            {
                "trait_name": "trait_foo3",
                "leader_class": "official"
            },
            {
                "trait_name": "trait_foo4",
                "leader_class": "official"
            },
        ]
    actual = sort_traits_asc(test_data)
    assert expected == actual

def test_leader_trait_aggressive_2():
    test_data = {
        "leader_trait_aggressive_2": {
            "replace_traits": [ "leader_trait_aggressive" ],
            "inline_script": {
                "script": "trait/icon",
                "CLASS": "commander",
                "ICON": "GFX_leader_trait_aggressive",
                "RARITY": "common",
                "COUNCIL": False,
                "TIER": 2
            },
            "fleet_modifier": {
                "ship_fire_rate_mult": 0.05,
                "ship_weapon_damage": 0.05
            },
            "leader_class": [ "commander" ],
            "opposites": {
                "leader_trait_cautious",
                "leader_trait_cautious_2"
            }
        }
    }
    expected = {
        "trait_name": "leader_trait_aggressive_2",
        "gfx": "GFX_leader_trait_aggressive",
        "leader_class": "commander",
        "rarity": "common",
        "fleet_modifier": {
            "ship_fire_rate_mult": 0.05,
            "ship_weapon_damage": 0.05
        },
        "requires_paragon_dlc": False
    }
    actual = filter_trait_info(test_data)
    assert expected == actual

def test_leader_trait_adventurous_spirit():
    test_data = {
        "leader_trait_adventurous_spirit": {
            "leader_trait_type": "veteran",
            "inline_script": {
                "script": "trait/icon",
                "CLASS": "leader",
                "ICON": "GFX_leader_trait_adventurous_spirit",
                "RARITY": "veteran",
                "COUNCIL": False,
                "TIER": 1
            },
            "triggered_self_modifier": {
                "leaders_upkeep_mult": -0.1
            },
            "leader_potential_add": {
                "has_paragon_dlc": True
            },
            "custom_tooltip_with_modifiers": "leader_trait_adventurous_spirit_effect",
            "leader_class": [ "commander", "scientist", "official" ]
        }
    }
    expected = {
        "trait_name": "leader_trait_adventurous_spirit",
        "gfx": "GFX_leader_trait_adventurous_spirit",
        "leader_class": "commander",
        "rarity": "veteran",
        "triggered_self_modifier": {
            "leaders_upkeep_mult": -0.1
        },
        "requires_paragon_dlc": True,
        "custom_tooltip_with_modifiers": "leader_trait_adventurous_spirit_effect",
        "leader_potential_add": {
            "has_paragon_dlc": True
        },
    }
    actual = filter_trait_info(test_data, for_class="commander")
    assert expected == actual

def test_populate_subclasses_for_related_traits():
    test_data = [
        {
            "trait_name": "leader_trait_wrecker",
            "required_subclass": "subclass_commander_admiral"
        },
        {
            "trait_name": "leader_trait_wrecker_2"
        },
        {
            "trait_name": "leader_trait_wrecker_3"
        },
        {
            "trait_name": "leader_trait_scout",
            "required_subclass": "subclass_scientist_explorer"
        },
    ]

def test_collect_custom_tooltip():
    """ Some traits dont have modifiers, they have effect-based mods which are described in
      a custom tooltip that PDX puts together """

    # Note that 'has_subclass_trait' is something we make during yaml conversion
    test_data = {
        "leader_trait_bellicose": {
            "leader_trait_type": "destiny",
            "force_councilor_trait": True,
            "inline_script": {
                "script": "trait/icon",
                "CLASS": "commander",
                "ICON": "GFX_leader_trait_bellicose",
                "RARITY": "paragon",
                "COUNCIL": True,
                "TIER": "none"
            },
            "custom_tooltip": "leader_trait_bellicose_effect",
            "leader_potential_add": {
                "has_paragon_dlc": True,
                "has_subclass_trait": ["subclass_commander_councilor"]
            },
            "leader_class": [ "commander" ],
            "selectable_weight": {
                "weight": "@subclass_trait_weight",
                "inline_script": "paragon/council_weight_mult"
            },
            "background_icon": "GFX_leader_background_destiny_1"
        }
    }
    expected = {
        "trait_name": "leader_trait_bellicose",
        "destiny_trait": True,
        "gfx": "GFX_leader_trait_bellicose",
        "leader_class": "commander",
        "rarity": "paragon",
        "requires_paragon_dlc": True,
        "required_subclass": "subclass_commander_councilor",
        "custom_tooltip": "leader_trait_bellicose_effect",
        "is_councilor_trait": True,
        "leader_potential_add": {
            "has_paragon_dlc": True,
            "has_subclass_trait": ["subclass_commander_councilor"]
        },
    }
    actual = filter_trait_info(test_data)
    assert expected == actual

# def test_trait_ruler_champion_of_the_people__from_yaml():
#     test_yaml = """
# trait_ruler_champion_of_the_people:
#   inline_script:
#     script: trait/icon
#     CLASS: leader
#     ICON: "GFX_leader_trait_champion_of_the_people"
#     RARITY: common
#     COUNCIL: yes
#     TIER: 1
#   triggered_councilor_modifier:
#     potential:
#       exists: owner
#       owner:
# #       #NOT: { has_civic: civic_dystopian_society
#     pop_happiness: 0.03
#   triggered_councilor_modifier:
#     potential:
#       exists: owner
# #     owner: has_civic: civic_dystopian_society
#     pop_cat_ruler_happiness: 0.05
#   leader_potential_add:
#     is_gestalt: no
#   leader_class: ['scientist', 'official', 'commander']
#   opposites:
#     leader_trait_tyrannical
#     leader_trait_tyrannical_2
#   selectable_weight:
#     weight: var_shared_trait_weight
#     inline_script: "paragon/council_weight_mult"
# """
#     expected_object = {
#         "trait_ruler_champion_of_the_people": {
#             "inline_script": {
#                 "script": "trait/icon",
#                 "CLASS": "leader",
#                 "ICON": "GFX_leader_trait_champion_of_the_people",
#                 "RARITY": "common",
#                 "COUNCIL": True,
#                 "TIER": 1
#             },
#             "triggered_councilor_modifier": {
#                 "potential": {
#                     "exists": "owner",
#                     "owner": None
#                 },
#                 "pop_happiness": 0.03
#             },
#             "triggered_councilor_modifier": {
#                 "potential": {
#                     "exists": "owner"
#                 },
#                 "pop_cat_ruler_happiness": 0.05
#             },
#             "leader_potential_add": {
#                 "is_gestalt": False
#             },
#             "leader_class": [
#                 "scientist",
#                 "official",
#                 "commander"
#             ],
#             "opposites": "leader_trait_tyrannical leader_trait_tyrannical_2",
#             "selectable_weight": {
#                 "weight": "var_shared_trait_weight",
#                 "inline_script": "paragon/council_weight_mult"
#             }
#         }
#     }
#     actual_object = safe_load(test_yaml)
#     assert expected_object == actual_object

#     expected_slim_trait = {
#         "trait_name": "trait_ruler_champion_of_the_people",
#         "gfx": "GFX_leader_trait_champion_of_the_people",
#         "leader_class": "commander",
#         "rarity": "common",
#         "requires_paragon_dlc": False,
#         "is_councilor_trait": True,
#         "triggered_councilor_modifier": {
#             "pop_cat_ruler_happiness": 0.05
#         },
#         "leader_potential_add": {
#             "is_gestalt": False
#         },
#     }
#     actual_slim_trait = filter_trait_info(actual_object, for_class="commander")
#     assert expected_slim_trait == actual_slim_trait

def test_guess_rarity_if_duplicate_inline_script():
    """
    In the wonderful world of Clausewitz script, there can be duplicate inline_script keys,
    so we will lose things like rarity and GFX
    """
    # this trait has two inline_script objects, second one has no useful data for us
    test_data = {
        "leader_trait_frontier_adventurer": {
            "leader_trait_type": "destiny",
            "inline_script": {
                "script": "trait/icon",
            },
            "modifier": {
                "science_ship_survey_speed": 0.25,
                "ship_speed_mult": 0.25,
                "ship_evasion_add": 15,
            },
            "leader_potential_add": {
                "has_paragon_dlc": True,
                "has_ancrel": True,
                "has_subclass_trait": ["subclass_scientist_explorer"]
            },
            "leader_class": [ "scientist" ]
        }
    }
    expected = {
        "trait_name": "leader_trait_frontier_adventurer",
        "destiny_trait": True,
        "gfx": "GFX_leader_trait_frontier_adventurer",
        "leader_class": "scientist",
        "rarity": "paragon",
        "requires_paragon_dlc": True,
        "required_subclass": "subclass_scientist_explorer",
        "modifier": {
            "science_ship_survey_speed": 0.25,
            "ship_speed_mult": 0.25,
            "ship_evasion_add": 15,
        },
        "leader_potential_add": {
            "has_paragon_dlc": True,
            "has_ancrel": True,
            "has_subclass_trait": ["subclass_scientist_explorer"]
        },
    }
    actual = filter_trait_info(test_data, for_class="scientist")
    assert expected == actual

def test_pick_subclass_from_has_trait_definition():
    """ Some cases, we missed getting the subclass ... """
    test_data = {
        "leader_trait_wrecker": {
            "leader_trait_type": "veteran",
            "inline_script": {
                "script": "trait/icon",
                "CLASS": "commander",
                "ICON": "GFX_leader_trait_wrecker",
                "RARITY": "veteran",
                "COUNCIL": False,
                "TIER": 1
            },
            "leader_potential_add": {
                "has_paragon_dlc": True,
                "has_trait": "subclass_commander_admiral"
            },
            "fleet_modifier": {
                "ship_weapon_damage": 0.1,
                "create_debris_chance": -0.25
            },
            "leader_class": [
                "commander"
            ],
            "opposites": "leader_trait_juryrigger leader_trait_juryrigger_2 leader_trait_juryrigger_3",
            "selectable_weight": {
                "weight": "var_subclass_trait_weight",
                "inline_script": "paragon/pilot_weight_mult"
            }
        }
    }
    expected = {
        "trait_name": "leader_trait_wrecker",
        "gfx": "GFX_leader_trait_wrecker",
        "leader_class": "commander",
        "rarity": "veteran",
        "requires_paragon_dlc": True,
        "required_subclass": "subclass_commander_admiral",
        "fleet_modifier": {
            "ship_weapon_damage": 0.1,
            "create_debris_chance": -0.25
        },
        'leader_potential_add': {
            'has_paragon_dlc': True,
            'has_trait': 'subclass_commander_admiral',
        }
    }
    actual = filter_trait_info(test_data, for_class="commander")
    assert expected == actual

def test_filter_trait_identify_is_ruler_allowance():
    test_data = {
        "leader_trait_carefree": {
        'trait_name': 'leader_trait_carefree',
        'inline_script': {
            'script': 'trait/icon',
            'CLASS': 'scientist',
            'ICON': 'GFX_leader_trait_carefree',
            'RARITY': 'common',
            'COUNCIL': False,
            'TIER': 1
        },
        'modifier': {
            'ship_anomaly_research_speed_mult': 0.1
        },
        'leader_potential_add': {
            'is_ruler': False
        },
        'leader_class': ['scientist'],
        'opposites': 'leader_trait_meticulous leader_trait_meticulous_2 leader_trait_neurotic leader_trait_neurotic_2', 
        'selectable_weight': {
            'weight': 'var_class_trait_weight',
            'inline_script': {
                'script': 'paragon/subclass_weight_mult',
                'SUBCLASS': 'scientist_scholar'
                }
            }, 'ai_weight': 50
        }
    }
    expected = {
        "trait_name": "leader_trait_carefree",
        "gfx": "GFX_leader_trait_carefree",
        "leader_class": "scientist",
        "rarity": "common",
        "requires_paragon_dlc": False,
        "modifier": {
            "ship_anomaly_research_speed_mult": 0.1
        },
        'leader_potential_add': {
            'is_ruler': False,
        },
        "allow_for_ruler": False
    }
    actual = filter_trait_info(test_data, for_class="scientist")
    assert expected == actual

def test_collect_trait_prerequisites():
    test_data = {
        "leader_trait_explorer_cloaking_focus_3": {
            "leader_trait_type": "veteran",
            "replace_traits": "leader_trait_explorer_cloaking_focus_2",
            "inline_script": {
                "script": "trait/icon",
                "CLASS": "scientist",
                "ICON": "GFX_leader_trait_explorer_cloaking_focus",
                "RARITY": "veteran",
                "COUNCIL": False,
                "TIER": 3,
            },
            "modifier": {
                "ship_cloaking_strength_add": 2
            },
            "custom_tooltip_with_modifiers": "leader_trait_explorer_cloaking_focus_3_tt",
            "prerequisites": "tech_cloaking_1",
            "leader_class": [ "scientist" ]
        }
    }
    expected = {
            "trait_name": "leader_trait_explorer_cloaking_focus_3",
            "gfx": "GFX_leader_trait_explorer_cloaking_focus",
            "leader_class": "scientist",
            "rarity": "veteran",
            "requires_paragon_dlc": False,
            "modifier": {
                "ship_cloaking_strength_add": 2
            },
            "prerequisites": [ "tech_cloaking_1" ],
            "custom_tooltip_with_modifiers": "leader_trait_explorer_cloaking_focus_3_tt",

    }
    actual = filter_trait_info(test_data, for_class="scientist")
    assert expected == actual

def test_3_11_eridanus_filter_negative_traits():
    """ leader_trait_type is where 'negative' is stored """
    parsed_trait = {
        'leader_trait_nervous': {
            "leader_trait_type": "negative",
            'replace_traits': 'leader_trait_nervous',
            'inline_script': {
                'script': 'trait/icon',
                'CLASS': 'official',
                'ICON': 'GFX_leader_trait_nervous',
                'RARITY': 'common', 'COUNCIL': False,
                'TIER': 2
            },
            'triggered_planet_modifier': {
                'potential': {'always': True},
                'planet_bureaucrats_unity_produces_mult': 0.05
            },
            'leader_class': ['official', 'commander', 'scientist']
        }
    }
    expected = {}
    actual = filter_trait_info(parsed_trait, for_class="official")
    assert expected == actual

def test_leader_trait_society_focus_3():
    test_data = {
        "leader_trait_society_focus_3":  {
            "leader_trait_type":  "veteran",
            "replace_traits": "leader_trait_society_focus_2",
            "inline_script": {
                "script": "trait/icon_society",
                "CLASS": "scientist",
                "ICON": "GFX_leader_trait_society_focus",
                "RARITY": "veteran",
                "COUNCIL": "yes",
                "TIER": "3"
            },
            "planet_modifier":  {
                "planet_jobs_society_research_produces_mult":  0.3
            },
            "sector_modifier":  {
                "planet_jobs_society_research_produces_mult":  0.15
            },
            "leader_class":  [ "scientist" ],
            "triggered_desc":  {
                "text":  "only_one_scientist_focus"
            },
            "ai_weight":  "100"
        }
    }
    expected = {
        "trait_name": "leader_trait_society_focus_3",
        "gfx": "GFX_leader_trait_society_focus",
        "leader_class": "scientist",
        "rarity": "veteran",
        "planet_modifier": {
            "planet_jobs_society_research_produces_mult": 0.3
        },
        "sector_modifier": {
            "planet_jobs_society_research_produces_mult": 0.15
        },
        "requires_paragon_dlc": False,
        "custom_tooltip": "only_one_scientist_focus"
    }
    actual = filter_trait_info(test_data, for_class="scientist")
    assert expected == actual
