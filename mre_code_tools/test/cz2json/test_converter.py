from unittest import TestCase
import re

from cz2json.converter import (
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
    handle_single_block_assignment,
)

class TestConverter(TestCase):

    def test_normalize_list(self):

        line = "    leader_class = { commander scientist }"
        expectation = "    \"leader_class\": [\"commander\", \"scientist\"],"
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
    \"opposites\": ["leader_trait_gale_speed", "leader_trait_gale_speed_2", "leader_trait_gale_speed_3"],
    selectable_weight = {
        weight = @class_negative_trait_weight
        inline_script = paragon/pilot_weight_mult
    }
"""
        actual = search_blob_crunch_lists(blob)
        assert expected == actual
    
    # def test_multiple_blocks_same_line(self):
    #     # not supporting crunching multiple blocks on the same line,
    #     # this should be resolved before processing with a substitution
    #     blob = "      leader_potential_add = { owner = { is_gestalt = no } }"
    #     with self.assertRaises(MultipleBlocksSameLine):
    #         result = clean_up_line(blob)

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


    def test_expanding_multiple_blocks_same_line(self):
        test_data = 'NOT = { has_trait_tier1or2 = { TRAIT = leader_trait_eager } }'

        expected = '"NOT": { "has_trait_tier1or2": { "TRAIT": "leader_trait_eager" } },'
        actual = clean_up_line(test_data)
        assert expected == actual

    def test_handle_single_block_assignment(self):
        test_data = "potential = { is_councilor = no }"
        expected = '"potential": { "is_councilor": "no" },'
        actual = clean_up_line(test_data)
        assert expected == actual

    def test_dot_scoping(self):
        test_data = "is_same_value = root.owner"
        expected = '"is_same_value": "root.owner",'
        actual = clean_up_line(test_data)
        assert expected == actual

    def test_math_comparisons(self):
        test_data = "has_skill > 1"
        expected = '"has_skill": "gt_1",'
        actual = clean_up_line(test_data)
        assert expected == actual

        test_data = "has_skill <= 10"
        expected = '"has_skill": "lte_10",'

    def test_concat_large_list(self):
        test_data = """opposites = {
		leader_trait_private_mines
		leader_trait_private_mines_2
		leader_trait_homesteader
	}"""
        expected = """"opposites": ["leader_trait_private_mines", "leader_trait_private_mines_2", "leader_trait_homesteader"],"""
        preprocessed = search_blob_crunch_lists(test_data)
        actual = clean_up_line(preprocessed)
        assert expected == actual

    def test_script_var_param_sorcery(self):
        test_data = "add_age = value:percent_of_leader_lifespan|PERCENT|-25|"
        expected = '"add_age": "value:percent_of_leader_lifespan|PERCENT|-25|",'
        actual = clean_up_line(test_data)
        assert expected == actual
