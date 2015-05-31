import ply.lex as lex

reserved = {
	'wala'			:	'NULL',
	'balik'			:	'RETURN',
	'putol'			:	'BREAK',
	'tuloy'			:	'CONTINUE',
	'kung'			:	'IF',
	'ediKung'		:	'ELSE_IF',
	'palit'			:	'SWITCH',
	'kaso'			:	'CASE',
	'walangKaso'	:	'DEFAULT',
	'tuwing'		:	'FOR',
	'gawin'			:	'DO',
	'habang'		:	'WHILE',
	'sulat'			:	'PRINT',
	'kuha'			:	'SCAN',
}
tokens = [
	# arithmetic ops
	'ADD_OP',
	'SUB_OP',
	'MULT_OP',
	'DIV_OP',
	'MOD_OP',
	#boolean ops
	'EQ',
	'NEQ',	
	'GT',
	'GE',
	'LT',
	'LE',
	#assign op
	'ASSIGN_OP',
	#logial ops
	'AND',
	'OR',
	#boundaries
	'LPAREN',
	'RPAREN',
	'LBRACE',
	'RBRACE',
	'LBRACKET',
	'RBRACKET',
	#identifiers
	'FLOAT_ID',
	'INT_ID',
	'CHAR_ID',
	'STR_ID',
	#literals
	'FLOAT_LIT',
	'INT_LIT',
	'CHAR_LIT',
	'STR_LIT',	
	#other
	'SEMI',
	'COMMA',
	'LINE_COMMENT',
	'MULTILINE_COMMENT',
	#main
	'MAIN',
	#unary_ops
	'INC',
	'DEC',

] + list(reserved.values())

t_ADD_OP    	= r" \+ "
t_SUB_OP   		= r'-'
t_MULT_OP   	= r'\*'
t_DIV_OP  		= r'/'
t_MOD_OP  		= r'%'

t_EQ			= r'=='
t_NEQ			= r'!='	
t_GT			= r'>'
t_GE 			= r'>='
t_LT 			= r'<'
t_LE 			= r'<='

t_ASSIGN_OP		= r'='

t_AND			= r'&&'
t_OR   			= r'\|\|'

t_LPAREN  		= r'\('
t_RPAREN  		= r'\)'
t_LBRACE 		= r'\{'
t_RBRACE 		= r'\}'
t_LBRACKET		= r'\['
t_RBRACKET		= r'\]'	

t_SEMI			= r';'
t_COMMA			= r','

t_INC 			= r'\+\+'
t_DEC			= r'--'

# Error handling rule
def t_error(t):
	print("Illegal character '%s' at line %s column %s" % (t.value[0], t.lineno, t.lexpos))
	t.lexer.skip(1)

def t_MAIN(t):
	r'bilang_puno'
	t.value = str(t.value)   
	return t	

def t_INT_ID(t):	
	r'bilang_[a-zA-Z][a-zA-Z0-9]*'
	t.value = str(t.value)   
	return t

def t_FLOAT_ID(t):
	r'tuldok_[a-zA-Z][a-zA-Z0-9]*'
	t.value = str(t.value)    
	return t

def t_CHAR_ID(t):
	r'letra_[a-zA-Z][a-zA-Z0-9]*'
	t.value = str(t.value)    
	return t

def t_STR_ID(t):
	r'salita_[a-zA-Z][a-zA-Z0-9]*'
	t.value = str(t.value)    
	return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    if t.type == 'ID' and str(t.value).startswith('bilang_'):
    	t_INT_ID(t)
    elif t.type == 'ID':	
    	t_error(t)
    else:	
    	return t
def t_FLOAT_LIT(t ):
	r'[-]?\d*\.\d*'
	t.value = float(t.value)    
	return t

def t_INT_LIT(t ):
	r'[-]?\d+'
	t.value = int(t.value)    
	return t

def t_CHAR_LIT(t):
	r'(L)?\'([^\\\n]|(\\.))*?\''
	if len(str(t.value)) == 2:
		t.value = ''	
	else:
		t.value = str(t.value)[1:len(str(t.value)) - 1]
	return t

def t_STR_LIT(t):
	r'"(.|\n|\t)*?\"'
	if len(str(t.value)) == 2:
		t.value = ""
	else:
		t.value = str(t.value)[1:len(t.value)-1]	
	return t

#line comment
def t_LINE_COMMENT(t):
	r'\#.*'
	print "Comment"
	pass

def t_MULTILINE_COMMENT(t):
    r'[~](.|\n)*?[~]'
    t.lexer.lineno += t.value.count('\n')
    return t

#for reserved words

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'


# Define a rule so we can track line INT_LITs
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

# Build the lexer
lexer = lex.lex()

# Test it out
data = '''
-1
-90.90 + -1
bilang_a++
-90.90+90--
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)
	