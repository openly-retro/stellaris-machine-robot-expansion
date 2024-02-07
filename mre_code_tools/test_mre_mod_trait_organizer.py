from mre_mod_trait_organizer import (
    pick_highest_tier_of_trait,
    filter_traits_by_mod_feature,
    trickle_up_subclass_requirements
)

def test_picking_highest_tier__2():
    test_data = [
        {
            "leader_trait_academia_recruiter": {
                "trait_name": "leader_trait_academia_recruiter",
            }
        },
        {
            "leader_trait_adaptable": {
                "trait_name": "leader_trait_adaptable",
            }
        },
        {
            "leader_trait_adaptable_2": {
                "trait_name": "leader_trait_adaptable_2",
            }
        },
        {
            "leader_trait_adventurous_spirit": {
                "trait_name": "leader_trait_adventurous_spirit",
            }
        },
        {
            "leader_trait_adventurous_spirit_2": {
                "trait_name": "leader_trait_adventurous_spirit_2",
    
            }
        },
        {
            "leader_trait_adventurous_spirit_3": {
                "trait_name": "leader_trait_adventurous_spirit_3",
            }
        }
    ]
    expected = [
        {
            "leader_trait_academia_recruiter": {
                "trait_name": "leader_trait_academia_recruiter",
            }
        },
        {
            "leader_trait_adaptable_2": {
                "trait_name": "leader_trait_adaptable_2",
            }
        },
        {
            "leader_trait_adventurous_spirit_3": {
                "trait_name": "leader_trait_adventurous_spirit_3",
            }
        }
    ]
    actual = pick_highest_tier_of_trait(test_data)
    assert expected == actual

def test_sorting_traits_for_which_feature__1():
    # To leader-making feature, or core modifying?
    test_data = [
        {
            "leader_trait_adaptable": {
                "trait_name": "leader_trait_adaptable",
                "self_modifier": {  # Can go to both
                    "species_leader_exp_gain": 0.1
                }
            }
        },
        {
            "leader_trait_armada_logistician": {
                "trait_name": "leader_trait_armada_logistician",
                "is_councilor_trait": True,  # core-modifying
                "councilor_modifier": {
                    "ships_upkeep_mult": -0.05
                }
            }
        },
        {
            "leader_trait_artillerist": {
                "trait_name": "leader_trait_artillerist",
                "fleet_modifier": {  # leader-making
                    "ship_weapon_damage": 0.075
                }
            }
        },
        {
            "leader_trait_clone_army_commander": {}
        }
    ]
    expected = {
        "leader_making_traits": [
            {
                "leader_trait_adaptable": {
                    "trait_name": "leader_trait_adaptable",
                    "self_modifier": {
                        "species_leader_exp_gain": 0.1
                    }
                }
            },
            {
                "leader_trait_artillerist": {
                    "trait_name": "leader_trait_artillerist",
                    "fleet_modifier": {
                        "ship_weapon_damage": 0.075
                    }
                }
            },
        ],
        "core_modifying_traits": [
            {
                "leader_trait_adaptable": {
                    "trait_name": "leader_trait_adaptable",
                    "self_modifier": {
                        "species_leader_exp_gain": 0.1
                    }
                }
            },
            {
                "leader_trait_armada_logistician": {
                    "trait_name": "leader_trait_armada_logistician",
                    "is_councilor_trait": True,
                    "councilor_modifier": {
                        "ships_upkeep_mult": -0.05
                    }
                }
            },
        ],
        "outliers": []
    }
    actual = filter_traits_by_mod_feature(test_data)
    assert expected == actual

def test_transfer_subclass_reqs_to_other_traits_in_series():
    """ A tier-1 trait will have subclass requirements but often its tier 2/3 replacement wont """
    test_data = [
        {
            "leader_trait_adaptable": {
                "trait_name": "leader_trait_adaptable",
                "required_subclass": "subclass_commander_councilor"
            }
        },
        {
            "leader_trait_adaptable_2": {
                "trait_name": "leader_trait_adaptable"
            }
        },
    ]

    # for raw_trait in sorted_data:
    # trait_name = [*raw_trait][0]
    # assert raw_trait[trait_name]['required_subclass'] == "subclass_commander_admiral"
    expected = [
        {
            "leader_trait_adaptable": {
                "trait_name": "leader_trait_adaptable",
                "required_subclass": "subclass_commander_councilor"
            }
        },
        {
            "leader_trait_adaptable_2": {
                "trait_name": "leader_trait_adaptable",
                "required_subclass": "subclass_commander_councilor"
            }
        },
    ]
    actual = trickle_up_subclass_requirements(test_data)
    assert expected == actual
