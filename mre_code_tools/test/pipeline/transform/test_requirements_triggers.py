


from pipeline.transform.leader_trait_triggers import create_requirements_triggers_for_leader_traits


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
oxr_mdlc_leader_official_can_add_leader_trait_courtroom_training = {
    leader_class = official
    has_trait = subclass_official_diplomacy_councilor
    has_base_skill >= 4
    has_paragon_dlc = yes
    is_xenophobe = no
    exists = owner
    owner = { is_homicidal = no }
}
"""
    actual = create_requirements_triggers_for_leader_traits(test_data)
    assert expected == actual


def test_trigger_for_trait__robotist():
    test_data = {
        "leader_trait_robotist": {
            "trait_name": "leader_trait_robotist",
            "leader_class": "commander",
            "destiny_trait": True,
            "gfx": "GFX_leader_trait_robotist",
            "rarity": "paragon",
            "planet_modifier": {
                "planet_jobs_robotic_produces_mult": 0.2,
                "planet_pops_robotics_upkeep_mult": -0.2,
                "planet_cyborg_jobs_produces_mult": 0.2,
                "planet_pops_cyborgs_upkeep_mult": -0.2
            },
            "sector_modifier": {
                "planet_jobs_robotic_produces_mult": 0.1,
                "planet_pops_robotics_upkeep_mult": -0.1,
                "planet_cyborg_jobs_produces_mult": 0.1,
                "planet_pops_cyborgs_upkeep_mult": -0.1
            },
            "requires_paragon_dlc": True,
            "leader_potential_add": {
                "has_paragon_dlc": True,
                "OR": {
                    "has_trait": "subclass_commander_governor"
                },
                "exists": "owner",
                "owner": {
                    "OR": {
                        "has_technology": "tech_robotic_workers",
                        "has_cybernetic_ascension": True,
                        "is_individual_machine": True
                    }
                }
            }
        }
    }
    expected = """
oxr_mdlc_leader_commander_can_add_leader_trait_robotist = {
    leader_class = commander
    has_base_skill >= 8
    has_paragon_dlc = yes
    exists = owner
    owner = {  OR = { has_technology =  tech_robotic_workers   has_cybernetic_ascension = yes  is_individual_machine = yes } }
}
"""
    actual = create_requirements_triggers_for_leader_traits(test_data)
    assert expected == actual
