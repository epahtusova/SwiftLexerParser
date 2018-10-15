import ply.yacc as yacc
import lexer

tokens = lexer.tokens


def p_translation_unit(p):
    """
    translation-unit  :  statement-star
    """
    p[0] = tuple(p[1])


def p_statement_star(p):
    """
    statement-star  :
                    | statement statement-star
    """
    if p[1] != '':
        p[0] = (p[1], tuple(p[2]))
    else:
        p[0] = p[1]


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
    p[0] = p[1]


def p_global_const_defn(p):
    """
    global-const-defn  :  C_GLOBAL C_CONST var-decl SEMICOLON
    """
    p[0] = ('GLOBAL_CONSTANT', p[3])


def p_import_stmt(p):
    """
    import-stmt  :  D_IMPORT module-path SEMICOLON
                 | D_IMPORT STR_LITERAL SEMICOLON
    """
    p[0] = ('IMPORT', p[2])


def p_module_path(p):
    """
    module-path  :  ID path-star
    """
    p[0] = ('MODULE_PATH', tuple(p[1]))


def p_path_star(p):
    """
    path-star   :
                | DOT ID path-star
    """
    if p[1] != '':
        p[0] = ('PATH', p[2], tuple(p[3]))
    else:
        p[0] = p[1]


def p_pragma_stms(p):
    """
    pragma-stmt  :  C_PRAGMA ID expr  SEMICOLON
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
    func-hdr  :  type-params formal-arg-list func-name empty-or-arg-list
    """
    if p[4] != '':
        p[0] = (p[3], p[4], p[1], p[2])
    else:
        p[0] = (p[3], p[1], p[2])


def p_empty_or_arg_list(p):
    """
    empty-or-arg-list    :
                         |  formal-arg-list
    """
    p[0] = p[1]


def p_type_params(p):
    """
    type-params  :
                 | LESS var-name comma-name-star GREATER
    """
    if p[1] != '':
        p[0] = ('NAME', p[2], tuple(p[3]))
    else:
        p[0] = p[1]


def p_comma_name_star(p):
    """
    comma-name-star :
                    | COMMA var-name comma-name-star
    """
    if p[1] != '':
        p[0] = ('NAME', p[2], tuple(p[3]))
    else:
        p[0] = p[1]


def p_formal_arg_list(p):
    """
    formal-arg-list  :
                     | LPAREN ((formal-arg comma-args-star) | )  RPAREN
    """
    if p[1] != '':
        p[0] = ('ARGS', tuple(p[2]))
    else:
        p[0] = p[1]


def p_comma_args_star(p):
    """
    comma-args-star :
                    |    COMMA formal-arg comma-args-star
    """
    if p[1] != '':
        p[0] = ('ARGS', p[2], tuple(p[3]))
    else:
        p[0] = p[1]


def p_formal_arg(p):
    """
    formal-arg  :  type-prefix empty-or-range var-name type-suffix empty-or-ass-expr
    """
    p[0] = ('ARG', p[1], p[3], p[4], p[2], p[5])


def p_empty_or_range(p):
    """
    empty-or-range    :
                      |  RANGE
    """
    p[0] = p[1]


def p_empty_or_ass_expr(p):
    """
    empty-or-ass-expr    :
                         |  formal-arg-list ASSIGN expr
    """
    p[0] = ('ASSIGN', p[1], p[2])


def p_swift_func_defn(p):
    """
    swift-func-defn  :  annotation-star func-hdr ARROW block
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
    app-func-defn  :  annotation-star C_APP func-hdr LBRACE app-body RBRACE
    """
    p[0] = ('APP', p[3], p[5])


def p_app_body(p):
    """
    app-body  :  app-arg-expr app-arg-expr-star app-out-star empty-or-semicolon
    """
    p[0] = ('BODY', p[1], tuple(p[2]), tuple(p[3]), p[4])


def p_empty_or_semicolon(p):
    """
    empty-or-semicolon    :
                          |  SEMICOLON
    """
    p[0] = p[1]


def p_app_out_star(p):
    """
    app-out-star    :
                    | std-in-out-err ASSIGN expr app-out-star
    """
    if p[1] != '':
        p[0] = ('APP_OUT', (p[2], p[1], p[3]), tuple(p[4]))
    else:
        p[0] = p[1]


def p_std_in_out_err(p):
    """
    std-in-out-err  : E_STDIN
                    | E_STDOUT
                    | E_STDERR
    """
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
    foreign-func-body  :  STR_LITERAL STR_LITERAL ( | STR_LITERAL) ( | (LBRACKET (STR_LITERAL | MUL_STR_LITERAL) RBRACKET))
    """
    p[0] = ('FOREIGN_FUNC', p[1], p[2], p[3], p[4])


def p_empty_or_(p):
    """
    empty-or-semicolon    :
                          |  SEMICOLON
    """
    p[0] = p[1]


def p_var_decl(p):
    """
    var-decl  :  type-prefix var-decl-rest
    """
    p[0] = ('VARS_DEC', p[1], tuple(p[2]))


def p_var_decl_rest_star(p):
    """
    var-decl-rest-star  :
                        | COMMA var-decl-rest var-decl-rest-star
    """
    if p[1] != '':
        p[0] = ('VAR_DECL', p[2], tuple(p[3]))
    else:
        p[0] = p[1]


def p_var_decl_rest(p):
    """
    var-decl-rest  :  var-name type-suffix ( | var-mapping) ( | (ASSIGN expr))
    """
    p[0] = ('VAR_DECL_TAILER', p[1], p[2], p[3], p[4])


def p_type_prefix(p):
    """
    type-prefix  :  type-name
                 | param-type
    """
    p[0] = p[1]


def p_param_type(p):
    """
    param-type  :  type-name LESS standalone-type GREATER
    """
    p[0] = (p[3], p[1])


def p_type_suffix(p):
    """
    type-suffix  :
                 | (LBRACKET ( | standalone-type) RBRACKET) type_suffix
    """
    if p[1] != '':
        p[0] = ('TYPE_SUFFIX', p[2], p[1], tuple(p[3]))
    else:
        p[0] = p[1]


def p_standalone_type(p):
    """
    standalone-type  :  type-prefix type-suffix
    """
    p[0] = ('STANDALONE_TYPE', p[1], p[2])


def p_var_mapping(p):
    """
    var-mapping  :  LESS expr GREATER
    """
    p[0] = ('VAR_MAPPING', p[1])


def p_block(p):
    """
    block  :  LBRACE statement-star RBRACE
    """
    p[0] = ('CODE_BLOCK', tuple(p[2]))


def p_stmt_chain(p):
    """
    stmt-chain  :  chainable-stmt semicolon-or-arrow statement
    """
    p[0] = ('STATEMENT_CHAIN', ('STATEMENT', p[2]), p[1])


def p_semicolon_or_arrow(p):
    """
    semicolon-or-arrow  : SEMICOLON
                        | ARROW
    """
    p[0] = p[1]


def p_chainable_stmt(p):
    """
    chainable-stmt  :  var-name
                      | func-call
                      | var-decl
                      | assignment
    """
    p[0] = ('CHAINABLE_STMT', p[1])


def p_assignment(p):
    """
    assignment  :  lval-or-paren-lval assign-or-plusas expr-list
    """
    p[0] = ('ASSIGNMENT', p[3], p[1], p[2])


def p_assign_or_plusas(p):
    """
    assign-or-plusas    : ASSIGN
                        | PLUS_AS
    """
    p[0] = p[1]


def p_lval_or_paren_lval(p):
    """
    lval-or-paren-lval  :   lval-list
                        | LPAREN lval-list RPAREN
    """
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_update_stmt(p):
    """
    update-stmt  :  var-name LESS ID GREATER UPD expr SEMICOLON
    """
    p[0] = ('UPDATE', p[1], p[6])


def p_if_stmt(p):
    """
    if-stmt  :  IF LPAREN expr RPAREN block ( | (ELSE block))
    """
    p[0] = ('IF', p[3], p[4], (p[5]))


def p_switch_stmt(p):
    """
    switch-stmt  :  S_SWITCH LPAREN expr RPAREN LBRACE case-star( | default) RBRACE
    """
    p[0] = ('SWITCH', p[3], tuple(p[6]), p[7])


def p_case_star(p):
    """
    case-star   :
                |   case case-star
    """
    if p[1] != '':
        p[0] = ('CASES', p[1], tuple(p[2]))
    else:
        p[0] = p[1]


def p_case(p):
    """
    case  :  S_CASE int-literal COLON statement-star
    """
    p[0] = (p[1], p[2], tuple(p[4]))


def p_default(p):
    """
    default  :  S_DEFAULT COLON statement-star
    """
    p[0] = (p[1], tuple(p[3]))


def p_wait_stmt(p):
    """
    wait-stmt  :  E_WAIT ( | E_DEEP) LPAREN expr-list RPAREN block
    """
    p[0] = (p[1], p[2], p[3], p[4], p[5], p[6])


def p_foreach_loop(p):
    """
    foreach-loop  :  annotation-star S_FOREACH var-name ( | (COMMA var-name)) S_IN expr block
    """
    if len(p) == 9:
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8])
    else:
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7])


def p_for_loop(p):
    """
    for-loop  :  annotation-star S_FOR LPAREN for-init-list SEMICOLON expr ; for-update-list RPAREN block
    """
    p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10])


def p_while_loop(p):
    """
    while-loop  :   annotation S_WHILE LPAREN expr RPAREN block
    """
    p[0] = (p[1], p[2], p[4], p[6])


def p_for_init_list(p):
    """
    for-init-list  :  for-init for-init-star
    """
    p[0] = (p[1], tuple(p[2]))


def p_for_init_star(p):
    """
    for-init-star   :
                    | COMMA for-init for-init-star
    """
    if p[1] != '':
        p[0] = (p[2], tuple(p[3]))
    else:
        p[0] = p[1]


def p_for_init(p):
    """
    for-init  :  for-assignment
              | type-prefix var-name type-suffix ASSIGN expr
    """
    if len(p) == 6:
        p[0] = (p[1], p[2], p[3], p[4], p[5])
    else:
        p[0] = p[1]


def p_for_update_list(p):
    """
    for-update-list  :  for-assignment for-assignment-star
    """
    p[0] = (p[1], tuple(p[2]))


def p_for_assignment_star(p):
    """
    for-assignment-star :
                        | COMMA for-assignment for-assignment-star
    """
    if p[1] != '':
        p[0] = (p[2], tuple(p[3]))
    else:
        p[0] = p[1]


def p_for_assignment(p):
    """
    for-assignment  :  var-name ASSIGN expr
    """
    p[0] = (p[2], p[1], p[3])


def p_iterate_loop(p):
    """
    iterate-loop  :  S_ITERATE var-name block S_UNTIL LPAREN expr RPAREN
    """
    p[0] = (p[1], p[2], p[3], p[4], p[6])


def p_expr(p):
    """
    expr  :  or-expr
    """
    p[0] = p[1]


def p_or_expr(p):
    """
    or-expr  :  and-expr
             | or-expr LOG_OR and-expr
    """
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_and_expr(p):
    """
    and-expr  :  eq-expr
              | and-expr LOG_AND eq-expr
    """
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_eq_expr(p):
    """
    eq-expr  :  cmp-expr
             | eq-expr eq-or-not-eq eq-expr
    """
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_eq_or_not_eq(p):
    """
    eq-or-not-eq    : EQUAL
                    | NOT_EQUAL
    """
    p[0] = p[1]


def p_cmp_expr(p):
    """
    cmp-expr  :  add-expr
              | cmp-expr cmp-sign add-expr
    """
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_cmp_sign(p):
    """
    cmp-sign        : LESS
                    | LESS_EQ
                    | EQUAL
                    | GREATER
                    | GREATER_EQ
    """
    p[0] = p[1]


def p_add_expr(p):
    """
    add-expr  :  mult-expr
              | add-expr add-sign mult-expr
    """
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_add_sign(p):
    """
    add-sign    : PLUS
                | MINUS
    """
    p[0] = p[1]


def p_mult_expr(p):
    """
    mult-expr  :  unary-expr
               | mult-expr mult-sign unary-expr
    """
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_mult_sign(p):
    """
    mult-sign   : MULT
                | DIV
                | MULTPER
                | DOUBLEPER
                | MOD
    """
    p[0] = p[1]


def p_unary_expr(p):
    """
    unary-expr  :  postfix-expr
                  | minus-or-excl postfix-expr
    """
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]


def p_minus_or_excl(p):
    """
    minus-or-excl   : MINUS
                    | EXCLAMATION
    """
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
    array-subscript  :  LBRACKET expr RBRACKET
    """
    p[0] = p[2]


def p_struct_subscript(p):
    """
    struct-subscript  :  DOT ID
    """
    p[0] = (p[1], p[2])


def p_base_expr(p):
    """
    base-expr  :  literal
                 | func-call
                 | var-name
                 | LPAREN expr RPAREN
                 | tuple-constructor
                 | array-constructor
    """
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_func_call(p):
    """
    func-call  :  annotation-star func-name LPAREN func-call-arg-list RPAREN
    """
    p[0] = (p[2], p[4], p[1])


def p_func_call_arg_list(p):
    """
    func-call-arg-list  :  (expr | kw-expr) func-call-arg-star
    """


def p_def_expr_star(p):
    """
    func-call-arg-star  :
                        |   COMMA (expr | kw-expr) func-call-arg-star
    """
    if p[1] != '':
        p[0] = (p[2], tuple(p[3]))
    else:
        p[0] = p[1]


def p_tuple_constructor(p):
    """
    tuple-constructor  :  LPAREN expr COMMA expr comma-expr-star RPAREN
    """
    p[0] = ('EXPRESSION_LIST', p[2], p[4], tuple(p[5]))


def p_comma_expr_star(p):
    """
    comma-expr-star :
                    |   COMMA expr comma-expr-star
    """
    if p[1] != '':
        p[0] = (p[2], tuple(p[3]))
    else:
        p[0] = p[1]


def p_array_constructor(p):
    """
    array-constructor  :  array-list-constructor
                       | array-range-constructor
                       | array-kv-constructor
    """
    p[0] = p[1]


def p_array_list_constructor(p):
    """
    array-list-constructor  :  LBRACKET ( | expr-list) RBRACKET
    """
    p[0] = ('ARRAY_CONSTRUCTOR', p[2])


def p_array_range_constructor(p):
    """
    array-range-constructor  :  LBRACKET expr COLON expr ( | (COLON expr)) RBRACKET
    """
    p[0] = ('ARRAY_RANGE_CONSTR', p[2], p[4], p[5])


def p_array_kv_constructor(p):
    """
    array-kv-constructor  :  LBRACE ( | (array-kv-elem comma-array-kv-elem-star)) RBRACE
    """
    p[0] = p('ARRAY_KV_CONSTRUCTOR', p[2])


def p_comma_array_kv_elem_star(p):
    """
    comma-array-kv-elem-star    :
                                |   COMMA array-kv-elem comma-array-kv-elem-star
    """
    if p[1] != '':
        p[0] = (p[2], tuple(p[3]))
    else:
        p[0] = p[1]


def p_array_kv_elem(p):
    """
    array-kv-elem  :  expr COLON expr
    """
    p[0] = (p[2], p[1], p[3])


def p_annotation(p):
    """
    annotation  :  AT ID
                | AT kw-expr
    """
    p[0] = (p[1], p[2])


def p_kw_expr(p):
    """
    kw-expr  :  ID ASSIGN expr
    """
    p[0] = (p[2], p[1], p[3])


def p_literal(p):
    """
    literal  :  STR_LITERAL
             | MUL_STR_LITERAL
             | int-literal
             | float-literal
             | bool-literal
    """
    p[0] = p[1]


def p_float_literal(p):
    """
    float-literal  :  DOUBLE
                     | DOUBLE
                     | INF
                     | NAN
    """
    p[0] = p[1]


def p_bool_literal(p):
    """
    bool-literal  :  E_TRUE
                  | E_FALSE
    """
    p[0] = p[1]


def p_expr_list(p):
    """
    expr-list  :  expr
    """
    p[0] = p[1]


def p_expr_star(p):
    """
    comma-expr-star :
                    | COMMA expr comma-expr-star
    """
    p[0] = (p[1], p[2], p[3])


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
               | id
    """
    p[0] = p[1]


def p_const_name(p):
    """
    const-name  :   D_LET ID
    """
    p[0] = (p[1], p[2])


def p_var_name(p):
    """
    var-name  :     ID
    """
    p[0] = p[1]


def p_func_name(p):
    """
    func-name  :  D_FUNCTION ID
    """
    p[0] = p[1]


def p_lval_list(p):
    """
    lval-list  :  lval-expr lval-expr-star
    """
    p[0] = ('LVAL_LIST', p[1], tuple(p[2]))


def p_lval_expr_star(p):
    """
    lval-expr-star  :
                    |   COMMA lval-expr lval-expr-star
    """
    if p[1] != '':
        p[0] = (p[2], tuple(p[3]))
    else:
        p[0] = p[1]


def p_lval_expr(p):
    """
    lval-expr  :  var-name subscript-star
    """
    p[0] = ('LVAL_EXPR', p[1], tuple(p[2]))


def p_subscript_star(p):
    """
    subscript-star   :
                     | array-subscript  subscript-star
                     | struct-subscript subscript-star
    """
    if p[1] != '':
        p[0] = ('SUBSCRIPT', p[1], tuple(p[2]))
    else:
        p[0] = p[1]


def p_app_arg_expr(p):
    """
    app-arg-expr  :  ( | AT) var-name
                    | literal
                    | array-constructor
                    | LPAREN expr RPAREN
    """
    if len(p) == 3:
        p[0] = ('APP_ARG', p[2], p[1])
    elif len(p) == 4:
        p[0] = ('APP_ARG', p[2])
    else:
        p[0] = p[1]


parser = yacc.yacc()


def parse(data, debug=0):
    parser.error = 0
    p = parser.parse(data, debug=debug)
    if parser.error:
        print('Error occurred during parsing stage')
        return None
    return p
