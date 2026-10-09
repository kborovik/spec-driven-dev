# Path-scoped auto-commit (canonical)

Every skill auto-commit path-scopes owned files:

```
git commit -m <subject> [-m <body>] -- <paths>
```

`-m` flags must precede `--` — tokens after `--` parse as pathspecs.
Bare `git add <paths>` + `git commit` banned (commits whole index → pre-staged file leaks).
`git add -A` banned.
