# SRT to TextGrid Converter

Convert .srt files to Praat TextGrid format via the command line. This script is particularly useful for converting .srt outputs from automatic transcribers like sonix.ai or otter.ai and preparing them for forced alignment. The output places Speaker 1 on the first tier and Speaker 2 on the second tier. Silences are indicated with s\ on the final TextGrid but need not be prewritten into your SRT.

## Requirements
- Written on Python 3.12.8
- Python 3.6 or higher is required
- .srt contains at most 2 unique speakers

## Installation and Running the Script
1. Download the script file `srt_textgrid_converter.py` to your computer.
2. Ensure Python 3.6+ is installed and accessible via your terminal.
3. Select option 3a or 3b to run your script:

**3a.** Type in the following command into your command prompt, terminal, or Anaconda Prompt

```bash
python "path\to\srt_textgrid_converter.py"
```

**3a cont.** Then, the command prompt will ask you some questions about file paths and speaker names. Enter these in one at a time.

<br>

**3b.** OR type the following command into your command prompt, terminal, or Anaconda Prompt
```bash
python "path\to\srt_textgrid_converter.py" path\to\input\srt\folder path\to\output\textgrid\folder Speaker1NameDisplayedOnSRT Speaker2NameDisplayedOnSRT
```

<br>
## Citation<br>
Vargo, Julian (2025). SRT to TextGrid File Converter [Python Script].<br>
Department of Spanish and Portuguese. UC Berkeley.<br>
