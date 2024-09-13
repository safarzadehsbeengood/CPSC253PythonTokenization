# Author: Ryan Safarzadeh
# Input: a python file
# Output: Categories and Tokens -> dict<str: list<str>>
# ********************************************************
# Example usage: python3 tokenization.py [filepath]

# --------------------
# # Example comment
# def add(a, b):
#     result = a + b
#     return result
#
# print(add(5, 3))
# --------------------

import sys
from categories import DELIMITERS, OPERATORS, KEYWORDS

NEWLINE_OR_SPACE_OR_DELIMITER = "\n " + ''.join(DELIMITERS)

class Tokens:
    keywords = []
    identifiers = []
    operators = []
    delimiters = []
    literals = []
    
    def asMap(self):
        return {
            "keywords": self.keywords,
            "identifiers": self.identifiers,
            "operators": self.operators,
            "delimiters": self.delimiters,
            "literals": self.literals
        }
        
    def print(self):
        for label, tokens in self.asMap().items():
            print(f'{label}: {tokens}')
    
masterTokens = Tokens()

def tokenize_line(s: str):

    def find_next(start: int, target: str):
        '''
        Returns the index of the first character found 
        in any character of target.
        '''
        pos = start
        while pos < len(s):
            if s[pos] in target:
                return pos
            pos += 1
        return None
        
    curr = 0

    while curr < len(s):
        # if we encounter a space, we can skip
        if s[curr] == ' ':
            # print("SPACE")
            curr += 1
            continue
        
        # if we encounter a pound, the rest of the line is a comment and we can ignore it
        if s[curr] == '#':
            break
        
        # if we encounter a delimiter, we can just add it
        if s[curr] in DELIMITERS:
            masterTokens.delimiters.append(s[curr])
            curr += 1
        
        # if we encounter a numeric literal, find the next space or delimiter
        elif s[curr].isnumeric():
            # print("NUMBER LITERAL")
            # find the next newline, space, or delimiter
            next_char = find_next(curr, NEWLINE_OR_SPACE_OR_DELIMITER)
            if next_char is None:
                masterTokens.literals.append(s[curr:])
                curr = len(s)
            else:
                masterTokens.literals.append(s[curr:next_char])
                curr = next_char
            
        # if we encounter a string literal, find the next matching quote
        elif s[curr] == '"' or s[curr] == "'":
            # print("STRING LITERAL")
            next_quote = find_next(curr+1, ('"' if s[curr] == '"' else "'"))
            if next_quote is None:
                masterTokens.literals.append(s[curr:])
                curr = len(s)
            else:
                masterTokens.literals.append(s[curr:next_quote+1])
                curr = next_quote + 1
                
        # if we encounter an operator, we can just add it.
        elif s[curr] in OPERATORS:
            # print("OPERATOR")
            if s[curr:curr+1] in OPERATORS:
                masterTokens.operators.append(s[curr:curr+1])
                curr += 2
            else:
                masterTokens.operators.append(s[curr])
                curr += 1
        
        # for identifiers and keywords, we can check first if it's a keyword; if not, it's an identifier
        else:
            # print("KEYWORD OR IDENTIFIER")
            end_of_token = find_next(curr, NEWLINE_OR_SPACE_OR_DELIMITER)
            # special case for EOL
            if end_of_token is None:
                if s[curr:] in KEYWORDS:
                    masterTokens.keywords.append(s[curr:])
                else:
                    masterTokens.identifiers.append(s[curr:])
                curr = len(s)
                continue
            if s[curr:end_of_token] in KEYWORDS:
                masterTokens.keywords.append(s[curr:end_of_token])
            else:
                masterTokens.identifiers.append(s[curr:end_of_token])
            curr = end_of_token

# commandline parsing
if len(sys.argv) < 2 or len(sys.argv) > 2:
    print("[tokenization.py] -> Error: ")
    sys.exit("\tExample usage: python3 tokenize.py [filepath]")

# file parsing
with open(sys.argv[1], 'r') as file:
    original_text = file.read()
    print(f'\nCode: \n{"*"*40}\n{original_text}\n{"*"*40}\n')
    file.seek(0)
    lines = [' '.join(line.strip().split()) for line in file.read().split('\n') if (line != '' and not line[0] == '#')]
    for line in lines:
        tokenize_line(line)
    masterTokens.print()
