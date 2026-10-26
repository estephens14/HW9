#!/usr/bin/env python
# coding: utf-8

# In[13]:


# Homework 6
# Emily Stephens 

# Continued from Practicum 4

# The following code was copied and pasted from my Practicum 4 assignment.

# Emily Stephens
# Practicum 4
# Homework 6
# Oct 1 2026

# Imports
import os 
import numpy as np
from astropy.io import fits

# Problem 1
print("Problem 1")

# a) Define two variables

# I had to change directory a few times and 
# figure out appropriate name to call the files 

datadir = 'hw6_data_export/'
fext    = ".fits"

# b) Initialize two lists 
print("b)")

objfile  = []
darkfile = []

files = os.listdir(datadir)

# Received an error stating that index was out of range
# so I ran this to see if the dark files were actually
# in hw6_data_export, and they were not. I am trouble shooting. 
print("Files in folder:")
for file in files:
    print(file)

# For loop for filtering names 
for file in files:
    if file.startswith("rdpharocor_stars_13s_") and file.endswith(fext):
        objfile.append(file[:-len(fext)])

    elif file.startswith("rdpharocor_dark_13s_") and file.endswith(fext):
        darkfile.append(file[:-len(fext)])

print("Files: ", files)

# c) Use informative statements to print datadir and fext. Make
# sure to only print the last elements from each (one each).
print("c)")

print("Data directory is: ", datadir)
print("FITS extension is: ", fext)
print("Last object file is: ", objfile[-1])
print("Last dark file is: ", darkfile[-1])

#print()

# d) Read any object file 
print("d)")

objdata = fits.getdata(datadir + objfile[0] + fext)

ny, nx = objdata.shape

print("Number of rows (ny): ", ny)
print("Number of columns (nx): ", nx)

# e) Figure out # of object files and dark files
print("e)")

nobj  = len(objfile)
ndark = len(darkfile)

print("Number of object files: ", nobj)
print("Number of fark files: ", ndark)

# Problem 3
print("Problem 3")

# a) Create the data cubes
print("a)")

objcube  = np.zeros((nobj, ny, nx), dtype=np.float64)
darkcube = np.zeros((ndark, ny, nx), dtype=np.float64)

# Print cube shapes
print("Object cube shape: ", objcube.shape)
print("Dark cube shape: ", darkcube.shape)

# b) data cubes
print("b)")

# Loop through the object files
for i in range(nobj):
    objcube[i] = fits.getdata(datadir + objfile[i] + fext)

# Loop through the dark files
for i in range(ndark):
    darkcube[i] = fits.getdata(datadir + darkfile[i] + fext)

objhead = fits.getheader(datadir + objfile[-1] + fext)
darkhead = fits.getheader(datadir + darkfile[-1] + fext)

# Print the observation dates from each header
print("Object DATE-OBS:", objhead["DATE-OBS"])
print("Dark DATE-OBS:", darkhead["DATE-OBS"])

# c) (Optional)
# Extra credit: Why is TIME-OBS not necessary?
# I think it does not need to be printed because the time is
# already included in the DATE-OBS? Not in the printed statement 
# but I would assume they are in the files. 


# In[17]:


# Homework 6

# Problem 2
print("\nProblem 2")

# a) Median-combine the dark images
print("a)")

# Find the median of the dark images along the given axis
darkmedian = np.median(darkcube, axis=0)

print("Median dark image shape: ", darkmedian.shape)


# b) Find the requested pixel value from given 
# 217 and 184 values. 
print("b)")

pixel_value = darkmedian[217, 184]

print("Value of pixel [217, 184]: ", pixel_value)


# c) Add 'History' entry to dark header
print("c)")
print("No print statement needed for c)")

darkhead["HISTORY"] = "Median-combined dark frame."


# d) Write the median dark to a file
print("d)")

darkmedian_file = "dark_13s_med.fits"

fits.writeto(darkmedian_file, darkmedian, darkhead, overwrite=True)

print("Median dark written to: ", darkmedian_file)

# e) Using no loops, subtract the median-combined dark 
# frame from each object frame.
print("e)")

# Subtract the median dark from all object frames
objcorrected = objcube - darkmedian

# Get the value of the requested pixel before subtraction
before = objcube[0, 217, 184]

# Get the value of the requested pixel after subtraction
after = objcorrected[0, 217, 184]

# Print the results
print("Pixel [217, 184] before dark subtraction: ", before)
print("Pixel [217, 184] after dark subtraction: ", after)

# Write only the first corrected object frame to a FITS file
output_file = "hw6_estephens_prob2_graph1.fits"

fits.writeto(output_file, objcorrected[0], objhead, overwrite=True)

# Print the results
print("First corrected object frame written to: ", output_file)


# In[12]:


# I had to use this code to trouble shoot why the dark files were
# producing an error "index out of range." I discovered that some of 
# the files were not listed in the hw6_data_export folder so I re-uploaded
# and refreshed the kernel. This solved the problem!

#import os

#print("Current working directory:")
# print(os.getcwd())

# print("Full path to hw6_data_export:")
# print(os.path.abspath("hw6_data_export/"))

# print("Files currently visible to Python (Jupyter):")
# print(os.listdir("hw6_data_export/"))


# In[ ]:




