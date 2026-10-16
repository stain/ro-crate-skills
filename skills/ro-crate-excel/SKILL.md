---
name: ro-crate-excel
description: Create or update an RO-Crate from a folder of files via an Excel spreadsheet with the ro-crate-excel tools (rocxl / xlro): generate a spreadsheet of the files, let people fill in metadata, and merge it back into ro-crate-metadata.json. Use when metadata is gathered by non-programmers in spreadsheets, or the user asks to go from Excel or a folder listing to an RO-Crate. Requires Siegfried.
---

# ro-crate-excel (`rocxl`, `xlro`)

Source https://github.com/Language-Research-Technology/ro-crate-excel (npm `ro-crate-excel` 1.2.1; beta on the tools list). Help output was checked; a full run was **not completed** here because the tool needs Siegfried (`sf`), which was not installed: it prints `File identification error ... Have you installed Siegfried?`. Install Siegfried (https://github.com/richardlehane/siegfried/wiki/Getting-started) first, and test on a copy.

```bash
npm install ro-crate-excel            # provides rocxl and xlro (same tool)
rocxl [options] <directories...>
```
Per its help: generates an Excel spreadsheet and RO-Crate metadata from a set of files and updates the RO-Crate with data filled into the spreadsheet; whichever of spreadsheet and `ro-crate-metadata.json` is newer wins; the file system is always traversed and file information merged in. Options: `-b/--bag [dir]` create BagIt bag(s), `-z/--zip` zip the bagged crate (with `--bag`), `-a/--add` merge `additional-ro-crate-metadata.xlsx` into an existing crate, `-j/--JSON` use the JSON file rather than the spreadsheet, `-p/--partOf` part of another crate, `-r/--recurse`, `-d/--depth`, `-m/--maxfiles`, `-u/--url` distribution URL, `-c/--cratescript`.

## Guidance
- Run it on a copy of the folder; it writes files into the directories you give it.
- The spreadsheet gets the people's names, licences and descriptions: review the generated crate and complete the root (`name`, `description`, `datePublished`, `license`), then validate (`ro-crate-validator`). Check which RO-Crate version the output declares: the Language Data Commons tools lag the spec.
- An alternative with a GUI is `chaos2crate` or Crate-O (see `ro-crate-tools`).
