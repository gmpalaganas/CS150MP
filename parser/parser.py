import lexer
import profile
import logging
import ply.yacc as yacc 
tokens = lexer.tokens

'''
REMAINING TASKS:
    >Code Generator/Executor
        >Note: Use the AST produced by the parser it is the output of runParser() 
            >see runParser()

ON AST:
What does this all mean?
To put it simply:
    >type -> what is the current node? is it a statement? an identifier? etc
          -> this will define what you will do with the node
    >children -> you can think of this as the parameters of the node
              -> basically you have to (depending on the node type) these first to be able to evaluate this node
    >leaf -> this contains the "operation" to be done in this node
          -> Examples:
            ASTNode("print_statement", ASTNode("constant","Hello World") , "sulat") == sulat("Hello World")

            ASTNode("if_statement", [ 
                ASTNode("relational_expression", [ 
                    ASTNode("identifier", bilang_x),
                    ASTNode("constant", 3) 
                ], "<"),
                ASTNode("print_statement", "Hello World", "sulat") 
            ], "kung") == 
                
                kung( bilang_x < 3) sulat("Hello World")
'''

class ASTNode:
    def __init__(self,type,children=None,leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = [ ]
        self.leaf = leaf

    def toString(self,prefix=0):
        if self.leaf:
            leaf_str = self.leaf
        else:
            leaf_str = "None"
        
        msg = ""

        if prefix > 0:
            msg += (prefix - 1) * "\t"

        msg = "AST Node \"%s\":\n" % self.type
        msg += prefix * "\t" + "Value: %s\n" % leaf_str 
        msg +=  prefix * "\t" +"Children:\n"
            
        if len(self.children) == 0:
            msg += prefix * "\t" + "\tNo Children\n"
        else:
            for child in self.children:
                if isinstance(child, ASTNode):
                    msg += prefix * "\t" + "\t" + child.toString(prefix + 1)
                else:
                    msg += prefix * "\t" + "\t" + child.__str__()
            msg += "\n"

        return msg

    
    def __str__(self):
        return self.toString()

def p_start(p):
    'start : external_declaration main external_declaration'
    #Root of the tree
    p[0] = ASTNode("start", [ p[1], p[2], p[3] ])

def p_external_declaration_1(p):
    '''
    external_declaration : assignment_expression external_declaration
                         | fxn_var_statement external_declaration
    '''
    p[0] = ASTNode("external_declaration", [ p[1], p[2] ] )

def p_external_declaration_3(p):
    'external_declaration : empty'
    p[0] = ASTNode("empty")

def p_main(p):
    'main : MAIN LPAREN empty RPAREN compound_statement'
    p[0] = ASTNode("main", [ p[5] ], p[1])

def p_fxn_var_statement_1(p):
    '''
    fxn_var_statement : fxn_prot
                      | fxn_definition
    '''
    p[0] = p[1]

def p_declaration(p):
    'declaration : init_declarator_list SEMI'
    p[0] = p[1]

def p_declaration_list_1(p):
    'declaration_list : declaration'
    p[0] = p[1]

def p_declaration_list_2(p):
    'declaration_list : declaration_list declaration'
    p[0] = ASTNode("declaration_list", [ p[1], p[2] ])

def p_init_declarator_list_1(p):
    'init_declarator_list : init_declarator'
    p[0] = p[1]

def p_init_declaration_list_2(p):
    'init_declarator_list : init_declarator_list COMMA init_declarator'
    p[0] = ASTNode("init_declarator_list", [ p[1], p[3] ])

def p_init_declarator_1(p):
    'init_declarator : declarator'
    p[0] = p[1]

# Variable declaration with initialization e.g. @bilang_a  += x
def p_init_declarator_2(p):
    'init_declarator : declarator ASSIGN_OP initializer'
    p[0] = ASTNode("init_declarator", [ p[1], p[3] ], p[2])

# Variable declaration e.g @bilang_a
def p_declarator_1(p):
    '''
    declarator : VAR FLOAT_ID
               | VAR INT_ID
               | VAR CHAR_ID
               | VAR STR_ID
    '''
    p[0] = ASTNode("var_declarator",[ p[2] ], p[1]) 

def p_declarator_5(p):
    'declarator : LPAREN declarator RPAREN'
    p[0] = ASTNode("declarator", [ p[2] ])
 

def p_declarator_6(p):
    'declarator : declarator LBRACKET constant_expression_opt RBRACKET'
    p[0] = ASTNode("declarator", [ p[1], p[3] ])

def p_initializer_1(p):
    'initializer : assignment_expression'
    p[0] = p[1]

#array initializer {a,b,c,d}
def p_initializer_2(p):
    '''
    initializer : LBRACE initializer_list RBRACE
                | LBRACE initializer_list COMMA RBRACE
    '''
    p[0] = ASTNode("array_initializer_list", [ p[2] ])


def p_initializer_list_1(p):
    'initializer_list : initializer'
    p[0] = ASTNode("initializer_list", [ p[1] ])

def p_initializer_list_2(p):
    'initializer_list : initializer_list COMMA initializer'
    p[0] = ASTNode("initializer_list", [ p[1] , p[3] ])

def p_fxn_prot(p):
    'fxn_prot 		: fxn_declaration SEMI'
    p[0] = ASTNode("fxn_prototype", [ p[1] ])

def p_fxn_definition(p):
    'fxn_definition : fxn_declaration compound_statement'
    p[0] = ASTNode("fxn_declaration", [ p[1], p[2] ])

def p_fxn_declaration_1(p):
    'fxn_declaration : VAR identifier LPAREN fxn_prot_args RPAREN'
    p[0] = ASTNode("fxn_declaration", [ p[2], p[4] ], p[1])

def p_fxn_declaration_2(p):
    'fxn_declaration : VAR identifier LPAREN empty RPAREN'
    p[0] = ASTNode("fxn_declaration", [ p[2] ], p[1])

def p_fxn_prot_args_1(p):
    'fxn_prot_args : identifier COMMA fxn_prot_args'
    p[0] = ASTNode("fxn_args", [ p[1], p[3] ], p[2]) 

def p_fxn_prot_args_2(p):
    'fxn_prot_args : identifier'
    p[0] = ASTNode("fxn_args", [ p[1] ])

#statement
def p_statement(p):
    '''
    statement : labeled_statement
              | expression_statement
              | compound_statement
              | selection_statement
              | iteration_statement
              | jump_statement
              | io_statement
    '''
    p[0] = p[1]
    pass

def p_io_statement_1(p):
    'io_statement : PRINT LPAREN logical_or_expression RPAREN'
    p[0] = ASTNode("print_statement", [ p[3] ], p[1])

def p_io_statement_2(p):
    'io_statement : SCAN LPAREN RPAREN'
    p[0] = ASTNode("scan_statement", leaf=p[1])

def p_labeled_statement_1(p):
    'labeled_statement : CASE constant_expression COLON statement'
    p[0] = ASTNode("case_statement", [ p[2], p[4] ], p[1])

def p_labeled_statement_2(p):
    'labeled_statement : DEFAULT COLON statement'
    p[0] = ASTNode("default_statement", [ p[3] ] , p[1])

def p_expression_statement(p):
    'expression_statement : expression_opt SEMI'
    p[0] = p[1]

def p_compound_statement_1(p):
    'compound_statement : LBRACE declaration_list statement_list RBRACE'
    p[0] = ASTNode("compound_statement", [ p[2], p[3] ])


def p_compund_statement_2(p):
    '''
    compound_statement : LBRACE statement_list RBRACE
                       | LBRACE declaration_list RBRACE
    '''
    p[0] = p[2]

def p_compund_statement_4(p):
    'compound_statement : LBRACE RBRACE'
    p[0] = ASTNode("empty_compound_statement")

def p_statement_list_1(p):
    'statement_list : statement'
    p[0] = p[1]

def p_statement_list_2(p):
    'statement_list : statement_list statement'
    p[0] = p[1]

'''
If ever mag-taka kayo bakit walang ELSE IF kasi may magic
at yun ay if you see sa dulo ng if-else gramar eh statment yung nandun 
and if you see selection statement is a statement soooo.... magic
ma-gegets nyo rin
'''
def p_selection_statement_1(p):
    'selection_statement : IF LPAREN expression RPAREN statement'
    p[0] = ASTNode("if_else_statement", [ p[3], p[5] ], p[1])

def p_selection_statement_2(p):
    'selection_statement : IF LPAREN expression RPAREN statement ELSE statement '
    p[0] = ASTNode("if_else_statement", [ p[3], p[5], p[7] ], p[1])

def p_else_if_statement_2(p):
    'else_if_statement : empty'
    p[0] = ASTNode("empty")

def p_selection_statement_3(t):
    'selection_statement : SWITCH LPAREN expression RPAREN statement '
    p[0] = ASTNode("switch_statement", [ p[3], p[5] ], p[1])


def p_iteration_statement_1(t):
    'iteration_statement : WHILE LPAREN expression RPAREN statement'
    p[0] = ASTNode("while_statement", [ p[3], p[5] ], p[1])

def p_iteration_statement_2(t):
    'iteration_statement : FOR LPAREN expression_opt SEMI expression_opt SEMI expression_opt RPAREN statement '
    p[0] = ASTNode("for_statement", [ p[3], p[5], p[7], p[9] ], p[1] )

def p_iteration_statement_3(t):
    'iteration_statement : DO statement WHILE LPAREN expression RPAREN SEMI'
    p[0] = ASTNode("do_while_statement", [ p[2], p[5] ], p[1] )

def p_jump_statement_1(p):
    '''
    jump_statement : CONTINUE SEMI
                   | BREAK SEMI
    '''
    p[0] = ASTNode("jump_statement", leaf=p[1])

def p_jump_statement_3(p):
    'jump_statement : RETURN expression_opt SEMI'
    p[0] = ASTNode("return_statement", [ p[2] ], p[1])

def p_expression_opt_1(p):
    'expression_opt : empty'
    pass

def p_expression_opt_2(p):
    'expression_opt : expression'
    p[0] = p[1]

def p_expression_1(p):
    'expression : assignment_expression'
    p[0] = p[1]

def p_expression_2(p):
    'expression : expression COMMA assignment_expression'
    p[0] = ASTNode("expression", [ p[1], p[3] ], p[2])

def p_assignment_expression_1(p):
    'assignment_expression : conditional_expression'
    p[0] = p[1]

def p_assignment_expression_2(p):
    '''
    assignment_expression : unary_expression ASSIGN_OP assignment_expression
                          | unary_expression ADD_ASSIGN assignment_expression
                          | unary_expression MIN_ASSIGN assignment_expression
                          | unary_expression MUL_ASSIGN assignment_expression
                          | unary_expression DIV_ASSIGN assignment_expression
                          | unary_expression MOD_ASSIGN assignment_expression
    '''
    p[0] = ASTNode("assignment_expression", [ p[1], p[3] ], p[2])

# (cond)?exp:exp;
def p_conditional_expression_1(p):
    'conditional_expression : logical_or_expression'
    p[0] = p[1]

def p_conditional_expression_2(p):
    'conditional_expression : logical_or_expression COND_OP expression COLON conditional_expression '
    p[0] = ASTNode("ternary_expression", [p[1], p[3], p[5]], p[2])

def p_constant_expression_opt_1(p):
    'constant_expression_opt : empty'
    pass

def p_constant_expression_opt_2(p):
    'constant_expression_opt : constant_expression'
    p[0] = p[1]

def p_constant_expression(p):
    'constant_expression : conditional_expression'
    p[0] = p[1]

def p_logical_or_expression_1(p):
    'logical_or_expression : logical_and_expression'
    p[0] = p[1]

def p_logical_or_expression_2(p):
    'logical_or_expression : logical_and_expression OR logical_or_expression'
    p[0] = ASTNode("logical_expression", [ p[1], p[3] ], p[2] )

def p_logical_and_expression_1(p):
    'logical_and_expression : equality_expression'
    p[0] = p[1]

def p_logical_and_expression_2(p):
    'logical_and_expression : logical_and_expression AND equality_expression'
    p[0] = ASTNode("logical_expression", [ p[1], p[3] ], p[2] )

def p_equality_expression_1(p):
    'equality_expression : relational_expression'
    p[0] = p[1]

def p_equality_expression_2(p):
    '''
    equality_expression : equality_expression EQ relational_expression
                        | equality_expression NEQ relational_expression
    '''
    p[0] = ASTNode("equality_expression", [ p[1], p[3] ], p[2] )

def p_relational_expression_1(p):
    'relational_expression : add_expression'
    p[0] = p[1]

def p_relational_expression_2(p):
    '''
    relational_expression : relational_expression LT add_expression
                          | relational_expression GT add_expression
                          | relational_expression LE add_expression
                          | relational_expression GE add_expression
    '''
    p[0] = ASTNode("relational_expression", [ p[1], p[3] ], p[2])

def p_add_expression_1(p):
    'add_expression : mult_expression'
    p[0] = p[1]

def p_add_expression_2(p):
    '''
    add_expression : add_expression ADD_OP mult_expression
                   | add_expression SUB_OP mult_expression
    '''
    p[0] = ASTNode("binary_expression", [ p[1], p[3] ], p[2])


def p_mult_expression_1(p):
    'mult_expression : unary_expression'
    p[0] = p[1]

def p_mult_expression_2(p):
    '''
    mult_expression : mult_expression MULT_OP unary_expression
                    | mult_expression DIV_OP unary_expression
                    | mult_expression MOD_OP unary_expression
    '''
    p[0] = ASTNode("binary_expression", [ p[1], p[3] ], p[2])


def p_unary_expression_1(p):
    'unary_expression : postfix_expression'
    p[0] = p[1]
    pass

def p_unary_expression_2(p):
    '''
    unary_expression : INC unary_expression
                     | DEC unary_expression
                     | SUB_OP add_expression
                     | NOT logical_or_expression
    '''
    p[0] = ASTNode("unary_expression", [ p[2] ], p[1])

def p_postfix_expression_1(p):
    'postfix_expression : primary_expression'
    p[0] = p[1]

def p_postfix_expression_2(p):
    'postfix_expression : postfix_expression LBRACKET expression RBRACKET'
    p[0] =  ASTNode("array",[ p[1], p[3] ])

#Function Call
def p_postfix_expression_3(p):
    'postfix_expression : postfix_expression LPAREN argument_expression_list RPAREN'
    p[0] = ASTNode("function_call", [ p[1], p[3] ]) 

#Function Call with no arguments
def p_postfix_expression_4(p):
    'postfix_expression : postfix_expression LPAREN RPAREN'
    p[0] =  ASTNode("function_call", [ p[1] ])

def p_postfix_expression_5(p):
    '''
    postfix_expression : postfix_expression INC
                       | postfix_expression DEC
    '''
    p[0] = ASTNode("postfix_expression", [ p[1] ], p[2])

def p_primary_expression_1(p):
    'primary_expression : identifier'
    p[0] = p[1]

def p_primary_expression_2(p):
    'primary_expression : constant'
    p[0] = p[1]

def p_primary_expression_3(p):
    'primary_expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_argument_expression_list_1(p):
    'argument_expression_list : assignment_expression'
    p[0] = p[1]
    pass

def p_argument_expression_list_2(p):
    'argument_expression_list : argument_expression_list COMMA assignment_expression'
    p[0] = ASTNode("argument_expression_list",[ p[1], p[3] ])

def p_identifier(p):
    '''
    identifier : FLOAT_ID 
               | INT_ID
               | CHAR_ID
               | STR_ID
    '''
    p[0] = ASTNode("identifier", leaf =  p[1] )
    
    pass

def p_constant(p):
    '''
    constant : FLOAT_LIT
             | INT_LIT
             | CHAR_LIT
             | STR_LIT
    '''
    p[0] = ASTNode("constant",  leaf = p[1] )    
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
    return parser.parse(data)

def runParser(file_name):
    puto_file = open(file_name, "r")
    data = puto_file.read()
    ast = parseString(data)
    puto_file.close()
    return ast
