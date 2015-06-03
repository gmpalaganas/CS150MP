from parser.lexer import runLexer
from parser.interpreter import interpret
from parser.parser import runParser
import sys

def main():
    #print runParser(sys.argv[1])
    ast = runParser(sys.argv[1])
    interpret(ast) 

if __name__ == "__main__":
    main()
