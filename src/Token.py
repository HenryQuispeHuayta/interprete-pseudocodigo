class Token:
  def __init__(self, type_, value=None, posStart=None, posEnd=None):
    self.type = type_
    self.value = value
    
    if posStart:
      self.posStart = posStart.copy()
      self.posEnd = posStart.copy()
      self.posEnd.advance()
      
    if posEnd:
      self.posEnd = posEnd.copy()

  def matches(self, type_, value):
    return self.type == type_ and self.value == value
  
  def __repr__(self):
    if self.value: return f'{self.type}:{self.value}'
    return str(self.type) # TODO: analyze if this is correct (str)
