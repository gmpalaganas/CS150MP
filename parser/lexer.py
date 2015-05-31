import sys
sys.path.insert(0."../..")

import ply.lex as lex

class Lexer:

    tokens = (
            #Identifier
            'ID',

            #Constants / Literals
            'INT', 'FLOAT', 'BOOL'
            'STRING',

            #Operators
            'PLUS', 'MINUS', 'MULT', 'DIVIDE', 'MOD',
            'AND', 'OR', 'NOT'
            'LE', 'GE', 'GT', 'LT', 'EQ', 'NE',
            'EQUALS', 
            'TIMESEQUALS', 'DIVEQUALS', 'PLUSEQUALS', 'MINUSEQUALS', 'MODEQUALS',
            'OREQUALS', 'ANDEQUALS',
            
            #Increment/Decrement
            'PLUSPLUS', 'MINUSMINUS',
            
            #Delimeters
            'LPAREN','RPAREN',
            'LBRACKET', 'RBRACKET',
            'LBRACE', 'RBRACE'
            'COMMA', 'SEMI', 'COLON',

            )

    reserved = {
        'kung' : 'IF',
        'ediKung' : 'ELIF',
        'iba' : 'ELSE',
        'palit' : 'SWITCH',
        'kaso' : 'CASE',
        'walangKaso' : 'DEFAULT',
        'gawin' : 'DO',
        'habang' : 'WHILE',
        'tuwing' : 'FOR',
        'ibalik' : 'RETURN',
        'sulat' : 'PRINT',
        'kuha' : 'SCAN',
        'laging' : 'CONST',
    }

    tokens = tokens + list(reserved.values())

    precedence = ()
    
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_MOD = r'%'
    t_AND = r'&&'
    t_OR = r'\|\|'
    t_NOT = r'!'
    t_LE = r'<='
    t_GE = r'>='
    t_LT = r'<'
    t_LG = r'>'
    t_EQ = r'=='
    t_NE = r'!='
    t_EQUALS = r'='
    t_PLUSEQUALS = r'\+='
    t_MINUSEQUALS = r'-='
    t_TIMESEQUALS = r'\*='
    t_DIVEQUALS = r'/='
    t_MODEQUALS = r'%='
    t_ANDEQUALS = r'&='
    t_OREQUALS = r'\|='

    t_PLUSPLUS = r'\+\+'
    t_MINUSMINUS = r'--'

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_COMMA = r','
    t_SEMI = r';'
    t_COLON = r':'

    t_BOOL = r'true|false'
    t_ignore = " \t"

    #handle reserved words
    def t_ID(self, t):
        r'(numero|tuldok|titik)_[a-zA-z_][a-zA-Z0-9_]*'
        t.type = reserved.get(t.value, 'ID')
        return t
		
    def t_STRING(self, t):
        r'\"([^\\\n]|(\\.))*?\"'
        try:
            t.value = str(t.value)
        except ValueError:
            printError("Invalid string value", t)

    def t_INT(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            printError("Invalid int value",t)
    
    def t_FLOAT(self,t):
        r'\d+(.\d+)'
        try:
            t.value = float(t.value)
        except ValueError:
            printError("Invalid float value",t)
            
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_comment(t):
        r'(/\*(.|\n)*?\*/)|//(.)'
        t.lexer.lineno += t.value.count('\n')

    def t_error(self, t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)

    def printError(msg,token):
        print msg, " ", token.value
        sys.exit(1)

    #build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module = self, **kwargs)
    
    #test the lexer
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
                if not tok:
                    break
            print(tok)
	
#to test
'''ex = Lexer()
ex.build()
ex.test("4 + 6")'''
