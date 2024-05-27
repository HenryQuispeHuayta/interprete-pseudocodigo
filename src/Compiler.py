from src.Context import Context
from src.Interpreter import Interpreter
from src.Lexer import Lexer
from src.Parser import Parser
from src.BuildInConst import globalSymbolTable

def run(fn, text):
  lexer = Lexer(fn, text)
  tokens, error = lexer.makeTokens()
  
  if error: return None, error

  parser = Parser(tokens)
  ast = parser.parse()
  if ast.error: return None, ast.error

  interpreter = Interpreter()
  context = Context('main')
  context.symbolTable = globalSymbolTable
  result = interpreter.visit(ast.node, context)

  return result.value, result.error
