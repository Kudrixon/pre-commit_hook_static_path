import re
import subprocess
import sys
import platform
import traceback
import argparse
from typing import Sequence

pattern = r'^\+\+\+ ./(.*)|^@@ -[0-9]+(,[0-9]+)? \+(.*)(?= @@)'

def extractMatches(text, pattern):
    result = []
    lines = text.splitlines()
    for line in lines:
        match = re.search(pattern, line)
        if match:
            result.append(match.group(0))
    return result

def findStringInRangeForFile(filename, keyword, changes_range):
    result = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            for start, end in changes_range:
                if start <= i+1 <= end and keyword in line:
                    result.append((filename, i+1, line))
    return result

def findStringInRange(filenames, keyword):
    result = []
    for filename in filenames:
        text = subprocess.run(['git', 'diff', "--unified=0", 'HEAD', filename], capture_output=True, text=True).stdout
        matches = extractMatches(text, pattern)
        changes_range = []
        for s in matches:
            if s.startswith("@@ -"):
                range_string = s.split(" ")[2]
                start = int(range_string.split(",")[0].replace("+", ""))
                end = start + sum(map(int, range_string.split(",")[1:]))
                if end - start <=0:
                    changes_range.append((start, end))
                else:
                    changes_range.append((start, end - 1))
        result += findStringInRangeForFile(filename, keyword, changes_range)
    return result

def findStringInFile(filename, keyword, retval):
    with open(filename, 'r') as f:
        lines = f.readlines()
    for line_num, line in enumerate(lines, start=1):
        if keyword in line:
            print(f"Specified keyword: {keyword} detected in file {filename}, line {line_num} content: {line}")
            retval = 1
    return retval


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    parser.add_argument('-k', '--keyword', help='Static string excluded in commiting', required=True)
    parser.add_argument('-nd', '--nodiff', default="false", choices=['true', 'false'], help='If you need to check just specified file select true')

    args = parser.parse_args(argv)

    retval = 0

    if(args.nodiff == "false"):
        text = subprocess.run(['git', 'diff', "--unified=0", 'HEAD'], capture_output=True, text=True).stdout
        matches = extractMatches(text, pattern)
        filenames = [match.replace("+++ b/", "") for match in matches if match.startswith("+++ b/")]
        filenames = [filename for filename in filenames if filename is not None]
        results = findStringInRange(filenames, args.keyword)
        for r in results:
            print(f"Static path of {args.keyword} detected in file {r[0]}, line {r[1]} content: {r[2]}, change to dynamic needed")
            retval = 1

    else:
        for filename in args.filenames:
            try:
                retval = findStringInFile(filename, args.keyword, retval)

            except SyntaxError:
                impl = platform.python_implementation()
                version = sys.version.split()[0]
                print(f'{filename}: failed parsing with {impl} {version}:')
                tb = '    ' + traceback.format_exc().replace('\n', '\n    ')
                print(f'\n{tb}')
                retval = 1

    return retval

if __name__ == '__main__':
    raise SystemExit(main())