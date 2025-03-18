from unittest import TestCase

from ..converter import (
    normalize_list,
    convert_block_open,
    clean_up_line,
    convert_simple_assignment,
    block_open_to_json,
)

class TestConverter(TestCase):

    def test_normalize_list(self):

        line = "	leader_class = { commander scientist }"
        expectation = "	leader_class: ['commander', 'scientist']"
        actual = normalize_list(line)
        assert expectation == actual
        
        actual2 = clean_up_line(line)
        assert expectation == actual2


    def test_block_open(self):
        line = "	leader_class = {"
        expectation = "	leader_class:"
        actual = convert_block_open(line)
        assert expectation == actual
        
        actual2 = clean_up_line(line)
        assert expectation == actual2
        
    def test_block_open_json(self):
        line = "    leader_class = {"
        expectation = "    \"leader_class\": {"
        actual = block_open_to_json(line)
        assert expectation == actual
        

    def test_simple_assign(self):
        line = "         has_trait = subclass_commander_admiral"
        expectation = "         has_trait: subclass_commander_admiral"
        actual = convert_simple_assignment(line)
        actual2 = clean_up_line(line)
        assert expectation == actual
        assert expectation == actual2

test_data = """
leader_trait_scout = {
	leader_trait_type = veteran
	inline_script = {
		script = trait/icon
		CLASS = leader
		ICON = GFX_leader_trait_scout
		RARITY = free_or_veteran
		COUNCIL = no
		TIER = 1
	}
	leader_potential_add = {
		OR = {
			has_paragon_dlc = no
			has_trait = subclass_commander_admiral
			has_trait = subclass_scientist_explorer
		}
	}
	modifier = {
		ship_speed_mult = 0.05
		ship_hyperlane_range_add = 2
		fleet_mia_time_mult = -0.1
	}

	leader_class = { commander scientist }
	selectable_weight = {
		inline_script = paragon/subclass_free_trait_weight
		inline_script = paragon/pilot_weight_mult
		inline_script = {
			script = paragon/dual_subclass_weight_mult
			SUBCLASS_1 = commander_admiral
			SUBCLASS_2 = scientist_explorer
		}
	}
}
"""