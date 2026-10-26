#!/usr/bin/env python
# coding: utf-8

# In[9]:


# Emily Stephens
# Homework 7

# Imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Problem 1
print("Problem 1")
print("No print statement needed")

# Problem 2
print("Problem 2")
print("No print statement needed")

# After reading the four assigned readings, summarize each reading, focusing on keypoints 
# learned, with 1-2 paragraphs. 

'''

Article 1 (A map of the day-night contrast of the extrasolar planet HD 189733b): 

Focuses on energy distribution from "dayside" to "nightside" to determine if energy is actually 
redistributed. Eclipse cycles were analyzed over a 33.1-hour period. The authors note a few important
factors to consider such as flux varying due to spots on the star. The seconday eclipse was 
also delayed and happened later than expected. They hypothesize that this is a result of
an eccentric orbit, third bodies in the system, or non-uniformity in planet emission. 
In conclusion, they discovered that energy irradiated from dayside is actually 
redistributed and can be recorded during nightside. 

Article 2 (The Broadband Infrared Emission Spectrum of the Exoplanet HD 189733b): 

This study of HD 189733b occurs over a shorter observation period of just 4.9 hours. The authors go into 
detail about the detector ramp technique used to analyze infrared data, focusing on analyzing pixels
without destructing any pixels during exposure time. This article highlights how a "re-analysis" of
the raw data obtained occurred for cinsistency purposes. This study also shows that the energy
is redistributed highly efficiently and supports the data gathered. 

Article 3 (The Deep Blue Color of HD 189733b...): 

Using albedo measurements, the study interprets data to explain the reasoning behind the planet's blue
color to its audience. However, it gathers and analyzes data similarly to that of the other three
studies in this assignment. Four Hubble Telescope (HST) observations were analyzed. The first
observation of the four was not included in this study due to artifact resulting from user 
error (the telescope was not given enough time to settle into its new position before data 
was collected). Something I found interesting about this study is a lack of background subtraction
as part of their analysis. They stated this was "negligible." The results of this dataset were
dependent on the existence/presence of reflective clouds in the planet's dayside atmosphere. It
seems that the blue hue of the atmosphere is a result of silicate drops in the atmosphere that 
scatter the blue light.

Article 4 (Retrievals on NIRCam Transmission and Emission Spectra of HD 189733b...): 

Using the James Webb Space Telescope (JWST) and NIRCam, this study analyzes data recorded during
eclipse cycles and transit cycles. There are excellent descriptions of the calibrations, ramp 
fittings, background removals, and subtractions of data that occurred. This article also includes
data analysis using PLATON 6, which is incredibly efficient in retrieving this type of data. There
was a discrepancy in two visits but solutions were explained in great detail. Incorporating 
chemical analysis, they found that this planet had consistent atmospheric components from dayside
to nightside. 

'''

# Imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

# Problem 3
print("Problem 3")

# a) Read data from hw7_synthetic_transit_lightcurve.csv and plot
# observations in a publication-ready plot. 
print("a)")

# Using numpy, read the data from the csv file
data = np.loadtxt('hw7_synthetic_transit_lightcurve.csv', delimiter=',', skiprows=1)

# Separate the columns
x = data[:, 0]
y = data[:, 1]

# Plot the data
plt.figure(figsize=(8, 5))
plt.plot(x, y, 'ko', markersize=3, label='Observations')

# Label the plot
plt.xlabel('Time')
plt.ylabel('Normalized Flux')
plt.title('Exoplanet Transit')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Display the plot
plt.show()


# b) Retrieve radius of planet from depth of transit
print("b)")

# i) Make a box window function
print("    i)")

def box_window(x, center, width, height):
    # Start with a flat baseline of 1
    model = np.ones(len(x))

    # Decrease the flux inside the transit
    model[np.abs(x - center) <= width / 2] = 1 - height

    return model


# ii) Fit the transit data using curve_fit
print("    ii)")

# Estimate the transit depth
depth_guess = np.max(y) - np.min(y)

# Estimate which observations are inside the transit
inside = y < (np.median(y) - depth_guess / 2)

# Estimate the center and width of the transit
if np.any(inside):
    center_guess = np.mean(x[inside])
    width_guess  = np.max(x[inside]) - np.min(x[inside])
else:
    center_guess = x[np.argmin(y)]
    width_guess  = (np.max(x) - np.min(x)) / 5

# Make sure the initial width is positive
width_guess = max(width_guess, (np.max(x) - np.min(x)) / 1000)

# Fit the data
popt, pcov = curve_fit(
    box_window, x, y,
    p0=[center_guess, width_guess, depth_guess],
    bounds=([np.min(x), 0, 0],
            [np.max(x), np.max(x) - np.min(x), 1]),
    maxfev=20000
)

# Save the best-fit parameters
center_fit, width_fit, depth_fit = popt

# Print the best-fit parameters
print("Center = ", center_fit)
print("Width  = ", width_fit)
print("Transit depth = ", depth_fit)

# Check whether the fit looks reasonable
print("Check the fit against the observations in part iv.")

# Do you believe the fit?
print("The fit is reasonable for this model if the plot matches the "
      "observed transit of the planet. This model even has a center "
      " close to zero, further supporting this. If this was not the "
      " case, the plot would have to be revised.")


# iii) Calculate the planet radius
print("    iii)")

# Stellar radius in solar radii
R_star = 1.14

# Calculate the planetary radius
R_planet = R_star * np.sqrt(depth_fit)

# Print the planetary radius
print("Planet radius (solar radii) = ", R_planet)

# What are the best-fit window-function properties? What is the
# exoplanet radius, if you know that the stellar radius is 1.14 R⊙?
print("The center is zero, the transit depth is 0.00978564, and "
      "the width is 0.01984 days.")

# iv) Plot the observations and best-fit model
print("    iv)")

# Create smooth x values for the model plot
x_fit = np.linspace(np.min(x), np.max(x), 2000)
y_fit = box_window(x_fit, center_fit, width_fit, depth_fit)

# Plot the observations and model
plt.figure(figsize=(8, 5))
plt.plot(x, y, 'ko', markersize=3, label='Observations')
plt.plot(x_fit, y_fit, 'r-', linewidth=2, label='Best-fit model')

# Label the plot
plt.xlabel('Time')
plt.ylabel('Normalized Flux')
plt.title('Exoplanet Transit with Best-Fit Model')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Display the plot
plt.show()


# c) Calculate the uncertainty in the planet radius
print("c)")

# Assign uncertainties
sigma_R_star = 0.01
sigma_depth  = 0.002

# Propagate the uncertainties
sigma_R_planet = np.sqrt(
    (np.sqrt(depth_fit) * sigma_R_star)**2
    + (R_star / (2 * np.sqrt(depth_fit)) * sigma_depth)**2
)

# Print the uncertainty
print("Uncertainty in planet radius (solar radii) = ",
      sigma_R_planet)

# What is the error in the planetary radius?
print("The uncertainty error is R = (0.11277 +- 0.01157) R⊙")


# In[ ]:




