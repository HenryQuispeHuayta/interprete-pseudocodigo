from src.StringsWithArrows import *
from src.Constants import errorMesaages

class Error:
  def __init__(self, posStart, posEnd, errorName, details):
    self.posStart = posStart
    self.posEnd = posEnd
    self.errorName = errorName
    self.details = details

  def asString(self):
    result = f'{self.errorName}: {self.details}\n'
    result += f'Archivo {self.posStart.fn}, línea {self.posStart.ln + 1}\n'
    result += '\n' + stringWithArrows(self.posStart.ftxt, self.posStart, self.posEnd)
    return result

class IllegalCharError(Error):
  def __init__(self, posStart, posEnd, details):
    super().__init__(posStart, posEnd, errorMesaages['IllegalCharError'], details)

class InvalidSyntaxError(Error):
  def __init__(self, posStart, posEnd, details=''):
    super().__init__(posStart, posEnd, errorMesaages['InvalidSyntaxError'], details)

class ExpectedCharError(Error):
  def __init__(self, posStart, posEnd, details=''):
    super().__init__(posStart, posEnd, errorMesaages['ExpectedCharError'], details)

class InvalidIndentationError(Error):
  def __init__(self, posStart, posEnd, details=''):
    super().__init__(posStart, posEnd, errorMesaages['InvalidIndentationError'], details)

class InvalidTokenError(Error):
  def __init__(self, posStart, posEnd, details=''):
    super().__init__(posStart, posEnd, errorMesaages['InvalidTokenError'], details)

class RunTimeError(Error):
  def __init__(self, posStart, posEnd, details, context):
    super().__init__(posStart, posEnd, errorMesaages['RunTimeError'], details)
    self.context = context

  def asString(self):
    result = self.generateTraceback()
    result += f'{self.errorName}: {self.details}\n'
    result += '\n' + stringWithArrows(self.posStart.ftxt, self.posStart, self.posEnd)
    return result

  def generateTraceback(self): # TODO: Analyze this method
    result = ''
    pos = self.posStart
    ctx = self.context
    notLoop = True

    while ctx:
      if notLoop:
        result = 'Rastreo del error(última llamada):\n' + f'Archivo {pos.fn}, línea {pos.ln + 1}, en {ctx.displayName}\n' + result
        notLoop = False
      else:
        result = f'Archivo {pos.fn}, línea {pos.ln + 1}, en {ctx.displayName}\n' + result
      pos = ctx.parentEntryPos
      ctx = ctx.parent

    return result

class ReturnError(Error):
  def __init__(self, posStart, posEnd, details=''):
    super().__init__(posStart, posEnd, errorMesaages['ReturnError'], details)
