class RunTimeResult:
  def __init__(self):
    self.reset()

  def reset(self):
    self.value = None
    self.error = None
    self.funcReturnValue = None
    self.loopShouldContinue = False
    self.loopShouldBreak = False

  def register(self, res):
    if res.error: self.error = res.error
    self.funcReturnValue = res.funcReturnValue
    self.loopShouldContinue = res.loopShouldContinue
    self.loopShouldBreak = res.loopShouldBreak
    return res.value

  def success(self, value):
    self.reset()
    self.value = value
    return self

  def successReturn(self, value):
    self.reset()
    self.funcReturnValue = value
    return self

  def successContinue(self):
    self.reset()
    self.loopShouldContinue = True
    return self

  def successBreak(self):
    self.reset()
    self.loopShouldBreak = True
    return self

  def failure(self, error):
    self.reset()
    self.error = error
    return self

  def shouldReturn(self):
    return (
      self.error or
      self.funcReturnValue or
      self.loopShouldContinue or
      self.loopShouldBreak
    )
