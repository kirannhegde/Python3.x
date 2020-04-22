import os
import re
import sys

# Assumptions:
# 1)utf-8 encoded
# 2)The input file is large enough to work with standard file functions
# 3)The script will be executed on Linux and not Windows(windows needs file paths with spaces to be enclosed in
# double quotes)
# 4)For every test case, there is one Start statement and only one Passed or Failed statement in the log.


file_path = input("Please enter the full path to the file, including the file extension:")
# Remove leading and trailing white spaces
file_name = file_path.strip()

# Necessary validation.
if os.path.exists(file_name):
    if not os.path.isfile(file_name):
        print("{} is not a valid file. Please provide the path to a valid file.".format(file_name))
        # Using f-strings for string formatting is cleaner. However, we need Python 3.6 or higher.
        # print(f"{file_name} is not a valid file. Please provide the path to a valid file.")
        sys.exit(1)
else:
    print("Path {} not found. Please provide a valid file path.".format(file_name))
    sys.exit(1)

# Assuming that the encoding is set to utf-8. Generally, utf-8 is the most common encoding found.
with open(file_name, "rt", encoding="utf-8") as fs:
    file_text = fs.read()

regexpr_started_tests = r"\s*Start\s*([0-9]+)"
started_tests = re.findall(regexpr_started_tests, file_text, re.IGNORECASE)
# Check if a list populated with matched strings is found.
# Empty sequences and collections in Python are considered false. Hence, using a list in an if condition is Pythonic.
# https://docs.python.org/3/library/stdtypes.html#truth-value-testing
if not started_tests:
    print("No information about started tests found in the log file at:{}",file_name)

regexpr_passed_tests = r".*#([0-9]+).*Passed"
passed_tests = re.findall(regexpr_passed_tests, file_text, re.IGNORECASE)
if not passed_tests:
    print("No information about passed tests found in the log file at:{}",file_name)

regexpr_failed_tests = r".*#([0-9]+).*Failed"
failed_tests = re.findall(regexpr_failed_tests, file_text, re.IGNORECASE)

# Print summary of all finished but failed tests.
if failed_tests:
    print("The following test cases failed during their execution:")
    print(*failed_tests,sep="\n")
else:
    print("No information about failed tests found in the log file at:{}",file_name)

# Print summary of all started but not finished tests
# Prefer to use the 'difference' and 'union' functions of the set class as they make the code more readable.
set_tests_with_results = set(passed_tests).union(set(failed_tests))
set_started_not_finished = set(started_tests).difference(set_tests_with_results)
if set_started_not_finished:
    print("The following test cases started but did not finish yet:")
    print(*set_started_not_finished,sep='\n')
else:
    print("Unable to determine the test cases which have started but not finished.")






