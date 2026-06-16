# Contributing

Thanks for helping keep this index sharp! 🎯

## Add or update a repo

1. Find the matching file in `categories/` (e.g. `categories/mcp-servers.md`).
2. Add a new row at the appropriate position (sorted by stars desc).
3. Keep the table columns: **Repository | Description | Language | Stars | Code**.
4. Use the existing badge styles (see other rows for examples).

## Fix a wrong category

If a repo is mis-categorised, just move the row to the correct file. Categories are decided by topic / description / language. A repo can appear in multiple files.

## Pull request checklist

- [ ] Repo URL works and is public
- [ ] Description is one short sentence
- [ ] Table renders correctly (preview the markdown)
- [ ] No duplicate rows in the same file

## Regenerate from the dataset

The whole project can be regenerated from `data/repos_5080_all_unique.json` via:

```bash
python3 scripts/build.py
```

(The build script lives in `scripts/build.py`.)
