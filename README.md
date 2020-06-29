# FRETcalc
This is a simple Python 3.0+ script to process image pairs within subdirectories to generate summary data for FRET analysis.
The script is run from within the directory that contains the subdirectories.

Image pairs are TRITC and FRET RGB images of size 3984x2656 with sequential names within each folder.
The script iterates over 100x100 blocks (ignoring the leftover 84 horizontal pixels and 56 vertical pixels) and identifies those whose average red pixel values are over a threshold value of 50. If so the average red pixel value is saved for this block and the corresponding block in the second image. A low-text representation of the used/unused blocks is outputted in the console. A tab-delimited textfile is generated that lists the filenames, average FRET ratio, ratio of the average pixel values, and the averages of these across all the images in that folder. The textfile is saved within each folder of images.

The imaging platform used was a Canon EOS 77D camera with LMscope adapter on an Olympus BX71 upright microscope. The program will need to be edited to suit individual applications.
