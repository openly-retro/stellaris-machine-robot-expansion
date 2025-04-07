import re
from json import loads
from json.decoder import JSONDecodeError
import sys

"""
Larger challenges:
- separating multiple blocks on the same line
- concatenating lists where items are individually on subsequent lines
- Preserving the order of effects (not an issue in traits files)
"""

""" Regex Patterns """
re_statement_left_side = re.compile(r"^\s{0,}(?P<assignee>\w*)\s{0,}=")
re_parse_list_assignment = re.compile(
    r"(?P<assignee>\w*) = {(?P<items>.*)}"
)
re_parse_simple_assignment = re.compile(
    r"(\w*) (?P<operand>[=|<|>|<=|>=]) (\w*)"
)
re_indendation = re.compile(r"^(?P<indent>\s*)")
re_block_open = re.compile(r"^(?P<indent>\s{0,})(?P<name>\w*) = {$")
re_single_word_line = re.compile(r"^\s{0,}(\w*){1}[ ]{0,}$")
re_code_block_open = re.compile(r"\s=\s{1,}\{")

# Use re.sub and give it a function that quotes a string,
# in order to quote all words in the text blob
re_nonnumber_words = re.compile(r"([a-zA-Z_\/]+)")
# unquote "no" and "yes" afterwards
re_detect_crunched_list = re.compile(r"(\w*): \[")

re_multiline_list = re.compile(
    r"(?P<blockname>\w*)\s{1,}=\s{1,}{(?P<words>((?:\n\s{0,})(\w*)){1,})\s{1,}}",
    re.MULTILINE
)
# re_simple_word = re.compile(r"\b(([\@a-zA-Z_\/]{2,}))\b")
re_simple_word = re.compile(r"([\@\/\._a-zA-Z0-9]+)")

COMMA = ','
EMPTY_LINE = ''

""" Code """
def clean_up_line(line: str) -> str:
    """ Handle a variety of line contents
    This is the main method that crunches any given line from a traits file
    """

    # Wipe out any comments
    if '#' in line:
        line = scrub_comments_from_line(line)
    # Spaces over tabs
    line.replace("\t", " ")

    line_opens_block = '= {' in line
    # ignore multiple blocks on same line
    if line_opens_block and line.count('{') > 1:
        # raise MultipleBlocksSameLine(f"ergg --> {line}")
        return format_multiple_assignment_single_line(line)
    # list values
    elif line_opens_block and line.count('=') == 1 and line.strip().endswith('}'):
        return normalize_list(line)
    # a line that's just one block
    elif line.count('{') == 1 and line.strip().endswith('}'):
        return handle_single_block_assignment(line)

    elif block_open_detected := re.match(re_block_open, line):
        return block_open_to_json(block_open_detected)
    elif len(line.strip().split(' ')) == 3:
        if line_has_math_comparison(line):
            return judo_chop_operators_into_strings(line)
        elif '|' in line:
            return preserve_script_value_refs(line)
        else:
            return convert_simple_assignment(line)
    elif line.strip() == '}':
        # Add comma
        return line + COMMA
    elif single_word_result := re.match(re_single_word_line, line):
        # If it's just one line, return that line ...
        return line
    # Don't munge a list that we crunched already
    elif list_detected := re.search(re_detect_crunched_list, line):
        return line
    elif line.strip() == '':
        # Pass whitespace, deal with it later
        return line
    else:
        raise WhatInTheShroud(line)

def block_open_to_json(re_results: re.Match) -> str:
    return f"{re_results.group('indent')}\"{re_results.group('name')}\": {{"

def convert_block_open(line) -> str:
    # To be run on a single line only
    quoted = re.sub(re_simple_word, quote_word, line)
    return quoted.replace(
        ' = {',
        ': {'
    )

def handle_single_block_assignment(line) -> str:
    # something like 'potential = { is_councilor = no }'
    cleaned_equals = re.sub(
        r"\s{1,}=\s{1,}",
        ': ',
        line
    )
    quoted = re.sub(re_simple_word, quote_word, cleaned_equals)

    # Check for integers as keys
    # ┻━┻ ︵ヽ(`Д´)ﾉ︵ ┻━┻
    first_word = line.strip().split(' ')[0]
    if first_word.isnumeric():

        quoted = quoted.replace(
            f"{first_word}:",
            f'"{first_word}":'
        )
    return quoted  + COMMA

def normalize_list(line) -> str:
    # leader_class = { word word word } into leader_class
    parsed = re.search(re_parse_list_assignment, line)
    indent = re.match(re_indendation, line).group("indent")

    items = parsed.group("items").strip().split(' ')

    if not '"' in str(items):
        # items = str(items)
        items = str(items).replace('\'','"')
    return f"{indent}\"{parsed.group('assignee')}\": {items}" + COMMA

def convert_simple_assignment(line) -> str:
    # But does it have math operators???
    quoted = re.sub(re_simple_word, quote_word, line)
    return quoted.replace(' =',':') + COMMA

def line_has_math_comparison(line):
    return '>' in line or '<' in line

def judo_chop_operators_into_strings(line):
    string_oper = None
    if '<' in line:
        string_oper = 'lt'
    elif '>' in line:
        string_oper = 'gt'
    if '=' in line:
        string_oper += 'e'
    line_parts = line.strip().split(' ')
    math_eval = f"{string_oper}_{line_parts[-1]}"
    reduced_line = f"\"{line_parts[0]}\": \"{math_eval}\","
    return reduced_line

def preserve_script_value_refs(line):
    parts = line.strip().split('=')
    effect = parts[0].strip()
    value = parts[1].strip()
    return f"\"{effect}\": \"{value}\","

def scrub_comments_from_line(line) -> str:
    # Have already done the check for '#' outside of this method
    line_parts = line.split('#')
    # doesn't matter if this is whitespace, we can't return None
    # return to the left of the comment, minus whitespace on the right side of that part
    return line_parts[0].rstrip()

def quote_word(word_match: str):
    try:
        float(word_match.group(0))
    except Exception as ex:
        # Not a floating point number, is a string
        return f"\"{word_match.group(0)}\""
    else:
        return word_match.group(0)

def to_json(lines):
    """ Iterate some lines and pray to the Shroud to convert to JSON """
    pass

def search_blob_crunch_lists(blob: str) -> str:
    crunched = ''
    if results := re.search(
        re_multiline_list,
        blob,
    ):
        crunched = re.sub(
            re_multiline_list,
            compress_list_result_from_search,
            blob
        )

    return crunched or blob

def compress_list_result_from_search(search_results) -> str:
    # given the "words" group, chew it
    words_raw = search_results.group("words")
    words_list = words_raw.strip().split("\n")
    cleaned_words = [ word.strip() for word in words_list ]
    list_with_json_quotes = str(cleaned_words).replace('\'','"')

    return f"\"{search_results.group('blockname')}\": {list_with_json_quotes},"

def iter_clean_up_lines(lines: list[str]) -> str:
    """ Iterate lines and return JSON as text in a single blob """
    processed_lines = []
    for line in lines:

        processed_lines.append(clean_up_line(line).strip())
    
    return " ".join(processed_lines)

def convert_iter_lines_to_dict(json_as_str: str) -> dict:
    # Take output of iter_clean_up_lines into dict
    # Check out this fun (:
    remove_extra_commas = json_as_str.replace(
        ', }',
        '}'
    ).replace(',}','}').strip().replace('""', '"').replace('\\','').rstrip(
        ','
    ).replace(
        ',,',','
    ).replace(
        '\'"', '"'
    ).replace(
        '"\'', '"'
    )

    try:
        results_as_json = loads(
            f"{{ {remove_extra_commas} }}"
        )
    except JSONDecodeError as exc:
        print(f"ERROR: {str(exc)}")
        print("**** DUMP OBJECT ****")
        # print(f"{{ {remove_extra_commas} }}")
        print("**********")
        err_range = remove_extra_commas[exc.colno-20:exc.colno+20]
        print(
            "Range: \n"
            f"{err_range}"
        )
        print(f"ERROR: {str(exc)}")
        sys.exit(1)

    return results_as_json

def format_multiple_assignment_single_line(naughty_line: str) -> str:
    """ Basically just quote words and add commas after closing braces,
    since JSON can parse goofy whitespace patterns  """
    open_braces_cleaned = re.sub(
        r"\s{1,}=\s{1,}",
        ": ",
        naughty_line
    )
    quoted = re.sub(r"\b\w{2,}\b", quote_word, open_braces_cleaned)
    return quoted + COMMA

# TODO: make this more memory efficient
# use a generator or something
# sucks we gotta crunch the file for lists then iterate over lines
def input_cz_output_json(file_contents: str) -> dict:
    contents = search_blob_crunch_lists(file_contents)
    processed_lines = []
    for line in contents.split("\n"):
        processed_lines.append(clean_up_line(line).strip())
    del contents
    cleaned_blob = " ".join(processed_lines)
    del processed_lines
    return convert_iter_lines_to_dict(cleaned_blob)
    del cleaned_blob


""" Exception Classes """
class MultipleBlocksSameLine(Exception):
    pass

class WhatInTheShroud(Exception):
    pass
