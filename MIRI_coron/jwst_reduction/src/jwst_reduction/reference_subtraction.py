
import numpy as np
import scipy.optimize as optimize

from .mask import create_annular_mask


def opt_1ref(data_target, data_ref, center_corono, rmin=0.5, rmax=4.0, pix_size=0.11, num_ref=0):
    '''
    Create an optimal reference with the best dither from reference observations by scaling the flux.

    Parameters:
    data_target (numpy.ndarray): Target data array (image to process).
    data_ref (list of numpy.ndarray): List of reference images.
    center_corono (tuple): Coordinates of the coronagraphic center (x, y).
    num_ref (int, optional): Index of the reference image to use (default is 0).
    rmin (float, optional): Inner radius of the optimization mask in arcseconds (default is 9).
    rmax (float, optional): Outer radius of the optimization mask in arcseconds (default is 12)
    
    Returns:
    numpy.ndarray: Optimized reference image for subtraction and the scaling factor.
    '''
    
    # Dimensions
    h, w = data_target.shape
    
    # Annular mask
    mask_annulus = create_annular_mask(h, w,(center_corono[0], center_corono[1]),rmin/pix_size, rmax/pix_size)

    # Sélection des pixels valides dans l’anneau
    # et exclus les NaN dans target et ref
    target = data_target
    ref = data_ref[num_ref]
    print("target:", target.shape)
    print("ref:", ref.shape)
    print("mask:", mask_annulus.shape)

    valid = (
        mask_annulus &
        np.isfinite(target) &
        np.isfinite(ref)
    )

    # Extraction des pixels utiles
    T = target[valid]
    R = ref[valid]

    # --- Facteur de scaling analytique ---
    P = np.sum(T * R) / np.sum(R * R)

    # Nouvelle référence
    new_ref = ref * P
    
    return new_ref, P

def optimize_refs(data_target, data_ref, center_corono, rmin, rmax):
    """ 
    Create an optimized reference from the reference observations 
    
    Parameters:
    data_target (numpy.ndarray): Target data array.
    data_ref (list of numpy.ndarray): List of reference data arrays.
    center_corono (tuple): Center of the coronograph.
    rmin (float): Minimum radius for annular mask in arcsec.
    rmax (float): Maximum radius for annular mask in arcsec.

    Returns:
    numpy.ndarray: Data subtracted from optimized reference.
    """
    nb_refs = len(data_ref)
    
    h, w = np.shape(data_target)
    pixscale = 0.11 # MIRI pixel scale

    # Mask where to optimize the subtraction from rmin to rmax
    mask_annulus = create_annular_mask(h, w, center=center_corono, small_radius=rmin/pixscale, big_radius=rmax/pixscale)
    data_mask = np.ma.array(data_target, mask=~mask_annulus)
    data_ref_mask = [np.ma.array(data_ref[i], mask=~mask_annulus) for i in range(nb_refs)]

    # Function to minimize
    def function_min(P):
        return np.sum((data_mask - np.sum(P[i] * data_ref_mask[i] for i in range(nb_refs)))**2)

    
    # Initialize parameters
    b = np.ones(nb_refs) / nb_refs
    # Optimize
    P, fopt, iter, funcalls, warnflag = optimize.fmin(function_min, x0=b, disp=False, full_output=True)
    
    print("Rescaled flux factor:", P)
    print("Valeur finale de la fonction χ²:", fopt)
    print(warnflag)
    
    # Compute optimized reference
    new_ref = sum(P[i] * data_ref[i] for i in range(nb_refs))

    return data_target - new_ref, P


def reference_subtract(data_target, data_ref, err_target, err_ref, center_corono, rmin=0.1, rmax=3.0, num_ref=0):
    '''
    Subtract the target image by the optimal reference.

    Parameters:
    data_target (numpy.ndarray): Target data array (image to process).
    data_ref (list of numpy.ndarray): List of reference images.
    err_target (numpy.ndarray): Error of target image.
    err_ref (numpy.ndarray): Error of reference image.
    center_corono (tuple): Coordinates of the coronagraphic center (x, y).
    num_ref (int, optional): Index of the reference image to use (default is 0).
    
    Returns:
    numpy.ndarray: Optimized reference image for subtraction and the scaling factor.

    '''
    
    new_ref, P = opt_1ref(data_target, data_ref, center_corono, rmin=rmin, rmax=rmax, num_ref=num_ref)

    image_final = data_target- new_ref
    err_final = np.sqrt(err_target**2 + (P*err_ref[num_ref])**2)

    return image_final, err_final, P