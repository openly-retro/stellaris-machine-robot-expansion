from mre_mod_trait_organizer import (
    pick_highest_tier_of_trait
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

