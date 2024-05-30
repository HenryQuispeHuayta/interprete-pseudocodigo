class StringNode:
  def __init__(self, value): # TODO: value to token
    self.value = value
    self.posStart = self.value.posStart
    self.posEnd = self.value.posEnd

  def __repr__(self):
    return f'{self.value}'

class NumberNode:
  def __init__(self, value):
    self.value = value
    self.posStart = self.value.posStart
    self.posEnd = self.value.posEnd

  def __repr__(self):
    return f'{self.value}'

class ListNode:
  def __init__(self, elementNodes, posStart, posEnd):
    self.elementNodes = elementNodes
    self.posStart = posStart
    self.posEnd = posEnd

class VarAccessNode:
  def __init__(self, varNameToken):
    self.varNameToken = varNameToken
    self.posStart = self.varNameToken.posStart
    self.posEnd = self.varNameToken.posEnd

class VarAssignNode:
  def __init__(self, varNameToken, valueNode):
    self.varNameToken = varNameToken
    self.valueNode = valueNode
    self.posStart = self.varNameToken.posStart
    self.posEnd = self.valueNode.posEnd

class BinOpNode:
  def __init__(self, leftNode, opToken, rightNode):
    self.leftNode = leftNode
    self.opToken = opToken
    self.rightNode = rightNode
    self.posStart = self.leftNode.posStart
    self.posEnd = self.rightNode.posEnd

  def __repr__(self):
    return f'({self.leftNode}, {self.opToken}, {self.rightNode})'

class UnaryOpNode:
  def __init__(self, opToken, node):
    self.opToken = opToken
    self.node = node
    self.posStart = self.opToken.posStart
    self.posEnd = self.node.posEnd

  def __repr__(self):
    return f'({self.opToken}, {self.node})'

class IfNode:
  def __init__(self, cases, elseCase):
    self.cases = cases
    self.elseCase = elseCase
    self.posStart = self.cases[0][0].posStart
    self.posEnd = (self.elseCase or self.cases[-1])[0].posEnd

class ForNode:
  def __init__(self, varNameToken, startValueNode, endValueNode, stepValueNode, bodyNode, shouldReturnNull):
    self.varNameToken = varNameToken
    self.startValueNode = startValueNode
    self.endValueNode = endValueNode
    self.stepValueNode = stepValueNode
    self.bodyNode = bodyNode
    self.shouldReturnNull = shouldReturnNull
    self.posStart = self.varNameToken.posStart
    self.posEnd = self.bodyNode.posEnd

class WhileNode:
  def __init__(self, conditionNode, bodyNode, shouldReturnNull):
    self.conditionNode = conditionNode
    self.bodyNode = bodyNode
    self.shouldReturnNull = shouldReturnNull
    self.posStart = self.conditionNode.posStart
    self.posEnd = self.bodyNode.posEnd

class FuncDefNode:
  def __init__(self, varNameToken, argNameTokens, bodyNode, shouldAutoReturn):
    self.varNameToken = varNameToken
    self.argNameTokens = argNameTokens
    self.bodyNode = bodyNode
    self.shouldAutoReturn = shouldAutoReturn

    if self.varNameToken:
      self.posStart = self.varNameToken.posStart
    elif len(self.argNameTokens) > 0:
      self.posStart = self.argNameTokens[0].posStart
    else:
      self.posStart = self.bodyNode.posEnd # TODO: posStart = bodyNode.posStart?

    self.posEnd = self.bodyNode.posEnd

class CallNode:
  def __init__(self, nodeToCall, argNodes):
    self.nodeToCall = nodeToCall
    self.argNodes = argNodes
    self.posStart = self.nodeToCall.posStart

    if len(self.argNodes) > 0:
      self.posEnd = self.argNodes[-1].posEnd
    else:
      self.posEnd = self.nodeToCall.posEnd

class CallListNode:
  def __init__(self, listToCall, listIndexNode):
    self.listToCall = listToCall
    self.listIndexNode = listIndexNode
    self.posStart = self.listToCall.posStart
    self.posEnd = self.listToCall.posEnd

class ReturnNode:
  def __init__(self, nodeToReturn, posStart, posEnd):
    self.nodeToReturn = nodeToReturn
    self.posStart = posStart
    self.posEnd = posEnd

class ContinueNode:
  def __init__(self, posStart, posEnd):
    self.posStart = posStart
    self.posEnd = posEnd

class BreakNode:
  def __init__(self, posStart, posEnd):
    self.posStart = posStart
    self.posEnd = posEnd
