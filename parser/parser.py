import lexer
import profile
import logging
import ply.yacc as yacc 
tokens = lexer.tokens

def p_start(p):
    '''
    start : external_declaration main external_declaration
    '''
    pass 
def p_external_declaration_1(p):
    'external_declaration : assignment_expression external_declaration'
    pass

def p_external_declaration_2(p):
    'external_declaration : fxn_var_statement external_declaration'

def p_external_declaration_3(p):
    'external_declaration : empty'

def p_main(p):
    'main : MAIN LPAREN empty RPAREN compound_statement'
    pass

def p_fxn_var_statement_1(p):
    'fxn_var_statement : fxn_prot'
    pass

def p_fxn_var_statement_2(p):
    'fxn_var_statement : fxn_definition'

def p_declaration(p):
    'declaration : init_declarator_list SEMI'
    pass

def p_declaration_list_1(p):
    'declaration_list : declaration'
    pass

def p_declaration_list_2(p):
    'declaration_list : declaration_list declaration'

def p_init_declarator_list_1(p):
    'init_declarator_list : init_declarator'
    pass

def p_init_declaration_list_2(p):
    'init_declarator_list : init_declarator_list COMMA init_declarator'

def p_init_declarator_1(p):
    'init_declarator : declarator'
    pass

def p_init_declarator_2(p):
    'init_declarator : declarator ASSIGN_OP initializer'
    pass

def p_declarator_1(p):
    'declarator : identifier'
    pass

def p_declarator_2(p):
    'declarator : LPAREN declarator RPAREN'

def p_declarator_3(p):
    'declarator : declarator LBRACKET constant_expression_opt RBRACKET'

def p_initializer_1(p):
    'initializer : assignment_expression'
    pass

def p_initializer_2(p):
    'initializer : LBRACE initializer_list RBRACE'

def p_initializer_3(p):
    'initializer : LBRACE initializer_list COMMA RBRACE'

def p_initializer_list_1(p):
    'initializer_list : initializer'
    pass

def p_initializer_list_2(p):
    'initializer_list : initializer_list COMMA initializer'

def p_fxn_prot(p):
    'fxn_prot 		: fxn_declaration SEMI'

    print "fxn prot"
    p[0] = 'fxn prot'

def p_fxn_definition(p):
    'fxn_definition : fxn_declaration compound_statement'
    pass

def p_fxn_declaration_1(p):
    'fxn_declaration : identifier LPAREN fxn_prot_args RPAREN'
    pass

def p_fxn_declaration_2(p):
    'fxn_declaration : identifier LPAREN empty RPAREN'

def p_fxn_prot_args_1(p):
    'fxn_prot_args : identifier COMMA fxn_prot_args'

def p_fxn_prot_args_2(p):
    'fxn_prot_args : identifier'

#statement
def p_statement(p):
    '''
    statement : labeled_statement
              | expression_statement
              | compound_statement
              | selection_statement
              | iteration_statement
              | jump_statement
    '''
    pass

def p_labled_statement_1(p):
    'labeled_statement : identifier COLON statement'
    pass

def p_labeled_statement_2(p):
    'labeled_statement : CASE constant_expression COLON statement'

def p_labeled_statement_3(p):
    'labeled_statement : DEFAULT COLON statement'

def p_expression_statement(p):
    'expression_statement : expression_opt SEMI'
    pass

def p_compound_statement_1(p):
    '''
    compound_statement : LBRACE declaration_list statement_list RBRACE
    '''
    pass 

def p_compund_statement_2(p):
    'compound_statement : LBRACE statement_list RBRACE'

def p_compound_statement_3(p):
    'compound_statement : LBRACE declaration_list RBRACE'

def p_compund_statement_4(p):
    'compound_statement : LBRACE RBRACE'

def p_statement_list_1(p):
    'statement_list : statement'
    pass

def p_statement_list_2(p):
    'statement_list : statement_list statement'

def p_selection_statement_1(t):
    'selection_statement : IF LPAREN expression RPAREN statement else_if_statement'
    pass

def p_selection_statement_2(t):
    'selection_statement : IF LPAREN expression RPAREN statement else_if_statement ELSE statement '
    pass

def p_else_if_statement_1(p):
    'else_if_statement : ELSE_IF LPAREN expression RPAREN statement else_if_statement'

def p_selection_statement_3(t):
    'selection_statement : SWITCH LPAREN expression RPAREN statement '
    pass

def p_else_if_statement_2(p):
    'else_if_statement : empty'
    pass

def p_iteration_statement_1(t):
    'iteration_statement : WHILE LPAREN expression RPAREN statement'
    pass

def p_iteration_statement_2(t):
    'iteration_statement : FOR LPAREN expression_opt SEMI expression_opt SEMI expression_opt RPAREN statement '
    pass

def p_iteration_statement_3(t):
    'iteration_statement : DO statement WHILE LPAREN expression RPAREN SEMI'
    pass

def p_jump_statement_1(p):
    'jump_statement : CONTINUE SEMI'
    pass

def p_jump_statement_2(p):
    'jump_statement : BREAK SEMI'

def p_jump_statement_3(p):
    'jump_statement : RETURN expression_opt SEMI'

def p_expression_opt_1(p):
    'expression_opt : empty'
    pass

def p_expression_opt_2(p):
    'expression_opt : expression'

def p_expression_1(p):
    'expression : assignment_expression'
    pass

def p_expression_2(p):
    'expression : expression COMMA assignment_expression'

def p_assignment_expression(p):
    'assignment_expression : conditional_expression'
    pass

def p_assignment_expression_2(p):
    'assignment_expression : unary_expression assignment_operator assignment_expression'

def p_assignment_operator(p):
    '''
    assignment_operator : ASSIGN_OP
                        | ADD_ASSIGN
                        | MIN_ASSIGN
                        | MUL_ASSIGN
                        | DIV_ASSIGN
                        | MOD_ASSIGN
    '''
    pass

# (cond)?exp:exp;
def p_conditional_expression_1(p):
    'conditional_expression : logical_or_expression'
    pass

def p_conditional_expression_2(p):
    'conditional_expression : logical_or_expression COND_OP expression COLON conditional_expression '

def p_constant_expression_opt_1(p):
    'constant_expression_opt : empty'
    pass

def p_constant_expression_opt_2(p):
    'constant_expression_opt : constant_expression'

def p_constant_expression(p):
    'constant_expression : conditional_expression'
    pass

def p_logical_or_expression_1(p):
    'logical_or_expression : logical_and_expression'
    pass

def p_logical_or_expression_2(p):
    'logical_or_expression : logical_and_expression OR logical_or_expression'

def p_logical_and_expression_1(p):
    'logical_and_expression : equality_expression'
    pass

def p_logical_and_expression_2(p):
    'logical_and_expression : logical_and_expression AND equality_expression'

def p_equality_expression_1(p):
    'equality_expression : relational_expression'
    pass

def p_equality_expression_2(p):
    'equality_expression : equality_expression EQ relational_expression'

def p_equality_expression_3(p):
    'equality_expression : equality_expression NEQ relational_expression'

def p_relational_expression_1(p):
    'relational_expression : add_expression'
    pass

def p_relational_expression_2(p):
    'relational_expression : relational_expression LT add_expression'

def p_relational_expression_3(p):
    'relational_expression : relational_expression GT add_expression'

def p_relational_expression_4(p):
    'relational_expression : relational_expression LE add_expression'

def p_relational_expression_5(p):
    'relational_expression : relational_expression GE add_expression'

def p_add_expression_1(p):
    'add_expression : mult_expression'
    pass

def p_add_expression_2(p):
    'add_expression : add_expression ADD_OP mult_expression'

def p_add_expression_3(p):
    'add_expression : add_expression SUB_OP mult_expression'


def p_mult_expression_1(p):
    'mult_expression : unary_expression'
    pass

def p_mult_expression_2(p):
    'mult_expression : mult_expression MULT_OP unary_expression'

def p_mult_expression_3(p):
    'mult_expression : mult_expression DIV_OP unary_expression'

def p_mult_expression_4(p):
    'mult_expression : mult_expression MOD_OP unary_expression'

def p_unary_expression_1(p):
    'unary_expression : postfix_expression'
    pass

def p_unary_expression_2(p):
    'unary_expression : INC unary_expression'

def p_unary_expression_3(p):
    'unary_expression : DEC unary_expression'

def p_unary_expression_4(p):
    'unary_expression : SUB_OP add_expression'

def p_unary_expression_5(p):
    'unary_expression : NOT logical_or_expression'

def p_postfix_expression_1(p):
    'postfix_expression : primary_expression'

def p_postfix_expression_2(p):
    'postfix_expression : postfix_expression LBRACKET expression RBRACKET'

def p_postfix_expression_3(p):
    'postfix_expression : postfix_expression LPAREN argument_expression_list RPAREN'

def p_postfix_expression_4(p):
    'postfix_expression : postfix_expression LPAREN RPAREN'

def p_postfix_expression_5(p):
    'postfix_expression : postfix_expression INC'

def p_postfix_expression_6(p):
    'postfix_expression : postfix_expression DEC'

def p_primary_expression(p):
    '''
    primary_expression : identifier
                       | constant
                       | LPAREN expression RPAREN
                       | SCAN
                       | PRINT
    '''
    pass

def p_argument_expression_list(p):
    '''
    argument_expression_list : assignment_expression
                             | argument_expression_list COMMA assignment_expression
    '''
    pass

def p_identifier(p):
    '''
    identifier : FLOAT_ID 
               | INT_ID
               | CHAR_ID
               | STR_ID
    '''
    pass

def p_constant(p):
    '''
    constant : FLOAT_LIT
             | INT_LIT
             | CHAR_LIT
             | STR_LIT
    '''
    pass

def p_empty(p):
    'empty : '
    pass

def p_error(p):
    print "Syntax Error ", p 
    pass 

def parseString(data):

    logging.basicConfig(
            level = logging.DEBUG,
            filename = "parser_debug.txt",
            filemode = "w",
            format = "%(filename)10s:%(lineno)4d:%(message)s"
            )

    log = logging.getLogger()
    lex = lexer.lexer
    parser = yacc.yacc(debug=True, debuglog=log)
    result = parser.parse(data)
    print result

def runParser(file_name):
    puto_file = open(file_name, "r")
    data = puto_file.read()
    parseString(data)
    puto_file.close()
