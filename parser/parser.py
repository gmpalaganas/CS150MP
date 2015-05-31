import lexer
import ply.yacc as yacc

tokens = lexer.tokens

def p_identifier(t):
    'identifier : FLOAT_ID | INT_ID | CHAR_ID | STR_ID'

#statement
def p_statement(t):
    '''
    statement : labaled_statement
              | expression_statement
              | compound_statemet
              | selection_statement
              | iteration_statement
    '''
