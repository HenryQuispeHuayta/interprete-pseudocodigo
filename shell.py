import signal
import sys
import os
import ctypes

try:
	ctypes.windll.kernel32.SetConsoleTitleW("Consola")
except:
	pass

from src.Compiler import run
from src.Values import Empty

def signalHandler(sig, frame):
	print("\n\nSaliendo...")
	sys.exit(0)

signal.signal(signal.SIGINT, signalHandler)

def cli():
  for arg in sys.argv:
    if arg == '-':
      sys.argv.remove(arg)
  if len(sys.argv) == 1:
    while True:
      folder = os.path.basename(os.getcwd())
      inputText = input(f"{folder} > ")
      inputText = inputText.replace("\\", "\\\\")
      if inputText.strip() == "":
        continue
      result, error = run(__file__, inputText)
      
      if error:
        print(error.asString())

      elif result:
        for i, res in enumerate(result.elements):
          if type(res) == Empty:
            result.elements.pop(i)

        for programRes in result.elements:
          print(repr(programRes))

  else:
    uri = sys.argv[1]
    uri = uri.replace("\\", "\\\\")
    result, error = run(__file__, f'correr("{uri}")')
    if error:
      print(error.asString())

    elif result:
      for i, res in enumerate(result.elements):
        if type(res) == Empty:
          result.elements.pop(i)

      if len(result.elements) == 1:
        print(repr(result.elements[0]))
      elif len(result.elements) > 1:
        print(repr(result))

    folder = os.path.basename(os.getcwd())
    input(f"\nPresione enter para salir...")
    sys.exit(0)

cli()