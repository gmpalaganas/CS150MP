import parser

def interpret(ast):
    if ast.type == "start":
        for child in ast.children:
            interpret(child)
        return None
    elif ast.type == "main":
        interpret(ast.children[0])
        return None
    elif ast.type == "compound_statement":
        for child in ast.children:
            interpret(child)
        return None
    elif ast.type == "mix_list":
        for child in ast.children:
            interpret(child)
        return None
    elif ast.type == "print_expression":
        msg = interpret(ast.children[0])
        print msg
        return None
    elif ast.type == "str_constant":
        return ast.value
