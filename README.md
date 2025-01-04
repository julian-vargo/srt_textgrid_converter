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

## Usage
1. Download the script file `srt_textgrid_converter.py` to your computer.
2. Ensure Python 3.6+ is installed and accessible via your terminal
3a. Type in the following command into your command prompt
'''bash
python "path\to\srt_textgrid_converter.py"

3b. OR type the following command into your command prompt
'''bash
python "path\to\srt_textgrid_converter.py" path\to\input\srt\folder path\to\output\textgrid\folder Speaker1NameDisplayedOnSRT Speaker2NameDisplayedOnSRT
