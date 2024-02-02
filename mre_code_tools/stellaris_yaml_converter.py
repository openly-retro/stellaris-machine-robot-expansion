from copy import copy
import re
import sys
import argparse
from tempfile import NamedTemporaryFile
import argparse
from yaml import safe_load

def convert_stellaris_script_to_standard_yaml(input_string):
    # NOT aren't used in trait description anyway
    convert_tabs_to_spaces = re.sub(r"\t", '  ', input_string)
    remove_comment_blocks = re.sub(r"\n#.*", '', convert_tabs_to_spaces)
    comment_nots = re.sub("NOT", '#NOT', remove_comment_blocks)
    convert_blocks = re.sub(r"(?<!NOT) = \{\n", ':\n', comment_nots)
    convert_sameline_blocks = re.sub(r"(?<!NOT) = \{", ':', convert_blocks)
    remove_closing_braces = re.sub(r"\s*\}\n", '\n', convert_sameline_blocks)
    create_key_value_pairs = re.sub(' = ', ': ', remove_closing_braces)
    clean_closing_brace_no_newline = re.sub(r"\s*\}", '', create_key_value_pairs)
    remove_extralines = re.sub(r"\n{2,}", '\n', clean_closing_brace_no_newline)
    # One-liners with multiple nested {} don't cleanly replace, so comment those lines
    # since we are doing traits anyway.. dont need those lines
    comment_nested_multiline = re.sub(r"\n(\s)(?=((.*:){2,4}))", '\n#', remove_extralines)
    # leftover_multiline_comment = re.sub('#{2,}', '', comment_nested_multiline)
    comment_out_variables = re.sub(r"\@", 'var_', comment_nested_multiline)  # YAML doesn't like the @ symbol
    # Carefully go through leader_class definitions
    structured_leader_class_lists3 = convert_leader_class_definitions_to_lists(comment_out_variables, 3)
    structured_leader_class_lists2 = convert_leader_class_definitions_to_lists(structured_leader_class_lists3, 2)
    structured_leader_class_lists = convert_leader_class_definitions_to_lists(structured_leader_class_lists2)

    # Take care of repeated has_trait keys >:o
    tidy_subclass_has_trait_duplicates = concatenate_multiline_has_trait_definitions(structured_leader_class_lists)
    
    # Also need to comment out "inline_script = paragon" because PDX are using duplicate keys AGAIN >_<
    return tidy_subclass_has_trait_duplicates

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

def concatenate_multiline_has_trait_definitions(input_string, min_occurrences: int=1):
    """ PDX put multiple lines with the same key definition, so we have to deal with that """
    multiple_has_trait_lines = re.compile(r"((\s*has_trait: subclass\w*\n){1,})")
    results = re.findall(multiple_has_trait_lines, input_string)
    input_string_copy = copy(input_string)
    for result in results:
        """
        It's going to be one big string starting with \n
        """
        complete_line = result[0]
        pieces = result[0].strip().split('\n')
        subclasses = [ piece.split(': ')[1] for piece in pieces ]
        indentation = result[0].split('has_trait: ')[0].count(' ')
        substitution = f"\n{indentation*" "}has_trait: {subclasses}\n"
        input_string_copy = re.sub(complete_line, substitution, input_string_copy)
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
    parser.add_argument(
        '-o', '--outfile', required=False,
        help="Name of file to write the newly converted standard YAML to"
    )
    args = parser.parse_args()
    buffer = ''
    if not args.infile:
        sys.exit('Need to specify an input file with --infile <filename>')
    sys.stdout.write('0xRetro Stellaris script chopper.. spinning up blades\n')
    with open(args.infile, "r") as infile:
        buffer = convert_stellaris_script_to_standard_yaml(
            infile.read()
        )
        try:
            _ = safe_load(buffer)
        except Exception as ex:
            sys.exit(f"There was a problem validating the YAML after chopping up the Stellaris script: {ex}")
        if args.outfile:
            with open(args.outfile, 'w+') as outfile:
                outfile.write(buffer)
        else:
            print(buffer)
        print("Done. There's a high change this finished correctly.")
        sys.exit()
