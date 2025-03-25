from unittest import TestCase
import re

from ..converter import (
    block_open_to_json,
    re_block_open,
    clean_up_line,
    convert_block_open,
    convert_simple_assignment,
    input_cz_output_json,
    MultipleBlocksSameLine,
    normalize_list,
    scrub_comments_from_line,
    search_blob_crunch_lists,
    iter_clean_up_lines,
    convert_iter_lines_to_dict,
)

class TestConverter(TestCase):

    def test_normalize_list(self):

        line = "    leader_class = { commander scientist }"
        expectation = "    \"leader_class\": ['commander', 'scientist'],"
        actual = normalize_list(line)
        assert expectation == actual
        
        actual2 = clean_up_line(line)
        assert expectation == actual2


    def test_block_open(self):
        line = "	leader_class = {"
        expectation = "	\"leader_class\": {"
        actual = convert_block_open(line)
        assert expectation == actual
        
        actual2 = clean_up_line(line)
        assert expectation == actual2
        
    def test_block_open_json(self):
        line = "    leader_class = {"
        expectation = "    \"leader_class\": {"
        re_match = re.match(re_block_open, line)
        actual = block_open_to_json(re_match)
        assert expectation == actual
        

    def test_simple_assign(self):
        line = "         has_trait = subclass_commander_admiral"
        expectation = "         \"has_trait\": \"subclass_commander_admiral\","
        actual = convert_simple_assignment(line)
        actual2 = clean_up_line(line)
        assert expectation == actual
        assert expectation == actual2
    
    def test_touching_numbers(self):
        line = "fleet_mia_time_mult = -0.1"
        expectation = "\"fleet_mia_time_mult\": -0.1,"
        actual = convert_simple_assignment(line)
        actual2 = clean_up_line(line)
        assert expectation == actual
        assert expectation == actual2
    
    def test_handle_separate_list_items(self):
        lines = [
        "opposites = {",
        "    leader_trait_gale_speed",
        "    leader_trait_gale_speed_2",
        "    leader_trait_gale_speed_3",
        "}",
        ]
        expectations = [
        "\"opposites\": {",
        "    leader_trait_gale_speed",
        "    leader_trait_gale_speed_2",
        "    leader_trait_gale_speed_3",
        "},",
        ]
        for line, expect in zip(lines, expectations):
            actual = clean_up_line(line)
            assert actual == expect
    
    def test_global_crunch_list(self):
        # Need to read the whole file/blob at once to make the conversion
        blob = """
	leader_potential_add = {
		is_gestalt = no
	}
	leader_class = { commander }
	opposites = {
		leader_trait_gale_speed
		leader_trait_gale_speed_2
		leader_trait_gale_speed_3
	}
	selectable_weight = {
		weight = @class_negative_trait_weight
		inline_script = paragon/pilot_weight_mult
	}
"""
        expected = """
	leader_potential_add = {
		is_gestalt = no
	}
	leader_class = { commander }
	\"opposites\": ['leader_trait_gale_speed', 'leader_trait_gale_speed_2', 'leader_trait_gale_speed_3'],
	selectable_weight = {
		weight = @class_negative_trait_weight
		inline_script = paragon/pilot_weight_mult
	}
"""
        actual = search_blob_crunch_lists(blob)
        assert expected == actual
    
    def test_multiple_blocks_same_line(self):
        # not supporting crunching multiple blocks on the same line,
        # this should be resolved before processing with a substitution
        blob = "      leader_potential_add = { owner = { is_gestalt = no } }"
        with self.assertRaises(MultipleBlocksSameLine):
            result = clean_up_line(blob)

    def test_scrub_comment_from_line(self):
        data = "      has_paragon_dlc = no  # some comment"
        expected = "      has_paragon_dlc = no"
        actual = scrub_comments_from_line(data)
        assert expected == actual
    
    def test_iterating_a_block(self):
        lines = [
            "modifier = {",
            "    ship_speed_mult = 0.05",
            "    ship_hyperlane_range_add = 2",
            "    fleet_mia_time_mult = -0.1",
            "}",
        ]

        expectations = [
            "\"modifier\": {",
            "    \"ship_speed_mult\": 0.05,",
            "    \"ship_hyperlane_range_add\": 2,",
            "    \"fleet_mia_time_mult\": -0.1,",
            "},",
        ]
        for line, expect in zip(lines, expectations):
            actual = clean_up_line(line)
            assert actual == expect
    
    def test_converting_block_string_to_json(self):
        lines = [
            "modifier = {",
            "    ship_speed_mult = 0.05",
            "    ship_hyperlane_range_add = 2",
            "    fleet_mia_time_mult = -0.1",
            "}",
        ]
        joined = iter_clean_up_lines(lines)
        result = convert_iter_lines_to_dict(joined)
        assert type(result) == dict
    
    def test_converting_larger_trait_data__leader_trait_scout(self):
        data = """
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
}
"""
        expected = {
            "leader_trait_scout": {
                "leader_trait_type": "veteran",
                "inline_script": {
                    "script": "trait/icon",
                    "CLASS": "leader",
                    "ICON": "GFX_leader_trait_scout",
                    "RARITY": "free_or_veteran",
                    "COUNCIL": "no",
                    "TIER": 1
                }
            }
        }
        actual = input_cz_output_json(data)
        assert expected == actual


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