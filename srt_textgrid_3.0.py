import os
from tkinter import Tk, Label, Button, Entry, filedialog, StringVar
from tkinter import ttk

global speaker1
global speaker2
global indexNumber
global currentIndex
global currentTimecode
global currentSpeaker
global currentContent
global currentXmin
global currentXmax
global currentTierOneInterval
global currentTierTwoInterval
global indexNumber2
global currentIndex2
global previousXmax
global tierOneIndex
global tierTwoIndex
global finalSpeakerOneXmax
global finalSpeakerTwoXmax
global size
global inputFolder
global outputFolder

def start_processing():
    inputFolder  = inputFoldertk.get().strip()
    outputFolder = outputFoldertk.get().strip()
    speaker1    = speaker1tk.get().strip()
    speaker2    = speaker2tk.get().strip()

    for file in os.listdir(inputFolder):

        if "\\" in inputFolder:
            filePath = inputFolder + "\\" + file
            fileObject = open(filePath, "r", encoding="utf-8")
            outputPath = outputFolder + "\\" + file.replace(".srt", ".TextGrid")
        else:
            filePath = inputFolder + "/" + file
            fileObject = open(filePath, "r", encoding="utf-8")
            outputPath = outputFolder + "/" + file.replace(".srt", ".TextGrid")

        speakerOneTempPath = outputPath.replace(".TextGrid", "_speakerOneTempPath.TextGrid")
        speakerTwoTempPath = outputPath.replace(".TextGrid", "_speakerTwoTempPath.TextGrid")
        speakerOneTempPath2 = speakerOneTempPath.replace(".TextGrid", "_2.TextGrid")
        speakerTwoTempPath2 = speakerTwoTempPath.replace(".TextGrid", "_2.TextGrid")

        try:
            os.remove(speakerOneTempPath)
        except:
            print("")
        try:
            os.remove(speakerTwoTempPath)
        except:
            print("")
        try:
            os.remove(speakerOneTempPath2)
        except:
            print("")
        try:
            os.remove(speakerTwoTempPath2)
        except:
            print("")
        try:
            os.remove(outputPath)
        except:
            print("")

        # first pass
        indexNumber = 0
        currentIndex = 0
        currentTimecode = ""
        currentSpeaker = speaker1
        currentContent = ""
        currentXmin = 0.0
        currentXmax = 0.0
        currentTierOneInterval = 0
        currentTierTwoInterval = 0
        for line in fileObject:
            indexNumber = indexNumber + 1
            line = line.strip()
            if line.isdigit():
                currentIndex = indexNumber
                useFourthLine = "false"
            if indexNumber == currentIndex + 1:
                currentTimecode = line
            if indexNumber == currentIndex + 2:
                if line == f"{speaker1}:":
                    currentSpeaker = speaker1
                    useFourthLine = "true"
                elif line == f"{speaker2}:":
                    currentSpeaker = speaker2
                    useFourthLine = "true"
                else:
                    currentContent = line
            if indexNumber == currentIndex + 3:
                if useFourthLine == "true":
                    currentContent = line
                currentTimecode = currentTimecode.replace(" --> ", ",")
                currentTimecode = currentTimecode.replace(",", ":")
                startHoursi, startMinutesi, startSecondsi, startMillii, endHoursi, endMinutesi, endSecondsi, endMillii = currentTimecode.split(':')
                startHours = float(startHoursi)
                startMinutes = float(startMinutesi)
                startSeconds = float(startSecondsi)
                startMilli = float(startMillii)
                endHours = float(endHoursi)
                endMinutes = float(endMinutesi)
                endSeconds = float(endSecondsi)
                endMilli = float(endMillii)

                xminHours = startHours * 3600
                xminMinutes = startMinutes * 60            
                xminMilli = startMilli * 0.001
                currentXmin = xminHours + xminMinutes + startSeconds + xminMilli
                xmaxHours = endHours * 3600
                xmaxMinutes = endMinutes * 60
                xmaxMilli = endMilli * 0.001
                currentXmax = xmaxHours + xmaxMinutes + endSeconds + xmaxMilli

                if currentSpeaker == speaker1:
                    currentTierOneInterval = currentTierOneInterval + 1
                    speakerOneTempFile = open(speakerOneTempPath, "a", encoding="utf-8")
                    speakerOneTempFile.write(f'intervals [{currentTierOneInterval}]:\n')
                    speakerOneTempFile.write(f"xmin = {currentXmin}\n")
                    speakerOneTempFile.write(f"xmax = {currentXmax}\n")
                    speakerOneTempFile.write(f'text = "{currentContent}"\n')
                    speakerOneTempFile.close()
                if currentSpeaker == speaker2:
                    currentTierTwoInterval = currentTierTwoInterval + 1
                    speakerTwoTempFile = open(speakerTwoTempPath, "a", encoding="utf-8")
                    speakerTwoTempFile.write(f'intervals [{currentTierTwoInterval}]:\n')
                    speakerTwoTempFile.write(f"xmin = {currentXmin}\n")
                    speakerTwoTempFile.write(f"xmax = {currentXmax}\n")
                    speakerTwoTempFile.write(f'text = "{currentContent}"\n')
                    speakerTwoTempFile.close()
        speakerOneTempFile = open(speakerOneTempPath, "r", encoding="utf-8")
        currentIndex2 = 0
        previousXmax = 0.0
        currentXmin = 0
        currentXmax = 0

        #second pass, speaker 1
        for line in speakerOneTempFile:
            line = line.strip()
            if "xmin =" in line:
                currentXmin = line.replace("xmin = ", "")
            if "xmax =" in line:
                currentXmax = line.replace("xmax = ", "")
            if "text" in line:
                currentContent = line.replace('text = "', '')
                currentContent = currentContent.replace('"', '')
                currentContent = currentContent.replace("s\\", "-")
                currentContent = currentContent.replace("\\s", "-")
                currentContent = currentContent.replace("s/", "-")
                currentContent = currentContent.replace("/s", "-")
                currentXminf = float(currentXmin)
                currentXmaxf = float(currentXmax)
                previousXmaxf = float(previousXmax)
                if previousXmaxf < currentXminf:
                    currentIndex2 = currentIndex2 + 1
                    speakerOneTempFile2 = open(speakerOneTempPath2, "a", encoding="utf-8")
                    speakerOneTempFile2.write(f"intervals [{currentIndex2}]:\n")
                    speakerOneTempFile2.write(f"xmin = {previousXmax}\n")
                    speakerOneTempFile2.write(f"xmax = {currentXminf}\n")
                    speakerOneTempFile2.write(f'text = "."\n')
                    currentIndex2 = currentIndex2 + 1
                    speakerOneTempFile2.write(f"intervals [{currentIndex2}]:\n")
                    speakerOneTempFile2.write(f"xmin = {currentXminf}\n")
                    speakerOneTempFile2.write(f"xmax = {currentXmaxf}\n")
                    speakerOneTempFile2.write(f'text = "{currentContent}"\n')
                    speakerOneTempFile2.close()
                if previousXmaxf > currentXminf:
                    currentIndex2 = currentIndex2 + 1
                    speakerOneTempFile2 = open(speakerOneTempPath2, "a", encoding="utf-8")
                    speakerOneTempFile2.write(f"intervals [{currentIndex2}]:\n")
                    speakerOneTempFile2.write(f"xmin = {previousXmax}\n")
                    speakerOneTempFile2.write(f"xmax = {currentXmaxf}\n")
                    speakerOneTempFile2.write(f'text = "{currentContent}"\n')
                    if previousXmaxf < currentXmaxf:
                        print(f"{file} contains erroneous timestamp inputs at {previousXmax}, you should hand-correct these")
                    speakerOneTempFile2.close()
                if previousXmaxf == currentXminf:
                    speakerOneTempFile2 = open(speakerOneTempPath2, "a", encoding="utf-8")       
                    currentIndex2 = currentIndex2 + 1
                    speakerOneTempFile2.write(f"intervals [{currentIndex2}]:\n")
                    speakerOneTempFile2.write(f"xmin = {currentXminf}\n")
                    speakerOneTempFile2.write(f"xmax = {currentXmaxf}\n")
                    speakerOneTempFile2.write(f'text = "{currentContent}"\n')
                    speakerOneTempFile2.close()
                previousXmax = currentXmax
                currentXmaxf = float(currentXmax)
                tierOneIndex = currentIndex2
                finalSpeakerOneXmax = currentXmaxf
        speakerOneTempFile.close()

        # second pass, speaker 2
        if speaker2 != "":
            speakerTwoTempFile = open(speakerTwoTempPath, "r", encoding="utf-8")
            tierTwoIndex = currentIndex2
            finalSpeakerTwoXmax = currentXmaxf
            currentIndex2 = 0
            previousXmax = 0.0
            currentXmin = 0
            currentXmax = 0
            if speaker2 != "":
                for line in speakerTwoTempFile:
                    line = line.strip()
                    if "xmin =" in line:
                        currentXmin = line.replace("xmin = ", "")
                    if "xmax =" in line:
                        currentXmax = line.replace("xmax = ", "")
                    if "text" in line:
                        currentContent = line.replace('text = "', '')
                        currentContent = currentContent.replace('"', '')
                        currentXminf = float(currentXmin)
                        currentXmaxf = float(currentXmax)
                        previousXmaxf = float(previousXmax)
                        if previousXmaxf < currentXminf:
                            currentIndex2 = currentIndex2 + 1
                            speakerTwoTempFile2 = open(speakerTwoTempPath2, "a", encoding="utf-8")
                            speakerTwoTempFile2.write(f"intervals [{currentIndex2}]:\n")
                            speakerTwoTempFile2.write(f"xmin = {previousXmax}\n")
                            speakerTwoTempFile2.write(f"xmax = {currentXminf}\n")
                            speakerTwoTempFile2.write(f'text = "."\n')
                            currentIndex2 = currentIndex2 + 1
                            speakerTwoTempFile2.write(f"intervals [{currentIndex2}]:\n")
                            speakerTwoTempFile2.write(f"xmin = {currentXminf}\n")
                            speakerTwoTempFile2.write(f"xmax = {currentXmaxf}\n")
                            speakerTwoTempFile2.write(f'text = "{currentContent}"\n')
                            speakerTwoTempFile2.close()
                        if previousXmaxf > currentXminf:
                            currentIndex2 = currentIndex2 + 1
                            speakerTwoTempFile2 = open(speakerTwoTempPath2, "a", encoding="utf-8")
                            speakerTwoTempFile2.write(f"intervals [{currentIndex2}]:\n")
                            speakerTwoTempFile2.write(f"xmin = {previousXmax}\n")
                            speakerTwoTempFile2.write(f"xmax = {currentXmaxf}\n")
                            speakerTwoTempFile2.write(f'text = "{currentContent}"\n')
                            if previousXmaxf > currentXmaxf:
                                print(f"{file} contains erroneous timestamp inputs at {previousXmax} seconds or {previousXmaxf / 60.0} minutes, you should hand-correct these")
                            speakerTwoTempFile2.close()
                        if previousXmaxf == currentXminf:
                            speakerTwoTempFile2 = open(speakerTwoTempPath2, "a", encoding="utf-8")       
                            currentIndex2 = currentIndex2 + 1
                            speakerTwoTempFile2.write(f"intervals [{currentIndex2}]:\n")
                            speakerTwoTempFile2.write(f"xmin = {currentXminf}\n")
                            speakerTwoTempFile2.write(f"xmax = {currentXmaxf}\n")
                            speakerTwoTempFile2.write(f'text = "{currentContent}"\n')
                            speakerTwoTempFile2.close()
                        previousXmax = currentXmax
                        currentXmaxf = float(currentXmax)
                speakerTwoTempFile.close()
                tierTwoIndex = currentIndex2
                finalSpeakerTwoXmax = currentXmaxf
        os.remove(speakerOneTempPath)
        
        if speaker2 != "":
            os.remove(speakerTwoTempPath)
            if finalSpeakerTwoXmax > finalSpeakerOneXmax:
                globalMax = finalSpeakerTwoXmax
            else:
                globalMax = finalSpeakerOneXmax

        if speaker2 != "":
            outputFile = open(outputPath, "a", encoding="utf-8")
            outputFile.write('File type = "ooTextFile"\n')
            outputFile.write('Object class = "TextGrid"\n')
            outputFile.write('\n')
            outputFile.write('xmin = 0\n')
            outputFile.write(f'xmax = {globalMax}\n')
            outputFile.write('tiers? <exists>\n')
            outputFile.write(f'size = 2\n')
            outputFile.write('item []:\n')
            outputFile.write('item [1]:\n')
            outputFile.write('class = "IntervalTier"\n')
            outputFile.write(f'name = "{speaker1}"\n')
            outputFile.write('xmin = 0\n')
            outputFile.write(f'xmax = {finalSpeakerOneXmax}\n')
            outputFile.write(f'intervals: size = {tierOneIndex}\n')
            speakerOne = open(speakerOneTempPath2, "r", encoding="utf-8")
            speakerTwo = open(speakerTwoTempPath2, "r", encoding="utf-8")
            outputFile.write(speakerOne.read())
            outputFile.write('item [2]:\n')
            outputFile.write('class = "IntervalTier"\n')
            outputFile.write(f'name = "{speaker2}"\n')
            outputFile.write('xmin = 0\n')
            outputFile.write(f'xmax = {finalSpeakerTwoXmax}\n')
            outputFile.write(f'intervals: size = {tierTwoIndex}\n')
            outputFile.write(speakerTwo.read())
            speakerTwo.close()
            os.remove(speakerTwoTempPath2)
        else:
            outputFile = open(outputPath, "a", encoding="utf-8")
            outputFile.write('File type = "ooTextFile"\n')
            outputFile.write('Object class = "TextGrid"\n')
            outputFile.write('xmin = 0\n')
            outputFile.write(f'xmax = {finalSpeakerOneXmax}\n')
            outputFile.write('tiers? <exists>\n')
            outputFile.write(f'size = 1\n')
            outputFile.write('item []:\n')
            outputFile.write('item [1]:\n')
            outputFile.write('class = "IntervalTier"\n')
            outputFile.write(f'name = "{speaker1}"\n')
            outputFile.write('xmin = 0\n')
            outputFile.write(f'xmax = {finalSpeakerOneXmax}\n')
            outputFile.write(f'intervals: size = {tierOneIndex}\n')
            speakerOne = open(speakerOneTempPath2, "r", encoding="utf-8")
            outputFile.write(speakerOne.read())
        outputFile.close()
        speakerOne.close()
        os.remove(speakerOneTempPath2)

## UI DESIGN
app = Tk()
app.title("SRT to TextGrid Converter - Julian Vargo 2025 - UC Berkeley")
app.configure(bg="grey20")

style = ttk.Style()
style.configure("TLabel", foreground="azure", background="grey20")
style.configure("TButton", background="grey15", foreground="azure", relief="flat")
style.configure("TEntry", fieldbackground="grey15", foreground="azure")

inputFoldertk = StringVar()
outputFoldertk = StringVar()
speaker1tk = StringVar(value="Speaker1")
speaker2tk = StringVar(value="Speaker2")

Label(app, text="Enter your input folder containing your SRT files.", bg="grey20", fg="azure").grid(row=0, column=0, sticky="w", padx=10, pady=5)
Entry(app, textvariable=inputFoldertk, width=40, bg="grey15", fg="azure", insertbackground="azure").grid(row=0, column=1, padx=10, pady=5)

Label(app, text="Enter your output folder where you want your TextGrids to go.", bg="grey20", fg="azure").grid(row=4, column=0, sticky="w", padx=10, pady=5)
Entry(app, textvariable=outputFoldertk, width=40, bg="grey15", fg="azure", insertbackground="azure").grid(row=4, column=1, padx=10, pady=5)

Label(app, text="Enter the name of Speaker 1 exactly as it appears in the SRT files (eg. Speaker1, Interviewer)", bg="grey20", fg="azure").grid(row=8, column=0, sticky="w", padx=10, pady=5)
Entry(app, textvariable=speaker1tk, width=40, bg="grey15", fg="azure", insertbackground="azure").grid(row=8, column=1, padx=10, pady=5)

Label(app, text="Enter the name of Speaker 2. Leave blank if you don't want a Speaker 2 tier.", bg="grey20", fg="azure").grid(row=12, column=0, sticky="w", padx=10, pady=5)
Entry(app, textvariable=speaker2tk, width=40, bg="grey15", fg="azure", insertbackground="azure").grid(row=12, column=1, padx=10, pady=5)
Button(app, text="Start Processing", command=start_processing, bg="grey15", fg="azure").grid(row=14, column=0, columnspan=3, pady=10)
app.mainloop()