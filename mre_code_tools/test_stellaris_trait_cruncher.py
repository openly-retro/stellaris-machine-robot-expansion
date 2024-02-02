from stellaris_trait_cruncher import (
    filter_trait_info,
    sort_traits_by_leader_class,
    sort_traits_asc
)

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
                'planet_administrators_unity_produces_mult': 0.05
            },
            'triggered_sector_modifier': {
                'potential': {'always': True},
                'planet_administrators_unity_produces_mult': 0.025
            },
            'triggered_desc': {
                'exclusive_trigger': {'always': True},
                'text': 'leader_trait_bureaucrat_2_tt'
            },
            'leader_class': ['official', 'commander', 'scientist']
        }
    }
    filtered_info = filter_trait_info(parsed_trait)
    expected_info = {
        "trait_name": "leader_trait_bureaucrat_2",
        "leader_class": ['official', 'commander', 'scientist'],
        "gfx": "GFX_leader_trait_bureaucrat",
        "rarity": "common",
        "planet_modifier": {
            'planet_administrators_unity_produces_mult': 0.05
        },
        "sector_modifier": {
            'planet_administrators_unity_produces_mult': 0.025
        },
        "requires_paragon_dlc": False
    }
    assert expected_info == filtered_info

def test_crunch__trait_ruler_architectural_sense_3():
    # Councilor traits are good candidate for core-modifying ruler traits
    test_data = {
        "trait_ruler_architectural_sense_3": {
            "replace_traits": "trait_ruler_architectural_sense_2",
            "inline_script": {
                "script": "trait/icon",
                "CLASS": "official",
                "ICON": "GFX_leader_trait_architectural_sense",
                "RARITY": "veteran",
                "COUNCIL": "yes",
                "TIER": 3
            },
            "councilor_modifier": {
                "planet_buildings_cost_mult": -0.1,
                "planet_districts_cost_mult": -0.1,
                "planet_buildings_upkeep_mult": -0.05,
                "planet_districts_upkeep_mult": -0.05,
                "planet_building_build_speed_mult": 0.25
            },
            "veteran_class_locked_trait": "yes",
            "leader_potential_add": {
                "has_paragon_dlc": "yes"
            },
            "leader_class": [
                "official"
            ]
        }
    }
    actual = filter_trait_info(test_data)
    expected = {
        "trait_name": "trait_ruler_architectural_sense_3",
        "leader_class": ["official"],
        "gfx": "GFX_leader_trait_architectural_sense",
        "rarity": "veteran",
        "councilor_modifier": {
            "planet_buildings_cost_mult": -0.1,
            "planet_districts_cost_mult": -0.1,
            "planet_buildings_upkeep_mult": -0.05,
            "planet_districts_upkeep_mult": -0.05,
            "planet_building_build_speed_mult": 0.25
        },
        "requires_paragon_dlc": True
    }
    assert expected == actual

def test_crunch__leader_trait_reformer():
    test_data = {
        "leader_trait_reformer": {
            "inline_script": {
                "script": "trait/icon",
                "CLASS": "official",
                "ICON": "GFX_leader_trait_reformer",
                "RARITY": "free_or_veteran",
                "COUNCIL": "yes",
                "TIER": 1
            },
            "leader_potential_add": {
                "is_gestalt": "no",
                "OR": {
                    "has_paragon_dlc": "no",
                    "has_trait": "subclass_official_economy_councilor"
                }
            },
            "councilor_modifier": {
                "country_unity_produces_mult": 0.05,
                "pop_government_ethic_attraction": 0.35
            },
            "veteran_class_locked_trait": "yes",
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
        "requires_paragon_dlc": False
    }

def test_crunch__leader_trait_arbiter():
    # Destiny trait
    test_data = {
        "leader_trait_arbiter": {
            "destiny_trait": "yes",
            "inline_script": {
                "script": "trait/icon",
                "CLASS": "commander",
                "ICON": "GFX_leader_trait_arbiter",
                "RARITY": "paragon",
                "COUNCIL": "no",
                "TIER": "none"
            },
            "leader_potential_add": {
                "has_paragon_dlc": "yes",
                "has_trait": "subclass_commander_governor"
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
        "leader_class": ["commander"],
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
        "required_subclass": "subclass_commander_governor"
    }
    assert expected == actual

def test_crunch__leader_trait_scout():
    """ An example which has TWO potential subclasses """
    test_data = {}
    # leader_trait_scout = {
    #     veteran_class_locked_trait = yes
    #     inline_script = {
    #         script = trait/icon
    #         CLASS = leader
    #         ICON = GFX_leader_trait_scout
    #         RARITY = free_or_veteran
    #         COUNCIL = no
    #         TIER = 1
    #     }
    #     leader_potential_add = {
    #         OR = {
    #             has_paragon_dlc = no
    #             has_trait = subclass_commander_admiral
    #             has_trait = subclass_scientist_explorer
    #         }
    #     }
    #     modifier = {
    #         ship_speed_mult = 0.05
    #         ship_hyperlane_range_add = 2
    #         fleet_mia_time_mult = -0.1
    #     }

    #     leader_class = { commander scientist }
    #     selectable_weight = {
    #         inline_script = paragon/subclass_free_trait_weight
    #         inline_script = paragon/pilot_weight_mult
    #         inline_script = {
    #             script = paragon/dual_subclass_weight_mult
    #             SUBCLASS_1 = commander_admiral
    #             SUBCLASS_2 = scientist_explorer
    #         }
    #     }
    # }


def test_sort_traits_by_leader_class():

    test_data = {
        "trait_foo1": {
            "trait_name": "trait_foo1",
            "leader_class": ["official"]
        },
        "trait_foo2": {
            "trait_name": "trait_foo2",
            "leader_class": ["commander", "official", "scientist"]
        },
        "trait_foo3": {
            "trait_name": "trait_foo3",
            "leader_class": ["commander", "scientist"]
        }
    }
    actual = sort_traits_by_leader_class(test_data)
    expected = {
        "official": [
            {
                "trait_name": "trait_foo1",
                "leader_class": "official"
            },
            {
                "trait_name": "trait_foo2",
                "leader_class": "official"
            }
        ],
        "commander": [
            {
                "trait_name": "trait_foo2",
                "leader_class": "commander"
            },
            {
                "trait_name": "trait_foo3",
                "leader_class": "commander"
            }
        ],
        "scientist": [
            {
                "trait_name": "trait_foo2",
                "leader_class": "scientist"
            },
            {
                "trait_name": "trait_foo3",
                "leader_class": "scientist"
            }
        ]
    }
    assert expected == actual

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
