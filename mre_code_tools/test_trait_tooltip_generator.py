from trait_tooltip_generator import (
    convert_stellaris_script_to_standard_yaml
)


def test_leader_trait_private_mines_2():
    # Common trait
    stellaris_script = """

"""
    expected_output = """

 leader_trait_private_mines_2:0 "$leader_trait_private_mines$ II"
 leader_trait_private_mines_2_desc:0 "$leader_trait_private_mines_desc$"
"""
    pass

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
				#NOT: { is_planet_class: pc_shattered_ring_habitable
			trait_is_gestalt_check: no
		job_miner_add: 4
	triggered_background_planet_modifier:
		potential:
			exists: FROM
			FROM:
				exists: owner
				owner:
					is_same_value: root.owner
				#NOT: { is_planet_class: pc_shattered_ring_habitable
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
	leader_class: commander scientist official
"""
    assert expected_output == actual_output