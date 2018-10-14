import ply.yacc as yacc
import lexer


tokens = lexer.tokens


def p_translation_unit(p):
    'translation-unit  :  statement*'

def p_statement(p):
    """
    statement  :  ';'
                | new-type-defn
                | global-const-defn
                | import-stmt
                | pragma-stmt
                | func-defn
                | block
                | if-stmt
                | switch-stmt
                | wait-stmt
                | foreach-loop
                | for-loop
                | iterate-loop
                | stmt-chain
                | update-stmt
    """

def p_new_type_defn(p):
    """
    new-type-defn  :  'type' type-name '{' (var-decl ';') * '}' (new struct or subtype)
                    | 'type' type-name standalone-type ';'
                    | 'typedef' type-name standalone-type ';'
    """

def p_global_const_defn(p):
    """
    global-const-defn  :  'global' 'const' var-decl ';'
    """

def p_import_stmt(p):
    """
    import-stmt  :  'import' module-path ';'
                  | 'import' string-literal ';'
    """

def p_module_path(p):
    """
    module-path  :  id ('.' id>)*
    """

def p_pragma_stms(p):
    """
    pragma-stmt  :  'pragma' id expr  ';'
    """
