from src.Constants import errorDetails
from src.Context import Context
from src.Errors import RunTimeError
from src.RunTimeResult import RunTimeResult
from src.SymbolTable import SymbolTable

import os
import math

class Value:
  def __init__(self):
    self.setPos()
    self.setContext()

  def setPos(self, posStart=None, posEnd=None):
    self.posStart = posStart
    self.posEnd = posEnd
    return self

  def setContext(self, context=None):
    self.context = context
    return self

  def add(self, other):
    return None, self.illegalOperation(other)

  def sub(self, other):
    return None, self.illegalOperation(other)

  def mul(self, other):
    return None, self.illegalOperation(other)

  def div(self, other):
    return None, self.illegalOperation(other)

  def pow(self, other):
    return None, self.illegalOperation(other)

  def mod(self, other):
    return None, self.illegalOperation(other)

  def getComparisonEq(self, other):
    return None, self.illegalOperation(other)

  def getComparisonNe(self, other):
    return None, self.illegalOperation(other)

  def getComparisonLt(self, other):
    return None, self.illegalOperation(other)

  def getComparisonGt(self, other):
    return None, self.illegalOperation(other)

  def getComparisonLte(self, other):
    return None, self.illegalOperation(other)

  def getComparisonGte(self, other):
    return None, self.illegalOperation(other)

  def anded(self, other):
    return None, self.illegalOperation(other)

  def ored(self, other):
    return None, self.illegalOperation(other)

  def notted(self):
    return None, self.illegalOperation()

  def isTrue(self):
    return False
  
  def execute(self, args): # TODO: Analyze this method
    return RunTimeResult().failure(self.illegalOperation())

  def copy(self):
    raise Exception('No se ha implementado el método copy()')

  def illegalOperation(self, other=None):
    if not other: other = self
    return RunTimeError(
      self.posStart, other.posEnd,
      errorDetails['illegalOperationError'],
      self.context
    )

class Number(Value):
  def __init__(self, value):
    super().__init__()
    self.value = value

  def add(self, other):
    if isinstance(other, Number):
      return Number(self.value + other.value).setContext(self.context), None
    else:
      return None, Value.illegalOperation(self, other)

  def sub(self, other):
    if isinstance(other, Number):
      return Number(self.value - other.value).setContext(self.context), None
    else:
      return None, Value.illegalOperation(self, other)

  def mul(self, other):
    if isinstance(other, Number):
      return Number(self.value * other.value).setContext(self.context), None
    else:
      return None, Value.illegalOperation(self, other)

  def div(self, other):
    if isinstance(other, Number):
      if other.value == 0:
        return None, RunTimeError(
          other.posStart, other.posEnd,
          errorDetails['zeroDivisionError'],
          self.context
        )
      return Number(self.value / other.value).setContext(self.context), None
    else:
      return None, Value.illegalOperation(self, other)

  def pow(self, other):
    if isinstance(other, Number):
      return Number(self.value ** other.value).setContext(self.context), None
    else:
      return None, Value.illegalOperation(self, other)

  def mod(self, other):
    if isinstance(other, Number):
      return Number(self.value % other.value).setContext(self.context), None
    else:
      return None, Value.illegalOperation(self, other)

  def getComparisonEq(self, other):
    if isinstance(other, Number):
      return Number(int(self.value == other.value)).setContext(self.context), None
    else:
      return None, Value.illegalOperation(self, other)

  def getComparisonNe(self, other):
    if isinstance(other, Number):
      return Number(int(self.value != other.value)).setContext(self.context), None
    else:
      return None, Value.illegalOperation(self, other)

  def getComparisonLt(self, other):
    if isinstance(other, Number):
      return Number(int(self.value < other.value)).setContext(self.context), None
    else:
      return None, Value.illegalOperation(self, other)

  def getComparisonGt(self, other):
    if isinstance(other, Number):
      return Number(int(self.value > other.value)).setContext(self.context), None
    else:
      return None, Value.illegalOperation(self, other)

  def getComparisonLte(self, other):
    if isinstance(other, Number):
      return Number(int(self.value <= other.value)).setContext(self.context), None
    else:
      return None, Value.illegalOperation(self, other)

  def getComparisonGte(self, other):
    if isinstance(other, Number):
      return Number(int(self.value >= other.value)).setContext(self.context), None
    else:
      return None, Value.illegalOperation(self, other)

  def anded(self, other):
    if isinstance(other, Number):
      return Number(int(self.value and other.value)).setContext(self.context), None
    else:
      return None, Value.illegalOperation(self, other)

  def ored(self, other):
    if isinstance(other, Number):
      return Number(int(self.value or other.value)).setContext(self.context), None
    else:
      return None, Value.illegalOperation(self, other)

  def notted(self):
    return Number(1 if self.value == 0 else 0).setContext(self.context), None

  def isTrue(self):
    return self.value != 0

  def copy(self):
    copy = Number(self.value)
    copy.setPos(self.posStart, self.posEnd)
    copy.setContext(self.context)
    return copy

  def __repr__(self):
    return str(self.value)

Number.null = Number(None)
Number.false = Number(0)
Number.true = Number(1)
Number.mathPI = Number(math.pi)
Number.mathE = Number(math.e)

class Empty(Value):
  def __init__(self):
    super().__init__()

  def copy(self):
    return Empty()

  def __repr__(self):
    return 'Nulo'

  def __str__(self):
    return 'Nulo'

class String(Value):
  def __init__(self, value):
    super().__init__()
    self.value = value

  def add(self, other):
    if isinstance(other, String):
      return String(self.value + other.value).setContext(self.context), None
    else:
      return None, Value.illegalOperation(self, other)

  def mul(self, other):
    if isinstance(other, Number):
      return String(self.value * other.value).setContext(self.context), None
    else:
      return None, Value.illegalOperation(self, other)

  def isTrue(self):
    return len(self.value) > 0

  def copy(self):
    copy = String(self.value)
    copy.setPos(self.posStart, self.posEnd)
    copy.setContext(self.context)
    return copy

  def __repr__(self):
    return f'"{self.value}"'

  def __str__(self):
    return self.value

String.null = String('')
String.false = String('0')
String.true = String('1')

class List(Value):
  def __init__(self, elements):
    super().__init__()
    self.elements = elements

  def add(self, other): # TODO: Analyze this method
    newList = self.copy()
    newList.elements.append(other)
    return newList, None

  def sub(self, other):
    if isinstance(other, Number):
      newList = self.copy()
      try:
        newList.elements.pop(other.value)
        return newList, None
      except:
        return None, RunTimeError(
          other.posStart, other.posEnd,
          errorDetails['listIndexError'],
          self.context
        )
    else:
      return None, Value.illegalOperation(self, other)

  def mul(self, other): # TODO: Analyze this method
    if isinstance(other, List):
      newList = self.copy()
      newList.elements.extend(other.elements)
      return newList, None
    else:
      return None, Value.illegalOperation(self, other)

  def div(self, other):
    if isinstance(other, Number):
      try:
        return self.elements[other.value], None
      except:
        return None, RunTimeError(
          other.posStart, other.posEnd,
          errorDetails['listIndexError'],
          self.context
        )
    else:
      return None, Value.illegalOperation(self, other)

  def copy(self):
    copy = List(self.elements)
    copy.setPos(self.posStart, self.posEnd)
    copy.setContext(self.context)
    return copy

  def __repr__(self):
    return f'[{", ".join([str(x) for x in self.elements])}]'

  def __str__(self):
    return f'[{", ".join([str(x) for x in self.elements])}]'

class BaseFunction(Value):
  def __init__(self, name):
    super().__init__()
    self.name = name or '<anónimo>'

  def generateNewContext(self):
    newContext = Context(self.name, self.context, self.posStart)
    newContext.symbolTable = SymbolTable(newContext.parent.symbolTable)
    return newContext

  def checkArgs(self, argNames, args):
    res = RunTimeResult()

    if len(args) > len(argNames):
      return res.failure(RunTimeError(
        self.posStart, self.posEnd,
        errorDetails['tooManyArgsError'].format(len(args), len(argNames)),
        self.context
      ))

    if len(args) < len(argNames):
      return res.failure(RunTimeError(
        self.posStart, self.posEnd,
        errorDetails['tooFewArgsError'].format(len(args), len(argNames)),
        self.context
      ))

    return res.success(None)

  def populateArgs(self, argNames, args, execCtx):
    for i in range(len(args)):
      argName = argNames[i]
      argValue = args[i]
      argValue.setContext(execCtx)
      execCtx.symbolTable.set(argName, argValue)

  def checkAndPopulateArgs(self, argNames, args, execCtx):
    res = RunTimeResult()
    res.register(self.checkArgs(argNames, args))
    if res.error: return res
    self.populateArgs(argNames, args, execCtx)
    return res.success(None)

class Function(BaseFunction):
  def __init__(self, name, bodyNode, argNames, shouldAutoReturn):
    super().__init__(name)
    self.bodyNode = bodyNode
    self.argNames = argNames
    self.shouldAutoReturn = shouldAutoReturn

  def execute(self, args):
    from src.Interpreter import Interpreter
    res = RunTimeResult()
    interpreter = Interpreter()
    newContext = self.generateNewContext()

    res.register(self.checkAndPopulateArgs(self.argNames, args, newContext))
    if res.shouldReturn(): return res

    value = res.register(interpreter.visit(self.bodyNode, newContext))
    if res.shouldReturn() and res.funcReturnValue == None: return res

    returnValue = (value if self.shouldAutoReturn else None) or res.funcReturnValue or Number.null
    return res.success(returnValue)

  def copy(self):
    copy = Function(self.name, self.bodyNode, self.argNames, self.shouldAutoReturn)
    copy.setContext(self.context)
    copy.setPos(self.posStart, self.posEnd)
    return copy

  def __repr__(self):
    return f'<función {self.name}>'

class BuiltInFunction(BaseFunction):
  def __init__(self, name):
    super().__init__(name)

  def execute(self, args):
    res = RunTimeResult()
    newContext = self.generateNewContext()

    methodName = f'execute{self.name.capitalize()}'
    method = getattr(self, methodName, self.noVisitMethod)

    res.register(self.checkAndPopulateArgs(method.argNames, args, newContext))
    if res.shouldReturn(): return res

    returnValue = res.register(method(newContext))
    if res.shouldReturn(): return res
    return res.success(returnValue)

  def noVisitMethod(self, node, context):
    raise Exception(f'No se ha implementado el método execute_{self.name} para la clase BuiltInFunction')

  def copy(self):
    copy = BuiltInFunction(self.name)
    copy.setContext(self.context)
    copy.setPos(self.posStart, self.posEnd)
    return copy

  def __repr__(self):
    return f'<función incorporada {self.name}>'

  def executePrint(self, execCtx):
    print(str(execCtx.symbolTable.get('value')))
    return RunTimeResult().success(Number.null)
  executePrint.argNames = ['value']

  def executePrintRet(self, execCtx):
    return RunTimeResult().success(String(str(execCtx.symbolTable.get('value'))))
  executePrintRet.argNames = ['value']

  def executeInput(self, execCtx):
    text = input(execCtx.symbolTable.get('prompt') or '¿Qué deseas ingresar?')
    return RunTimeResult().success(String(text))
  executeInput.argNames = ['prompt']

  def executeInputInt(self, execCtx):
    while True:
      text = input(execCtx.symbolTable.get('prompt') or 'Escribe un número entero:')
      try:
        number = int(text)
        break
      except ValueError:
        print(f"'{text}' debe ser un número entero. Intenta de nuevo.")
    return RunTimeResult().success(Number(number))
  executeInputInt.argNames = ['prompt']

  def executeClear(self, execCtx):
    os.system('cls' if os.name == 'nt' else 'clear')
    return RunTimeResult().success(Number.null)
  executeClear.argNames = []

  def executeIsNumber(self, execCtx):
    isNumber = isinstance(execCtx.symbolTable.get('value'), Number)
    return RunTimeResult().success(Number.true if isNumber else Number.false)
  executeIsNumber.argNames = ['value']

  def executeIsString(self, execCtx):
    isString = isinstance(execCtx.symbolTable.get('value'), String)
    return RunTimeResult().success(Number.true if isString else Number.false)
  executeIsString.argNames = ['value']

  def executeIsList(self, execCtx):
    isList = isinstance(execCtx.symbolTable.get('value'), List)
    return RunTimeResult().success(Number.true if isList else Number.false)
  executeIsList.argNames = ['value']

  def executeIsFunction(self, execCtx):
    isFunction = isinstance(execCtx.symbolTable.get('value'), BaseFunction)
    return RunTimeResult().success(Number.true if isFunction else Number.false)
  executeIsFunction.argNames = ['value']

  def executeAppend(self, execCtx):
    list_ = execCtx.symbolTable.get('list')
    value = execCtx.symbolTable.get('value')

    if not isinstance(list_, List):
      return RunTimeResult().failure(RunTimeError(
        self.posStart, self.posEnd,
        errorDetails['invalidTypeError'].format('list', list_),
        execCtx
      ))

    list_.elements.append(value)
    return RunTimeResult().success(Number.null) # TODO: Analyze this return
  executeAppend.argNames = ['list', 'value']

  def executePop(self, execCtx):
    list_ = execCtx.symbolTable.get('list')
    index = execCtx.symbolTable.get('index')

    if not isinstance(list_, List):
      return RunTimeResult().failure(RunTimeError(
        self.posStart, self.posEnd,
        errorDetails['invalidTypeError'].format('list', list_), # TODO: Analyze this line
        execCtx
      ))

    if not isinstance(index, Number):
      return RunTimeResult().failure(RunTimeError(
        self.posStart, self.posEnd,
        errorDetails['invalidTypeError'].format('number', index),
        execCtx
      ))

    try:
      element = list_.elements.pop(index.value)
    except:
      return RunTimeResult().failure(RunTimeError(
        self.posStart, self.posEnd,
        errorDetails['listIndexError'],
        execCtx
      ))

    return RunTimeResult().success(element)
  executePop.argNames = ['list', 'index']

  def executeExtend(self, execCtx):
    listA = execCtx.symbolTable.get('listA')
    listB = execCtx.symbolTable.get('listB')

    if not isinstance(listA, List):
      return RunTimeResult().failure(RunTimeError(
        self.posStart, self.posEnd,
        errorDetails['invalidTypeError'].format('list', listA),
        execCtx
      ))

    if not isinstance(listB, List):
      return RunTimeResult().failure(RunTimeError(
        self.posStart, self.posEnd,
        errorDetails['invalidTypeError'].format('list', listB),
        execCtx
      ))

    listA.elements.extend(listB.elements)
    return RunTimeResult().success(listA)
  executeExtend.argNames = ['listA', 'listB']

  def executeLen(self, execCtx):
    list_ = execCtx.symbolTable.get('list')

    if not isinstance(list_, List):
      return RunTimeResult().failure(RunTimeError(
        self.posStart, self.posEnd,
        errorDetails['invalidTypeError'].format('list', list_),
        execCtx
      ))

    return RunTimeResult().success(Number(len(list_.elements)))
  executeLen.argNames = ['list']

  def executeRun(self, execCtx):
    fn = execCtx.symbolTable.get('fn')

    if not isinstance(fn, String):
      return RunTimeResult().failure(RunTimeError(
        self.posStart, self.posEnd,
        'el nombre del archivo debe ser una cadena',
        execCtx
      ))

    if fn.value[-4:] != '.inf':
      return RunTimeResult().failure(RunTimeError(
        self.posStart, self.posEnd,
        errorDetails['invalidFileNameError'],
        execCtx
      ))

    fn = os.path.abspath(fn.value)

    try:
      with open(fn, 'r') as f:
        script = f.read()
    except Exception as e:
      return RunTimeResult().failure(RunTimeError(
        self.posStart, self.posEnd,
        errorDetails['runTimeError'].format(str(e)),
        execCtx
      ))
    from src.Compiler import run
    
    _, error = run(fn, script)

    if error:
      return RunTimeResult().failure(RunTimeError(
        self.posStart, self.posEnd,
        errorDetails['runTimeError']+':\n'+error.asString(),
        execCtx
      ))

    return RunTimeResult().success(Number.null)
  executeRun.argNames = ['fn']

BuiltInFunction.print = BuiltInFunction('print')
BuiltInFunction.printRet = BuiltInFunction('printRet')
BuiltInFunction.input = BuiltInFunction('input')
BuiltInFunction.inputInt = BuiltInFunction('inputInt')
BuiltInFunction.clear = BuiltInFunction('clear')
BuiltInFunction.isNumber = BuiltInFunction('isNumber')
BuiltInFunction.isString = BuiltInFunction('isString')
BuiltInFunction.isList = BuiltInFunction('isList')
BuiltInFunction.isFunction = BuiltInFunction('isFunction')
BuiltInFunction.append = BuiltInFunction('append')
BuiltInFunction.pop = BuiltInFunction('pop')
BuiltInFunction.extend = BuiltInFunction('extend')
BuiltInFunction.len = BuiltInFunction('len')
BuiltInFunction.run = BuiltInFunction('run')
