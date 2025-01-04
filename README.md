# SRT to TextGrid Converter

Convert SRT files to Praat TextGrid format with customizable speaker names. This script is designed to help linguists and researchers quickly convert subtitle files into TextGrid format for linguistic analysis.

## Features
- Supports custom speaker names.
- Handles silent intervals automatically.
- Easy-to-use command line input

## Requirements
- This script was written on Python 3.12.8
- Python 3.6 or higher is required
- SRT filed with at most 2 unique speakers

## Installation and Running the Script
1. Download the script file `srt_textgrid_converter.py` to your computer.
2. Ensure Python 3.6+ is installed and accessible via your terminal.
3. Select option 3a or 3b to run your script:
<br>
**3a.** Type in the following command into your command prompt, terminal, or Anaconda Prompt
<br>
```bash
python "path\to\srt_textgrid_converter.py"
```
**3a cont.** Then, the command prompt will prompt you with some questions about file paths and speaker names. Enter these in one at a time.
<br><br>
**3b.** OR type the following command into your command prompt, terminal, or Anaconda Prompt
```bash
python "path\to\srt_textgrid_converter.py" path\to\input\srt\folder path\to\output\textgrid\folder Speaker1NameDisplayedOnSRT Speaker2NameDisplayedOnSRT
```
