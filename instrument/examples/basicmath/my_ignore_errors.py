python
def exe(arg):
  try:
    gdb.execute("print \"" + "Executing command: " + arg + "\"")
    gdb.execute (arg)
  except:
    gdb.execute("print \"" + "ERROR: " + arg + "\"")
    pass

