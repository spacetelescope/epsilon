import os
from astropy.io import fits
import numpy as np

def subtract_background(scifile, outdir, bkg_sci_min, bkg_sci_min_err):
    filename = os.path.basename(scifile)
    outfile = os.path.join(outdir, filename.replace('_cal.fits', '_bkgsub_cal.fits'))

    with fits.open(scifile) as hdul:
        sci = hdul['SCI'].data
        sci_err = hdul['ERR'].data
        sci_hdr = hdul[0].header
        
        # Background subtraction and Error propagation
        sci_bkg_sub = sci - bkg_sci_min
        sci_bkg_sub_err = np.sqrt(sci_err**2 + bkg_sci_min_err**2)

        # Extensions updated
        hdul['SCI'].data = sci_bkg_sub
        hdul['ERR'].data = sci_bkg_sub_err

        # Saving
        hdul.writeto(outfile, overwrite=True)
    return outfile
