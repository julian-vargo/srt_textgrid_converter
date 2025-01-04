import os
import codecs
import argparse
from pathlib import Path

class srtInterval:
    def __init__(self, number, range, content):
        self.number = number[:]
        self.range = range[:]
        self.startTime, self.endTime = [
            self._convert_time(t) for t in range.split(" --> ")
        ]
        self.content = content.replace('"', '""')

    def _convert_time(self, time_str):
        h, m, s = time_str.replace(",", ".").split(":")
        return round(int(h) * 3600 + int(m) * 60 + float(s), 6)

def process_file(inFile, output_file_path, speaker1_name="Speaker1", speaker2_name="Speaker2"):
    print(f"Processing file: {inFile}")
    intervals = []
    with codecs.open(inFile, 'r', 'utf-8') as iFile:
        lines = iFile.read().splitlines()
        if lines[-1] != "":
            lines.append("")
        lines = [line for i, line in enumerate(lines) if not (line == "" and lines[i - 1] == "")]
        lineCounter = 0
        lastSpeaker = None
        while lineCounter < len(lines):
            tempIndex = lines[lineCounter]
            lineCounter += 1
            tempTime = lines[lineCounter]
            lineCounter += 1
            tempContent = lines[lineCounter]
            lineCounter += 1
            while lineCounter < len(lines) and lines[lineCounter].strip() != "":
                tempContent += "\n" + lines[lineCounter]
                lineCounter += 1
            lineCounter += 1
            currentInterval = srtInterval(tempIndex, tempTime, tempContent)
            if f"{speaker1_name}:" in currentInterval.content:
                currentInterval.content = currentInterval.content.replace(f"{speaker1_name}:", "").strip()
                lastSpeaker = speaker1_name
            elif f"{speaker2_name}:" in currentInterval.content:
                currentInterval.content = currentInterval.content.replace(f"{speaker2_name}:", "").strip()
                lastSpeaker = speaker2_name
            intervals.append((currentInterval.startTime, currentInterval.endTime, lastSpeaker, currentInterval.content))
    intervals.sort(key=lambda x: x[0])
    speaker1_tier = []
    speaker2_tier = []
    last_end_time_speaker1 = 0
    last_end_time_speaker2 = 0
    for start, end, speaker, content in intervals:
        if speaker == speaker2_name and last_end_time_speaker1 < start:
            speaker1_tier.append((last_end_time_speaker1, start, "s\\"))
            last_end_time_speaker1 = start
        if speaker == speaker1_name and last_end_time_speaker2 < start:
            speaker2_tier.append((last_end_time_speaker2, start, "s\\"))
            last_end_time_speaker2 = start
        if speaker == speaker1_name:
            if last_end_time_speaker1 < start:
                speaker1_tier.append((last_end_time_speaker1, start, "s\\"))
            speaker1_tier.append((start, end, content))
            last_end_time_speaker1 = end
        elif speaker == speaker2_name:
            if last_end_time_speaker2 < start:
                speaker2_tier.append((last_end_time_speaker2, start, "s\\"))
            speaker2_tier.append((start, end, content))
            last_end_time_speaker2 = end
    xmax = max(last_end_time_speaker1, last_end_time_speaker2)
    speaker1_tier = merge_silent_intervals(speaker1_tier)
    speaker2_tier = merge_silent_intervals(speaker2_tier)
    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write("File type = \"ooTextFile\"\n")
            output_file.write("Object class = \"TextGrid\"\n\n")
            output_file.write("xmin = 0\n")
            output_file.write(f"xmax = {xmax}\n")
            output_file.write("tiers? <exists>\n")
            output_file.write("size = 2\n")
            output_file.write("item []:\n")
            output_file.write("\titem [1]:\n")
            output_file.write("\t\tclass = \"IntervalTier\"\n")
            output_file.write(f"\t\tname = \"{speaker1_name}\"\n")
            output_file.write("\t\txmin = 0\n")
            output_file.write(f"\t\txmax = {xmax}\n")
            output_file.write(f"\t\tintervals: size = {len(speaker1_tier)}\n")
            for i, (start, end, text) in enumerate(speaker1_tier, start=1):
                output_file.write(f"\t\tintervals [{i}]:\n")
                output_file.write(f"\t\t\txmin = {start}\n")
                output_file.write(f"\t\t\txmax = {end}\n")
                output_file.write(f"\t\t\ttext = \"{text}\"\n")
            output_file.write("\titem [2]:\n")
            output_file.write("\t\tclass = \"IntervalTier\"\n")
            output_file.write(f"\t\tname = \"{speaker2_name}\"\n")
            output_file.write("\t\txmin = 0\n")
            output_file.write(f"\t\txmax = {xmax}\n")
            output_file.write(f"\t\tintervals: size = {len(speaker2_tier)}\n")
            for i, (start, end, text) in enumerate(speaker2_tier, start=1):
                output_file.write(f"\t\tintervals [{i}]:\n")
                output_file.write(f"\t\t\txmin = {start}\n")
                output_file.write(f"\t\t\txmax = {end}\n")
                output_file.write(f"\t\t\ttext = \"{text}\"\n")
        print(f"TextGrid file successfully written to {output_file_path}")
    except Exception as e:
        print(f"Error while writing TextGrid file: {e}")

def merge_silent_intervals(tier):
    merged = []
    for start, end, text in tier:
        if text == "s\\" and merged and merged[-1][2] == "s\\" and merged[-1][1] == start:
            merged[-1] = (merged[-1][0], end, text)
        else:
            merged.append((start, end, text))
    return merged

def sanitize_path(path):
    return path.strip('"')

def main():
    parser = argparse.ArgumentParser(description="Convert SRT files to TextGrid with custom speaker names.")
    parser.add_argument("input_folder", type=str, nargs="?", help="Path to the input folder containing SRT files.")
    parser.add_argument("output_folder", type=str, nargs="?", help="Path to the output folder for TextGrid files.")
    parser.add_argument("--speaker1", type=str, default="Speaker1", help="Custom name for Speaker 1.")
    parser.add_argument("--speaker2", type=str, default="Speaker2", help="Custom name for Speaker 2.")
    args = parser.parse_args()

    # Prompt for missing arguments interactively
    input_folder = args.input_folder or input("Enter the path to the input folder containing SRT files: ").strip()
    output_folder = args.output_folder or input("Enter the path to the output folder for TextGrid files: ").strip()

    input_folder = sanitize_path(input_folder)
    output_folder = sanitize_path(output_folder)

    speaker1_name = input(f"Enter the name for Speaker 1 (default: {args.speaker1}): ").strip() or args.speaker1
    speaker2_name = input(f"Enter the name for Speaker 2 (default: {args.speaker2}): ").strip() or args.speaker2

    Path(output_folder).mkdir(parents=True, exist_ok=True)
    for filename in os.listdir(input_folder):
        if filename.endswith(".srt"):
            inFile = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename.replace(".srt", ".TextGrid"))
            process_file(inFile, output_file_path, speaker1_name, speaker2_name)
    print("Processing complete.")

if __name__ == "__main__":
    main()
