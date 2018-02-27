# ImageProcessor

This project contains python scripts for PCI Geomatica algorithms and processes.

## Usage: landsat8Processor.py

This python script runs an unsupervised classification, an fmo, a sieve and ras2poly on an input file
and exports the result as a shape file. The parameters for the algorithms are pre-defined in the script and
can be modified in the source code only.
To run this script for Landsat8 satellite imagery, place the input files into **./landsat/input**. Then execute
**landsat8Processor.py** by **double-clicking or by a windows command prompt**.
It is recommended to use command prompt window. With an open command prompt navigate to the **/imageProcessor** folder and  
execute the script using:

`python imageProcessor.python`

By using a command prompt, the processing comments and times will be visible in the console, making
the process easier to follow.
The output shape files will be placed into **./landsat/output**. A classification report will be generated
within the  **./landsat** folder

## Links

PCI python Algorithm documentation:

  * [PCI Python API reference guide](http://www.pcigeomatics.com/python-api-doc/modules.html)

  * [K-means classification](http://www.pcigeomatics.com/geomatica-help/references/pciFunction_r/python/P_kclus.html )

  * [Mode Filter](http://www.pcigeomatics.com/geomatica-help/references/pciFunction_r/python/P_fmo.html )

  * [Sieve](http://www.pcigeomatics.com/geomatica-help/references/pciFunction_r/python/P_sieve.html )

  * [Raster to polygon](http://www.pcigeomatics.com/geomatica-help/references/pciFunction_r/python/P_ras2poly.html )
