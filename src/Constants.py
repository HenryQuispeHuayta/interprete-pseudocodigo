import string

# Constants
DIGITS = "0123456789"
LETTERS = string.ascii_letters + "ñÑ"
LETTERS_DIGITS = LETTERS + DIGITS

# Tokens Types
# TT_DOT = "DOT"
TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_STRING = "STRING"
TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_MOD = "MOD"
TT_POW = "POW"
TT_EQ = "EQ"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_LSQUARE = "LSQUARE"
TT_RSQUARE = "RSQUARE"
TT_EE = "EE"
TT_MM = "MM"
TT_NE = "NE"
TT_LT = "LT"
TT_GT = "GT"
TT_LTE = "LTE"
TT_GTE = "GTE"
TT_COMMA = "COMMA"
TT_ARROW = "ARROW"
TT_NEWLINE = "NEWLINE"
TT_EOF = "EOF"

KEYWORDS = [
  "var",
  "y",
  "o",
  "no",
  "si",
  "entonces",
  "osi",
  "sino",
  "fora",
  "hasta",
  "de",
  "mientras",
  "funcion",
  "fin",
  "retornar",
  "continuar",
  "romper",
]

errorMesaages = {
  "IllegalCharError": "Caracter ilegal",
  "InvalidSyntaxError": "Sintaxis invalida",
  "ExpectedCharError": "Caracter esperado",
  "InvalidIndentationError": "Indentacion invalida",
  "InvalidTokenError": "Token invalido",
  "RunTimeError": "Error en tiempo de ejecucion",
  "ReturnError": "Error de retorno",
}

errorDetails = {
  "intOrFloatExpected": "Se esperaba un entero o un flotante",
  "expExpected": "Se esperaba un exponente",
  "operationExpected": "Se esperaba una operacion",
  "openParenExpected": "Se esperaba '('",
  "closeParenExpected": "Se esperaba ')'",
  "identifierExpected": "Se esperaba un identificador",
  "equalExpected": "Se esperaba '='",
  "equalAfterIdentifierExpected": "Se esperaba '=' despues del identificador",
  "equalAfterNotExpected": "Se esperaba '!='",
  "zeroDivisionError": "Division por cero",
  "unknowVariable": "Variable desconocida",
  "lenguageSyntaxError": "Error de sintaxis del lenguaje",
  "illegalOperationError": "Operacion no soportada",
  "indexOutOfBoundsError": "Indice fuera de rango",
  "listIndexError": "Indice de lista invalido",
  "tooManyArgsError": "Demasiados argumentos",
  "tooFewArgsError": "Faltan argumentos",
  "invalidTypeError": "Tipo invalido",
  "invalidFileNameError": "La extension del archivo debe ser '.inf'",
  "runTimeError": "Error en tiempo de ejecucion {}",
  "exprExpected": "Se esperaba una expresion",
  "rsquareExpected": "Se esperaba ']'",
  "lsquareExpected": "Se esperaba '['",
  "endExpected": "Se esperaba 'fin'",
  "ifExpected": "Se esperaba 'si'",
  "thenExpected": "Se esperaba 'entonces'",
  "forExpected": "Se esperaba 'para'",
  "equalsExpected": "Se esperaba '=='",
  "toExpected": "Se esperaba 'a'",
  "funcExpected": "Se esperaba 'funcion'",
  "newlineExpected": "Se esperaba un salto de linea",
  "varNotDefined": "Variable '{}' no definida",
  "equalsAfterNotExpected": "Se esperaba '=' despues de '!'",
  "toIntError": "No se puede convertir a entero '{}'",
  "invalidTypeError": "Tipo invalido '{}' para '{}'",
  "toFloatError": "No se puede convertir a flotante '{}'",
  "missingArgsError": "Faltan argumentos en la llamada a '{}'",
}
