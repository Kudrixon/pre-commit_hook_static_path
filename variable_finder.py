import ast
import subprocess


def find_vars(file_name):
    # Get the output of the `git diff` command
    diff_output = subprocess.run(
        ['git', 'diff', 'HEAD', file_name], capture_output=True, text=True).stdout
    print(diff_output)

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
        elif isinstance(node, ast.Name):
            vars.append((node.id, node.lineno))
    return vars


file_name = 'sample.py'
print(find_vars(file_name))
