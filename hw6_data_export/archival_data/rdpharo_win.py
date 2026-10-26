import numpy as np
import astropy.io.fits as fits
import time
import os
#import pwd

def rdpharo(filename):
  '''
    This function reads a PHARO FITS image and reconstructs the data array.

    Parameters
    ----------
    filename: string
        The name of the FITS file to read.
      
    Returns
    -------
    header: Fits header object
        The FITS header of the data file.
    data: ndarray
        The reconstructed data array.

    Notes
    -----
    Reorders array from 512x512x4 -> 1024x1024.  Updates header.

    Examples
    --------
    Read and re-order file 'pharofile.fits', return its header and
    data in variables so named:

    >>> header, data = rdpharo('pharofile.fits')

    Revisions
    ---------
    2003-02-19 0.1  jh@oobleck.astro.cornell.edu Original version
    2003-02-25 0.2  jh@oobleck.astro.cornell.edu Added FILENAME to FITS header.
    2007-09-30 0.3  jh@physics.ucf.edu	     Converted to Python from IDL.
    2007-10-15 0.4  jh@physics.ucf.edu	     Fix cards with float values.
    2009-10-01 0.5  jh@physics.ucf.edu	     Update docstring, clean up code.
    2014-10-05 0.5  jh@physics.ucf.edu	     pyfits->astropy.io.fits
    2017-10-08 0.6  jh@physics.ucf.edu	     replaced deprecated header.update()
  '''

  # read the data into an hdulist rather than a header/data pair, to verify
  hdulist = fits.open(filename)

  # verify (fix broken cards)
  hdulist.verify('silentfix')
  
  # break it into header and input data
  header = hdulist[0].header
  indata = hdulist[0].data

  # indata, header = fits.getdata(filename, header=True)
  ny, nx = indata.shape[1:]
   
  # create the output array, with the same type as the input
  data = np.zeros((2*ny, 2*nx), dtype=indata.dtype)

  # the hardwired numbers are peculiar to PHARO
  data[   : ny,   : nx] = indata[1, :, :]
  data[   : ny, nx:   ] = indata[0, :, :]
  data[ ny:   ,   : nx] = indata[2, :, :]
  data[ ny:   , nx:   ] = indata[3, :, :]

  # update the header
  header['NAXIS']  = 2
  header['NAXIS1'] = 2 * nx
  header['NAXIS2'] = 2 * ny
  del header['NAXIS3']

  # update the header history
  header.add_history(  'rdpharo: '
                     + time.strftime('%a %b %d %H:%M:%S %Z %Y'))
                     
  header.add_history('Unpacked 512x512x4 array into 1024x1024 array')
  header['FILENAME'] = (filename, ' image filename')

  return (header, data)
