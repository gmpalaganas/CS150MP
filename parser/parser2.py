import ply.yacc as yacc
from lexer import tokens

def p_statements(p):
	'''
	fxn 			: fxn_prot
					| fxn_dec
					| fxn_call	
					| assign_statement
	'''	
	p[0] = 'fxn'
	print "fxn stuff"

def p_fxn_prot(p):
	'''
	fxn_prot 		: id LPAREN fxn_prot_args RPAREN SEMI
					| id LPAREN void RPAREN SEMI	
	'''
	print "fxn prot"
	p[0] = 'fxn prot'


def p_fxn_dec(p):
	'''
	fxn_dec 		: id LPAREN fxn_prot_args RPAREN LBRACE
					| id LPAREN void RPAREN LBRACE	
	'''
	print "fxn dec"
	p[0] = 'fxn dec'

def p_fxn_call(p):
	'''
	fxn_call 		: id LPAREN fxn_call_args RPAREN SEMI
					| id LPAREN void RPAREN SEMI
	'''
	print "fxn call"
	p[0] = 'fxn call'

def p_fxn_call_args(p):
	'''
	fxn_call_args 	: fxn_call_args COMMA id
					| fxn_call_args COMMA constants
					| id
					| constants	
	'''
	print "fxn call args0"
	p[0] = "call args here bro"

def p_fxn_prot_args(p):
	'''
	fxn_prot_args 	: fxn_prot_args COMMA id
					| id
	'''
	print "fxn prot args"
	p[0] = "prot args here bro"

def p_main_fxn(p):
	'main_fxn : MAIN LPAREN void RPAREN LBRACE'
	print "start main" 
	p[0] = "yahoo"


def p_assign_statement(p):
	'''
	assign_statement 	: INT_ID ASSIGN_OP additive_exp SEMI
						| FLOAT_LIT ASSIGN_OP additive_exp SEMI
						| INT_ID INC SEMI
						| INT_ID DEC SEMI
						| FLOAT_ID INC SEMI
						| FLOAT_ID DEC SEMI
						| INT_ID ASSIGN_OP LBRACE int_args RBRACE SEMI
						| FLOAT_ID ASSIGN_OP LBRACE num_args RBRACE SEMI  
						| INT_ID LBRACKET INT_LIT RBRACKET ASSIGN_OP additive_exp SEMI
						| FLOAT_ID LBRACKET	INT_LIT RBRACKET ASSIGN_OP additive_exp SEMI					
	'''
	print "assign"

def p_numArgs(p):
	'''
	num_args			: num_args COMMA INT_LIT
						| num_args COMMA INT_ID
						| num_args COMMA FLOAT_LIT
						| num_args COMMA FLOAT_ID
						| FLOAT_LIT
						| FLOAT_ID
						| int_args
	'''

def p_intArgs(p):
	'''
	int_args 			: int_args COMMA INT_ID
						| int_args COMMA INT_LIT
						| INT_ID	
						| INT_LIT
	'''

def p_additive_expr(p):
	'''
	additive_exp		: mult_exp
						| additive_exp ADD_OP mult_exp
						| additive_exp SUB_OP mult_exp
						| LPAREN additive_exp RPAREN
	'''
	print "arith"

def p_mult_expr(p):
	'''
	mult_exp			: primary_exp
						| mult_exp MULT_OP primary_exp
						| mult_exp DIV_OP primary_exp
						| mult_exp MOD_OP primary_exp
						| LPAREN mult_exp RPAREN
	'''
	print "mult/div/mod"

def p_primary_exp(p):
	'''
	primary_exp		: id
					| constants
					| fxn_call_a
	'''

def p_fxn_call_a(p):
	'''
	fxn_call_a 		: id LPAREN fxn_call_args RPAREN SEMI
					| id LPAREN void RPAREN SEMI
	'''
	print "fxn call"
	p[0] = 'fxn call'

def p_fxn_call_args(p):
	'''
	fxn_call_args 	: fxn_call_args COMMA id
					| fxn_call_args COMMA constants
					| id
					| constants	
	'''
	print "fxn call args0"
	p[0] = "call args here bro"	

def p_id(p):
	'''
	id 		: INT_ID
			| FLOAT_ID
			| CHAR_ID
			| STR_ID
	'''
	print "identifier"
	p[0] = "var"

def p_constants(p):
	'''
	constants 		: INT_LIT
					| FLOAT_LIT
					| CHAR_LIT
					| STR_LIT
	'''
	print "constant"
	p[0] = 'imma constant yey'

def p_void(p):
	'''
	void   	: NULL
			| empty
	'''
	print "void"
	p[0] = 'void'


def p_empty(p):
	'empty :'
	pass
# Error rule for syntax errors
def p_error(p):
	print p
	print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = raw_input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)