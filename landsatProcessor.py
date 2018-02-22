#
# This test-script runs an unsupervised classification on the input Landsat8 pix files, then applies a mode filter
# and a sieve and eventually exports the classified raster to an output shape file.

# Packages & libraries
import os
import glob
import time
from pci.kclus import kclus
from pci.fmo import *
from pci.sieve import *
from pci.ras2poly import *
from pci.pcimod import pcimod
from pci.exceptions import *
from pci.his import his
from pci.nspio import Report, enableDefaultReport
from pci.api import datasource as ds

# Data
inputFolder = "D:\Bulk\Uni\uji_data\RS\FinalAss\landsat\input\\"
outputFolder = "D:\Bulk\Uni\uji_data\RS\FinalAss\landsat\output\\"

# classification function

def classification(path, image):

    print ""
    print "Classifying " + str(file)
    print ""

    # Set timer
    start = time.time()

    # Define output file name
    file_name, ext = os.path.splitext(str(image))
    outputFile = file_name+"_classified.shp"
    output = outputFolder + "\\" + outputFile

    inputfile = path+image

    # get image statistics to extract channel number
    print "Detecting current channels..."
    with ds.open_dataset(inputfile) as dataset:
        chansCount = dataset.chan_count
    print str(chansCount) + " channels detected"
    print ""

    # Whipe previously created channels (only use if you want a fresh clean input file and don't need previously created channels)
    chansDel = range(10,chansCount+1)
    if chansCount > 9:                      # Adjust depending on image bands
        pcimod( file=inputfile,pciop='del',pcival=chansDel)
        print str(len(chansDel)) + " previously created channels deleted"

    # Whipe previously created shape files in output folder
    files = glob.glob(outputFolder+ "\\" + '*')
    for f in files:
        f_name, ext = os.path.splitext(str(os.path.basename(f)))
        if file_name in f_name:
            os.remove(f)
            print str(f) + " deleted"
    print ""

    # Redefine chansCount
    with ds.open_dataset(inputfile) as dataset:
        chansCount = dataset.chan_count

    # Count input channels and create input channel list
    with ds.open_dataset(inputfile) as dataset:
        inputChansCount = dataset.chan_count
    inputChans = range(1,8)                         # Define input channels (eg: (1,7)=channel 1 to channel 6))
    print inputChans

    # Add 3 channels to the image for storing algorithm output
    print "Adding three 8-bit channels to image..."
    pcimod(file=inputfile, pciop='add', pcival=[3, 0, 0, 0, 0, 0])
    print "Three 8-bit channels added"
    print ""

    # Run k-means cluster algorithm
    classesNumber = [10]         # define number of classes
    iterations = [10]            # define number iterations
    moveThresh = [0.01]         # define move threshhold
    print "Running unsupervized k-means classification..."
    print "Creating "+str(classesNumber)+ " classes, applying "+str(iterations)+" iterations at a move-threshhold of "+str(moveThresh)

    kclus( file = inputfile, dbic = inputChans, dboc = [chansCount+1], numclus = classesNumber, maxiter = iterations, movethrs = moveThresh)
    flag1 = time.time()
    print "Classification complete! Time ellapsed: " + str(flag1 - start) +" seconds"
    print ""

    # Run mode filter
    print "Running Mode Filter..."
    filter = [5,5]
    fmo(file = inputfile, dbic = [chansCount+1], dboc = [chansCount+2], thinline = "OFF", flsz = [3,3])
    flag2 = time.time()
    print "Filtering complete! Time ellapsed: " + str(flag2 - start) +" seconds"
    print ""

    # Run sieve
    print "Applying sieve..."
    sieve(file = inputfile, dbic = [chansCount+2], dboc = [chansCount+3], sthresh = [32])
    flag3 = time.time()
    print "Sieve complete! Time ellapsed: " + str(flag3 - start) +" seconds"
    print ""

    # Create vector ploygons and export as shape file
    print "Creating polygons..."
    ras2poly(fili = inputfile, dbic = [chansCount+3], filo = output, ftype = "SHP")
    flag4 = time.time()
    print "Polygons created! Time ellapsed: " + str(flag4 - start) +" seconds"
    print ""

    print "Exporting as shape file..."

    end = time.time()
    print "Processing time ellapsed for "+image+": " + str(end - start) + " seconds"
    print ""

# Run classification on all files in the folder
start = time.time()

for file in os.listdir(inputFolder):
    if file.endswith(".pix"):
        classification(inputFolder, file);

end = time.time()

print "Total time ellapsed: " + str(end - start) + " seconds"
