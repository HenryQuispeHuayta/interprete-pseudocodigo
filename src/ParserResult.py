class ParserResult:
  def __init__(self):
    self.error = None
    self.node = None
    self.advanceCount = 0
    self.toReverseCount = 0

  def register(self, res):
    self.lastRegisteredAdvanceCount = res.advanceCount
    self.advanceCount += res.advanceCount
    if res.error: self.error = res.error
    return res.node

  def tryRegister(self, res):
    if res.error:
      self.toReverseCount = res.advanceCount
      return None
    return self.register(res)

  def registerAdvancement(self):
    self.advanceCount += 1
    self.lastRegisteredAdvanceCount = 1

  def success(self, node):
    self.node = node
    return self

  def failure(self, error):
    if not self.error or self.lastRegisteredAdvanceCount == 0: # TODO: analyze this condition
      self.error = error
    return self
