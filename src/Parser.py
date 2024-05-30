from src.Constants import *
from src.Errors import InvalidSyntaxError
from src.ParserResult import ParserResult
from src.Nodes import *

class Parser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.tokIdx = -1
    self.advance()

  def advance(self):
    self.tokIdx += 1
    self.updateCurrentTok()
    return self.currentTok

  def reverse(self, amount=1):
    self.tokIdx -= amount
    self.updateCurrentTok()
    return self.currentTok

  def updateCurrentTok(self):
    if self.tokIdx >= 0 and self.tokIdx < len(self.tokens):
      self.currentTok = self.tokens[self.tokIdx]

  def parse(self):
    res = self.statements()
    if not res.error and self.currentTok.type != TT_EOF:
      return res.failure(InvalidSyntaxError(
        self.currentTok.posStart, self.currentTok.posEnd,
        errorDetails['exprExpected']
      ))
    return res

  def statements(self):
    res = ParserResult()
    statements = []
    posStart = self.currentTok.posStart.copy()

    while self.currentTok.type == TT_NEWLINE:
      res.registerAdvancement()
      self.advance()

    statement = res.register(self.statement())
    if res.error: return res
    statements.append(statement)

    moreStatements = True

    while True:
      newlineCount = 0
      while self.currentTok.type == TT_NEWLINE:
        res.registerAdvancement()
        self.advance()
        newlineCount += 1
      if newlineCount == 0:
        moreStatements = False

      if not moreStatements: break
      statement = res.tryRegister(self.statement())
      if not statement:
        self.reverse(res.toReverseCount)
        moreStatements = False
        continue
      statements.append(statement)

    return res.success(ListNode(
      statements,
      posStart,
      self.currentTok.posEnd.copy()
    ))

  def statement(self):
    res = ParserResult()
    posStart = self.currentTok.posStart.copy()

    if self.currentTok.matches(TT_KEYWORD, 'retornar'):
      res.registerAdvancement()
      self.advance()

      expr = res.tryRegister(self.expr())
      if not expr:
        self.reverse(res.toReverseCount)
      return res.success(ReturnNode(expr, posStart, self.currentTok.posStart.copy()))

    if self.currentTok.matches(TT_KEYWORD, 'continuar'):
      res.registerAdvancement()
      self.advance()
      return res.success(ContinueNode(posStart, self.currentTok.posStart.copy()))

    if self.currentTok.matches(TT_KEYWORD, 'romper'):
      res.registerAdvancement()
      self.advance()
      return res.success(BreakNode(posStart, self.currentTok.posStart.copy()))

    expr = res.register(self.expr())
    if res.error:
      return res.failure(InvalidSyntaxError(
        self.currentTok.posStart, self.currentTok.posEnd,
        errorDetails['exprExpected']
      ))

    return res.success(expr)

  def expr(self):
    res = ParserResult()

    if self.currentTok.matches(TT_KEYWORD, 'var'):
      res.registerAdvancement()
      self.advance()

      if self.currentTok.type != TT_IDENTIFIER:
        return res.failure(InvalidSyntaxError(
          self.currentTok.posStart, self.currentTok.posEnd,
          errorDetails['identifierExpected']
        ))

      varName = self.currentTok
      res.registerAdvancement()
      self.advance()

      while self.currentTok.type == TT_COMMA:
        self.advance()
        
        if self.currentTok.type != TT_IDENTIFIER:
          return res.failure(InvalidSyntaxError(
            self.currentTok.posStart, self.currentTok.posEnd,
            errorDetails['identifierExpected']
          ))

        varName.append(self.currentTok)
        self.advance()

      if self.currentTok.type != TT_EQ:
        return res.failure(InvalidSyntaxError(
          self.currentTok.posStart, self.currentTok.posEnd,
          errorDetails['equalsExpected']
        ))

      res.registerAdvancement()
      self.advance()
      expr = res.register(self.expr())
      if res.error: return res
      return res.success(VarAssignNode(varName, expr))

    node = res.register(self.binOp(self.compExpr, ((TT_KEYWORD, 'y'), (TT_KEYWORD, 'o'))))

    if res.error:
      return res.failure(InvalidSyntaxError(
        self.currentTok.posStart, self.currentTok.posEnd,
        errorDetails['exprExpected']
      ))

    return res.success(node)

  def compExpr(self):
    res = ParserResult()

    if self.currentTok.matches(TT_KEYWORD, 'no'):
      opTok = self.currentTok
      res.registerAdvancement()
      self.advance()

      node = res.register(self.compExpr())
      if res.error: return res
      return res.success(UnaryOpNode(opTok, node))

    node = res.register(self.binOp(self.arithExpr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE, TT_MM)))

    if res.error:
      return res.failure(InvalidSyntaxError(
        self.currentTok.posStart, self.currentTok.posEnd,
        errorDetails['exprExpected']
      ))

    return res.success(node)

  def arithExpr(self):
    return self.binOp(self.term, (TT_PLUS, TT_MINUS))

  def term(self):
    return self.binOp(self.factor, (TT_MUL, TT_DIV, TT_MOD))

  def factor(self):
    res = ParserResult()
    tok = self.currentTok

    if tok.type in (TT_PLUS, TT_MINUS):
      res.registerAdvancement()
      self.advance()
      factor = res.register(self.factor())
      if res.error: return res
      return res.success(UnaryOpNode(tok, factor))

    return self.power()

  def power(self):
    return self.binOp(self.call, (TT_POW,), self.factor) # TODO: check this

  def call(self):
    res = ParserResult()
    atom = res.register(self.atom())
    if res.error: return res

    if self.currentTok.type == TT_LSQUARE:
      res.registerAdvancement()
      self.advance()
      node = res.register(self.expr())
      
      if res.error:
        return res.failure(InvalidSyntaxError(
          self.currentTok.posStart, self.currentTok.posEnd,
          errorDetails['exprExpected']
        ))
      
      if self.currentTok.type != TT_RSQUARE:
        return res.failure(InvalidSyntaxError(
          self.currentTok.posStart, self.currentTok.posEnd,
          errorDetails['rsquareExpected']
        ))

      res.registerAdvancement()
      self.advance()
      return res.success(CallListNode(atom, node))

    if self.currentTok.type == TT_LPAREN:
      res.registerAdvancement()
      self.advance()
      argNodes = []

      if self.currentTok.type == TT_RPAREN:
        res.registerAdvancement()
        self.advance()
      else:
        argNodes.append(res.register(self.expr()))
        if res.error:
          return res.failure(InvalidSyntaxError(
            self.currentTok.posStart, self.currentTok.posEnd,
            errorDetails['exprExpected']
          ))

        while self.currentTok.type == TT_COMMA:
          res.registerAdvancement()
          self.advance()

          argNodes.append(res.register(self.expr()))
          if res.error: return res

        if self.currentTok.type != TT_RPAREN:
          return res.failure(InvalidSyntaxError(
            self.currentTok.posStart, self.currentTok.posEnd,
            errorDetails['closeParenExpected']
          ))

        res.registerAdvancement()
        self.advance()

      return res.success(CallNode(atom, argNodes))
    return res.success(atom)

  def atom(self):
    res = ParserResult()
    tok = self.currentTok

    if tok.type in (TT_INT, TT_FLOAT):
      res.registerAdvancement()
      self.advance()
      return res.success(NumberNode(tok))

    if tok.type == TT_STRING:
      res.registerAdvancement()
      self.advance()
      return res.success(StringNode(tok))

    elif tok.type == TT_IDENTIFIER:
      res.registerAdvancement()
      self.advance()
      return res.success(VarAccessNode(tok))

    elif tok.type == TT_LPAREN:
      res.registerAdvancement()
      self.advance()
      expr = res.register(self.expr())
      if res.error: return res
      if self.currentTok.type == TT_RPAREN:
        res.registerAdvancement()
        self.advance()
        return res.success(expr)
      else:
        return res.failure(InvalidSyntaxError(
          self.currentTok.posStart, self.currentTok.posEnd,
          errorDetails['closeParenExpected']
        ))

    elif tok.type == TT_LSQUARE:
      listNode = res.register(self.listExpr())
      if res.error: return res
      return res.success(listNode)

    elif tok.matches(TT_KEYWORD, 'si'):
      ifExpr = res.register(self.ifExpr())
      if res.error: return res
      return res.success(ifExpr)

    elif tok.matches(TT_KEYWORD, 'para'):
      forExpr = res.register(self.forExpr())
      if res.error: return res
      return res.success(forExpr)

    elif tok.matches(TT_KEYWORD, 'mientras'):
      whileExpr = res.register(self.whileExpr())
      if res.error: return res
      return res.success(whileExpr)

    elif tok.matches(TT_KEYWORD, 'funcion'):
      funcDef = res.register(self.funcDef())
      if res.error: return res
      return res.success(funcDef)

    elif tok.type == TT_NEWLINE:
      self.advance()
      statement = res.register(self.statement())
      if res.error: return res
      return res.success(statement)

    return res.failure(InvalidSyntaxError(
      tok.posStart, tok.posEnd,
      errorDetails['exprExpected']
    ))

  def listExpr(self):
    res = ParserResult()
    elementNodes = []
    posStart = self.currentTok.posStart.copy()

    if self.currentTok.type != TT_LSQUARE:
      return res.failure(InvalidSyntaxError(
        self.currentTok.posStart, self.currentTok.posEnd,
        errorDetails['lsquareExpected']
      ))

    res.registerAdvancement()
    self.advance()

    if self.currentTok.type == TT_RSQUARE:
      res.registerAdvancement()
      self.advance()
    else:
      elementNodes.append(res.register(self.expr()))
      if res.error:
        return res.failure(InvalidSyntaxError(
          self.currentTok.posStart, self.currentTok.posEnd,
          errorDetails['exprExpected']
        ))

      while self.currentTok.type == TT_COMMA:
        res.registerAdvancement()
        self.advance()

        elementNodes.append(res.register(self.expr()))
        if res.error: return res

      if self.currentTok.type != TT_RSQUARE:
        return res.failure(InvalidSyntaxError(
          self.currentTok.posStart, self.currentTok.posEnd,
          errorDetails['rsquareExpected']
        ))

      res.registerAdvancement()
      self.advance()

    return res.success(ListNode(
      elementNodes,
      posStart,
      self.currentTok.posEnd.copy()
    ))

  def ifExpr(self):
    res = ParserResult()
    allCases = res.register(self.ifExprCases('si'))
    if res.error: return res
    cases, elseCase = allCases
    return res.success(IfNode(cases, elseCase))

  def ifExprB(self):
    return self.ifExprCases('osi')

  def ifExprC(self):
    res = ParserResult()
    elseCase = None

    if self.currentTok.matches(TT_KEYWORD, 'sino'):
      res.registerAdvancement()
      self.advance()

      if self.currentTok.type == TT_NEWLINE:
        res.registerAdvancement()
        self.advance()

        statements = res.register(self.statements())
        if res.error: return res
        elseCase = (statements, True)

        if self.currentTok.matches(TT_KEYWORD, 'fin'):
          res.registerAdvancement()
          self.advance()
        else:
          return res.failure(InvalidSyntaxError(
            self.currentTok.posStart, self.currentTok.posEnd,
            errorDetails['endExpected']
          ))
      else:
        expr = res.register(self.statement())
        if res.error: return res
        elseCase = (expr, False)

    return res.success(elseCase)

  def ifExprBOrC(self):
    res = ParserResult()
    cases, elseCase = [], None

    if self.currentTok.matches(TT_KEYWORD, 'osi'):
      allCases = res.register(self.ifExprB())
      if res.error: return res
      cases, elseCase = allCases
    else:
      elseCase = res.register(self.ifExprC())
      if res.error: return res

    return res.success((cases, elseCase))

  def ifExprCases(self, caseKeyword):
    res = ParserResult()
    cases = []
    newElseCase = None

    if not self.currentTok.matches(TT_KEYWORD, caseKeyword):
      return res.failure(InvalidSyntaxError(
        self.currentTok.posStart, self.currentTok.posEnd,
        errorDetails['ifExpected']
      ))

    res.registerAdvancement()
    self.advance()

    condition = res.register(self.expr())
    if res.error: return res

    if not self.currentTok.matches(TT_KEYWORD, 'entonces'):
      return res.failure(InvalidSyntaxError(
        self.currentTok.posStart, self.currentTok.posEnd,
        errorDetails['thenExpected']
      ))

    res.registerAdvancement()
    self.advance()

    if self.currentTok.type == TT_NEWLINE:
      res.registerAdvancement()
      self.advance()

      statements = res.register(self.statements())
      if res.error: return res
      cases.append((condition, statements, True))

      if self.currentTok.matches(TT_KEYWORD, 'fin'):
        res.registerAdvancement()
        self.advance()
      else:
        allCases = res.register(self.ifExprBOrC())
        if res.error: return res
        newCases, newElseCase = allCases
        cases.extend(newCases)
    else:
      expr = res.register(self.statement())
      if res.error: return res
      cases.append((condition, expr, False))

      allCases = res.register(self.ifExprBOrC())
      if res.error: return res
      newCases, newElseCase = allCases
      cases.extend(newCases)

    return res.success((cases, newElseCase))

  def forExpr(self):
    res = ParserResult()

    if not self.currentTok.matches(TT_KEYWORD, 'para'):
      return res.failure(InvalidSyntaxError(
        self.currentTok.posStart, self.currentTok.posEnd,
        errorDetails['forExpected']
      ))

    res.registerAdvancement()
    self.advance()

    if self.currentTok.type != TT_IDENTIFIER:
      return res.failure(InvalidSyntaxError(
        self.currentTok.posStart, self.currentTok.posEnd,
        errorDetails['identifierExpected']
      ))

    varName = self.currentTok
    res.registerAdvancement()
    self.advance()

    if self.currentTok.type != TT_EQ:
      return res.failure(InvalidSyntaxError(
        self.currentTok.posStart, self.currentTok.posEnd,
        errorDetails['equalsExpected']
      ))

    res.registerAdvancement()
    self.advance()

    startValue = res.register(self.expr())
    if res.error: return res

    if not self.currentTok.matches(TT_KEYWORD, 'hasta'):
      return res.failure(InvalidSyntaxError(
        self.currentTok.posStart, self.currentTok.posEnd,
        errorDetails['toExpected']
      ))

    res.registerAdvancement()
    self.advance()

    endValue = res.register(self.expr())
    if res.error: return res

    if self.currentTok.matches(TT_KEYWORD, 'de'):
      res.registerAdvancement()
      self.advance()

      stepValue = res.register(self.expr())
      if res.error: return res
    else:
      stepValue = None

    if not self.currentTok.matches(TT_KEYWORD, 'entonces'):
      return res.failure(InvalidSyntaxError(
        self.currentTok.posStart, self.currentTok.posEnd,
        errorDetails['thenExpected']
      ))

    res.registerAdvancement()
    self.advance()

    if self.currentTok.type == TT_NEWLINE:
      res.registerAdvancement()
      self.advance()

      body = res.register(self.statements())
      if res.error: return res

      if not self.currentTok.matches(TT_KEYWORD, 'fin'):
        return res.failure(InvalidSyntaxError(
          self.currentTok.posStart, self.currentTok.posEnd,
          errorDetails['endExpected']
        ))

      res.registerAdvancement()
      self.advance()

      return res.success(ForNode(varName, startValue, endValue, stepValue, body, True))

    body = res.register(self.statement())
    if res.error: return res

    return res.success(ForNode(varName, startValue, endValue, stepValue, body, False))

  def whileExpr(self):
    res = ParserResult()

    if not self.currentTok.matches(TT_KEYWORD, 'mientras'):
      return res.failure(InvalidSyntaxError(
        self.currentTok.posStart, self.currentTok.posEnd,
        errorDetails['whileExpected']
      ))

    res.registerAdvancement()
    self.advance()

    condition = res.register(self.expr())
    if res.error: return res

    if not self.currentTok.matches(TT_KEYWORD, 'entonces'):
      return res.failure(InvalidSyntaxError(
        self.currentTok.posStart, self.currentTok.posEnd,
        errorDetails['thenExpected']
      ))

    res.registerAdvancement()
    self.advance()

    if self.currentTok.type == TT_NEWLINE:
      res.registerAdvancement()
      self.advance()

      body = res.register(self.statements())
      if res.error: return res

      if not self.currentTok.matches(TT_KEYWORD, 'fin'):
        return res.failure(InvalidSyntaxError(
          self.currentTok.posStart, self.currentTok.posEnd,
          errorDetails['endExpected']
        ))

      res.registerAdvancement()
      self.advance()

      return res.success(WhileNode(condition, body, True))

    body = res.register(self.statement())
    if res.error: return res

    return res.success(WhileNode(condition, body, False))

  def funcDef(self):
    res = ParserResult()

    if not self.currentTok.matches(TT_KEYWORD, 'funcion'):
      return res.failure(InvalidSyntaxError(
        self.currentTok.posStart, self.currentTok.posEnd,
        errorDetails['funcExpected']
      ))

    res.registerAdvancement()
    self.advance()

    if self.currentTok.type == TT_IDENTIFIER:
      varNameToken = self.currentTok
      res.registerAdvancement()
      self.advance()
      if self.currentTok.type != TT_LPAREN:
        return res.failure(InvalidSyntaxError(
          self.currentTok.posStart, self.currentTok.posEnd,
          errorDetails['openParenExpected']
        ))
    else:
      varNameToken = None
      if self.currentTok.type != TT_LPAREN:
        return res.failure(InvalidSyntaxError(
          self.currentTok.posStart, self.currentTok.posEnd,
          errorDetails['openParenExpected']
        ))

    res.registerAdvancement()
    self.advance()
    argNameTokens = []

    if self.currentTok.type == TT_IDENTIFIER:
      argNameTokens.append(self.currentTok)
      res.registerAdvancement()
      self.advance()

      while self.currentTok.type == TT_COMMA:
        res.registerAdvancement()
        self.advance()

        if self.currentTok.type != TT_IDENTIFIER:
          return res.failure(InvalidSyntaxError(
            self.currentTok.posStart, self.currentTok.posEnd,
            errorDetails['identifierExpected']
          ))

        argNameTokens.append(self.currentTok)
        res.registerAdvancement()
        self.advance()

      if self.currentTok.type != TT_RPAREN:
        return res.failure(InvalidSyntaxError(
          self.currentTok.posStart, self.currentTok.posEnd,
          errorDetails['closeParenExpected']
        ))
    else:
      if self.currentTok.type != TT_RPAREN:
        return res.failure(InvalidSyntaxError(
          self.currentTok.posStart, self.currentTok.posEnd,
          errorDetails['closeParenExpected']
        ))

    res.registerAdvancement()
    self.advance()

    if self.currentTok.type == TT_ARROW:
      res.registerAdvancement()
      self.advance()
      body = res.register(self.expr())
      if res.error: return res

      return res.success(FuncDefNode(
        varNameToken,
        argNameTokens,
        body,
        True
      ))

    if self.currentTok.type != TT_NEWLINE:
      return res.failure(InvalidSyntaxError(
        self.currentTok.posStart, self.currentTok.posEnd,
        errorDetails['newlineExpected']
      ))

    res.registerAdvancement()
    self.advance()

    body = res.register(self.statements())
    if res.error: return res

    if not self.currentTok.matches(TT_KEYWORD, 'fin'):
      return res.failure(InvalidSyntaxError(
        self.currentTok.posStart, self.currentTok.posEnd,
        errorDetails['endExpected']
      ))

    res.registerAdvancement()
    self.advance()

    return res.success(FuncDefNode(
      varNameToken,
      argNameTokens,
      body,
      False
    ))

  def binOp(self, funcA, ops, funcB=None):
    if funcB == None:
      funcB = funcA

    res = ParserResult()
    left = res.register(funcA())
    if res.error: return res

    while self.currentTok.type in ops or (self.currentTok.type, self.currentTok.value) in ops:
      opTok = self.currentTok
      res.registerAdvancement()
      self.advance()
      right = res.register(funcB())
      if res.error: return res
      left = BinOpNode(left, opTok, right)

    return res.success(left)
