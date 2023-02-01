import ast
import subprocess
import re


def findVars(file_name):
    # Get the output of the `git diff` command
    diff_output = subprocess.run(
        ['git', 'diff', 'HEAD', file_name], capture_output=True, text=True).stdout
    print(diff_output)

    incorrectVariables = []

    for line in diff_output.splitlines():
        if line.startswith("+"):
            if "/home/tester" in line:
                result = re.search('(?<=\+)(.*?)(?=\=)', line)
                incorrectVariables.append(result.group(1).strip())

    print(incorrectVariables)
    with open(file_name, 'r') as file:
        source_code = file.read()
    tree = ast.parse(source_code)
    vars = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args = [
                arg.arg for arg in node.args.args if arg in incorrectVariables]
            vars += args
            print()
        elif isinstance(node, ast.Name) and node.id in incorrectVariables:
            vars.append((node.id, node.lineno))
    return vars


file_name = 'sample.py'
print(findVars(file_name))
