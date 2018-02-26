# ImageProcessor

This project contains python scripts for PCI Geomatica algorithms and processes.

## Usage

To run this script for Landsat8 satellite imagery, place the input files into **./landsat/input**. Then
execute the script. The output shape files will be placed into **./landsat/output**.
It is recommended to open a command prompt window, navigate to the **/imageProcessor** folder and to 
execute the script using: 

`python imageProcessor.python`

By using a command prompt, the processing comments and times will be visible in the console, making 
the process easier to follow.

## Links

PCI python Algorithm documentation:

..*[PCI Python API reference guide](http://www.pcigeomatics.com/python-api-doc/modules.html)

..*[K-means classification](http://www.pcigeomatics.com/geomatica-help/references/pciFunction_r/python/P_kclus.html )

..*[Mode Filter](http://www.pcigeomatics.com/geomatica-help/references/pciFunction_r/python/P_fmo.html )

..*[Sieve](http://www.pcigeomatics.com/geomatica-help/references/pciFunction_r/python/P_sieve.html )

..*[Raster to polygon](http://www.pcigeomatics.com/geomatica-help/references/pciFunction_r/python/P_ras2poly.html )