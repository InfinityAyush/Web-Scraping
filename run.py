from subprocess import call

def open_py_file():
    call(["python","step_1.py"])
    call (["python","step_2.py"])
    call(["python","step_3.py"])


open_py_file()