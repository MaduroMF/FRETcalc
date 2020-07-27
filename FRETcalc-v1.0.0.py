
# FRET reading program

import math
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import glob
import os
import sys

print ("\n*** FRET image analysis v1.0.0 ***\n")

threshold = 50 # minimum red value to read in block

filenames= os.listdir (".") # get all files' and folders' names in the current directory

directories = []
for filename in filenames: # loop through all the files and folders
    if os.path.isdir(os.path.join(os.path.abspath("."), filename)): # check whether the current object is a folder or not
        directories.append(filename)

print ("Found "+str(len(directories))+" directories.\n")

megafile = "" # initialize a text file with all subfiles
        
for j in range (0,len(directories)):        

    print ("\nOpening directory '"+directories[j]+"...")

    files = [] # get all the image files in this current directory
    files = (glob.glob(directories[j]+"/*.jpg"))

    totalimages = len(files)

    print ("# of image pairs: " + str(int(totalimages/2)) )

    print ("threshold pixel value: " + str(threshold) + "\n")

    if (totalimages==0):
        print ("Directory has no jpg files.")


    print ("\n")

    # initialize the column headers of the output file
    outputfile = "File1\tRed\tFile2\tFRET\tAverage Ratio\tRatio of Averages\n"

    totalaverageratio = 0
    totalratioofaverages = 0
        
    for i in range (0,totalimages,2): # take images in pairs
        print ("Analyzing "+ files[i] + ", " + files[i+1] + "...")

        controlimage = Image.open(files[i])
        testimage = Image.open(files[i+1])

        TRITC = controlimage.load()
        FRET = testimage.load()

        
        # we do the following for each pair of images
        totalblocks = 0 # initialize total blocks counted in this image
        tritcpixels = 0 # initialize total tritc pixel values
        fretpixels = 0 # initialize total fret pixel values
        ratiosum = 0 # initialize the sum of ratios
        for y in range (0,2600,100):
            line = ""
            for x in range (0,3900,100):
                # now we have the starting x,y coordinate
                # let's sample across the block of 100
                # for now use 10,30,50,70,90 as the coordinates in each direction
                totalred=0 # reset total red value to 0
                for suby in range (10,100,20):
                    for subx in range (10,100,20):
                        totalred += TRITC[x+subx,y+suby][0] # sum all 25 pixel values

                char = "."
                if (totalred/25 > threshold): # if block is good, collect the pixel values that we need
                    char = "*"
                    
                    # count the pixel values in the TRITC and FRET images in parallel    
                    tritctotal=0 # initialize total red for TRITC image
                    frettotal=0 # initialize total red for FRET image
                    totalblocks += 1 # increment the number of image blocks we counted
                    
                    for county in range (0,100):
                        for countx in range (0,100):
                            tritctotal += TRITC[x+countx,y+county][0]
                            frettotal += FRET[x+countx,y+county][0]
                            
                    tritcpixels += tritctotal/10000 # add the average pixel value of the TRITC block to the running total
                    fretpixels += frettotal/10000 # add the average pixel value of the FRET block to the running total

                    ratiosum += (frettotal/tritctotal) # add the ratio to the running total, no need to divide by 10000
                    
                line += char + " " # this is so we can print each line showing image progress
                
            print (line)
        # image is done now, compute our averages to store
        
        averageratio = ratiosum / totalblocks # compute the average of the ratios
        averagetritc = tritcpixels / totalblocks # average of the tritc pixel values
        averagefret = fretpixels / totalblocks # average of the fret pixel values
        ratioofaverages = averagefret / averagetritc # ratio of the average pixel values
        
        print ("Total blocks: "+ str(totalblocks) + "\naverage ratio = " + str (averageratio))
        print ("average TRITC = " + str(averagetritc))
        print ("average FRET = " + str(averagefret))
        print ("ratio of averages: " + str (ratioofaverages) + "\n\n")

        totalaverageratio += averageratio # sum for the average ratio at the end
        totalratioofaverages += ratioofaverages # sum for the total ratio of averages
        
    # remember the outputfile top row = "File1\tRed\tFile2\tFRET\tAverage Ratio\tRatio of Averages\n"    
        outputfile += files[i][-12:-4] + "\t" + str(averagetritc) + "\t" + files[i+1][-12:-4] + "\t" + str(averagefret) + "\t"
        outputfile += str(averageratio) + "\t" + str(ratioofaverages) + "\n"

    outputfile += " \t \t \taverages>>>\t"+str(totalaverageratio/(totalimages/2))+"\t"
    outputfile += str(totalratioofaverages/(totalimages/2)) + "\n"

    print ("\n\nOutput file:\n\n"+outputfile)

    print ("Saving output file as "+directories[j]+".txt\n")

    outputFile = open(directories[j]+"/"+directories[j]+"threshold"+str(threshold)+".txt","w")
    outputFile.write(outputfile)
    outputFile.close()
    
    megafile += directories[j] + "\n\n" + outputfile + "\n\n"

print ("Saving compiled file as compiled.txt\n")

outputFile = open("compiled-threshold="+str(threshold)+".txt","w")
outputFile.write(megafile)
outputFile.close()
    
print ("\nDone!")


