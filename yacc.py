import ply.yacc as yacc
import json
import lexer


tokens = lexer.tokens


def p_translation_unit(p):
    """
    translation-unit  :  statement-star
    """
    p[0] = p[1]

def p_statement_star(p):
    """
    statement-star  : statement statement-star
                    | empty
    """
    try:
        p[0] = (p[1], (p[2]))
    except:
        p[0] = p[1]

def p_statement(p):
    """
    statement  :  SEMICOLON
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
               | var-decl
               | while-loop
               | iterate-loop
               | stmt-chain
               | opt-else-block
               | var-name
               | assignment
               | func-call
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
    p[0] = ('MODULE_PATH', (p[1]))

def p_path_star(p):
    """
    path-star   : DOT ID path-star
	|
    """
    try:
        p[0] = ('PATH', p[2], (p[3]))
    except:
        p[0] = None

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
    func-hdr  :  type-params formal-arg-list ID empty-or-arg-list
    """
    if p[4] != '':
        p[0] = (p[3], p[4], p[1], p[2])
    else:
        p[0] = (p[3], p[1], p[2])

def p_empty_or_arg_list(p):
    """
    empty-or-arg-list    : formal-arg-list
	                     | empty
    """
    p[0] = p[1]


def p_type_params(p):
    """
    type-params  : LESS var-name comma-name-star GREATER
	             | empty
    """
    try:
        p[0] = ('NAME', p[2], (p[3]))
    except:
        p[0] = None

def p_comma_name_star(p):
    """
    comma-name-star : COMMA var-name comma-name-star
	|
    """
    try:
        p[0] = ('NAME', p[2], (p[3]))
    except:
        p[0] = None

def p_formal_arg_list(p):
    """
    formal-arg-list  : LPAREN opt-formal-args RPAREN
	| empty
    """
    try:
        p[0] = ('ARGS', p[2])
    except:
        p[0] = None

def p_opt_formal_args(p):
    """
    opt-formal-args : formal-arg comma-args-star
	| empty
    """
    try: p[0] = (p[1], (p[2]))
    except:
        p[0] = None

def p_comma_args_star(p):
    """
    comma-args-star : COMMA formal-arg comma-args-star
	| empty
    """
    try:
        p[0] = ('ARGS', p[2], (p[3]))
    except:
        p[0] = None

def p_formal_arg(p):
    """
    formal-arg  :  type-prefix empty-or-range var-name type-suffix empty-or-ass-expr
    """
    p[0] = ('ARG', p[1], p[3], p[4], p[2], p[5])


def p_empty_or_range(p):
    """
    empty-or-range    : RANGE
	| empty
    """
    p[0] = p[1]

def p_empty_or_ass_expr(p):
    """
    empty-or-ass-expr    : formal-arg-list ASSIGN expr
	| empty
    """
    p[0] = ('ASSIGN', p[1], p[2])

def p_swift_func_defn(p):
    """
    swift-func-defn  :   func-hdr ARROW block
    """
    p[0] = (p[2], (p[1]), p[4])


def p_app_func_defn(p):
    """
    app-func-defn  :   C_APP func-hdr LBRACE app-body RBRACE
    """
    p[0] = ('APP', p[3], p[5])


def p_app_body(p):
    """
    app-body  :  app-arg-expr app-arg-expr-star app-out-star empty-or-semicolon
    """
    p[0] = ('BODY', p[1], (p[2]), (p[3]), p[4])

def p_empty_or_semicolon(p):
    """
    empty-or-semicolon    : SEMICOLON
	| empty
    """
    p[0] = p[1]


def p_app_out_star(p):
    """
    app-out-star    : std-in-out-err ASSIGN expr app-out-star
	|
    """
    try:
        p[0] = ('APP_OUT', (p[2], p[1], p[3]), (p[4]))
    except:
        p[0] = None


def p_std_in_out_err(p):
    """
    std-in-out-err  : E_STDIN
                   | E_STDOUT
                   | E_STDERR
    """
    p[0] = p[1]


def p_app_arg_expr_star(p):
    """
    app-arg-expr-star   : app-arg-expr app-arg-expr-star
	|
    """
    try:
        p[0] = ('APP_ARG_EXPRESSION', p[1], (p[2]))
    except:
        p[0] = None

def p_foreign_func_defn(p):
    """
    foreign-func-defn  :   func-hdr foreign-func-body
    """
    p[0] = (p[2], p[3], (p[1]))

def p_foreign_func_body(p):
    """
    foreign-func-body  :  STR_LITERAL STR_LITERAL empty-or-literal empty-or-more-literals
    """
    p[0] = ('FOREIGN_FUNC', p[1], p[2], p[3], p[4])

def p_empty_or_literal(p):
    """
    empty-or-literal    : STR_LITERAL
	| empty
    """
    p[0] = p[1]

def p_empty_or_more_literals(p):
    """
    empty-or-more-literals  : LBRACKET single-or-multiple-literal  RBRACKET
	| empty
    """
    if len(p)==3:
        p[0] = (p[2])
    else:
        p[0] = p[1]

def p_single_or_multistring_literal(p):
    """
    single-or-multiple-literal  : STR_LITERAL
                               | MUL_STR_LITERAL
    """
    p[0] = (p[1])

def p_var_decl(p):
    """
    var-decl  :  type-prefix var-decl-rest
    """
    p[0] = ('VARS_DEC', p[1], (p[2]))

def p_var_decl_rest_star(p):
    """
    var-decl-rest-star  : COMMA var-decl-rest var-decl-rest-star
	|
    """
    try:
        p[0] = ('VAR_DECL', p[2], (p[3]))
    except:
        p[0] = None

def p_var_decl_rest(p):
    """
    var-decl-rest  :  var-name type-suffix empty-or-var-mapping empty-or-assign-expr
    """
    p[0] = ('VAR_DECL_TAILER', p[1], p[2], p[3], p[4])


def p_empty(p):
    """
    empty :
    """
    p[0] = (None)

def p_empty_or_var_mapping(p):
    """
    empty-or-var-mapping : var-mapping
                        | empty
    """
    try:
        p[0] = p[1]
    except:
        p[0] = None


def p_empty_or_assign_expr(p):
    """
    empty-or-assign-expr    : ASSIGN expr
	                        | empty
    """
    try: p[0] = ('ASSIGN', p[2])
    except:
        p[0] = None

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
    type-suffix  : LBRACKET empty-or-standalone-type RBRACKET type-suffix
	|
    """
    try:
        p[0] = ('TYPE_SUFFIX', p[4], (p[2]))
    except:
        p[0] = None

def p_empty_or_standalone_type(p):
    """
    empty-or-standalone-type    : standalone-type
	|
    """
    p[0] = (p[1])

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
    block  :  LBRACE translation-unit RBRACE
    """
    p[0] = ('CODE_BLOCK', (p[2]))

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


def p_lval_or_lval_list(p):
    """
    lval-or-lval-list   : lval-list
                       | LPAREN lval-list RPAREN
    """
    if len(p) == 1:
        p[0] = p[1]
    else:
        p[0] = (p[2])


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
    if-stmt  :  S_IF LPAREN expr RPAREN block opt-else-block
    """
    p[0] = ('IF', p[3], p[5], p[6])

def p_opt_else_block(p):
    """
    opt-else-block   : S_ELSE block
	| empty
    """
    try:
        p[0] = ('ELSE', p[2])
    except:
        p[0] = p[1]

def p_switch_stmt(p):
    """
    switch-stmt  :  S_SWITCH LPAREN expr RPAREN LBRACE case-star opt-default RBRACE
    """
    p[0] = ('SWITCH', p[3], (p[6]), p[7])

def p_opt_default(p):
    """
    opt-default : S_DEFAULT
	| empty
    """
    p[0] = p[1]

def p_case_star(p):
    """
    case-star   : case case-star
	| empty
    """
    try:
        p[0] = ('CASES', p[1], (p[2]))
    except:
        p[0] = None

def p_case(p):
    """
    case  :  S_CASE INT COLON translation-unit
    """
    p[0] = (p[1], p[2], (p[4]))

def p_default(p):
    """
    default  :  S_DEFAULT COLON translation-unit
    """
    p[0] = (p[1], (p[3]))

def p_wait_stmt(p):
    """
    wait-stmt  :  E_WAIT opt-deep LPAREN expr-list RPAREN block
    """
    p[0] = (p[1], p[2], p[3], p[4], p[5], p[6])

def p_opt_deep(p):
    """
    opt-deep    : E_DEEP
	| empty
    """
    p[0] = p[1]

def p_foreach_loop(p):
    """
    foreach-loop  :   S_FOREACH var-name opt-comma-var-name S_IN expr block
    """
    if len(p) == 8:
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8])
    else:
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7])

def p_opt_comma_var_name(p):
    """
    opt-comma-var-name  : COMMA var-name
	| empty
    """
    try: p[0] = (p[2])
    except:
        p[0] = None

def p_for_loop(p):
    """
    for-loop  :   S_FOR LPAREN for-init-list SEMICOLON expr SEMICOLON for-update-list RPAREN block
    """
    p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10])

def p_while_loop(p):
    """
    while-loop  :    S_WHILE LPAREN expr RPAREN block
    """
    p[0] = (p[1], p[3], p[5])

def p_for_init_list(p):
    """
    for-init-list  :  for-init for-init-star
    """
    p[0] = (p[1], (p[2]))

def p_for_init_star(p):
    """
    for-init-star   : COMMA for-init for-init-star
	| empty
    """
    try:
        p[0] = (p[2], (p[3]))
    except:
        p[0] = None

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
    p[0] = (p[1], (p[2]))

def p_for_assignment_star(p):
    """
    for-assignment-star : COMMA for-assignment for-assignment-star
	|
    """
    try:
        p[0] = (p[2], (p[3]))
    except:
        p[0] = None

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
                 | postfix-expr array-or-struct
    """
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]

def p_array_or_struct(p):
    """
    array-or-struct : array-subscript
                   | struct-subscript
    """
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
                | -constructor
                | array-constructor
    """
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_func_call(p):
    """
    func-call  :   ID LPAREN func-call-arg-list RPAREN
    """
    p[0] = (p[2], p[4], p[1])


def p_func_call_arg_list(p):
    """
    func-call-arg-list  :  expr-or-kw func-call-arg-star
    """
    p[0] = ('ARGS_CALL_LIST', p[0], (p[2]))

def p_def_expr_star(p):
    """
    func-call-arg-star  : COMMA expr-or-kw func-call-arg-star
	| empty
    """
    try:
        p[0] = (p[2], (p[3]))
    except:
        p[0] = None

def p_expr_or_kw(p):
    """
    expr-or-kw  :   expr
               |   kw-expr
               | empty
    """
    try:
        p[0] = p[1]
    except:
        p[0] = None

def p__constructor(p):
    """
    -constructor  :  LPAREN expr COMMA expr comma-expr-star RPAREN
    """
    p[0] = ('EXPRESSION_LIST', p[2], p[4], (p[5]))

def p_comma_expr_star(p):
    """
    comma-expr-star : COMMA expr comma-expr-star
	| empty
    """
    try:
        p[0] = (p[2], (p[3]))
    except:
        p[0] = None

def p_array_constructor(p):
    """
    array-constructor  :  array-list-constructor
                      | array-range-constructor
                      | array-kv-constructor
    """
    p[0] = p[1]

def p_array_list_constructor(p):
    """
    array-list-constructor  :  LBRACKET opt-expr-list RBRACKET
    """
    p[0] = ('ARRAY_CONSTRUCTOR', p[2])

def p_opt_expr_list(p):
    """
    opt-expr-list    : expr-list
	| empty
    """
    p[0] = p[1]

def p_array_range_constructor(p):
    """
    array-range-constructor  :  LBRACKET expr COLON expr opt-coloned-expr RBRACKET
    """
    p[0] = ('ARRAY_RANGE_CONSTR', p[2], p[4], p[5])

def p_opt_coloned_expr(p):
    """
    opt-coloned-expr    : COLON expr
	| empty
    """
    try:p[0]=(p[2])
    except:
        p[0] = None

def p_array_kv_constructor(p):
    """
    array-kv-constructor  :  LBRACE opt-array-constructor RBRACE
    """
    p[0] = ('ARRAY_KV_CONSTRUCTOR', p[2])

def p_opt_array_constructor(p):
    """
    opt-array-constructor   : array-kv-elem comma-array-kv-elem-star
	| empty
    """
    try:p[0]=(p[1], (p[2]))
    except:
        p[0] = None

def p_comma_array_kv_elem_star(p):
    """
    comma-array-kv-elem-star    : COMMA array-kv-elem comma-array-kv-elem-star
	| empty
    """
    try:
        p[0] = (p[2], (p[3]))
    except:
        p[0] = None

def p_array_kv_elem(p):
    """
    array-kv-elem  :  expr COLON expr
    """
    p[0] = (p[2], p[1], p[3])


def p_kw_expr(p):
    """
    kw-expr  :  ID ASSIGN expr
    """
    p[0] = (p[2], p[1], p[3])

def p_literal(p):
    """
    literal  :  STR_LITERAL
            | MUL_STR_LITERAL
            | INT
            | float-literal
            | bool-literal
    """
    p[0] = p[1]

def p_float_literal(p):
    """
    float-literal  :   DOUBLE
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
              | ID
    """
    p[0] = p[1]

def p_const_name(p):
    """
    const-name  :   ID
    """
    p[0] = (p[1], p[2])

def p_var_name(p):
    """
    var-name  :     ID
    """
    p[0] = p[1]

def p_lval_list(p):
    """
    lval-list  :  lval-expr lval-expr-star
    """
    p[0] = ('LVAL_LIST', p[1], (p[2]))

def p_lval_expr_star(p):
    """
    lval-expr-star  : COMMA lval-expr lval-expr-star
	|
    """
    try:
        p[0] = (p[2], (p[3]))
    except:
        p[0] = None

def p_lval_expr(p):
    """
    lval-expr  :  var-name subscript-star
    """
    p[0] = ('LVAL_EXPR', p[1], (p[2]))

def p_subscript_star(p):
    """
    subscript-star   : array-subscript  subscript-star
                    | struct-subscript subscript-star
                    | empty
    """
    try:
        p[0] = ('SUBSCRIPT', p[1], (p[2]))
    except:
        p[0] = None

def p_app_arg_expr(p):
    """
    app-arg-expr  :   opt-at var-name
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

def p_opt_at(p):
    """
    opt-at  : AT
	| empty
    """
    p[0] = p[1]


def parse():
    print('POEHALI')
    lex = lexer.tokenize()
    parser = yacc.yacc()
    ast = parser.parse(lexer=lex, debug=1)
    file = open('out.txt', 'w')
    file.write(json.dumps(ast, indent=4))
    print(json.dumps(ast, indent=4))