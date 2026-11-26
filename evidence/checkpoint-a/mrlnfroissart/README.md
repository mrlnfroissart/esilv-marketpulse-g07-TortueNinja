# Checkpoint A - Marlon Froissart (mrlnfroissart)

Team repository: mrlnfroissart/esilv-marketpulse-g07-TortueNinja

## 01_terminal_python.png
`python src/main.py` run on the TD04 commit `44b2d96`. It displays the MarketPulse summary
for AAPL (instrument) and SP500 (benchmark) from the local sample data, including
first/last observation dates and first/last close.

## 02_git_status_log.png
`git status` shows a clean working tree on `main`.
`git log --oneline` shows my commits, including:
- `c420d21` feat: add TD02 Python CSV/JSON notebook (TD03)
- `44b2d96` feat: display first and last observation dates (TD04)

## 03_branch_merge.png
The TD04 feature commit `44b2d96` was made on a feature branch created from `main`.
`git log --oneline --graph` shows it sitting directly on top of `b9cfd52`, so it was
integrated into `main` without a merge commit (fast-forward). The original branch is
kept locally as `archive/td04-local`.
`git branch -a --contains 44b2d96` lists `main` and `remotes/origin/main`, which shows
the feature is merged into `main`, locally and on GitHub.
