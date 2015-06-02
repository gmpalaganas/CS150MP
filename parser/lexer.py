import ply.lex as lex
import logging

reserved = {
	'wala'			:	'NULL',
	'balik'			:	'RETURN',
	'putol'			:	'BREAK',
	'tuloy'			:	'CONTINUE',
	'kung'			:	'IF',
        'iba'                   :       'ELSE',
	'palit'			:	'SWITCH',
	'kaso'			:	'CASE',
	'walangKaso'	        :	'DEFAULT',
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
	'ADD_ASSIGN',
        'MIN_ASSIGN',
        'MUL_ASSIGN',
        'DIV_ASSIGN',
        'MOD_ASSIGN',
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
        'COLON',
	'COMMA',
	'LINE_COMMENT',
	'MULTILINE_COMMENT',
	#main
	'MAIN',
	#unary_ops
	'INC',
	'DEC',
    'NOT',
    #ternary,
    'COND_OP',
    #var
    'VAR',


] + list(reserved.values())

t_ADD_OP                = r" \+ "
t_SUB_OP   		= r'-'
t_MULT_OP               = r'\*'
t_DIV_OP  		= r'/'
t_MOD_OP  		= r'%'

t_EQ			= r'=='
t_NEQ			= r'!='	
t_GT			= r'>'
t_GE 			= r'>='
t_LT 			= r'<'
t_LE 			= r'<='

t_ADD_ASSIGN            = r' \+= '
t_MIN_ASSIGN            = r'-='
t_MUL_ASSIGN            = r'\*='
t_DIV_ASSIGN            = r'/='
t_MOD_ASSIGN            = r'%='
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
t_COLON                 = r':'
t_COMMA			= r','

t_INC 			= r'\+\+'
t_DEC			= r'--'
t_NOT                   = r'!'

t_COND_OP               = r'\?'

t_VAR           =  r'@'

# Error handling rule
def t_error(t):
	print("Illegal character %s at line %s" % (t.value[0], t.lineno))
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

def t_comment(t):
    r'(\#(.)*?\n)|(~(.|\n)*?~)'
    t.lexer.lineno += t.value.count('\n')
    pass

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\x0c'


# Define a rule so we can track line INT_LITs
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

logging.basicConfig(
        level = logging.DEBUG,
        filename = "debug.txt",
        filemode = "w",
        format = "%(filename)10s:%(lineno)4d:%(message)s"
        )

log = logging.getLogger()

lexer = lex.lex(debug=True,debuglog=log)

def tokenizeString(data):
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        print(tok)	

def runLexer(file_name):
    puto_file = open(file_name, "r")
    data =  puto_file.read()
    tokenizeString(data)
    puto_file.close()
