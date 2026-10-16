---
name: ro-crate-excel
description: Create or update an RO-Crate from a folder of files via an Excel spreadsheet with the ro-crate-excel tools (rocxl / xlro): generate a spreadsheet of the files, let people fill in metadata, and merge it back into ro-crate-metadata.json. Use when metadata is gathered by non-programmers in spreadsheets, or the user asks to go from Excel or a folder listing to an RO-Crate. Requires Siegfried.
---

# ro-crate-excel (`rocxl`, `xlro`)

Source https://github.com/Language-Research-Technology/ro-crate-excel (npm `ro-crate-excel` 1.2.1; beta on the tools list). Tested end to end by two agents on a sample folder once Siegfried was installed.

## Install
```bash
npm install ro-crate-excel                 # provides rocxl and xlro (same tool)
```
It needs **Siegfried** (`sf`, file-format identification): download the binary from https://github.com/richardlehane/siegfried/releases, put `sf` on `PATH`, run `sf -update` once (the signature file `default.sig` goes in `~/siegfried/`). Without it the tool prints `File identification error ... Have you installed Siegfried?` and writes nothing.

## Use
```bash
cp -r folder folder-work && rocxl -r folder-work       # first run: spreadsheet + crate
# collaborators fill in ro-crate-metadata.xlsx
rocxl -r folder-work                                   # second run: merge the edited sheet into ro-crate-metadata.json
```
- Use `-r` (recurse): without it files in subfolders are skipped. First run writes `ro-crate-metadata.xlsx`, `ro-crate-metadata.json` and `ro-crate-preview.html` **in the folder**; sheets: `RootDataset` (Name/Value list for the crate), `@type=File`, `@type=Dataset` (one row per file/folder with `@id`, `name`, `description`, size, date, format; extra columns allowed), `@type=DigitalFormat` (PRONOM-identified formats).
- Whichever of the spreadsheet and the JSON is newer wins; the folder is re-scanned on every run and file information is merged in. Other options: `-b/--bag [dir]` BagIt bag(s), `-z/--zip` (with `--bag`), `-a/--add` merge `additional-ro-crate-metadata.xlsx`, `-j/--JSON` use the JSON rather than the spreadsheet, `-p/--partOf`, `-d/--depth`, `-m/--maxfiles`, `-u/--url`, `-c/--cratescript`.

## Checked output and cautions
- It declares **RO-Crate 1.2**, writes `license` as a plain string (give a licence URL or a licence entity), and in one round trip dropped `contentSize` of an edited file: compare before and after.
- It rewrites files in place: work on a copy or under version control.
- Multi-valued cells are JSON-like arrays (`["a","b"]`); brief the people filling the sheet.
- Review the generated crate, complete the root (`name`, `description`, `datePublished`, `license`), validate (`ro-crate-validator`; not done in the test runs).
- GUI alternatives without Excel: Crate-O, `chaos2crate` (see `ro-crate-tools`).
