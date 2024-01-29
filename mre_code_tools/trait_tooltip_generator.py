# Given Stellaris leader trait info as YAML, generate Stellaris tooltip game code from it
import re

def create_tooltip_for_leader(
    
):
    pass


def convert_stellaris_script_to_standard_yaml(input_string):
    # NOT aren't used in trait description anyway
    comment_nots = re.sub('NOT', '#NOT', input_string)
    convert_blocks = re.sub('(?<!NOT) = \{\n', ':\n', comment_nots)
    convert_sameline_blocks = re.sub('(?<!NOT) = \{', ':', convert_blocks)
    remove_closing_braces = re.sub('\s*\}\n', '\n', convert_sameline_blocks)
    # remove_empty_lines = re.sub('\n\s\n', '\n', remove_closing_braces)
    remove_whitespace = re.sub('\n\n', '\n', remove_closing_braces)
    create_key_value_pairs = re.sub(' = ', ': ', remove_whitespace)
    clean_closing_brace_no_newline = re.sub('\s*\}', '', create_key_value_pairs)
    return clean_closing_brace_no_newline
