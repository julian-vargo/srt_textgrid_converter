# SRT to TextGrid Converter

Convert .srt files to Praat TextGrid format. This program is excellent for converting .srt outputs from automatic transcribers like sonix.ai or otter.ai and preparing them for corpus development or forced alignment. The output places Speaker 1 on the first tier and (optionally) Speaker 2 on the second tier. Silences are indicated with a period "." on the final TextGrid and are automatically created by detecting gaps in the SRT.

## Installation and Running the Script
To run the program: <br>
-Download the .py file and run the program (you can do this through the command line or through an app that can run Python like VS Code. <br>

A user interface will appear. Just enter your desired file paths and speaker names into the entry box, and click "start processing".

## Citation
Vargo, Julian (2025). SRT to TextGrid File Converter [Python Script].<br>
Department of Spanish and Portuguese. UC Berkeley.<br>

## Requirements
- Written on Python 3.12.8
- Python 3.6 or higher is required
- .srt contains at most 2 unique speakers
