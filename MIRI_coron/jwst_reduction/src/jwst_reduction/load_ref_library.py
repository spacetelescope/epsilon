import glob
import os
from astropy.io import fits

from .sigma_clipping import clean_data


def load_reference_library(ref_root_dir,
                            fits_pattern="*bkgsub*cal.fits",
                            ext=1,
                            clean=True):
    """
    Load all reference stars from a reference library.

    Parameters
    ----------
    ref_root_dir : str
        Path to REF directory (e.g. .../F1140C/REF/)
    fits_pattern : str
        Pattern to select FITS files
    ext : int
        FITS extension to read
    clean : bool
        Apply clean_data() to each image

    Returns
    -------
    data_refs : list of ndarray
        List of cleaned reference images
    ref_names : list of str
        Corresponding reference star names
    """
    data_refs = []
    ref_names = []

    # Loop over all reference star directories
    ref_dirs = sorted(glob.glob(os.path.join(ref_root_dir, "H*")))

    for ref_dir in ref_dirs:
        stage2_dir = os.path.join(ref_dir, "stage2_bkg_subtract")

        if not os.path.isdir(stage2_dir):
            continue

        fits_files = sorted(glob.glob(os.path.join(stage2_dir, fits_pattern)))

        if len(fits_files) == 0:
            continue

        for f in fits_files:
            try:
                data = fits.open(f)[ext].data
                if clean:
                    data = clean_data(data)
                data_refs.append(data)
                ref_names.append(os.path.basename(ref_dir))
            except Exception as e:
                print(f"Problem with {f}: {e}")

    print(f"Loaded {len(data_refs)} reference images")
    return data_refs, ref_names