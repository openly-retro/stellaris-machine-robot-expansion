import re
from json import loads
from json.decoder import JSONDecodeError
import sys
import logging

logger = logging.getLogger(__name__)

DEBUG = False

def pdebug(message):
    if DEBUG:
        print(message)

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
re_block_open = re.compile(r"^(?P<indent>\s{0,})(?P<name>\w*) = {\s{0,}$")
re_single_word_line = re.compile(r"^\s{0,}(?P<word>\w*){1}[ ]{0,}$")
re_code_block_open = re.compile(r"\s=\s{1,}\{")

# Use re.sub and give it a function that quotes a string,
# in order to quote all words in the text blob
re_nonnumber_words = re.compile(r"([a-zA-Z_\/]+)")
# unquote "no" and "yes" afterwards
re_detect_crunched_list = re.compile(r"(\w*): \[")

re_multiline_list = re.compile(
    r"(?P<blockname>\w{1,})\s{1,}=\s{1,}{(?P<words>((?:\n\s{0,})(\w{1,})){1,})\s{1,}}",
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

    pdebug(f" + evaluation of : {line}")
    # Wipe out any comments
    if '#' in line:
        line = scrub_comments_from_line(line)
    if line.strip().startswith('#'):
        return ''

    # normalize spaces T_T
    line = line.replace('  =',' =')
    line = line.replace('=  ', '= ')

    result = None
    line_opens_block = '= {' in line
    # ignore multiple blocks on same line
    if line_opens_block and line.count('{') > 1:
        # raise MultipleBlocksSameLine(f"ergg --> {line}")
        result = format_multiple_assignment_single_line(line)
    # list values
    elif line_opens_block and line.count('=') == 1 and line.strip().endswith('}'):
        result = normalize_list(line)
    # a line that's just one block
    elif line.count('{') == 1 and line.strip().endswith('}'):
        result = handle_single_block_assignment(line)
    # a line that's a nicely formatted list we already processed
    # but don't trip over inline math
    # elif line_opens_block and line.count('=') == 1 and line.strip().endswith('{'):

    elif '[' in line and '=' not in line:
        result = line
    elif block_open_detected := re.match(re_block_open, line):
        result = block_open_to_json(block_open_detected)
    elif len(line.strip().split(' ')) == 3:
        if line_has_math_comparison(line):
            result = judo_chop_operators_into_strings(line)
        elif '|' in line or ':' in line:
            result = preserve_script_value_refs(line)
        else:
            result = convert_simple_assignment(line)
    elif line.strip() == '}':
        # Add comma
        result = line + COMMA
    elif single_word_result := re.match(re_single_word_line, line):
        # If it's just one line, return that line ...
        if 'tech_strike_craft_1' in line:
            result = f'"tech": "{single_word_result.group("word")}"'
        else:
            result = single_word_result.group("word")
    # Don't munge a list that we crunched already
    elif list_detected := re.search(re_detect_crunched_list, line):
        result = line
    elif line.strip() == '':
        # Pass whitespace, deal with it later
        result = line
    pdebug(f" - crunched to: {result}")

    if result is None:
        raise WhatInTheShroud(line)
    return result


def block_open_to_json(re_results: re.Match) -> str:
    pdebug(' = block_open_to_json')
    block_name = re_results.group('name')
    return f"{re_results.group('indent')}{(quote_string(block_name))}: {{"

def convert_block_open(line) -> str:
    # To be run on a single line only
    pdebug(' = convert_block_open')
    quoted = re.sub(re_simple_word, quote_word, line)
    return quoted.replace(
        ' = {',
        ': {'
    )

def handle_single_block_assignment(line) -> str:
    # something like 'potential = { is_councilor = no }'
    pdebug(' = handle_single_block_assignment')
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
    return append_comma(quoted)

def normalize_list(line) -> str:
    # leader_class = { word word word } into leader_class
    pdebug(' = normalize_list')
    parsed = re.search(re_parse_list_assignment, line)
    indent = re.match(re_indendation, line).group("indent")

    items = parsed.group("items").strip().split(' ')

    if not '"' in str(items):
        # items = str(items)
        items = str(items).replace('\'','"')
    assignee = parsed.group('assignee')
    formatted_content = f"{indent}{quote_string(assignee)}: {items}"
    return append_comma(formatted_content)


def convert_simple_assignment(line) -> str:
    # But does it have math operators???
    pdebug(' = convert_simple_assignment')
    quoted = re.sub(re_simple_word, quote_word, line)
    # handle yes or no
    if "yes" in quoted or "no" in quoted:
        quoted = quoted.replace(
            "\"yes\"", 'True'
        ).replace(
            "\"no\"", 'False'
        )
    return append_comma(quoted.replace(' =',':'))

def line_has_math_comparison(line):
    return '>' in line or '<' in line

def judo_chop_operators_into_strings(line):
    pdebug(' = judo_chop_operators_into_strings')
    string_oper = None
    if '<' in line:
        string_oper = 'lt'
    elif '>' in line:
        string_oper = 'gt'
    if '=' in line:
        string_oper += 'e'
    line_parts = line.strip().split(' ')
    math_eval = f"{string_oper}_{line_parts[-1]}"
    reduced_line = f"{quote_string(line_parts[0])}: {quote_string(math_eval)}"
    return append_comma(reduced_line)

def preserve_script_value_refs(line):
    pdebug(' = preserve_script_value_refs')
    parts = line.strip().split('=')
    effect = parts[0].strip()
    value = parts[1].strip()
    return f"\"{effect}\": \"{value}\","

def scrub_comments_from_line(line) -> str:
    # Have already done the check for '#' outside of this method
    pdebug(' = scrub_comments_from_line')
    line_parts = line.split('#')
    # doesn't matter if this is whitespace, we can't return None
    # return to the left of the comment, minus whitespace on the right side of that part
    return line_parts[0].rstrip()

def quote_word(word_match: str):
    try:
        float(word_match.group(0))
    except Exception as ex:
        # Not a floating point number, is a string
        return f"{quote_string(word_match.group(0))}"
    else:
        return word_match.group(0)

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
    words_raw = search_results.group("words").replace('\t','')
    # breakpoint()
    words_list = words_raw.strip().split("\n")
    cleaned_words = [ 
        word.strip() for word in words_list
    ]
    list_with_json_quotes = str(cleaned_words).replace('\'','"')

    blockname = search_results.group('blockname')
    contents = f"{quote_string(blockname)}: {list_with_json_quotes}"

    return append_comma(contents)

def iter_clean_up_lines(lines: list[str]) -> str:
    """ Iterate lines and return JSON as text in a single blob """
    processed_lines = []
    for line in lines:
        try:
            next_line = clean_up_line(line)
            if next_line.strip():
                processed_lines.append(clean_up_line(line).strip())
        except Exception as ex:
            sys.exit(
                f"Fell over parsing this line: {line}"
            )
    
    return " ".join(processed_lines)

def turn_prereqs_into_lists() -> str:
    1

def convert_iter_lines_to_dict(json_as_str: str) -> dict:
    # Take output of iter_clean_up_lines into dict
    # Check out this fun (:
    import ast

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
    ).replace('  ',' ')
    cleaned_content = f"{{ {remove_extra_commas} }}"
    # del remove_extra_commas
    # breakpoint()
    try:
        cleaned_content_obj = ast.literal_eval(cleaned_content)
    #  ValueError, TypeError, SyntaxError, MemoryError and RecursionError
    except SyntaxError as exc:
        breakpoint()
        err_range = f"-->{exc.text[exc.offset-60:exc.offset+60]}<--"
        
        print(
            "Range: \n"
            f"{err_range}"
        )
        print(f"ERROR: {str(exc)}")
        with open("err_dump.txt", "w") as err_dump_file:
            err_dump_file.write(cleaned_content)
        print(f"{exc}: dumped to err_dump.txt")
        sys.exit(1)
    except Exception as exc:
        breakpoint()
        print(f"ERROR: {str(exc)}")
        with open("err_dump.txt", "w") as err_dump_file:
            err_dump_file.write(cleaned_content)
        sys.exit(1)

    # try:
    #     results_as_json = loads(cleaned_content)
    # except JSONDecodeError as exc:
    #     pdebug(f"ERROR: {str(exc)}")
    #     pdebug("**** DUMP OBJECT ****")
    #     # pdebug(f"{{ {remove_extra_commas} }}")

    #     pdebug("**********")
    #     # breakpoint()
        # err_range = f"-->{cleaned_content[exc.colno-60:exc.colno+50]}<--"
        # pdebug(
        #     "Range: \n"
        #     f"{err_range}"
        # )
        # pdebug(f"ERROR: {str(exc)}")
    #     sys.exit(1)

    return cleaned_content_obj

def format_multiple_assignment_single_line(naughty_line: str) -> str:
    """ Basically just quote words and add commas after closing braces,
    since JSON can parse goofy whitespace patterns  """
    open_braces_cleaned = re.sub(
        r"\s{1,}=\s{1,}",
        ": ",
        naughty_line
    )
    quoted = re.sub(r"\b\w{2,}\b", quote_word, open_braces_cleaned)
    return append_comma(quoted)


def append_comma(string):
    return string + COMMA

def quote_string(text):
    return f"\"{text}\""

# TODO: make this more memory efficient
# use a generator or something
# sucks we gotta crunch the file for lists then iterate over lines
def input_cz_output_json(file_contents: str) -> dict:
    contents = search_blob_crunch_lists(file_contents)
    processed_lines = []
    for line in contents.split("\n"):
        if line.strip():
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
