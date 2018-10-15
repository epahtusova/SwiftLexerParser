import lexer, yacc
from preprocess_comments import format_inline_comment, format_multiline_comment

file = open('in.txt', 'r', encoding='utf8')
data = file.read()
data = format_multiline_comment(data)
data = format_inline_comment(data)

ast = yacc.parse(data)