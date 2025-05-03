import os
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

# If you don't want a Speaker2 tier, then just leave speaker2 blank with empty quotes ""
inputFolder = r"C:\Users\julia\Downloads\coding\python_scripts\bittar_srt_textgrid\test_input"
outputFolder = r"C:\Users\julia\Downloads\coding\python_scripts\bittar_srt_textgrid\test_output"
speaker1 = "Speaker1"
speaker2 = "Speaker2"

for file in os.listdir(inputFolder):
    filePath = inputFolder + "\\" + file
    fileObject = open(filePath, "r", encoding="utf-8")
    outputPath = outputFolder + "\\" + file.replace(".srt", ".TextGrid")
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
    for line in speakerOneTempFile:
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
    speakerOneTempFile.close()
    speakerTwoTempFile = open(speakerTwoTempPath, "r", encoding="utf-8")
    tierOneIndex = currentIndex2
    finalSpeakerOneXmax = currentXmaxf
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
    os.remove(speakerTwoTempPath)

    if speaker2 != "":
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
    speakerTwo.close()
    os.remove(speakerOneTempPath2)
    os.remove(speakerTwoTempPath2)