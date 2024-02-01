from stellaris_yaml_converter import (
    convert_stellaris_script_to_standard_yaml,
    convert_leader_class_definitions_to_lists
)

def test_convert_stellaris_script_to_standard_yaml():

    test_input = """
leader_trait_private_mines_2 = {
    replace_traits = { "leader_trait_private_mines" }
    inline_script = {
        script = trait/icon
        CLASS = leader
        ICON = "GFX_leader_trait_private_mines"
        RARITY = common
        COUNCIL = no
        TIER = 2
    }
    triggered_background_planet_modifier = {
        potential = {
            exists = FROM
            FROM = {
                exists = owner
                owner = {
                    is_same_value = root.owner
                }
                NOT = { is_planet_class = pc_shattered_ring_habitable }
            }
            trait_is_gestalt_check = no
        }
        job_miner_add = 4
    }
    triggered_background_planet_modifier = {
        potential = {
            exists = FROM
            FROM = {
                exists = owner
                owner = {
                    is_same_value = root.owner
                }
                NOT = { is_planet_class = pc_shattered_ring_habitable }
            }
            trait_is_gestalt_check = yes
        }
        job_mining_drone_add = 4
    }
    triggered_background_planet_modifier = {
        potential = {
            exists = FROM
            FROM = {
                exists = owner
                owner = {
                    is_same_value = root.owner
                }
                is_planet_class = pc_shattered_ring_habitable
            }
            trait_is_gestalt_check = no
        }
        job_scrap_miner_add = 4
    }
    triggered_background_planet_modifier = {
        potential = {
            exists = FROM
            FROM = {
                exists = owner
                owner = {
                    is_same_value = root.owner
                }
                is_planet_class = pc_shattered_ring_habitable
            }
            trait_is_gestalt_check = yes
        }
        job_scrap_miner_drone_add = 4
    }
    planet_modifier = {
        planet_miners_minerals_produces_mult = 0.10
    }
    sector_modifier = {
        planet_miners_minerals_produces_mult = 0.05
    }
    leader_class = { commander scientist official }
"""
    actual_output = convert_stellaris_script_to_standard_yaml(test_input)

    expected_output = """
leader_trait_private_mines_2:
    replace_traits: "leader_trait_private_mines"
    inline_script:
        script: trait/icon
        CLASS: leader
        ICON: "GFX_leader_trait_private_mines"
        RARITY: common
        COUNCIL: no
        TIER: 2
    triggered_background_planet_modifier:
        potential:
            exists: FROM
            FROM:
                exists: owner
                owner:
                    is_same_value: root.owner
#               #NOT: { is_planet_class: pc_shattered_ring_habitable
            trait_is_gestalt_check: no
        job_miner_add: 4
    triggered_background_planet_modifier:
        potential:
            exists: FROM
            FROM:
                exists: owner
                owner:
                    is_same_value: root.owner
#               #NOT: { is_planet_class: pc_shattered_ring_habitable
            trait_is_gestalt_check: yes
        job_mining_drone_add: 4
    triggered_background_planet_modifier:
        potential:
            exists: FROM
            FROM:
                exists: owner
                owner:
                    is_same_value: root.owner
                is_planet_class: pc_shattered_ring_habitable
            trait_is_gestalt_check: no
        job_scrap_miner_add: 4
    triggered_background_planet_modifier:
        potential:
            exists: FROM
            FROM:
                exists: owner
                owner:
                    is_same_value: root.owner
                is_planet_class: pc_shattered_ring_habitable
            trait_is_gestalt_check: yes
        job_scrap_miner_drone_add: 4
    planet_modifier:
        planet_miners_minerals_produces_mult: 0.10
    sector_modifier:
        planet_miners_minerals_produces_mult: 0.05
    leader_class: ['commander', 'scientist', 'official']
"""
    assert expected_output == actual_output

def test_convert_stellaris_script__destiny_trait():
    
    stellaris_script = """
leader_trait_naturalist_3 = {
    replace_traits = { "leader_trait_naturalist_2" }
    inline_script = {
        script = trait/icon
        CLASS = official
        ICON = "GFX_leader_trait_naturalist"
        RARITY = veteran
        COUNCIL = no
        TIER = 3
    }
    planet_modifier = {
        deposit_blockers_natural_unity_produces_add = 12
    }
    sector_modifier = {
        deposit_blockers_natural_unity_produces_add = 6
    }
    veteran_class_locked_trait = yes
    leader_class = { official scientist }
}
"""

    expected_output = """
leader_trait_naturalist_3:
    replace_traits: "leader_trait_naturalist_2"
    inline_script:
        script: trait/icon
        CLASS: official
        ICON: "GFX_leader_trait_naturalist"
        RARITY: veteran
        COUNCIL: no
        TIER: 3
    planet_modifier:
        deposit_blockers_natural_unity_produces_add: 12
    sector_modifier:
        deposit_blockers_natural_unity_produces_add: 6
    veteran_class_locked_trait: yes
    leader_class: ['official', 'scientist']
"""
    actual_output = convert_stellaris_script_to_standard_yaml(stellaris_script)

    assert expected_output == actual_output

def test_structuring_leader_class_lists():

    test_data = """
  leader_class: commander official scientist
  leader_class: official
"""
    actual_output = convert_leader_class_definitions_to_lists(test_data)

    expected_output = """
  leader_class: ['commander', 'official', 'scientist']
  leader_class: ['official']
"""
    assert expected_output == actual_output

def test_replace_var_symbol():

    test_data = """
selectable_weight = {
    weight = @shared_trait_weight
    inline_script = paragon/governor_weight_mult
    inline_script = {
        script = "paragon/existing_trait_weight_mult"
        TRAIT = leader_trait_bureaucrat
    }
}
"""
    actual_output = convert_stellaris_script_to_standard_yaml(test_data)
    expected_output = """
selectable_weight:
    weight: var_shared_trait_weight
    inline_script: paragon/governor_weight_mult
    inline_script:
        script: "paragon/existing_trait_weight_mult"
        TRAIT: leader_trait_bureaucrat
"""
    assert expected_output == actual_output
