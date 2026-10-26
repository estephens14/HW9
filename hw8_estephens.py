#!/usr/bin/env python
# coding: utf-8

# In[6]:


# Emily Stephens
# Homework 8
# 10/19/2026

# Continue from Practicum 5
import os
import numpy as np
from scipy.optimize import curve_fit
from astropy.io import fits

from practicum5_estephens import *


import os
import numpy as np
from astropy.io import fits

# Homework 8
# Emily Stephens
# FIXED: October 19, 2026


# Problem 1
print("Problem 1")

# a) Define two variables
datadir = 'hw6_data_export/'
fext = ".fits"

# b) Initialize two lists
print("b)")

objfile = []
darkfile = []

files = sorted(os.listdir(datadir))

# Find the object and dark files
for file in files:
    if file.startswith("rdpharocor_stars_13s_") and file.endswith(fext):
        objfile.append(file[:-len(fext)])

    elif file.startswith("rdpharocor_dark_13s_") and file.endswith(fext):
        darkfile.append(file[:-len(fext)])

print("Object files:", objfile)
print("Dark files:", darkfile)

# Check that the files were found
if len(objfile) == 0 or len(darkfile) == 0:
    raise ValueError("No object or dark files found. Check datadir.")

# c) Print information about the files
print("c)")

print("Data directory is:", datadir)
print("FITS extension is:", fext)
print("Last object file is:", objfile[-1])
print("Last dark file is:", darkfile[-1])

# d) Read an object file
print("d)")

objdata = fits.getdata(datadir + objfile[0] + fext)

ny, nx = objdata.shape

print("Number of rows (ny):", ny)
print("Number of columns (nx):", nx)

# e) Find the number of object and dark files
print("e)")

nobj = len(objfile)
ndark = len(darkfile)

print("Number of object files:", nobj)
print("Number of dark files:", ndark)


# Problem 2
print("Problem 2")
# a) Create the data cubes
print("a)")

objcube = np.zeros((nobj, ny, nx), dtype=np.float64)
darkcube = np.zeros((ndark, ny, nx), dtype=np.float64)

# b) Read the data into the cubes
print("b)")

for i in range(nobj):
    objcube[i] = fits.getdata(datadir + objfile[i] + fext)

for i in range(ndark):
    darkcube[i] = fits.getdata(datadir + darkfile[i] + fext)

print("Object cube shape:", objcube.shape)
print("Dark cube shape:", darkcube.shape)

# c) Create the median dark frame
print("c)")
darkmedian = np.median(darkcube, axis=0)

# d) Add a HISTORY entry to the dark header
print("d)")
darkhead = fits.getheader(datadir + darkfile[-1] + fext)
darkhead.add_history("Median-combined dark frame")

# e) Write the median dark frame to a FITS file
print("e)")
fits.writeto(
    "dark_13s_med.fits",
    darkmedian,
    header=darkhead,
    overwrite=True
)

# f) Subtract the median dark from the object data
print("f)")
objsub = objcube - darkmedian

# Write the first dark-subtracted object frame
objhead = fits.getheader(datadir + objfile[0] + fext)

fits.writeto(
    "hw8_estephens_prob2_graph1.fits",
    objsub[0],
    header=objhead,
    overwrite=True
)

print("Dark-subtracted object shape:", objsub.shape)


# a) Define the normalized median-combination function
print("a)")

def normmedcomb(data, normregion=None):

    '''
    Parameters:
        data: A 3D array containing dark-subtracted sky flux.
        normregion: Optional tuple containing the corner coordinates
                    of the normalization region. The default is
                    the whole image.

    Returns:
        mednorm: The normalized, median-combined 2D array.
        normfactor: A 1D array containing the normalization factor
                    for each frame.

    Example:
        sky_mednorm, normfactor = normmedcomb(
            objsub,
            ((225, 225), (-225, -225))
        )
    '''

    # Make a copy so the original data is not modified
    datacopy = data.copy()

    # Use the whole image if no region is provided
    if normregion is None:
        y1 = 0
        x1 = 0
        y2 = data.shape[1]
        x2 = data.shape[2]

    # Get the corner coordinates of the normalization region
    else:
        (y1, x1), (y2, x2) = normregion

    # Calculate the normalization factor for each frame
    normfactor = np.median(
        datacopy[:, y1:y2, x1:x2],
        axis=(1, 2)
    )

    # Check that the normalization factors are not zero
    if np.any(normfactor == 0):
        raise ValueError("A normalization factor is zero.")

    # Normalize each frame
    datacopy = datacopy / normfactor[:, np.newaxis, np.newaxis]

    # Median-combine the normalized frames
    mednorm = np.median(datacopy, axis=0)

    # Return the normalized median image and normalization factors
    return mednorm, normfactor


# b) Normalize and median-combine the dark-subtracted data
print("b)")
sky_mednorm, normfactor = normmedcomb(
    objsub,
    ((225, 225), (-225, -225))
)

# Print the normalization factors
print("Normalization factors:")
print(normfactor)

# Normalization factors from this run:
# Copy the printed values here after running the code.

# c) Write the normalized median sky frame to a FITS file
print("c)")
fits.writeto(
    "sky_13s_mednorm.fits",
    sky_mednorm,
    overwrite=True
)

# Problem 2
print("Problem 2")
# a) Define the sky-subtraction function
print("a)")

def skycormednorm(objdata, skymednorm, normregion=None):

    '''
    Parameters:
        objdata: A 2D dark-subtracted object frame.
        skymednorm: A 2D normalized, median-combined sky frame.
        normregion: Optional tuple containing the corner coordinates
                    of the normalization region. The default is
                    the whole image.

    Returns:
        objnosky: The sky-subtracted 2D object frame.

    Example:
        objnosky = skycormednorm(
            objsub[0],
            sky_mednorm,
            ((225, 225), (-225, -225))
        )
    '''

    # Make copies so the original arrays are not modified
    objcopy = objdata.copy()
    skycopy = skymednorm.copy()

    # Use the whole image if no region is provided
    if normregion is None:
        y1 = 0
        x1 = 0
        y2 = objdata.shape[0]
        x2 = objdata.shape[1]

    # Get the corner coordinates of the normalization region
    else:
        (y1, x1), (y2, x2) = normregion

    # Calculate the normalization factor for the object frame
    normfactor = np.median(objcopy[y1:y2, x1:x2])

    # Check that the normalization factor is not zero
    if normfactor == 0:
        raise ValueError("The object normalization factor is zero.")

    # De-normalize the sky frame
    skycopy = skycopy * normfactor

    # Subtract the sky frame from the object frame
    objnosky = objcopy - skycopy

    # Return the sky-subtracted object frame
    return objnosky


# b) Apply sky subtraction to all object frames
print("b)")
# Create an array to store the sky-subtracted frames
objnosky = np.zeros_like(objsub)

# Apply sky subtraction to each object frame
for i in range(nobj):
    objnosky[i] = skycormednorm(
        objsub[i],
        sky_mednorm,
        ((225, 225), (-225, -225))
    )

# c) Write the last sky-subtracted frame to a FITS file
print("c)")
lasthead = fits.getheader(datadir + objfile[-1] + fext)

fits.writeto(
    "stars_13s_9_nosky.fits",
    objnosky[-1],
    header=lasthead,
    overwrite=True
)

# d) Print pixel [217, 184] of the last frame
print("d)")
print("Pixel [217, 184] =", objnosky[-1, 217, 184])



# In[ ]:




