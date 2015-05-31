import lexer
import profile
import ply.yacc as yacc

tokens = lexer.tokens

#statement
def p_statement(t):
    '''
    statement : labeled_statement
              | expression_statement
              | compound_statemet
              | selection_statement
              | iteration_statement
              | jump_statement
    '''
    pass

def p_labled_statement(t):
    '''
    labeled_statement : identifier COLON statement
                      | CASE constant_expression COLON statement
                      | DEFAULT COLON statement
    '''
    pass

def p_expression_statment(t):
    'expression_statement : expression_opt SEMI'
    pass

def p_compound_statement(t):
    '''
    compound_statment : LBRACE declaration_list statment_list RBRACE
                      | LBRACE statement_list RBRACE
                      | LBRACE declaration_list RBRACE
                      | LBRACE RBRACE
    '''
    pass 

def p_statement_list(t):
    '''
    statement_list : statement
                   | statement_list statement
    '''
    pass

def p_selection_statement(t):
    '''
    selection_statement : IF LPAREN expression RPAREN statement
                        | IF LPAREEN expression RPAREN statement ELSE statement
                        | SWITCH LPAREN expression RPAREN statement
    '''
    pass

def p_iteration_statement(t):
    '''
    iteration_statement : WHILE LPAREN expression RPAREN statement
                        | FOR LPAREN expression_opt SEMI expression_opt SEMI expression_opt RPAREN statement
                        | DO statement WHILE LPAREN expression RPAREN SEMI
    '''
    pass

def p_jump_statement(t):
    '''
    jump_statement : CONTINUE SEMI
                   | BREAK SEMI
                   | RETURN expression_opt SEMI
    '''
    pass

def p_expression_opt(t):
    '''
    expression_opt : empty'
                   | expression
    '''
    pass

def p_expression(t):
    '''
    expression : assignment_expression
               | expression COMMA assignment_expression
    '''
    pass

def p_assignment_expression(t):
    '''
    assignment_expression : conditional_expression
                          | unary_expression assignment_operator assignment_expression
    '''
    pass

def p_assignment_operator(t):
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
def p_conditional_expression(t):
    '''
    conditional_expression : logical_or_expression
                           | logical_or_expression CONDOP expression COLON conditional_expression 
    '''
    pass

def p_logical_or_expression(t):
    '''
    logical_or_expression : logical_and_expression
                          | logical_and_expression OR logical_or_expression
    '''
    pass

def p_logical_and_expression(t):
    '''
    logical_and_expression : equality_expression
                           | logical_and_expression AND equality_expression
    '''
    pass

def p_equality_expression(t):
    '''
    equality_expression : relational_expression
                        | equality_expression EQ relational_expression
                        | equality_expression NE relational_expression
    '''
    pass

def p_relational_expression(t):
    '''
    relational_expression : add_expression
                          | relational_expression LT add_expression
                          | relational_expression GT add_expression
                          | relational_expression LE add_expression
                          | relational_expression GE add_expression
    '''
    pass

def p_add_expression(t):
    '''
    add_expression : mult_expression
                   | add_expression ADD_OP mult_expression
                   | add_expression MIN_OP mult_expression
    '''
    pass

def p_mult_expression(t):
    '''
    mult_expression : unary_expression
                    | mult_expression MULT_OP unary_expression
                    | mult_expression DIV_OP unary_expression
                    | mult_expression MOD_OP unary_expression
    '''
    pass

def p_unary_expression(t):
    '''
    unary_expression : primary_expression
                     | PLUSPLUS unary_expression
                     | MINMIN unary_expression
                     | MIN add_expression
                     | NOT logical_or_expression
    '''
    pass

def p_primary_expression(t):
    '''
    primary_expression : identifier
                       | constant
                       | LPAREN expression RPAREN
    '''
    pass

def p_argument_expression_list(t):
    '''
    argument_expression_list : assignment_expression
                             | argument_expression_list COMMA assignment_expression
    '''
    pass

def p_identifier(t):
    'identifier : FLOAT_ID | INT_ID | CHAR_ID | STR_ID'
    pass

def p_constant(t):
    '''
    constant : FLOAT_LIT
             | INT_LIT
             | CHAR_LIT
             | STR_LIT
    '''
    pass

def p_empty(t):
    'empty: '
    pass

def p_error(t):
    print "ERROR PARSING"

