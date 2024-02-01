import re
import sys
import argparse
from tempfile import NamedTemporaryFile

def convert_stellaris_script_to_standard_yaml(input_string):
    # NOT aren't used in trait description anyway
    convert_tabs_to_spaces = re.sub('\t', '  ', input_string)
    remove_comment_blocks = re.sub('\n#.*', '', convert_tabs_to_spaces)
    comment_nots = re.sub('NOT', '#NOT', remove_comment_blocks)
    convert_blocks = re.sub('(?<!NOT) = \{\n', ':\n', comment_nots)
    convert_sameline_blocks = re.sub('(?<!NOT) = \{', ':', convert_blocks)
    remove_closing_braces = re.sub('\s*\}\n', '\n', convert_sameline_blocks)
    create_key_value_pairs = re.sub(' = ', ': ', remove_closing_braces)
    clean_closing_brace_no_newline = re.sub('\s*\}', '', create_key_value_pairs)
    remove_extralines = re.sub('\n{2,}', '\n', clean_closing_brace_no_newline)
    # One-liners with multiple nested {} don't cleanly replace, so comment those lines
    # since we are doing traits anyway.. dont need those lines
    comment_nested_multiline = re.sub('\n(\s)(?=((.*:){2,4}))', '\n#', remove_extralines)
    # leftover_multiline_comment = re.sub('#{2,}', '', comment_nested_multiline)

    # official scientist
    # commander official
    # commander official scientist
    # official scientist commander
    # official commander scientist
    # Carefully go through leader_class definitions
    # TODO: Fix bug where list of fewer elements is patched before long list
    structured_leader_class_lists3 = convert_leader_class_definitions_to_lists(comment_nested_multiline, 3)
    structured_leader_class_lists2 = convert_leader_class_definitions_to_lists(structured_leader_class_lists3, 2)
    structured_leader_class_lists = convert_leader_class_definitions_to_lists(structured_leader_class_lists2)
    return structured_leader_class_lists

def convert_leader_class_definitions_to_lists(input_string, min_classes_length: int=1):
    # convert like 'leader_class: commander official' to
    # 'leader_class: ["commander", "official"]' which is valid yaml
    # min_classes_length means crunch N number of sequential leader class names into a list.
    leader_class_query = re.compile(f"(leader_class:(\s(commander|official|scientist)){{{min_classes_length},}})")
    results = re.findall(leader_class_query, input_string)
    # we get a list of tuples like [('leader_class: commander official scientist', ' scientist', 'scientist'),
    # ('leader_class: commander official', ' official', 'official'), etc
    input_string_copy = input_string
    for result in results:
        complete_line = result[0]
        parts = complete_line.split(': ')
        unformatted_classes = parts[1]
        classes_as_list = unformatted_classes.split(' ')
        # now we have ["commander", "official", "scientist"]
        # the trick is directly insert the str version of the list
        # breakpoint()
        line_with_structured_data = f"{parts[0]}: {str(classes_as_list)}"
        # oh the horror
        input_string_copy = re.sub(complete_line, line_with_structured_data, input_string_copy)
    return input_string_copy

def convert_leader_class_definitions_to_lists_1(input_string):
    # convert like 'leader_class: commander official' to
    # 'leader_class: ["commander", "official"]' which is valid yaml
    leader_class_query = re.compile("(leader_class:(\s(commander|official|scientist)){1,})")
    results = re.findall(leader_class_query, input_string)
    # we get a list of tuples like [('leader_class: commander official scientist', ' scientist', 'scientist'),
    # ('leader_class: commander official', ' official', 'official'), etc
    input_string_copy = input_string
    for result in results:
        complete_line = result[0]
        parts = complete_line.split(': ')
        unformatted_classes = parts[1]
        classes_as_list = unformatted_classes.split(' ')
        # now we have ["commander", "official", "scientist"]
        # the trick is directly insert the str version of the list
        # breakpoint()
        line_with_structured_data = f"{parts[0]}: {str(classes_as_list)}"
        # oh the horror
        input_string_copy = re.sub(complete_line, line_with_structured_data, input_string_copy)
    return input_string_copy

def mega_resort_base_leader_traits(
    stellaris_base_traits_path
):
    # Just over 300 KB
    leader_trait_files = [
        "00_admiral_traits",
        "00_general_traits",
        "00_generic_leader_traits",
        "00_governor_traits",
        "00_scientist_traits",
        "00_starting_ruler_traits",
    ]
    # super "load everything in memory and mega-sort"
    # generic (all leader classes)
    # commander, official, scientist
    # FOUR files in total
    leader_any_json = leader_commander_json = leader_scientist_json = leader_official_json
    for stellaris_script in leader_trait_files:
        file_contents_as_dict = convert_stellaris_script_to_standard_yaml(stellaris_script)
        pass
    

if __name__=="__main__":
    parser = argparse.ArgumentParser(
        prog="0xRetro Stellaris->>YAML",
        description="Mostly converts Stellaris script to standard YAML"
    )
    parser.add_argument('-i', '--infile', help='Stellaris traits file to read')
    args = parser.parse_args()
    buffer = ''
    if not args.infile:
        sys.exit('Need to specify an input file with --infile <filename>')
    with open(args.infile, "r") as infile:
        buffer = convert_stellaris_script_to_standard_yaml(
            infile.read()
        )
    print(buffer)
