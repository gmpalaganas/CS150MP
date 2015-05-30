import ply.lex as lex
import ply.yacc as yacc

class Parser:

    literals = "+-*/=!{}[]()"

    tokens = (
            'IDENT',
            'INT', 'FLOAT', 'DOUBLE',
            'STRING',
            'AND', 'OR',
            'BOOL',
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

    precedence = (
            ('left', '+', '-'),
            ('left', '*', '/'),
            ('left', 'AND', 'OR'),
            ('right', 'UMINUS'),
            ('right', '!'),
            )
    
    t_IDENT = r'[a-zA-z_][a-zA-Z0-9_]*'
    t_AND = r'&&'
    t_OR = r'||'
    t_BOOL = r'true|false'

    def t_STRING(self, t):
        r'"[\w \t]+"'
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
        r'\d+(.\d+)f'
        try:
            t.value = float(t.value)
        except ValueError:
            printError("Invalid float value",t)

    def t_DOUBLE(self,t):
        r'\d+(.\d+)'
        try:
            t.value = float(t.value)
            printError("Invalid double value",t)
            
    def run(self):
        while 1:
            try:
                s = raw_input('calc > ')
            except EOFError:
                break
            if not s: continue
            yacc.parse(s)

    def printError(msg,token):
        print msg, " ", token.value
        sys.exit(1)
 
    def __init__(self, **keywargs):
        self.debug = keywargs.get('debug',0)
        self.names = { }
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[1] + "_" + self.__class__.__name__
        except:
            modname = "parser"+"_"+ self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"

        lex.lex(module=self,debug=self.debug)
        yacc.yacc(module=self,
            debug=self.debug,
            debugfile=self.debugfile,
