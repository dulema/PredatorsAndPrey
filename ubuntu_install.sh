#!/bin/bash

if zenity --question --text="This script will check for and install the following packges needed for PredPreyAlgorithm\n\tpython2.6\n\tpython-numpy\n\tpython-psyco\n\tpython-tk\n\tpython-imaging-tk\n\nThis will require root privlages. Would you like to continue?"; then
    gksudo apt-get install python2.6 python-numpy python-tk python-imaging-tk python-psyco
else
    zenity --error --text="Installation Aborted\!"
fi
