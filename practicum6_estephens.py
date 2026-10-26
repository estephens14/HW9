#!/usr/bin/env python
# coding: utf-8

# In[7]:


# Emily Stephens
# Practicum 6
# 10/23/2026

import os
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

# Import functions and variables from previous homework/practicum files
from hw6_estephens import *
from hw7_estephens import *
from hw8_estephens import *
from practicum5_estephens import *

####### Practicum 6

# Problem 1
print("Problem 1")
# Define a function to create a circular mask
def disk(radius, center, shape):

    '''
    Parameters:
        radius = radius of the disk in pixels
        center = (y, x) coordinates of the center of the disk
        shape = (number of y pixels, number of x pixels) in the image

    Description:
        Creates a circular mask with the given radius and center.
        The mask has the same shape as the input image.

    Example:
        disk(6.2, (12.3, 14.5), (25, 30))
        Produces a 25 x 30 Boolean array with a circular region
        of True values centered at (12.3, 14.5) with a radius of 6.2.
    '''

    # Get the y and x coordinates of the center
    ycenter = center[0]
    xcenter = center[1]
    # Get the number of rows and columns in the image
    ny = shape[0]
    nx = shape[1]
    # Create arrays containing the y and x pixel coordinates
    y, x = np.indices((ny, nx))
    # Calculate the distance of each pixel from the center
    distance = np.sqrt((y - ycenter)**2 + (x - xcenter)**2)
    # Select pixels that are within the given radius
    mask = distance <= radius
    # Return the circular mask
    return mask

# Test the disk function using the given radius, center, and image size
testdisk = disk(6.2, (12.3, 14.5), (25, 30))

# Save the test disk as a FITS file
# astype(np.uint8) changes True/False values into 1/0
#     I had to look up how to do the astype portion
fits.writeto("disktest.fits", testdisk.astype(np.uint8), overwrite=True)

# Check the value of a pixel that should be inside the disk
print("Pixel [14, 14] =", testdisk[14, 14])
# Check the value of a pixel that should be outside the disk
print("Pixel [2, 1] =", testdisk[2, 1])


# Problem 2
print("Problem 2")
# 2a)
# Get all files in the data directory and sort them
files = sorted(os.listdir(datadir))
# Create empty lists to store lamp-on and lamp-off files
lamponfile  = []
lampofffile = []

# Go through each file in the data directory
for file in files:

    # Find the lamp-on files and add them to the list
    if file.startswith("rdpharocor_k_lampon_") and file.endswith(fext):
        lamponfile.append(file)

    # Find the lamp-off files and add them to the list
    elif file.startswith("rdpharocor_k_lampoff_") and file.endswith(fext):
        lampofffile.append(file)

# Read the lamp-on files and combine them into a 3D array
lamponcube = np.array([
    fits.getdata(datadir + file) for file in lamponfile
])

# Read the lamp-off files and combine them into a 3D array
lampoffcube = np.array([
    fits.getdata(datadir + file) for file in lampofffile
])

# Take the median of the lamp-on images at each pixel
lamponmedian = np.median(lamponcube, axis=0)
# Take the median of the lamp-off images at each pixel
lampoffmedian = np.median(lampoffcube, axis=0)

# Subtract the lamp-off median from the lamp-on median
# This removes the background signal from the lamp-on image
flat = lamponmedian - lampoffmedian

# Normalize using the central region
# The central region is used to calculate the median value
normregion = flat[225:-225, 225:-225]

# Find the median pixel value in the normalization region
normfactor = np.median(normregion)

# Divide the flat field by the normalization factor
# This makes the median value of the flat field equal to 1
flat = flat / normfactor

# Save the normalized flat field as a FITS file
fits.writeto("flat_test1.fits", flat, overwrite=True)

# Print the flat-field value at the specified pixel
print("Flat field pixel [217, 184] =", flat[217, 184])

# Problem 2b
# Apply the flat field correction to the sky-subtracted object data
objflat = objnosky / flat

# Print the flat-corrected values at pixel [217, 184]
# The values for all object frames are printed
print("Flat-corrected pixels [217, 184] =", objflat[:, 217, 184])

# Get the header from the last object frame
lasthead = fits.getheader(datadir + objfile[-1] + fext)

# Add a note to the FITS header describing the correction
lasthead.add_history("Flat-field corrected after sky subtraction")

# Save the last flat-field corrected object frame
fits.writeto(
    "stars_13s_9_flat.fits",
    objflat[-1],
    header=lasthead,
    overwrite=True
)

# Read the normalized flat field back in from the FITS file
image = fits.getdata("flat_test.fits")

# Find the 1st and 99th percentile values
# These are used to set the minimum and maximum values of the plot
vmin, vmax = np.nanpercentile(image, [1, 99])

# Create a figure for the flat-field image
plt.figure(figsize=(8, 6))

plt.imshow(                   # I did have to look up how
    image,                    # to do this step to make the 
    origin="lower",           # plot look nice.
    cmap="gray",
    vmin=vmin,
    vmax=vmax
)

# Add a color bar showing the pixel values
plt.colorbar(label="Pixel value")
# Add a title to the plot
plt.title("Practicum 6: Flat Field")
# Label the x-axis
plt.xlabel("X Pixel")
# Label the y-axis
plt.ylabel("Y Pixel")
# Adjust the spacing so everything fits nicely
plt.tight_layout()
# Display the plot
plt.show()


# In[ ]:




