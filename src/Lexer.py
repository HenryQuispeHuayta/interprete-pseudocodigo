from src.Constants import *
from src.Errors import *
from src.Position import Position
from src.Token import Token

class Lexer:
  def __init__(self, fn, text):
    self.fn = fn
    self.text = text
    self.pos = Position(-1, 0, -1, fn, text)
    self.currentChar = None
    self.advance()

  def advance(self):
    self.pos.advance(self.currentChar)
    self.currentChar = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

  def makeTokens(self):
    tokens = []

    while self.currentChar != None:
      if self.currentChar in ' \t':
        self.advance()
      elif self.currentChar == '#':
        self.skipComment()
      elif self.currentChar in ';\n':
        tokens.append(Token(TT_NEWLINE, posStart=self.pos))
        self.advance()
      elif self.currentChar in DIGITS + ".":
        token, error = self.makeNumber()
        if error: return [], error
        tokens.append(token)
      elif self.currentChar in LETTERS:
        tokens.append(self.makeIdentifier())
      elif self.currentChar == '"':
        tokens.append(self.makeString())
      elif self.currentChar == '(':
        tokens.append(Token(TT_LPAREN, posStart=self.pos, posEnd=self.pos))
        self.advance()
      elif self.currentChar == ')':
        tokens.append(Token(TT_RPAREN, posStart=self.pos, posEnd=self.pos))
        self.advance()
      elif self.currentChar == '[':
        tokens.append(Token(TT_LSQUARE, posStart=self.pos, posEnd=self.pos))
        self.advance()
      elif self.currentChar == ']':
        tokens.append(Token(TT_RSQUARE, posStart=self.pos, posEnd=self.pos))
        self.advance()
      elif self.currentChar == '%':
        tokens.append(Token(TT_MOD, posStart=self.pos, posEnd=self.pos))
        self.advance()
      elif self.currentChar == ',':
        tokens.append(Token(TT_COMMA, posStart=self.pos, posEnd=self.pos))
        self.advance()
      elif self.currentChar == '=':
        tokens.append(self.makeEquals())
      elif self.currentChar == '+':
        tokens.append(Token(TT_PLUS, posStart=self.pos, posEnd=self.pos))
        self.advance()
      elif self.currentChar == '-':
        tokens.append(Token(TT_MINUS, posStart=self.pos, posEnd=self.pos))
        self.advance()
        # tokens.append(Token(self.makeMinusOrArrow()))
      elif self.currentChar == '*':
        tokens.append(Token(TT_MUL, posStart=self.pos, posEnd=self.pos))
        self.advance()
      elif self.currentChar == '/':
        tokens.append(Token(TT_DIV, posStart=self.pos, posEnd=self.pos))
        self.advance()
      elif self.currentChar == '^':
        tokens.append(Token(TT_POW, posStart=self.pos, posEnd=self.pos))
        self.advance()
      elif self.currentChar == '!':
        token, error = self.makeNotEquals()
        if error: return [], error
        tokens.append(token)
      elif self.currentChar == '<':
        tokens.append(self.makeLessThan())
      elif self.currentChar == '>':
        tokens.append(self.makeGreaterThan())
      else:
        char = self.currentChar
        if char != " ":
          posStart = self.pos.copy()
          self.advance()
          return [], IllegalCharError(posStart, self.pos, char)
        else:
          self.advance()
    
    tokens.append(Token(TT_EOF, posStart=self.pos))
    return tokens, None

  def makeNumber(self):
    numStr = ''
    dotCount = 0
    posStart = self.pos.copy()

    while self.currentChar != None and self.currentChar in DIGITS + '.':
      if self.currentChar == '.':
        if dotCount == 1: break
        dotCount += 1
        numStr += '.'
      else:
        numStr += self.currentChar
      self.advance()

    if numStr[0] != '.':
      if dotCount == 0:
        return Token(TT_INT, int(numStr), posStart, self.pos), None
      else:
        return Token(TT_FLOAT, float(numStr), posStart, self.pos), None
    else:
      numStr = '0' + numStr
      return Token(TT_FLOAT, float(numStr), posStart, self.pos), None

  def makeString(self):
    string = ''
    posStart = self.pos.copy()
    escapeCharacter = False
    self.advance()

    escapeCharacters = {
      'n': '\n',
      't': '\t'
    }

    while self.currentChar != None and (self.currentChar != '"' or escapeCharacter):
      if escapeCharacter:
        string += escapeCharacters.get(self.currentChar, self.currentChar)
        escapeCharacter = False
      else:
        if self.currentChar == '\\':
          escapeCharacter = True
        else:
          string += self.currentChar
      self.advance()

    self.advance()
    return Token(TT_STRING, string, posStart, self.pos)

  def makeIdentifier(self, nextChar=None):
    idStr = ''
    posStart = self.pos.copy()

    if nextChar == None:
      while self.currentChar != None and self.currentChar in LETTERS:
        idStr += self.currentChar
        self.advance()
    else:
      idStr = nextChar

    tokType = TT_KEYWORD if idStr.lower() in KEYWORDS else TT_IDENTIFIER
    return Token(tokType, idStr, posStart, self.pos)

  def makeEquals(self):
    tokType = TT_EQ
    posStart = self.pos.copy()
    self.advance()

    if self.currentChar == '=':
      self.advance()
      tokType = TT_EE

    return Token(tokType, posStart=posStart, posEnd=self.pos)

  def makeNotEquals(self):
    posStart = self.pos.copy()
    self.advance()

    if self.currentChar == '=':
      self.advance()
      return Token(TT_NE, posStart=posStart, posEnd=self.pos), None

    self.advance()
    return None, ExpectedCharError(posStart, self.pos, errorDetails['equalsAfterNotExpected'])

  def makeLessThan(self):
    tokType = TT_LT
    posStart = self.pos.copy()
    self.advance()

    if self.currentChar == '=':
      self.advance()
      tokType = TT_LTE

    return Token(tokType, posStart=posStart, posEnd=self.pos)

  def makeGreaterThan(self):
    tokType = TT_GT
    posStart = self.pos.copy()
    self.advance()

    if self.currentChar == '=':
      self.advance()
      tokType = TT_GTE

    return Token(tokType, posStart=posStart, posEnd=self.pos)

  def makeMinusOrArrow(self):
    tokType = TT_MINUS
    posStart = self.pos.copy()
    self.advance()

    if self.currentChar == '>':
      self.advance()
      tokType = TT_ARROW

    return Token(tokType, posStart=posStart, posEnd=self.pos)

  def skipComment(self):
    while self.currentChar != '\n' and self.currentChar != None:
      self.advance()

