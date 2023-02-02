import ast
import subprocess
import re


def checkDiffVariables(diff, keyword):
    varList = []
    for line in diff.splitlines():
        if line.startswith("+"):
            if keyword in line:
                result = re.search('(?<=\+)(.*?)(?=\=)', line)
                if result != None:
                    varList.append(result.group(1).strip())
    return varList


def checkDiffArguments(diff, keyword):
    argList = []
    for line in diff.splitlines():
        if line.startswith("+"):
            if keyword in line:
                result = re.search('(?<=\())(.*?)(?=\))', line)
                if result != None:
                    argList.append(result.group(1).strip())
    return argList


def findVars(file_name):
    diff_output = subprocess.run(
        ['git', 'diff', 'HEAD', file_name], capture_output=True, text=True).stdout
    print(diff_output)

    incorrectVariables = checkDiffVariables(diff_output, "/home/tester")

    print(incorrectVariables)
    with open(file_name, 'r') as file:
        source_code = file.read()
    tree = ast.parse(source_code)
    vars = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args = [
                arg.arg for arg in node.args.args]
            vars += args
            print()
        elif isinstance(node, ast.Name) and node.id in incorrectVariables:
            vars.append((node.id, node.lineno))
    return vars


file_name = 'sample.py'
print(findVars(file_name))
