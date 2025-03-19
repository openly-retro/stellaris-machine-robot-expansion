import re


# expressions
# line_opens_block
# line is assignment only (no braces)
# line is list assignment

statement_left_side = re.compile(r"^\s{0,}(?P<assignee>\w*)\s{0,}=")
parse_list_assignment = re.compile(
    r"(?P<assignee>\w*) = {(?P<items>.*)}"
)
parse_simple_assignment = re.compile(
    r"(\w*) (?P<operand>[=|<|>|<=|>=]) (\w*)"
)
indentation = re.compile(r"^(?P<indent>\s*)")
block_open = re.compile(r"^(?P<indent>\s{0,})(?P<name>\w*) = {$")
re_single_word_line = re.compile(r"^\s{0,}(\w*){1}[ ]{0,}$")

# Use re.sub and give it a function that quotes a string,
# in order to quote all words in the text blob
nonnumber_words = re.compile(r"([a-zA-Z_\/]+)")
# unquote "no" and "yes" afterwards
detect_crunched_list = re.compile(r"(\w*): ")

re_multiline_list = re.compile(
    r"(?P<blockname>\w*) = {(?P<words>((?:\n\s{0,})(\w*)){1,})\s{1,}}",
    re.MULTILINE
)

def clean_up_line(line: str) -> str:
    """ Handle a variety of line contents """
    # Open a block
    # if line_opens_block := re.match(block_open, line):
    #     return 

    line_opens_block = '= {' in line
    # ignore multiple blocks on same line
    if line_opens_block and line.count('{') > 1:
        raise MultipleBlocksSameLine(f"ergg --> {line}")
    # list values
    elif line_opens_block and line.strip().endswith('}'):
        return normalize_list(line)
    # beginning of block
    # elif line.strip().endswith('= {'):
    #     return convert_block_open(line)
    elif re_block_open := re.match(block_open, line):
        return block_open_to_json(re_block_open)
    elif len(line.strip().split(' ')) == 3:
        return convert_simple_assignment(line)
    elif line.strip() == '}':
        return line
    elif single_word_result := re.match(re_single_word_line, line):
        return line
    # Don't munge a list that we crunched already
    elif list_detected := re.search(detect_crunched_list, line):
        return line
    else:
        raise WhatInTheShroud(line)


def block_open_to_json(re_results: re.Match) -> str:
    return f"{re_results.group('indent')}{re_results.group('name')}: {{"

def convert_block_open(line):
    return line.replace(' = {',': {')

def normalize_list(line):
    # leader_class = { word word word } into leader_class
    parsed = re.search(parse_list_assignment, line)
    indent = re.match(indentation, line).group("indent")
    items = parsed.group("items").strip().split(' ')
    return f"{indent}{parsed.group('assignee')}: {items}"

def convert_simple_assignment(line):
    return line.replace(' =',':')

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
    return crunched

def compress_list_result_from_search(search_results) -> str:
    # given the "words" group, chew it
    words_raw = search_results.group("words")
    words_list = words_raw.strip().split("\n")
    cleaned_words = [ word.strip() for word in words_list ]
    cleaned_words_done = ",".join(cleaned_words)
    return f"{search_results.group('blockname')}: {str(cleaned_words)}"

class CzOneLiner(Exception):
    pass

class MultipleBlocksSameLine(Exception):
    pass

class WhatInTheShroud(Exception):
    pass

