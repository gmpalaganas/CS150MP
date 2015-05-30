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
            tabmodule=self.tabmodule)

    def run(self):
        while 1:
            try:
                s = raw_input('calc > ')
            except EOFError:
                break
            if not s: continue
            yacc.parse(s)
            
