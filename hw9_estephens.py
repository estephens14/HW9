#!/usr/bin/env python
# coding: utf-8

# In[5]:


# Emily Stephens
# Homework 9
# 10/25/2026

############### Code from Practicum 6 #############
# It sounds like the assignmnt specified copying the 
# code in rather than importing

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

############ Homework 9 #####################

# Import the Gaussian fitting function from the class demo
from gaussian import fitgaussian

# Problem 2
print("Problem 2")
# Stellar photometry:
photometry = np.array([  # yguess, xguess, width, cy, cx, star, sky

    # star 0
    [[698, 512, np.nan, np.nan, np.nan, np.nan, np.nan],        # frame 0
     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],  # frame 1
     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]], # frame 2

    # star 1
    [[668, 520, np.nan, np.nan, np.nan, np.nan, np.nan],        # frame 0
     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],  # frame 1
     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]], # frame 2

    # star 2
    [[568, 283, np.nan, np.nan, np.nan, np.nan, np.nan],        # frame 0
     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],  # frame 1
     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]]  # frame 2

], dtype=float)


# Find the number of stars and frames from the table shape
nstars = photometry.shape[0]
nframes = photometry.shape[1]

# Get the first three corrected object frames from Practicum 6
# These have already been dark-subtracted, sky-subtracted,
# and flat-field corrected
photdata = np.asarray(objflat[:nframes], dtype=float)
# Print
print("Corrected object data shape:", photdata.shape)

# Check that the images are 2D and have the expected dimensions
if photdata.ndim != 3:
    raise ValueError("Expected a 3D array of corrected 2D images.")

if photdata.shape[0] != nframes:
    raise ValueError("Not enough corrected object frames were found.")

# Check that the known star coordinates are inside the image
if (photdata.shape[1] <= 698 or photdata.shape[2] <= 520):
    raise ValueError(
        "The corrected images are too small for the given "
        "star coordinates. Check the image processing from HW8."
    )


# Find the approximate position of star 0 in frames 1 and 2
# Use the image from frame 0 as a reference

# Set the size of the region around star 0
searchsize = 12
# Get the known location of star 0 in frame 0
y0 = int(photometry[0, 0, 0])
x0 = int(photometry[0, 0, 1])

# Make a copy of the small region around star 0
reference = photdata[0,
                     y0-searchsize:y0+searchsize+1,
                     x0-searchsize:x0+searchsize+1].copy()

# Replace bad values and subtract the median background
reference[~np.isfinite(reference)] = np.nan
reference = reference - np.nanmedian(reference)

# Replace any remaining bad values with zero
reference = np.nan_to_num(reference)

# Use cross-correlation to estimate the shifts between images
from scipy.signal import fftconvolve

# Loop through frames 1 and 2
for frame in range(1, nframes):

    # Make a copy of the current frame
    image = photdata[frame].copy()

    # Replace bad values with the image median
    image[~np.isfinite(image)] = np.nan
    image = image - np.nanmedian(image)
    image = np.nan_to_num(image)

    # Compare the reference star with the current image
    correlation = fftconvolve(
        image,
        reference[::-1, ::-1],
        mode="valid"
    )

    # Find the location of the best match
    ymatch, xmatch = np.unravel_index(
        np.argmax(correlation),
        correlation.shape
    )

    # Convert the match to the center of the star
    ystar = ymatch + searchsize
    xstar = xmatch + searchsize

    # Store the approximate position of star 0
    photometry[0, frame, 0] = ystar
    photometry[0, frame, 1] = xstar

    print("Star 0 in frame", frame, "=", ystar, xstar)

# Calculate the y and x offsets of star 0
# between frame 0 and the other frames
offsets = np.zeros((nframes, 2))

for frame in range(1, nframes):

    offsets[frame, 0] = (
        photometry[0, frame, 0] - photometry[0, 0, 0]
    )

    offsets[frame, 1] = (
        photometry[0, frame, 1] - photometry[0, 0, 1]
    )


# Print the calculated offsets
print("Offsets:")
print(offsets)

# Use the offsets to calculate the positions of stars 1 and 2
for star in range(1, nstars):

    for frame in range(1, nframes):

        # Calculate the approximate y position
        photometry[star, frame, 0] = (
            photometry[star, 0, 0] + offsets[frame, 0]
        )

        # Calculate the approximate x position
        photometry[star, frame, 1] = (
            photometry[star, 0, 1] + offsets[frame, 1]
        )

# Print the updated photometry table
print("Photometry table:")
print(photometry)


# View the three frames and check the approximate star positions
for frame in range(nframes):

    plt.figure(figsize=(8, 6))

    # Set the image display limits
    vmin, vmax = np.nanpercentile(photdata[frame], [1, 99.5])

    plt.imshow(
        photdata[frame],
        origin="lower",
        cmap="gray",
        vmin=vmin,
        vmax=vmax
    )

    # Mark the approximate positions of the three stars
    for star in range(nstars):

        yguess = photometry[star, frame, 0]
        xguess = photometry[star, frame, 1]

        plt.plot(xguess, yguess, "ro", fillstyle="none")
        plt.text(xguess + 8, yguess + 8, str(star), color="red")

    plt.title("Frame " + str(frame) + ": Star Positions")
    plt.xlabel("X Pixel")
    plt.ylabel("Y Pixel")
    plt.tight_layout()
    plt.show()


# Problem 3
print("Problem 3")


# a) Fit a 2D Gaussian to each star

# Set the size of the subimage used for the Gaussian fit
subsize = 12


# Loop through each star
for star in range(nstars):

    # Loop through each observation frame
    for frame in range(nframes):

        # Get the approximate y and x position of the star
        yguess = int(round(photometry[star, frame, 0]))
        xguess = int(round(photometry[star, frame, 1]))

        # Find the boundaries of the subimage
        y1 = yguess - subsize
        y2 = yguess + subsize + 1

        x1 = xguess - subsize
        x2 = xguess + subsize + 1

        # Check that the subimage is inside the full image
        if (y1 < 0 or x1 < 0 or
            y2 > photdata.shape[1] or
            x2 > photdata.shape[2]):

            raise ValueError(
                "Subimage is outside the image for star "
                + str(star) + " frame " + str(frame)
            )

        # Make a copy of the subimage around the star
        # This prevents changes to the original image
        subimage = photdata[frame, y1:y2, x1:x2].copy()

        # Replace bad pixels with the median of the subimage
        subimage[~np.isfinite(subimage)] = np.nan

        median = np.nanmedian(subimage)

        if not np.isfinite(median):
            raise ValueError("Subimage contains no valid pixels.")

        subimage = np.where(np.isfinite(subimage), subimage, median)

        # Subtract the median to approximately remove the background
        subimage = subimage - median

        # Create coordinate arrays for the subimage
        y, x = np.indices(subimage.shape)

        # Set the initial y and x positions relative to the subimage
        cyguess = yguess - y1
        cxguess = xguess - x1

        # Make an initial guess for the Gaussian widths
        widthguess = (3., 3.)

        # Make an initial guess for the height
        heightguess = np.max(subimage)

        # Put the initial guesses together
        guess = (widthguess, (cyguess, cxguess), heightguess)

        # Fit the 2D Gaussian to the subimage
        width, center, height, err = fitgaussian(
            subimage,
            np.array([y, x]),
            guess=guess
        )

        # Convert the fitted positions back to the full image
        cy = center[0] + y1
        cx = center[1] + x1

        # Find the average of the two fitted widths
        average_star_width = np.mean(np.abs(width))

        # Store the average width in the table
        photometry[star, frame, 2] = average_star_width

        # Store the fitted y position in the table
        photometry[star, frame, 3] = cy

        # Store the fitted x position in the table
        photometry[star, frame, 4] = cx


# Print the completed table
print("Photometry table after Gaussian fitting:")
print(photometry)

# Check whether the fitted positions agree with the guesses
for star in range(nstars):

    for frame in range(nframes):
        # Calculate the difference between fitted and guessed positions
        dy = photometry[star, frame, 3] - photometry[star, frame, 0]
        dx = photometry[star, frame, 4] - photometry[star, frame, 1]

        print("Star", star, "Frame", frame,
              "Y difference =", dy,
              "X difference =", dx)


# b) Find the average width of all the stars
average_width = np.nanmean(photometry[:, :, 2])
print("Average width =", average_width)


# Set the photometry aperture radius
aprad = 3 * average_width

# Set the inner radius of the sky annulus
skyin = 5 * average_width

# Set the outer radius of the sky annulus
skyout = 7 * average_width

# Set the size of the subimage used for photometry
subsize = int(np.ceil(10 * average_width))


# The aperture radius is 3 times the star width so that
# most of the star's light is included in the aperture.

# The inner sky radius is 5 times the star width so that
# the sky annulus is separated from the star.

# The outer sky radius is 7 times the star width so that
# enough pixels are included to estimate the sky level.

# The subimage half-size is 10 times the star width so that
# there is enough space around the star for photometry.


# Print the final photometry parameters
print("Photometry aperture radius =", aprad)
print("Inner sky radius =", skyin)
print("Outer sky radius =", skyout)
print("Subimage half-size =", subsize)


# In[ ]:




