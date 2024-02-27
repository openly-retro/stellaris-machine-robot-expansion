from copy import copy
import re
import sys
import argparse
import argparse
from yaml import safe_load

TAB_SIZE = 2

def convert_stellaris_script_to_standard_yaml(input_string):
    # NOT aren't used in trait description anyway
    add_spaces_between_brace_and_text_opening = re.sub(
        r"(\{)(?=\w)", '{ ', input_string
    )
    add_spaces_between_brace_and_text_closing = re.sub(
        r"(?<=\w)(\})", ' }', add_spaces_between_brace_and_text_opening
    )
    expand_multiple_one_line_assignments = make_newlines_for_multiple_assignments(add_spaces_between_brace_and_text_closing)

    convert_tabs_to_spaces = re.sub(r"\t", ' '*TAB_SIZE, expand_multiple_one_line_assignments)
    remove_comment_blocks = re.sub(r"\n\s{0,}#.*", '', convert_tabs_to_spaces)
    # comment_nots = re.sub("NOT", '#NOT', remove_comment_blocks)
    # convert_blocks = re.sub(r"(?<!NOT) = \{\n", ':\n', comment_nots)
    # convert_sameline_blocks = re.sub(r"(?<!NOT) = \{", ':', convert_blocks)
    remove_closing_braces = re.sub(r"\s*\}\n", '\n', remove_comment_blocks)
    remove_opening_braces = re.sub(r"\s{0,}\{", '', remove_closing_braces)
    create_key_value_pairs = re.sub(' = ', ': ', remove_opening_braces)
    clean_closing_brace_no_newline = re.sub(r"\s*\}", '', create_key_value_pairs)
    remove_extralines = re.sub(r"\n{2,}", '\n', clean_closing_brace_no_newline)
    # One-liners with multiple nested {} don't cleanly replace, so comment those lines
    # since we are doing traits anyway.. dont need those lines
    # comment_nested_multiline = re.sub(r"\n(\s)(?=((.*:){2,4}))", '\n#', remove_extralines)
    # leftover_multiline_comment = re.sub('#{2,}', '', comment_nested_multiline)
    comment_out_variables = re.sub(r"\@", 'var_', remove_extralines)  # YAML doesn't like the @ symbol

    # Sometimes a traits file begins with a variable definition. Nuke it.
    nuke_variable_definitions = re.sub(
        "(var_\w*: ((-){0,}\d{1,}.{0,}\d{1,}))", '', comment_out_variables
    )
    # Carefully go through leader_class definitions
    structured_leader_class_lists3 = convert_leader_class_definitions_to_lists(nuke_variable_definitions, 3)
    structured_leader_class_lists2 = convert_leader_class_definitions_to_lists(structured_leader_class_lists3, 2)
    structured_leader_class_lists = convert_leader_class_definitions_to_lists(structured_leader_class_lists2)

    # Take care of repeated has_trait keys >:o
    tidy_subclass_has_trait_duplicates_2 = concatenate_multiline_has_trait_definitions(
        structured_leader_class_lists, min_occurrences=2)
    tidy_subclass_has_trait_duplicates = concatenate_multiline_has_trait_definitions(
        tidy_subclass_has_trait_duplicates_2, min_occurrences=1)

    # Also need to comment out "inline_script = paragon" because PDX are using duplicate keys AGAIN >_<
    # comment_out_inline_scripts = comment_nested_multiline = re.sub(r"\n(\s)(?=((inline_script: \w){2,}))", '\n#', tidy_subclass_has_trait_duplicates)
    # Hello rogue operators
    replace_greater_than = re.sub(r" > ", ': greater_than_', tidy_subclass_has_trait_duplicates)
    # Make your time
    replace_less_than = re.sub(r" < ", ": less_than_", replace_greater_than)
    converts_equals_to_colon = re.sub(r"\s{0,}=", ":", replace_less_than)
    return converts_equals_to_colon

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
        line_with_structured_data = f"{parts[0]}: {str(classes_as_list)}"
        # oh the horror
        input_string_copy = re.sub(complete_line, line_with_structured_data, input_string_copy)
    return input_string_copy

def concatenate_multiline_has_trait_definitions(input_string, min_occurrences: int=1):
    """ PDX put multiple lines with the same key definition, so we have to deal with that """
    multiple_has_trait_lines = re.compile(r"((\s*has_trait: subclass\w*\n){" + f"{min_occurrences}" + r",})")
    # multiple_has_trait_lines = re.compile(r"((\s*has_trait: subclass\w*\n){1,})")
    results = re.findall(multiple_has_trait_lines, input_string)
    input_string_copy = copy(input_string)
    for result in results:
        """
        It's going to be one big string starting with \n
        """
        # breakpoint()
        complete_line = result[0]
        pieces = result[0].split('\n')
        indendation = result[0].split('has_trait')[0]
        subclasses = [ piece.strip() for piece in result[0].split('has_trait: ')[1:] ]
        # indentation = result[0].split('has_trait: ')[0].count(' ')
        substitution = f"{indendation}has_subclass_trait: {subclasses}\n"
        input_string_copy = re.sub(complete_line, substitution, input_string_copy)
    return input_string_copy

def make_newlines_for_multiple_assignments(input_string):
    """ convert instances of = { to \\s\\n """
    # multiple_assignments_re = re.compile(r"(^\s*(?:\w* = {){1,}.*)")
    multiple_assignments_re = re.compile(r"(\s*(?:\w* = {).* = .*)")
    # ' = { ' but allow for errors in spacing
    # assignment_block = re.compile(r"\s{0,}=\s{0,}\{\s{0,}")
    results = re.findall(multiple_assignments_re, input_string)
    # breakpoint()
    input_string_copy = copy(input_string)
    for result in results:
        # Do operations on the complete line, goign to split this
        complete_line = copy(result)
        # Capture what the initial indent is bc we have to indent add'l lines
        num_tab_indents = complete_line.count('\t')
        existing_indendation = '\t' * num_tab_indents
        # pieces = re.split(assignment_block, complete_line)
        # ['\n\tNOT', 'has_trait_tier1or2', 'TRAIT = leader_trait_eager } }']
        pieces = complete_line.split(' = { ')
        # Clean up all pieces but the first assignment
        new_pieces = [
            piece.replace('{','').replace('}','')
            for piece in pieces[1:]
        ]
        reconstructed_line = [pieces[0]]
        # Starting with the 2nd depth
        for key_definition in new_pieces:
            new_indentation = "\t" * (new_pieces.index(key_definition)+1)
            reconstructed_line.append(
                f"{existing_indendation}{new_indentation}{key_definition.strip()}"
            )
        # reconstructed_line.append(new_pieces[-1])
        substitution = ":\n".join(reconstructed_line)
        # breakpoint()
        input_string_copy = re.sub(complete_line, substitution, input_string_copy)
    return input_string_copy

# def fix_replace_traits_no_spacing(input_string):
#     # Placed higher up in the substitution queue
#     list_assignments_with_no_spaces = re.compile(
#         r"(\s*replace_traits = \{(\w*)\})"
#     )
#     results = re.findall(list_assignments_with_no_spaces, input_string)
#     input_string_copy = copy(input_string)
#     for result in results:
#         complete_line = result[0]
#         trait_to_replace = result[1]
#         indentation = complete_line.count("\t")*"  " 
#         replacement = f"\n{indentation}replace_traits: {trait_to_replace}"
#         input_string_copy = re.sub(complete_line, replacement, input_string_copy)
#     return input_string_copy

def validate_chopped_up_data(buffer):
    try:
        _ = safe_load(buffer)
    except Exception as ex:
        sys.exit(f"There was a problem validating the YAML after chopping up the Stellaris script: {ex}")

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
    sys.stdout.write('0xRetro Stellaris script chopper.. spinning up blades...\n')
    with open(args.infile, "r") as infile:
        buffer = convert_stellaris_script_to_standard_yaml(
            infile.read()
        )
        validate_chopped_up_data(buffer)
        if args.outfile:
            with open(args.outfile, 'w') as outfile:
                outfile.write(buffer)
        else:
            print(buffer)
        print("Done. There's a high change this finished correctly.")
        sys.exit()
