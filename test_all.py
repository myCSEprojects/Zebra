'''
Run this file to get perform all the checks
'''

import os # to get the test file names at the run time
from importlib import import_module
import io
from contextlib import redirect_stdout
from zebra import executeFile

# Get the list of all the file names in the tests folder
files = list (os.listdir("tests/"))

# Lists for failed and succeded test cases
tests_succeed = []
tests_fail = []

# Iterating through all the files in the tests folder
for test_file in files:

    # Striping spaces if any
    test_file = test_file.strip()

    # if (test_file.endswith(".py") and test_file.startswith("test")):
    #     # Verbose text
    #     print(f"\033[95mCurrent Test File:\033[00m \033[93m{test_file}\033[00m")

    #     # Importing the test file at runtime
    #     test = import_module("tests." + test_file[:-3]).test
        
    #     try:
    #         # Cheking if the test case return the value 0 or -1
    #         if (test() == -1):
    #             tests_fail.append(test_file)
    #         else:
    #             tests_succeed.append(test_file)
    #     except:
    #         tests_fail.append(test_file)
        
    #     print("\033[04m" + (" " * os.get_terminal_size().columns) + "\033[0m")
    if (test_file.endswith(".zebra") and test_file.startswith("test")):
        # Verbose text
        print(f"\033[95mCurrent Test File:\033[00m \033[93m{test_file}\033[00m")
        
        # Redirecting the output to a string
        f = io.StringIO()
        try:
            with redirect_stdout(f):
                executeFile("tests/" + test_file, False, True)
        except:
            pass
        
        out = f.getvalue().strip()
        
        # Print the output
        print(out)
        
        # Compare the output with the expected output
        with open("tests/" + test_file[:-6] + ".out", 'r') as file:
            out_exp = ''.join(file.readlines()).strip()
            if out_exp == out:
                tests_succeed.append(test_file)
            else:
                tests_fail.append(test_file)
        
        print("\033[04m" + (" " * os.get_terminal_size().columns) + "\033[0m")

# Display the failed and the succeded test cases
for test_file in tests_succeed:
    print (f"\033[1;92mTest {test_file} succeeded\033[0m")

for test_file in tests_fail:
    print (f"\033[1;91mTest {test_file} failed\033[0m")