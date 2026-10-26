#!/usr/bin/env python
# coding: utf-8

# In[30]:


# Emily Stephens
# Practicum 5
# 10/13/2026

# Continue from HW7

import os
import numpy as np
from scipy.optimize import curve_fit
from astropy.io import fits

from hw7_estephens import *
from hw6_estephens import *

# Practicum 5

# Problem 2
print("Problem 2")

# FIXED: October 19, 2026
datadir = 'hw6_data_export/'
fext = ".fits"

objfile = []
darkfile = []

files = os.listdir(datadir)

# I broke down and used a 'for' loop. 
for file in files:
    if file.startswith("rdpharocor_stars_13s_") and file.endswith(fext):
        objfile.append(file[:-len(fext)])

    elif file.startswith("rdpharocor_dark_13s_") and file.endswith(fext):
        darkfile.append(file[:-len(fext)])

nobj = len(objfile)
ndark = len(darkfile)

objdata = fits.getdata(datadir + objfile[0] + fext)

ny, nx = objdata.shape

objcube = np.zeros((nobj, ny, nx), dtype=np.float64)
darkcube = np.zeros((ndark, ny, nx), dtype=np.float64)

# Used these for loops to assist with data files.
for i in range(nobj):
    objcube[i] = fits.getdata(datadir + objfile[i] + fext)

for i in range(ndark):
    darkcube[i] = fits.getdata(datadir + darkfile[i] + fext)

# a) Define the normalized median combination function
print("a)")
def normmedcomb(data, normregion=None):

    '''
    Parameters:
        data: A 3D array containing the dark-subtracted sky flux.
        normregion: Optional tuple containing the corner coordinates
                    of the normalization region. The default is the
                    whole image.

    Returns:
        mednorm: A 2D array containing the normalized, median-combined
                 image.
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

    # Use the whole image if no normalization region is provided
    if normregion is None:
        y1 = 0
        x1 = 0
        y2 = data.shape[1]
        x2 = data.shape[2]

    # Get the corner coordinates of the specified region
    else:
        (y1, x1), (y2, x2) = normregion
    # Calculate the median flux in the normalization region
    # for each frame
    normfactor = np.median(
        datacopy[:, y1:y2, x1:x2],
        axis=(1, 2)
    )

    # Normalize each frame using its normalization factor
    datacopy = datacopy / normfactor[:, np.newaxis, np.newaxis]
    # Calculate the median of the normalized frames
    mednorm = np.median(datacopy, axis=0)
    # Return the normalized median image and normalization factors
    return mednorm, normfactor


# Problem 3
print("Problem 3")

# a) Create the median dark frame
print("a)")
darkmedian = np.median(darkcube, axis=0)

# b) Subtract the median dark from the object data
print("b)")

# Create the median dark frame
darkmedian = np.median(darkcube, axis=0)

# Subtract the median dark from the object data
objsub = objcube - darkmedian

# c) Normalize and median combine the dark-subtracted object data
print("c)")
sky_mednorm, normfactor = normmedcomb(
    objsub,
    ((225, 225), (-225, -225))
)

# Print the normalization factors
print("Normalization factors = ", normfactor)

# d) Write the normalized median-combined image to a FITS file
print("d)")
fits.writeto(
    "sky_13s_mednorm.fits",
    sky_mednorm,
    overwrite=True
)


# In[ ]:




