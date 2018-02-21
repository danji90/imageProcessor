#
# This test-script runs an unsupervised classification on the input file(s), then applies a mode filter
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
input = "D:\Bulk\Uni\uji_data\RS\FinalAss\golden_horseshoePython.pix"
outputFolder = "D:\Bulk\Uni\uji_data\RS\FinalAss\output"

# classification function

def classification(image):

    # Set timer
    start = time.time()

    # Define output file name
    outputFile = "GH_classPolygons.shp"
    output = outputFolder + "\\" + outputFile

    # get image statistics to extract channel number
    with ds.open_dataset(image) as dataset:
        chansCount = dataset.chan_count
    print str(chansCount) + " channels detected"

    # Whipe previously created channels (only use if you want a fresh clean input file and don't need previously created channels)
    chansDel = range(7,chansCount+1)
    if chansCount > 6:                      # Adjust depending on image bands
        pcimod( file=image,pciop='del',pcival=chansDel)
        print str(len(chansDel)) + " previously created channels deleted"

    # Whipe previously created shape files in output folder
    files = glob.glob(outputFolder+ "\\" + '*')
    for f in files:
        os.remove(f)
    print "Previous output files deleted"

    # Count input channels and create input channel list
    with ds.open_dataset(image) as dataset:
        inputChansCount = dataset.chan_count
    inputChans = range(1,inputChansCount+1)

    # Add 3 channels to the image for storing algorithm output
    print "Adding three 8-bit channels to image..."
    pcimod(file=image, pciop='add', pcival=[3, 0, 0, 0, 0, 0])
    print "Three 8-bit channels added"
    print ""

    # Run k-means cluster algorithm
    print "Running unsupervized k-means classification..."
    kclus( file = image, dbic = [1,2,3,4,5,6], dboc = [7], numclus = [8], maxiter = [10], movethrs = [0.01])
    flag1 = time.time()
    print "Classification complete! time ellapsed: " + str(flag1 - start) +" seconds"
    print ""

    # Run mode filter
    print "Running Mode Filter..."
    fmo(file = image, dbic = [7], dboc = [8], thinline = "OFF", flsz = [3,3])
    flag2 = time.time()
    print "Filtering complete! Time ellapsed: " + str(flag2 - start) +" seconds"
    print ""

    # Run sieve
    print "Applying sieve..."
    sieve(file = image, dbic = [8], dboc = [9], sthresh = [16])
    flag3 = time.time()
    print "Sieve complete! Time ellapsed: " + str(flag3 - start) +" seconds"
    print ""

    # Create vector ploygons and export as shape file
    print "Creating polygons..."
    ras2poly(fili = image, dbic = [9], filo = output, ftype = "SHP")
    flag4 = time.time()
    print "Polygons created! Time ellapsed: " + str(flag4 - start) +" seconds"
    print ""

    print "Exporting as shape file..."

    end = time.time()
    print "Total time ellapsed: " + str(end - start) + " seconds"

# Run classification
classification(input);
