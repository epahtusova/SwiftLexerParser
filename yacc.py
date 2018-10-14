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
    new-type-defn  :  'type' type-name '{' (var-decl ';') * '}'
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
    module-path  :  id ('.' id)*
    """

def p_pragma_stms(p):
    """
    pragma-stmt  :  'pragma' id expr  ';'
    """

def p_func_defn(p):
    """
    func-defn  :  swift-func-defn
                | app-func-defn
                | foreign-func-defn
    """

def p_func_hdr(p):
    """
    func-hdr  :  type-params formal-arg-list func-name ( | formal-arg-list)
    """

def p_type_params(p):
    """
    type-params  :
                 | '<' var-name (',' var-name) * '>'
    """

def p_formal_arg_list(p):
    """
    formal-arg-list  :
                     | '(' ((formal-arg (',' formal-arg)*) | )  ')'
    """

def p_formal_arg(p):
    """
    formal-arg  :  type-prefix (  | '...') var-name type-suffix ( | ('=' expr))
    """

def p_swift_func_defn(p):
    """
    swift-func-defn  :  annotation * func-hdr block
    """

def p_app_func_defn(p):
    """
    app-func-defn  :  annotation * 'app' func-hdr '{' app-body '}'
    """

def p_app_body(p):
    """
    app-body  :  app-arg-expr app-arg-expr * ('@'('stdin' | 'stdout' | 'stderr') '=' expr) * ( | ';')
    """

def p_foreign_func_defn(p):
    """
    foreign-func-defn  :  annotation * func-hdr foreign-func-body
    """

def p_foreign_func_body(p):
    """
    foreign-func-body  :  string-literal string-literal ( | string-literal) ('[' string-literal | multiline-string-literal']')?
    """

def p_var_decl(p):
    """
    var-decl  :  type-prefix var-decl-rest (',' var-decl-rest)*
    """

def p_var_decl_rest(p):
    """
    var-decl-rest  :  var-name type-suffix ( | var-mapping) ( | ('=' expr))
    """

def p_type_prefix(p):
    """
    type-prefix  :  type-name
                    | param-type
    """

def p_param_type(p):
    """
    param-type  :  type-name '<' standalone-type '>'
    """

def p_type_suffix(p):
    """
    type-suffix  :  ('[' ( | standalone-type) ']')*
    """

def p_standalone_type(p):
    """
    standalone-type  :  type-prefix type-suffix
    """

def p_var_mapping(p):
    """
    var-mapping  :  '<' expr '>'
    """

def p_block(p):
    """
    block  :  '{' statement * '}'
    """

def p_stmt_chain(p):
    """
    stmt-chain  :  chainable-stmt (';' | '=' '>' statement)
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
    assignment  :  (lval-list | '(' lval-list ')') ('=' | '+=') expr-list
    """

def p_update_stmt(p):
    """
    update-stmt  :  var-name '<' id '>' ':=' expr ';'
    """

def p_if_stmt(p):
    """
    if-stmt  :  'if' '(' expr ')' block ( | ('else' block))
    """

def p_switch_stmt(p):
    """
    switch-stmt  :  'switch' '(' expr ')' '{' case * ( | default) '}'
    """

def p_case(p):
    """
    case  :  'case' int-literal ':' statement*
    """

def p_default(p):
    """
    default  :  'default' ':' statement*
    """

def p_wait_stmt(p):
    """
    wait-stmt  :  'wait' ( | 'deep') '(' expr-list ')' block
    """

def p_foreach_loop(p):
    """
    foreach-loop  :  annotation * 'foreach' var-name ( | (',' var-name)) 'in' expr block
    """

def p_for_loop(p):
    """
    for-loop  :  annotation * 'for' '(' for-init-list ';' expr ; for-update-list ')' block
    """

def p_for_init_list(p):
    """
    for-init-list  :  for-init (','for-init)*
    """

def p_for_init(p):
    """
    for-init  :  for-assignment
              | type-prefix var-name type-suffix '=' expr
    """

def p_for_update_list(p):
    """
    for-update-list  :  for-assignment (',' for-assignment)*
    """

def p_for_assignment(p):
    """
    for-assignment  :  var-name '=' expr
    """

def p_iterate_loop(p):
    """
    iterate-loop  :  'iterate' var-name block 'until' '(' expr ')'
    """

def p_expr(p):
    """
    expr  :  or-expr
    """

def p_or_expr(p):
    """
    or-expr  :  and-expr
             | or-expr '||' and-expr
    """

def p_and_expr(p):
    """
    and-expr  :  eq-expr
              | and-expr '&&' eq-expr
    """

def p_eq_expr(p):
    """
    eq-expr  :  cmp-expr
             | eq-expr ('==' | '!=') eq-expr
    """

def p_cmp_expr(p):
    """
    cmp-expr  :  add-expr
              | cmp-expr ('<' | '=' | '>' | '>=') add-expr
    """

def p_add_expr(p):
    """
    add-expr  :  mult-expr
              | add-expr ('+' | '-') mult-expr
    """

def p_mult_expr(p):
    """
    mult-expr  :  unary-expr
               | mult-expr ('*' | '/' | '%/' | '%%' | '%') unary-expr
    """

def p_unary_expr(p):
    """
    unary-expr  :  postfix-expr
                  | ('-' | '!') postfix-expr
    """

def p_postfix_expr(p):
    """
    postfix-expr  :  base-expr
                  | postfix-expr(array-subscript | struct-subscript)
    """

def p_array_subscript(p):
    """
    array-subscript  :  '[' expr ']'
    """

def p_struct_subscript(p):
    """
    struct-subscript  :  '.' id
    """

def p_base_expr(p):
    """
    base-expr  :  literal
                 | func-call
                 | var-name
                 | '(' expr ')'
                 | tuple-constructor
                 | array-constructor
    """

def p_func_call(p):
    """
    func-call  :  annotation* func-name '(' func-call-arg-list ')'
    """

def p_func_call_arg_list(p):
    """
    func-call-arg-list  :  (expr | kw-expr) (',' (expr | kw-expr))*
    """

def p_tuple_constructor(p):
    """
    tuple-constructor  :  '(' expr ',' expr (',' expr) * ')'
    """

def p_array_constructor(p):
    """
    array-constructor  :  array-list-constructor
                       | array-range-constructor
                       | array-kv-constructor
    """

def p_array_list_constructor(p):
    """
    array-list-constructor  :  '[' expr-list? ']'
    """

def p_array_range_constructor(p):
    """
    array-range-constructor  :  '[' expr ':' expr (':' expr)? ']'
    """

def p_array_kv_constructor(p):
    """
    array-kv-constructor  :  '{' (array-kv-elem (',' array-kv-elem)*)? '}'
    """

def p_array_kv_elem(p):
    """
    array-kv-elem  :  expr ':' expr
    """

def p_annotation(p):
    """
    annotation  :  '@' id | '@' kw-expr
    """

def p_kw_expr(p):
    """
    kw-expr  :  id '=' expr
    """

def p_literal(p):
    """
    literal  :  string-literal
             | multiline-string-literal
             | int-literal
             | float-literal
             | bool-literal
    """

def p_float_literal(p):
    """
    float-literal  :  decimal
                     | sci-decimal
                     | 'inf'
                     | 'NaN'
    """

def  p_bool_literal(p):
    """
    bool-literal  :  'true'
                  | 'false'
    """

def p_expr_list(p):
    """
    expr-list  :  expr (',' expr)*
    """

def p_type_name(p):
    """
    type-name  :  id
    """

def p_var_name(p):
    """
    var-name  :  id
    """

def p_func_name(p):
    """
    func-name  :  id
    """

def p_lval_list(p):
    """
    lval-list  :  lval-expr (',' lval-expr)*
    """

def p_lval_expr(p):
    """
    lval-expr  :  var-name (array-subscript | struct-subscript)*
    """

def p_app_arg_expr(p):
    """
    app-arg-expr  :  ( | '@') var-name
                    | literal
                    | array-constructor
                    | '(' expr ')'
    """
