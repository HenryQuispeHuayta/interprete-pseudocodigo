from src.Constants import *
from src.Errors import *
from src.RunTimeResult import RunTimeResult
from src.Values import *

class Interpreter:
  def visit(self, node, context):
    methodName = f'visit{type(node).__name__}' # TODO: analyze this line
    method = getattr(self, methodName, self.noVisitMethod)
    return method(node, context)

  def noVisitMethod(self, node, context): # TODO: analyze this line
    raise Exception(f'No visit{type(node).__name__} method defined')

  def visitNumberNode(self, node, context):
    return RunTimeResult().success(Number(node.value.value).setContext(context).setPos(node.posStart, node.posEnd))

  def visitStringNode(self, node, context):
    return RunTimeResult().success(String(node.value.value).setContext(context).setPos(node.posStart, node.posEnd))

  def visitListNode(self, node, context):
    res = RunTimeResult()
    elements = []

    for elementNode in node.elementNodes:
      elements.append(res.register(self.visit(elementNode, context)))
      if res.shouldReturn(): return res

    return res.success(List(elements).setContext(context).setPos(node.posStart, node.posEnd))

  def visitVarAccessNode(self, node, context):
    res = RunTimeResult()
    varName = node.varNameToken.value
    value = context.symbolTable.get(varName)

    if value == None:
      return res.failure(RunTimeError(
        node.posStart, node.posEnd,
        errorDetails['varNotDefined'].format(varName),
        context
      ))

    value = value.copy().setPos(node.posStart, node.posEnd).setContext(context)
    return res.success(value)

  def visitVarAssignNode(self, node, context):
    res = RunTimeResult()
    varName = node.varNameToken.value
    value = res.register(self.visit(node.valueNode))
    if res.shouldReturn(): return res # TODO: shouldReturn()

    context.symbolTable.set(varName, value)
    return res.success(value)

  def visitBinOpNode(self, node, context):
    res = RunTimeResult()
    left = res.register(self.visit(node.leftNode, context))
    if res.shouldReturn(): return res

    right = res.register(self.visit(node.rightNode, context))
    if res.shouldReturn(): return res

    if node.opToken.type == TT_PLUS:
      result, error = left.add(right)
    elif node.opToken.type == TT_MINUS:
      result, error = left.sub(right)
    elif node.opToken.type == TT_MUL:
      result, error = left.mul(right)
    elif node.opToken.type == TT_DIV:
      result, error = left.div(right)
    elif node.opToken.type == TT_POW:
      result, error = left.pow(right)
    elif node.opToken.type == TT_MOD:
      result, error = left.mod(right)
    elif node.opToken.type == TT_EE:
      result, error = left.getComparisonEq(right)
    elif node.opToken.type == TT_NE:
      result, error = left.getComparisonNe(right)
    elif node.opToken.type == TT_LT:
      result, error = left.getComparisonLt(right)
    elif node.opToken.type == TT_GT:
      result, error = left.getComparisonGt(right)
    elif node.opToken.type == TT_LTE:
      result, error = left.getComparisonLte(right)
    elif node.opToken.type == TT_GTE:
      result, error = left.getComparisonGte(right)
    elif node.opToken.matches(TT_KEYWORD, 'y'):
      result, error = left.anded(right)
    elif node.opToken.matches(TT_KEYWORD, 'o'):
      result, error = left.ored(right)

    if error:
      return res.failure(error)
    else:
      return res.success(result.setPos(node.posStart, node.posEnd))

  def visitUnaryOpNode(self, node, context):
    res = RunTimeResult()
    number = res.register(self.visit(node.node, context))
    if res.shouldReturn(): return res

    error = None

    if node.opToken.type == TT_MINUS:
      number, error = number.mul(Number(-1))

    if node.opToken.matches(TT_KEYWORD, 'no'):
      number, error = number.notted()

    if error:
      return res.failure(error)
    else:
      return res.success(number.setPos(node.posStart, node.posEnd))

  def visitIfNode(self, node, context):
    res = RunTimeResult()

    for condition, expr, shouldReturnNull in node.cases:
      conditionValue = res.register(self.visit(condition, context))
      if res.shouldReturn(): return res

      if conditionValue.isTrue():
        exprValue = res.register(self.visit(expr, context))
        if res.shouldReturn(): return res
        return res.success(Number.null if shouldReturnNull else exprValue)

    if node.elseCase:
      expr, shouldReturnNull = node.elseCase
      exprValue = res.register(self.visit(expr, context))
      if res.shouldReturn(): return res
      return res.success(Number.null if shouldReturnNull else exprValue)

    return res.success(Number.null)

  def visitForNode(self, node, context):
    res = RunTimeResult()
    elements = []

    startValue = res.register(self.visit(node.startValueNode, context))
    if res.shouldReturn(): return res

    endValue = res.register(self.visit(node.endValueNode, context))
    if res.shouldReturn(): return res

    if node.stepValueNode:
      stepValue = res.register(self.visit(node.stepValueNode, context))
      if res.shouldReturn(): return res
    else:
      stepValue = Number(1)

    i = startValue.value

    if stepValue.value >= 0:
      condition = lambda: i < endValue.value
    else:
      condition = lambda: i > endValue.value

    while condition():
      context.symbolTable.set(node.varNameToken.value, Number(i))
      i += stepValue.value

      value = res.register(self.visit(node.bodyNode, context))
      if res.shouldReturn() and res.loopShouldContinue == False and res.loopShouldBreak == False: return res

      if res.loopShouldContinue: continue
      if res.loopShouldBreak: break

      elements.append(value)

    return res.success(
      Number.null if node.shouldReturnNull else List(elements).setContext(context).setPos(node.posStart, node.posEnd)
    )

  def visitWhileNode(self, node, context):
    res = RunTimeResult()
    elements = []

    while True:
      condition = res.register(self.visit(node.conditionNode, context))
      if res.shouldReturn(): return res

      if not condition.isTrue(): break

      value = res.register(self.visit(node.bodyNode, context))
      if res.shouldReturn() and res.loopShouldContinue == False and res.loopShouldBreak == False: return res

      if res.loopShouldContinue: continue
      if res.loopShouldBreak: break

      elements.append(value)

    return res.success(
      Number.null if node.shouldReturnNull else List(elements).setContext(context).setPos(node.posStart, node.posEnd)
    )

  def visitFuncDefNode(self, node, context):
    res = RunTimeResult()
    funcName = node.varNameToken.value if node.varNameToken else None
    bodyNode = node.bodyNode
    argNames = [argName.value for argName in node.argNameTokens]
    funcValue = Function(funcName, bodyNode, argNames, node.shouldAutoReturn).setContext(context).setPos(node.posStart, node.posEnd)

    if node.varNameToken:
      context.symbolTable.set(funcName, funcValue)

    return res.success(funcValue)

  def visitCallNode(self, node, context):
    res = RunTimeResult()
    args = []

    valueToCall = res.register(self.visit(node.nodeToCall, context))
    if res.shouldReturn(): return res
    valueToCall = valueToCall.copy().setPos(node.posStart, node.posEnd)

    for argNode in node.argNodes:
      args.append(res.register(self.visit(argNode, context)))
      if res.shouldReturn(): return res

    returnValue = res.register(valueToCall.execute(args))
    if res.shouldReturn(): return res
    returnValue = returnValue.copy().setPos(node.posStart, node.posEnd).setContext(context)

    return res.success(returnValue)

  def visitReturnNode(self, node, context):
    res = RunTimeResult()

    if node.nodeToReturn:
      value = res.register(self.visit(node.nodeToReturn, context))
      if res.shouldReturn(): return res
    else:
      value = Number.null

    return res.successReturn(value)

  def visitContinueNode(self, node, context):
    return RunTimeResult().successContinue()

  def visitBreakNode(self, node, context):
    return RunTimeResult().successBreak()

  def visitIndexNode(self, node, context):
    res = RunTimeResult()
    list_ = res.register(self.visit(node.listNode, context))
    if res.shouldReturn(): return res
    index = res.register(self.visit(node.indexNode, context))
    if res.shouldReturn(): return res

    element = list_.getElementAtIndex(index)
    if element == None:
      return res.failure(RunTimeError(
        node.posStart, node.posEnd,
        errorDetails['listIndexOutOfBounds'].format(index.value),
        context
      ))

    return res.success(element)
