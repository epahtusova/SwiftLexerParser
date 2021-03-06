import ply.lex as lex
from preprocess_comments import format_inline_comment, format_multiline_comment

reserved = {
    # DECLARATIONS
    'associatedtype': 'D_ASSOCIATED_TYPE',
    'deinit': 'D_DEINIT',
    'enum': 'D_ENUM',
    'extension': 'D_EXTENSION',
    'fileprivate': 'D_FILE_PRIVATE',
    'func': 'D_FUNCTION',
    'import': 'D_IMPORT',
    'init': 'D_INIT',
    'inout': 'D_INOUT',
    'let': 'D_LET',
    'operator': 'D_OPERATOR',
    'private': 'D_PRIVATE',
    'protocol': 'D_PROTOCOL',
    'public': 'D_PUBLIC',
    'static': 'D_STATIC',
    'struct': 'D_STRUCT',
    'subscript': 'D_SUBSCRIPT',
    'typealias': 'D_TYPE_ALIAS',
    'var': 'D_VAR',
    # STATEMENTS
    'break': 'S_BREAK',
    'case': 'S_CASE',
    'continue': 'S_CONTINUE',
    'default': 'S_DEFAULT',
    'defer': 'S_DEFER',
    'do': 'S_DO',
    'else': 'S_ELSE',
    'fallthrough': 'S_FALLTHROUGH',
    'for': 'S_FOR',
    'foreach': 'S_FOREACH',
    'guard': 'S_GUARD',
    'if': 'S_IF',
    'in': 'S_IN',
    'repeat': 'S_REPEAT',
    'return': 'S_RETURN',
    'switch': 'S_SWITCH',
    'where': 'S_WHERE',
    'while': 'S_WHILE',
    'until': 'S_UNTIL',
    'iterate': 'S_ITERATE',
    # EXPRESSIONS
    'as': 'E_AS',
    'Any': 'E_ANY',
    'catch': 'E_CATCH',
    'false': 'E_FALSE',
    'true': 'E_TRUE',
    'try': 'E_TRY',
    'is': 'E_IS',
    'nil': 'E_NIL',
    'rethrows': 'E_RETHROWS',
    'super': 'E_SUPER',
    'self': 'E_SELF',
    'Self': 'E_SELF_CAPITAL',
    'throw': 'E_THROW',
    'throws': 'E_THROWS',
    'wait': 'E_WAIT',
    'stdin': 'E_STDIN',
    'stdout': 'E_STDOUT',
    'stderr': 'E_STDERR',
    'deep': 'E_DEEP',
    # PATTERNS
    '_': 'P_UNDERSCORE',
    # KEYWORD WITH A NUMBER SIGN
    '#available': 'N_AVAILABLE',
    '#colorLiteral': 'N_COLOR_LITERAL',
    '#column': 'N_COLUMN',
    '#else': 'N_ELSE',
    '#elseif': 'N_ELSE_IF',
    '#endif': 'N_END_IF',
    '#error': 'N_ERROR',
    '#file': 'N_FILE',
    '#fileLiteral': 'N_FILE_LITERAL',
    '#function': 'N_FUNCTION',
    '#if': 'N_IF',
    '#imageLiteral': 'N_IMAGE_LITERAL',
    '#line': 'N_LINE',
    '#selector': 'N_SELECTOR',
    '#sourceLocation': 'N_SOURCE_LOCATION',
    '#warning': 'N_WARNING',
    # KEYWORDS RESERVED IN PARTICULAR CONTEXTS
    'associativity': 'C_ASSOCIATIVITY',
    'convenience': 'C_CONVENIENCE',
    'dynamic': 'C_DYNAMIC',
    'didSet': 'C_DID_SET',
    'final': 'C_FINAL',
    'get': 'C_GET',
    'infix': 'C_INFIX',
    'indirect': 'C_INDIRECT',
    'lazy': 'C_LAZY',
    'left': 'C_LEFT',
    'mutating': 'C_MUTATING',
    'none': 'C_NONE',
    'nonmutating': 'C_NONMUTATING',
    'optional': 'C_OPTIONAL',
    'override': 'C_OVERRIDE',
    'postfix': 'C_POSTFIX',
    'precedence': 'C_PRECEDENCE',
    'prefix': 'C_PREFIX',
    'Protocol': 'C_PROTOCOL',
    'required': 'C_REQUIRED',
    'right': 'C_RIGHT',
    'global': 'C_GLOBAL',
    'const': 'C_CONST',
    'Type': 'C_TYPE',
    'typedef': 'C_TYPEDEF',
    'pragma': 'C_PRAGMA',
    'set': 'C_SET',
    'app': 'C_APP',
    'unowned': 'C_UNOWNED',
    'weak': 'C_WEAK',
    'willSet': 'C_WILLSET',
    # Default classes
    'Int': 'class_INT',
    'Double': 'class_DOUBLE',
    'Float': 'class_FLOAT',
    'Void': 'class_VOID',
    'UInt': 'class_UINT',
    'Bool': 'class_BOOL',
    'Character': 'class_CHARACTER',
    'String': 'class_String',
    # Collections
    'Set': 'collection_SET',
    'Array': 'collection_ARRAY',
    'Dictionary': 'collection_DICT',

}

tokens = [
             'ID', 'INT', 'DOUBLE', 'ASSIGN', 'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD', 'GREATER', 'GREATER_EQ', 'LESS',
             'LESS_EQ', 'EQUAL', 'NOT_EQUAL', 'MULT_AS', 'MINUS_AS', 'PLUS_AS', 'DIV_AS', 'MOD_AS', 'LPAREN', 'RPAREN',
             'LBRACE', 'RBRACE', 'RBRACKET', 'LBRACKET', 'DOT', 'COMMA', 'COLON', 'SEMICOLON', 'AT', 'HASH',
             'AMPERSAND', 'BIT_OR', 'BIT_XOR', 'BIT_NOT', 'LSHIFT', 'RSHIFT', 'RANGE', 'HRANGE', 'ARROW', 'BACKTICK',
             'QUESTION', 'EXCLAMATION', 'LOG_AND', 'LOG_OR', 'INF', 'NAN', 'MULTPER', 'DOUBLEPER', 'UPD', 'STR_LITERAL',
             'MUL_STR_LITERAL'
         ] + list(reserved.values())
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_MULTPER = r'%/'
t_DOUBLEPER = r'%%'
t_DIV = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_DOT = r'\.'
t_COMMA = r','
t_COLON = r':'
t_SEMICOLON = r';'
t_ASSIGN = r'='
t_AT = r'@'
t_HASH = r'\#'
t_AMPERSAND = r'\&'
t_BIT_NOT = r'\~'
t_BIT_OR = r'\|'
t_BIT_XOR = r'\^'
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_RANGE = r'\.\.\.'
t_HRANGE = r'\.\.<'
t_ARROW = r'\->'
t_BACKTICK = r'`'
t_QUESTION = r'\?'
t_EXCLAMATION = r'!'
t_LOG_AND = r'\&\&'
t_LOG_OR = r'\|\|'
t_MOD = r'%'
t_GREATER = r'>'
t_GREATER_EQ = r'>='
t_LESS = r'<'
t_LESS_EQ = r'<='
t_EQUAL = r'=='
t_NOT_EQUAL = r'!='
t_MULT_AS = r'\*='
t_MINUS_AS = r'-='
t_PLUS_AS = r'\+='
t_DIV_AS = r'/='
t_MOD_AS = r'%='
t_INF = r'inf'
t_NAN = r'nan'
t_UPD = r':='


def t_ID(t):
    r'[#]?[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


def t_MUL_STR_LITERAL(t):
    r'"""([^"\n]|(\\")|\n)*"""'
    return t


def t_STR_LITERAL(t):
    r'"([^"\n]|(\\"))*"'
    return t


def t_DOUBLE(t):
    r'[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Ignored characters
t_ignore = " \t\r"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex(debug=0)


def tokenize():
    # Give the lexer some input
    file = open('in.txt', 'r', encoding='utf8')
    data = file.read()
    data = format_multiline_comment(data)
    data = format_inline_comment(data)
    lexer.input(data)
    return lexer



# tokenize()
