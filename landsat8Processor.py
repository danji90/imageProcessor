#
# This test-script runs an unsupervised classification on the input Landsat8 pix files, then applies a mode filter
# and a sieve and eventually exports the classified raster to an output shape file.

# Packages & libraries
import os, glob, time, sys, logging
from pci.kclus import kclus
from pci.fmo import *
from pci.sieve import *
from pci.ras2poly import *
from pci.pcimod import pcimod
from pci.exceptions import *
from pci.his import his
from pci.nspio import Report, enableDefaultReport
from pci.api import datasource as ds

# delete previous classification report
report = os.getcwd() + "\landsat\classReport.txt"
if os.path.isfile(report):
    os.remove(report)

# Data inpu/output
inputFolder = os.getcwd() + "\landsat\input\\"
outputFolder = os.getcwd() + "\landsat\output\\"

# classification function
def classification(path, image):

    print ""
    print "Classifying " + str(image)
    print ""

    # Set timer
    start = time.time()

    # Define input/output file names
    file_name, ext = os.path.splitext(str(image))
    outputFile = file_name+"_classified.shp"
    output = outputFolder + "\\" + outputFile
    inputfile = path+image

    # Whipe previously created shape files in output folder
    files = glob.glob(outputFolder+ "\\" + '*')
    for f in files:
        f_name, ext = os.path.splitext(str(os.path.basename(f)))
        if file_name in f_name:
            os.remove(f)
            print str(f) + " deleted"
    print ""

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

    # Redefine chansCount
    with ds.open_dataset(inputfile) as dataset:
        chansCount = dataset.chan_count

    # Count input channels and create input channel list
    with ds.open_dataset(inputfile) as dataset:
        inputChansCount = dataset.chan_count
    inputChans = range(2,8)                         # Define input channels (eg: (1,7)=channel 1 to channel 6))
    print "Input channels: "+str(inputChans)

    # Add 3 channels to the image for storing algorithm output
    print "Adding three 16-bit channels to image..."
    pcimod(file=inputfile, pciop='add', pcival=[0, 0, 3, 0, 0, 0])
    print "Three 16-bit channels added"
    print ""

    # Run k-means cluster algorithm
    def kclusInput():
        while True:
            try:
                classesNumber = [int(raw_input("Define maximum number of classes for clustering: "))]        # define number of classes
            except:
                print("Input not accepted! Try again, this time inserting an integer.")
            else:
                break
        while True:
            try:
                iterations = [int(raw_input("Define number of iterations (e.g. 10): "))]         # define number of iterations
            except:
                print("Input not accepted! Try again, this time inserting an integer.")
            else:
                break
        while True:
            try:
                moveThresh = [float(raw_input("Define move threshold (e.g. 0.01): "))]         # define number of move threshold
            except:
                print("Does not accept strings")
            else:
                break
        return [classesNumber, iterations, moveThresh]

    variable = kclusInput()
    classesNumber = variable[0]
    iterations = variable[1]
    moveThresh = variable[2]

    print "Running unsupervized k-means classification..."
    print "Creating "+str(classesNumber)+ " classes, applying "+str(iterations)+" iterations at a move-threshhold of "+str(moveThresh)
    try:
        Report.clear()
        enableDefaultReport(report)
        kclus( file = inputfile, dbic = inputChans, dboc = [chansCount+1], numclus = classesNumber, maxiter = iterations, movethrs = moveThresh)
    finally:
        enableDefaultReport('term')  # this will close the report file
    flag1 = time.time()
    print "Classification complete! Time elapsed: " + str(flag1 - start) +" seconds"
    print ""

    # Run mode filter
    print "Running Mode Filter..."
    filter = [5,5]
    fmo(file = inputfile, dbic = [chansCount+1], dboc = [chansCount+2], thinline = "OFF", flsz = filter)
    flag2 = time.time()
    print "Filtering complete! Time elapsed: " + str(flag2 - start) +" seconds"
    print ""

    # Run sieve
    print "Applying sieve..."
    sieve(file = inputfile, dbic = [chansCount+2], dboc = [chansCount+3], sthresh = [32])
    flag3 = time.time()
    print "Sieve complete! Time elapsed: " + str(flag3 - start) +" seconds"
    print ""

    # Create vector ploygons and export as shape file
    print "Creating polygons..."
    ras2poly(fili = inputfile, dbic = [chansCount+3], filo = output, ftype = "SHP")
    flag4 = time.time()
    print "Polygons created! Time elapsed: " + str(flag4 - start) +" seconds"
    print ""

    print "Exporting as shape file..."

    end = time.time()
    print "Processing time elapsed for "+image+": " + str(end - start) + " seconds"
    print ""

# Run classification on all files in the folder
start = time.time()

for file in os.listdir(inputFolder):
    if file.endswith(".pix"):
        classification(inputFolder, file);

end = time.time()

print "Total time elapsed: " + str(end - start) + " seconds"
