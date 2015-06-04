import parser
import sys

STR = "str_identifier"
INT = "int_identifier"
FLT = "flt_identifier"
CHR = "chr_identifier"

class SymbolTableScope:
    def __init__(self,parent=None):
        self.parent = parent
        self.symbols = {}

    def getSymbol(self,symbol):
        if self.symbols.has_key(symbol):
            return self.symbols[symbol]
        else:
            return None

class SymbolTable:
    
    defaults = { STR : ' ', INT : 0, FLT : 0.0, CHR : '\0' }
    types = { STR: 'string', INT : 'int', FLT : 'float', CHR : 'char' }

    def __init__(self):
        self.globalScope = SymbolTableScope()
        self.curScope = self.globalScope

    def pushScope(self):
        self.curScope = SymbolTableScope(self.curScope)
        return self.curScope

    def popScope(self):
        self.curScope = self.curScope.parent
        return self.curScope

    def declareSymbol(self,symbol,s_type,value=None):
        scope = self.curScope
   
        if scope.symbols.has_key(symbol):
           i_error("Variable %s already exists" % symbol) 
        
        set_val = self.defaults[s_type] 
        if value:
            try:
                if(s_type == STR): 
                    set_val = str(value) 
                elif(s_type == CHR):
                    set_val = str(value)[1:len(str(value)) - 1]
                elif(s_type == INT):
                    set_val = int(value)
                elif(s_type == FLT):
                    set_val = float(value)
            except ValueError:
               i_error("%s expects %s but '%s' is of type %s " % (symbol, self.types[s_type], str(value), type(value)))
       
        scope.symbols[symbol] = set_val

    def lookupSymbol(self,symbol):
        lookupScope = self.curScope
        val = lookupScope.getSymbol(symbol)

        while not lookupScope.symbols.has_key(symbol):
            lookupScope = lookupScope.parent
            if lookupScope == None:
                i_error("Variable %s does not exist within scope" % symbol)
            val = lookupScope.getSymbol(symbol)
        
        return val

    def updateSymbol(self,symbol,s_type,value):
        lookupScope = self.curScope
        val = lookupScope.getSymbol(symbol) 

        while not lookupScope.symbols.has_key(symbol):
            lookupScope = lookupScope.parent
            if lookupScope == None:
                i_error("Variable %s does not exist within scope" % symbol)
            val = lookupScope.getSymbol(symbol)
        

        set_val = None
        if value != None:
            try:
                if(s_type == STR): 
                    set_val = str(value) 
                elif(s_type == CHR):
                    set_val = str(value)[1:len(str(value)) - 1]
                elif(s_type == INT):
                    set_val = int(value)
                elif(s_type == FLT):
                    set_val = float(value)
            except ValueError:
               i_error("%s expects %s but '%s' is of type %s " % (symbol, self.types[s_type], str(value), type(value)))
        lookupScope.symbols[symbol] = set_val
    
    #finds number of elements in ast.children[x] node
def childTot(child):
    tot = 0
    for each in child:
        tot = tot + 1
    return tot

symbolTable = SymbolTable() 

def interpret(ast,extraParam=None):
    if ast.type == "start":
        for child in ast.children:
            interpret(child)
        return None
    elif ast.type == "main":
        interpret(ast.children[0])
        return None
    elif ast.type == "init_declarator":
        symbol = interpret(ast.children[0])
        value = interpret(ast.children[1])
        symbolTable.updateSymbol(symbol,ast.children[0].children[0].type,value)
    elif ast.type == "var_declarator":
        symbol = interpret(ast.children[0])
        symbolTable.declareSymbol(symbol,ast.children[0].type)
        return str(symbol)
    elif ast.type == "compound_statement":
        symbolTable.pushScope()
        for child in ast.children:
            ret = interpret(child,extraParam)
            if ret == "break" or ret == "continue":
                return ret
        symbolTable.popScope()
        return None
    elif ast.type == "mix_list":
        for child in ast.children:
            ret = interpret(child,extraParam)
            if ret == "break" or ret == "continue":
                return ret
        return None  
    elif ast.type == "println_expression":
        msg = interpret(ast.children[0])
        print(msg)
        return None
    elif ast.type == "print_expression":
        msg = interpret(ast.children[0])
        print(msg),
        return None
    elif ast.type == "scan_expression":
        return raw_input();
    elif ast.type == "variable_call":
        symbol = interpret(ast.children[0])
        return symbolTable.lookupSymbol(symbol)
    elif ast.type == "binary_expression":
        val1 = interpret(ast.children[0])
        val2 = interpret(ast.children[1])
        if ast.value == "+":
            return val1 + val2
        elif ast.value == "-":
            return val1 - val2
        elif ast.value == '*':
            return val1 * val2
        elif ast.value == '/':
            return val1 / val2
    #this unary_expression else if block is not yet checked
    elif ast.type == "unary_expression":
        val1 = interpret(ast.children[0])
        if ast.value == "++":
            if ast.children[0].type == "variable_call":
                val2 = symbolTable.lookupSymbol(val1.children[0])
                symbolTable.updateSymbol(val1,ast.children[0].children[0].type,val2 + 1)
                return val1
            else:
                return val1 + 1
        elif ast.value == "--":
            if ast.children[0].type == "variable_call":
                val2 = symbolTable.lookupSymbol(val1.children[0])
                symbolTable.updateSymbol(val1,ast.children[0].children[0].type,val2 - 1)
                return val1
            return val1 - 1
        elif ast.value == "!":
            return not val1
        elif ast.value == "-":
            return -val1
    elif ast.type == "postfix_expression":
        variable = ast.children[0].children[0].value
        var_type = ast.children[0].children[0].type
        val = symbolTable.lookupSymbol(variable)
        if ast.value == "++":
            symbolTable.updateSymbol(variable,var_type, val + 1)
        elif ast.value == "--":
            symbolTable.updateSymbol(variable,var_type, val - 1)
    elif ast.type == "assignment_expression":
        variable = ast.children[0].children[0].value
        val = symbolTable.lookupSymbol(variable)
        val2 = interpret(ast.children[1]);
        op = ast.value
        var_type = ast.children[0].children[0].type
        if op == "=":
            symbolTable.updateSymbol(variable, var_type, val2)
        elif op == "+=":
            symbolTable.updateSymbol(variable, var_type, val + val2)
        elif op == "-=":
            symbolTable.updateSymbol(variable, var_type, val - val2)
        elif op == "*=":
            symbolTable.updateSymbol(variable, var_type, val * val2)
        elif op == "/=":
            symbolTable.updateSymbol(variable, var_type, val / val2)
        elif op == "%=":
            symbolTable.updateSymbol(variable, var_type, val % val2)
        return variable
        
    elif ast.type == "str_constant":
        return ast.value
    elif ast.type == "int_constant":
        return ast.value
    elif ast.type == "flt_constant":
        return ast.value    
    elif ast.type == "chr_constant":
        return ast.value
    elif ast.type == "str_identifier":
        return ast.value
    elif ast.type == "int_identifier":
        return ast.value
    elif ast.type == "flt_identifier":
        return ast.value   
    elif ast.type == "chr_identifier":
        return ast.value
    elif ast.type == "relational_expression":
        val1 = interpret(ast.children[0])
        val2 = interpret(ast.children[1])
        if ast.value == "<":
            return val1 < val2
        elif ast.value == ">":
            return val1 > val2
        elif ast.value == "<=":
            return val1 <= val2
        elif ast.value == ">=":
            return val1 >= val2
    elif ast.type == "logical_expression":
        val1 = interpret(ast.children[0])
        val2 = interpret(ast.children[1])
        if ast.value == "||":
            return val1 or val2
        elif ast.value == "&&":
            return val1 and val2
    elif ast.type == "equality_expression":
        val1 = interpret(ast.children[0])
        val2 = interpret(ast.children[1])
        if ast.value == "==":
            return val1 == val2
        elif ast.value == "!=":
            return val1 != val2
    elif ast.type == "switch_statement":
        varSw = ast.children[0].children[0].value
        ret = interpret(ast.children[1],varSw)
    elif ast.type == "case_statement":
        varSw = extraParam
        val = interpret(ast.children[0])
        if symbolTable.lookupSymbol(varSw) == val:              
            return interpret(ast.children[1])
    elif ast.type == "default_statement":
        interpret(ast.children[0])
    elif ast.type == "if_else_statement":
        size = len(ast.children)
        if size == 2: #if number of elements in ast.children is 2
            if interpret(ast.children[0]):
                return interpret(ast.children[1])
        elif size == 3:
            if interpret(ast.children[0]):
                return interpret(ast.children[1])
            else:
                return interpret(ast.children[2])
    elif ast.type == "while_statement":
        while interpret(ast.children[0]):
            ret = interpret(ast.children[1])
            if ret == "break":
                break;
            elif ret == "continue":
                continue;
    elif ast.type == "for_statement":
        interpret(ast.children[0])
        while interpret(ast.children[1]):
            ret = interpret(ast.children[3])
            interpret(ast.children[2])
            if ret == "break":
                break;
            elif ret == "continue":
                continue;
    elif ast.type == "do_while_statement":
        ret = interpret(ast.children[0])
        if ret != "break":
            while interpret(ast.children[1]):
                ret = interpret(ast.children[0])
                if ret == "break":
                    break;
                elif ret == "continue":
                    continue;
    elif ast.type == "return_statement":
        val = interpret(ast.children[0])
        return val
    elif ast.type == "jump_statement":
        if ast.value == "putol":
            return "break";
        elif ast.value == "tuloy":
            return "continue"

def i_error(msg):
    print "Interpreter error: ", msg
    exit(1)

