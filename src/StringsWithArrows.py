def stringWithArrows(text, posStart, posEnd):
  result = ''

  idxStart = max(text.rfind('\n', 0, posStart.idx), 0)
  idxEnd = text.find('\n', idxStart + 1)
  if idxEnd < 0: idxEnd = len(text)

  lineCount = posEnd.ln - posStart.ln + 1
  for i in range(lineCount):
    line = text[idxStart:idxEnd]
    colStart = posStart.col if i == 0 else 0
    colEnd = posEnd.col if i == lineCount - 1 else len(line) - 1

    result += line + '\n'
    result += ' ' * colStart + '^' * (colEnd - colStart)
    
    idxStart = idxEnd
    idxEnd = text.find('\n', idxStart + 1)
    if idxEnd < 0: idxEnd = len(text)

  return result.replace('\t', '')
