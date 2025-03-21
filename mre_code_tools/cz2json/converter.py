import re
from json import loads

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

# Use re.sub and give it a function that quotes a string,
# in order to quote all words in the text blob
re_nonnumber_words = re.compile(r"([a-zA-Z_\/]+)")
# unquote "no" and "yes" afterwards
re_detect_crunched_list = re.compile(r"(\w*): \[")

re_multiline_list = re.compile(
    r"(?P<blockname>\w*) = {(?P<words>((?:\n\s{0,})(\w*)){1,})\s{1,}}",
    re.MULTILINE
)
re_simple_word = re.compile(r"\b(([a-zA-Z_\/]{2,}))\b")

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

    line_opens_block = '= {' in line
    # ignore multiple blocks on same line
    if line_opens_block and line.count('{') > 1:
        raise MultipleBlocksSameLine(f"ergg --> {line}")
    # list values
    elif line_opens_block and line.strip().endswith('}'):
        return normalize_list(line)
    # beginning of block

    elif re_re_block_open := re.match(re_block_open, line):
        return block_open_to_json(re_re_block_open)
    elif len(line.strip().split(' ')) == 3:
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
    quoted = re.sub(
        re_simple_word,
        quote_word,
        line
    )
    return quoted.replace(
        ' = {',
        ': {'
    )

def normalize_list(line) -> str:
    # leader_class = { word word word } into leader_class
    parsed = re.search(re_parse_list_assignment, line)
    indent = re.match(re_indendation, line).group("indent")
    items = parsed.group("items").strip().split(' ')
    return f"{indent}\"{parsed.group('assignee')}\": {items}" + COMMA

def convert_simple_assignment(line) -> str:
    quoted = re.sub(
        re_simple_word,
        quote_word,
        line
    )
    return quoted.replace(' =',':') + COMMA

def scrub_comments_from_line(line) -> str:
    # Have already done the check for '#' outside of this method
    line_parts = line.split('#')
    # doesn't matter if this is whitespace, we can't return None
    # return to the left of the comment, minus whitespace on the right side of that part
    return line_parts[0].rstrip()

def quote_word(word_match: str):
    return f"\"{word_match.group(0)}\""

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

    return f"\"{search_results.group('blockname')}\": {str(cleaned_words)},"

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
    ).replace(',}','}').strip()
    return loads(f"{{{remove_extra_commas.rstrip(',')}}}")

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
