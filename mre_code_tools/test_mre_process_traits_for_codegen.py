from mre_process_traits_for_codegen import (
    pick_highest_tier_of_trait,
    filter_traits_by_mod_feature,
    trickle_up_subclass_requirements,
    trait_qualifies_for_councilor_editor,
    create_requirements_triggers_for_leader_traits,
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
            "leader_trait_adaptable_2": {
                "trait_name": "leader_trait_adaptable_2",
                "leader_class": "commander",
                "gfx": "GFX_leader_trait_adaptable",
                "rarity": "common",
                "self_modifier": {
                    "species_leader_exp_gain": 0.2
                },
                "requires_paragon_dlc": False,
                "is_councilor_trait": False
            }
        },
        {
            "trait_ruler_eye_for_talent_2": {
                "trait_name": "trait_ruler_eye_for_talent_2"
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
        },
        {
            "leader_trait_carefree": {
                "trait_name": "leader_trait_carefree",
                "gfx": "GFX_leader_trait_carefree",
                "allow_for_ruler": False
            }
        }
    ]
    expected = {
        "leader_making_traits": [
            {
                "leader_trait_adaptable_2": {
                    "trait_name": "leader_trait_adaptable_2",
                    "leader_class": "commander",
                    "gfx": "GFX_leader_trait_adaptable",
                    "rarity": "common",
                    "self_modifier": {
                        "species_leader_exp_gain": 0.2
                    },
                    "requires_paragon_dlc": False,
                    "is_councilor_trait": False
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
            {
                "leader_trait_carefree": {
                    "trait_name": "leader_trait_carefree",
                    "gfx": "GFX_leader_trait_carefree",
                    "allow_for_ruler": False
                }
            }
        ],
        "core_modifying_traits": [
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
        "councilor_editor_traits": [
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
    actual = trickle_up_subclass_requirements(test_data, for_class="commander")
    assert expected == actual

def test_trait_qualifies_for_councilor_editor__various_traits():
    pass

def test_create_trigger_for_trait__courtroom_training():
    test_data = {
        "leader_trait_courtroom_training": {
            "trait_name": "leader_trait_courtroom_training",
            "leader_class": "official",
            "gfx": "GFX_leader_trait_courtroom_training",
            "rarity": "veteran",
            "councilor_modifier": {
                "country_trust_cap_add": 35
            },
            "requires_paragon_dlc": True,
            "leader_potential_add": {
                "has_paragon_dlc": True,
                "has_subclass_trait": [
                    "subclass_official_diplomacy_councilor"
                ],
                "is_xenophobe": False,
                "exists": "owner",
                "owner": {
                    "is_homicidal": False
                }
            },
            "required_subclass": "subclass_official_diplomacy_councilor",
            "is_councilor_trait": True
        }
    }

    expected = """
oxr_mdlc_leader_can_add_leader_trait_courtroom_training = {
    leader_class = official
    has_trait = subclass_official_diplomacy_councilor
    has_skill >= 4
    has_paragon_dlc = yes
    is_xenophobe = no
    exists = owner
}
"""
    actual = create_requirements_triggers_for_leader_traits(test_data)
    assert expected == actual
