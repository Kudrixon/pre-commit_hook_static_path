# Pre-commit-check: Check static paths/strings 

Pre-commit hook based on https://pre-commit.com.

## Use-Case: Need to exclude specific string from commiting to codebase

### Sample Usage

#### 1. Add the hook to your .pre-commit-config.yaml

```
repos:
- repo: https://github.com/Kudrixon/pre-commit_hook_static_path
  rev: v1.0.0
  hooks:
    - id: check-static-path
      args: ["-k=/home/tester"]
      verbose: true
```

Run this in your terminal:
```
pre-commit run check-static-path
```

Expected output if no occurrences in files:
```
pre-commit run check-static-path
check static path........................................................Passed
- hook id: check-static-path
- duration: 0.4s
```

Expected output diff mode if string exists:
```
pre-commit run check-static-path
check static path........................................................Failed
- hook id: check-static-path
- duration: 0.54s
- exit code: 1

Static path of /home/vtest detected in file pre_commit_hooks/sample.py, line 33 content: kualalumpur("/home/vtest"), change to 
dynamic needed
```

Expected output no-diff mode if string exists:
```
pre-commit run --files .\pre_commit_hooks\sample.py  
check static path........................................................Failed
- hook id: check-static-path
- duration: 0.22s
- exit code: 1

Specified keyword: /home/vtest detected in file pre_commit_hooks/sample.py, line 1 content: kualalumpur("/home/vtest")
```


### Parameters

***--filename***:
By default this pre-commit dont need You to provide filename because diff mechanism gets it by itself. When executed pre-commit mechanism gets filename parameter anyway.

***--keywords, -k***:
[REQUIRED] Provide this to find specific list of strings existing in incoming commit, or to find it in file specified by You

***--nodiff, -nd***:
If You wish to use this pre-commit to check for string in whole file not just in incoming changes you can use this flag with parameters: "false" which is default setting for using script in diff mode, "true" sets script in no-diff mode which allows user to find phrase in whole file chosen previously
