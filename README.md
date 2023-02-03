# pre-commit-check 

Pre-commit hook based on https://pre-commit.com.

## Use-Case: Need to exclude spefific string from commiting to codebase

### Sample Usage

#### 1. Add the hook to your .pre-commit-config.yaml

```
repos:
- repo: https://github.com/Kudrixon/pre-commit_hook_static_path
  rev: v1.0.0
  hooks:
    - id: check-static-path
      args: ["/home/tester]
```
