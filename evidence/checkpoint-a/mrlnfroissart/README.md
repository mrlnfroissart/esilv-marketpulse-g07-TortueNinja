# Checkpoint A - Marlon Froissart (mrlnfroissart)

Team repository: mrlnfroissart/esilv-marketpulse-g07-TortueNinja

## 01_terminal_python.png
`python src/main.py` runs and displays the MarketPulse summary for AAPL (instrument)
and SP500 (benchmark), including first/last observation dates and first/last close.

## 02_git_status_log.png
`git status` shows a clean working tree on `main`.
`git log --oneline` shows my commits:
- `c420d21` feat: add TD02 Python CSV/JSON notebook (TD03)
- `44b2d96` feat: display first and last observation dates (TD04)

## 03_branch_merge.png
Feature branch `feature/display-observation-dates` was created from `main`,
the feature was committed on it (`44b2d96`), then merged into `main`.
The merge was a fast-forward, so the graph stays linear at the top.
`git branch --merged` lists the feature branch as merged into `main`.
