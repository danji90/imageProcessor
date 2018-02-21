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

    start = time.time()
    print(start)

    outputFile = "GH_classPolygons.shp"
    output = outputFolder + "\\" + outputFile
    print output

    # get image statistics to extract channel number
    with ds.open_dataset(image) as dataset:
        chans = dataset.chan_count

    print chans

    # Whipe previously created channels
    if chans > 6:
        pcimod( file=image,pciop='del',pcival=[7,8,9])
        print "Previously created channels deleted"

    files = glob.glob(outputFolder+ "\\" + '*')
    for f in files:
        os.remove(f)


    # Add 3 channels to the image for storing algorithm output
    print "Adding three 8 bit channels to image"
    print "..."
    pcimod(file=image, pciop='add', pcival=[3, 0, 0, 0, 0, 0])
    print "Three 8-bit channels added"
    print ""

    # Run k-means cluster algorithm
    print "Running unsupervized k-means classification"
    print "..."
    kclus( file = image, dbic = [1,2,3,4,5,6], dboc = [7], numclus = [8], maxiter = [10], movethrs = [0.01])
    print "Classification complete"
    print ""

    flag1 = time.time()
    print ("time ellapsed: " + str(flag1 - start))
    print ""

    # Run mode filter
    print "Running Mode Filter"
    print "..."
    fmo(file = image, dbic = [7], dboc = [8], thinline = "OFF", flsz = [5,5])
    print "Filtering complete"
    print ""

    # Run sieve
    print "Applying sieve"
    print "..."
    sieve(file = image, dbic = [8], dboc = [9], sthresh = [64])
    print "Sieve complete"
    print ""

    # Create vector ploygons and export as shape file
    print "Creating polygons"
    print "..."
    ras2poly(fili = image, dbic = [9], filo = output, ftype = "SHP")
    print "Polygons created"
    print "Exporting as shape file"

    end = time.time()
    print("Time ellapsed: " + str(end - start))

# Run classification
classification(input);
