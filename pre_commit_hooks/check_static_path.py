import re
import subprocess

def extractMatches(text, pattern):
    result = []
    lines = text.splitlines()
    for line in lines:
        match = re.search(pattern, line)
        if match:
            result.append(match.group(0))
    return result

pattern = r'^\+\+\+ ./(.*)|^@@ -[0-9]+(,[0-9]+)? \+(.*)(?= @@)'

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


text = subprocess.run(['git', 'diff', "--unified=0", 'HEAD'], capture_output=True, text=True).stdout
matches = extractMatches(text, pattern)

filenames = [match.replace("+++ b/", "") for match in matches if match.startswith("+++ b/")]
filenames = [filename for filename in filenames if filename is not None]

keyword = "/home/tester"
results = findStringInRange(filenames, keyword)


for r in results:
    print(f"Static path of {keyword} detected in file {r[0]}, line {r[1]} content: {r[2]}, change to dynamic needed")
