from parser.lexer import runLexerOnFile
import sys

def main():
    runLexerOnFile(sys.argv[1])

if __name__ == "__main__":
    main()
