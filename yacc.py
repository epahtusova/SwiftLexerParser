import ply.yacc as yacc
import lexer


tokens = lexer.tokens


def p_translation_unit(p):
    """
    translation-unit  :  statement-star
    """

def p_statement_star(p):
    """
    statement-star  :
                    | statement statement-star
    """

def p_statement(p):
    """
    statement  :  t_SEMICOLON
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

def p_global_const_defn(p):
    """
    global-const-defn  :  C_GLOBAL C_CONST var-decl t_SEMICOLON
    """
    p[0] = ('GLOBAL_CONSTANT', p[3])

def p_import_stmt(p):
    """
    import-stmt  :  D_IMPORT module-path t_SEMICOLON
                 | D_IMPORT t_STR_LITERAL t_SEMICOLON
    """
    p[0] = ('IMPORT', p[2])

def p_module_path(p):
    """
    module-path  :  t_ID path-star
    """
    p[0] = ('MODULE_PATH', tuple(p[1]))

def p_path_star(p):
    """
    path-star   :
                | t_DOT t_ID path-star
    """
    if p[1] != '':
        p[0] = ('PATH', p[2], tuple(p[3]))
    else:
        p[0] = p[1]

def p_pragma_stms(p):
    """
    pragma-stmt  :  C_PRAGMA t_ID expr  t_SEMICOLON
    """
    p[0] = ('PRAGMA', p[2], p[3])

def p_func_defn(p):
    """
    func-defn  :  swift-func-defn
                | app-func-defn
                | foreign-func-defn
    """
    p[0] = p[1]

def p_func_hdr(p):
    """
    func-hdr  :  type-params formal-arg-list func-name ( | formal-arg-list)
    """
    if p[4] != '':
        p[0] = (p[3], p[4], p[1], p[2])
    else:
        p[0] = (p[3], p[1], p[2])

def p_type_params(p):
    """
    type-params  :
                 | t_LESS var-name comma-name-star t_GREATER
    """
    if p[1] != '':
        p[0] = ('NAME', p[2], tuple(p[3]))
    else:
        p[0] = p[1]

def p_comma_name_star(p):
    """
    comma-name-star :
                    | t_COMMA var-name comma-name-star
    """
    if p[1] != '':
        p[0] = ('NAME', p[2], tuple(p[3]))
    else:
        p[0] = p[1]

def p_formal_arg_list(p):
    """
    formal-arg-list  :
                     | t_LPAREN ((formal-arg comma-args-star) | )  t_RPAREN
    """
    if p[1] != '':
        p[0] = ('ARGS', tuple(p[2]))
    else:
        p[0] = p[1]

def p_comma_args_star(p):
    """
    comma-args-star :
                    |    t_COMMA formal-arg comma-args-star
    """
    if p[1] != '':
        p[0] = ('ARGS', p[2], tuple(p[3]))
    else:
        p[0] = p[1]

def p_formal_arg(p):
    """
    formal-arg  :  type-prefix (  | t_RANGE) var-name type-suffix ( | (t_ASSIGN expr))
    """
    range_ = ''
    assign = ''
    if p[2] != '': range_ = p[2]
    if p[5] != '': assign = ('ASSIGN', p[5])
    p[0] = ('ARG', p[1], p[3], p[4], range_, assign)

def p_swift_func_defn(p):
    """
    swift-func-defn  :  annotation-star func-hdr t_ARROW block
    """
    p[0] = (p[2], tuple(p[1]), p[4])
    
def p_annotation_star(p):
    """
    annotation-star :   
                    |   annotation annotation-star 
    """
    if p[1] != '':
        p[0] = ('ANNOTATION', p[1])
    else:
        p[0] = p[1]

def p_app_func_defn(p):
    """
    app-func-defn  :  annotation-star C_APP func-hdr t_LBRACE app-body t_RBRACE
    """
    p[0] = ('APP', p[3], p[5])


def p_app_body(p):
    """
    app-body  :  app-arg-expr app-arg-expr-star app-out-star ( | t_SEMICOLON)
    """
    p[0] = ('BODY', p[1], tuple(p[2]), tuple(p[3]), p[4])


def p_app_out_star(p):
    """
    app-out-star    :
                    | (E_STDIN | E_STDOUT | E_STDERR) t_ASSIGN expr app-out-star
    """
    if p[1] != '':
        p[0] = ('APP_OUT', (p[2], p[1], p[3]), tuple(p[4]))
    else:
        p[0] = p[1]

def p_app_arg_expr_star(p):
    """
    app-arg-expr-star   :
                        | app-arg-expr app-arg-expr-star
    """
    if p[1] != '':
        p[0] = ('APP_ARG_EXPRESSION', p[1], tuple(p[2]))
    else:
        p[0] = p[1]


def p_foreign_func_defn(p):
    """
    foreign-func-defn  :  annotation-star func-hdr foreign-func-body
    """
    p[0] = (p[2], p[3], tuple(p[1]))

def p_foreign_func_body(p):
    """
    foreign-func-body  :  t_STR_LITERAL t_STR_LITERAL ( | t_STR_LITERAL) ( | (t_LBRACKET (t_STR_LITERAL | t_MUL_STR_LITERAL) t_RBRACKET))
    """
    p[0] = ('FOREIGN_FUNC', p[1], p[2], p[3], p[4])

def p_var_decl(p):
    """
    var-decl  :  type-prefix var-decl-rest
    """
    p[0] = ('VARS_DEC', p[1], tuple(p[2]))

def p_var_decl_rest_star(p):
    """
    var-decl-rest-star  :
                        | t_COMMA var-decl-rest var-decl-rest-star
    """
    if p[1] != '':
        p[0] = ('VAR_DECL', p[2], tuple(p[3]))
    else:
        p[0] = p[1]

def p_var_decl_rest(p):
    """
    var-decl-rest  :  var-name type-suffix ( | var-mapping) ( | (t_ASSIGN expr))
    """

def p_type_prefix(p):
    """
    type-prefix  :  type-name
                    | param-type
    """

def p_param_type(p):
    """
    param-type  :  type-name t_LESS standalone-type t_GREATER
    """

def p_type_suffix(p):
    """
    type-suffix  :  (t_LBRACKET ( | standalone-type) t_RBRACKET)*
    """

def p_standalone_type(p):
    """
    standalone-type  :  type-prefix type-suffix
    """

def p_var_mapping(p):
    """
    var-mapping  :  t_LESS expr t_GREATER
    """

def p_block(p):
    """
    block  :  t_LBRACE statement * t_RBRACE
    """

def p_stmt_chain(p):
    """
    stmt-chain  :  chainable-stmt (t_SEMICOLON | t_ARROW statement)
    """

def p_chainable_stmt(p):
    """
    chainable-stmt  :  var-name
                      | func-call
                      | var-decl
                      | assignment
    """

def p_assignment(p):
    """
    assignment  :  (lval-list | t_LPAREN lval-list t_RPAREN) (t_ASSIGN | t_PLUS_AS) expr-list
    """

def p_update_stmt(p):
    """
    update-stmt  :  var-name t_LESS t_ID t_GREATER t_UPD expr t_SEMICOLON
    """

def p_if_stmt(p):
    """
    if-stmt  :  IF t_LPAREN expr t_RPAREN block ( | (ELSE block))
    """

def p_switch_stmt(p):
    """
    switch-stmt  :  S_SWITCH t_LPAREN expr t_RPAREN t_LBRACE case * ( | default) t_RBRACE
    """

def p_case(p):
    """
    case  :  S_CASE int-literal t_COLON statement*
    """

def p_default(p):
    """
    default  :  S_DEFAULT t_COLON statement*
    """

def p_wait_stmt(p):
    """
    wait-stmt  :  E_WAIT ( | E_DEEP) t_LPAREN expr-list t_RPAREN block
    """

def p_foreach_loop(p):
    """
    foreach-loop  :  annotation-star S_FOREACH var-name ( | (t_COMMA var-name)) S_IN expr block
    """

def p_for_loop(p):
    """
    for-loop  :  annotation-star S_FOR t_LPAREN for-init-list t_SEMICOLON expr ; for-update-list t_RPAREN block
    """

def p_while_loop(p):
    """
    while-loop  :   annotation WHILE t_LPAREN expr t_RPAREN block
    """

def p_for_init_list(p):
    """
    for-init-list  :  for-init (t_COMMAfor-init)*
    """

def p_for_init(p):
    """
    for-init  :  for-assignment
              | type-prefix var-name type-suffix t_ASSIGN expr
    """

def p_for_update_list(p):
    """
    for-update-list  :  for-assignment (t_COMMA for-assignment)*
    """

def p_for_assignment(p):
    """
    for-assignment  :  var-name t_ASSIGN expr
    """

def p_iterate_loop(p):
    """
    iterate-loop  :  S_ITERATE var-name block S_UNTIL t_LPAREN expr t_RPAREN
    """

def p_expr(p):
    """
    expr  :  or-expr
    """

def p_or_expr(p):
    """
    or-expr  :  and-expr
             | or-expr t_OR and-expr
    """

def p_and_expr(p):
    """
    and-expr  :  eq-expr
              | and-expr t_AND eq-expr
    """

def p_eq_expr(p):
    """
    eq-expr  :  cmp-expr
             | eq-expr (t_EQUAL | t_NOT_EQUAL) eq-expr
    """

def p_cmp_expr(p):
    """
    cmp-expr  :  add-expr
              | cmp-expr (t_LESS | t_ASSIGN | t_GREATER | t_GREATER_EQ) add-expr
    """
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_add_expr(p):
    """
    add-expr  :  mult-expr
              | add-expr (t_PLUS | t_MINUS) mult-expr
    """
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_mult_expr(p):
    """
    mult-expr  :  unary-expr
               | mult-expr (t_MULT | t_DIV | t_MULTPER | t_DOUBLEPER | t_MOD) unary-expr
    """
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_unary_expr(p):
    """
    unary-expr  :  postfix-expr
                  | (t_MINUS | t_EXCLAMATION) postfix-expr
    """
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]

def p_postfix_expr(p):
    """
    postfix-expr  :  base-expr
                  | postfix-expr (array-subscript | struct-subscript)
    """
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]

def p_array_subscript(p):
    """
    array-subscript  :  t_LBRACKET expr t_RBRACKET
    """
    p[0] = p[2]

def p_struct_subscript(p):
    """
    struct-subscript  :  t_DOT t_ID
    """
    p[0] = (p[1], p[2])

def p_base_expr(p):
    """
    base-expr  :  literal
                 | func-call
                 | var-name
                 | t_LPAREN expr t_RPAREN
                 | tuple-constructor
                 | array-constructor
    """
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_func_call(p):
    """
    func-call  :  annotation* func-name t_LPAREN func-call-arg-list t_RPAREN
    """

def p_func_call_arg_list(p):
    """
    func-call-arg-list  :  (expr | kw-expr) (t_COMMA (expr | kw-expr))*
    """

def p_tuple_constructor(p):
    """
    tuple-constructor  :  t_LPAREN expr t_COMMA expr (t_COMMA expr) * t_RPAREN
    """

def p_array_constructor(p):
    """
    array-constructor  :  array-list-constructor
                       | array-range-constructor
                       | array-kv-constructor
    """
    p[0] = p[1]

def p_array_list_constructor(p):
    """
    array-list-constructor  :  t_LBRACKET expr-list? t_RBRACKET
    """

def p_array_range_constructor(p):
    """
    array-range-constructor  :  t_LBRACKET expr t_COLON expr (t_COLON expr)? t_RBRACKET
    """

def p_array_kv_constructor(p):
    """
    array-kv-constructor  :  t_LBRACE (array-kv-elem (t_COMMA array-kv-elem)*)? t_RBRACE
    """

def p_array_kv_elem(p):
    """
    array-kv-elem  :  expr t_COLON expr
    """
    p[0] = (p[2], p[1], p[3])

def p_annotation(p):
    """
    annotation  :  t_AT t_ID | t_AT kw-expr
    """
    p[0] = (p[1], p[2])

def p_kw_expr(p):
    """
    kw-expr  :  t_ID t_ASSIGN expr
    """
    p[0] = (p[2], p[1], p[3])

def p_literal(p):
    """
    literal  :  t_STR_LITERAL
             | t_MUL_STR_LITERAL 
             | int-literal
             | float-literal
             | bool-literal
    """
    p[0] = p[1]

def p_float_literal(p):
    """
    float-literal  :  t_DOUBLE
                     | t_DOUBLE
                     | t_INF
                     | t_NAN
    """
    p[0] = p[1]

def  p_bool_literal(p):
    """
    bool-literal  :  E_TRUE
                  | E_FALSE
    """
    p[0] = p[1]

def p_expr_list(p):
    """
    expr-list  :  expr (t_COMMA expr)*
    """

def p_type_name(p):
    """
    type-name  :  class_INT
               | class_DOUBLE
               | class_FLOAT
               | class_VOID
               | class_UINT
               | class_BOOL
               | class_CHARACTER
               | class_String
               | collection_SET
               | collection_ARRAY
               | collection_DICT
    """
    p[0] = p[1]

def p_const_name(p):
    """
    const-name  :   D_LET t_ID
    """
    p[0] = (p[1], p[2])

def p_var_name(p):
    """
    var-name  :     t_ID
    """
    p[0] = (p[1], p[2])

def p_func_name(p):
    """
    func-name  :  D_FUNCTION t_ID
    """
    p[0] = (p[1], p[2])

def p_lval_list(p):
    """
    lval-list  :  lval-expr (t_COMMA lval-expr)*
    """

def p_lval_expr(p):
    """
    lval-expr  :  var-name (array-subscript | struct-subscript)*
    """

def p_app_arg_expr(p):
    """
    app-arg-expr  :  ( | t_AT) var-name
                    | literal
                    | array-constructor
                    | t_LPAREN expr t_RPAREN
    """
    if len(p) == 3:
        p[0] = ('APP_ARG', p[2], p[1])
    elif len(p) == 4:
        p[0] = ('APP_ARG', p[2])
    else:
        p[0] = p[1]

yacc.yacc()
filename = ''
data = open(filename, 'r').readlines()
