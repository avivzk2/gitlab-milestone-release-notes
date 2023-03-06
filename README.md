### Gitlab Milestone Release Notes Generator
Easy script that generates release notes for a Gitlab milestone.

### Example output
```markdown
## v0.80 Release

#### Main Tasks
- Configuration validation
- Bug fixes
- CI: Add MyPy

##### Optional
- [ ] Deploy new pipeline

### Open Issues
 - API coverage ([#2058](<url>)) (@jessica)

### Closed Issues
 - Verify configration ([#2044](<url>)) (@bob)
 - Requested additions ([#2034](<url>)) (@michael)
 - Update demo server ([#2028](<url>)) (@roy)
 - Bug in response on feedback ([#2017](<url>)) (@jessica)

### Open MRs
 - Draft: Resolve "Move ALLOWED_HOSTS to .env file" ([#1761](<url>)) (@roy)
 - Draft: Resolve "Deploy pipeline" ([#1460](<url>)) (@jessica)
 - Draft: Resolve "Add MyPy to CI" ([#1455](<url>)) (@roy)

### Closed MRs
 - Draft: Resolve "Query API" ([#1453](<url>)) (none)
 - Update version in request ([#66](<url>)) (@jessica)

### Merged MRs
 - Resolve "Add Confluence data" ([#1467](<url>)) (@roy)
 - Resolve "Update status" ([#1465](<url>)) (@greg)
 - HOTFIX: Clear session cache ([#86](<url>)) (@jessica)
```


### Usage

Install dependencies
```
pip install -r requirements.txt
```

Run
```
python glrn.py <group_name> <milestone_name> --server <server_host> --token <token>
```

Example:
```
python glrn.py group1 "v0.44 release" --server https://gitlab.com --token xxxxxx
```
