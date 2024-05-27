class Context:
  def __init__(self, displayName, parent=None, parentEntryPos=None):
    self.displayName = displayName
    self.parent = parent
    self.parentEntryPos = parentEntryPos
    self.symbolTable = None
