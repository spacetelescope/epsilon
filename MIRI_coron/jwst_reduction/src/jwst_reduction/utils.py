import scipy.ndimage as ndimage
import numpy as np


def crop_center(image, center, size=200):
    """
    Extrait un crop carré autour d'un centre sub-pixel,
    sans interpolation ni modification des pixels.

    Parameters
    ----------
    image (np.ndarray): Image 2D (ny, nx).
    center (tuple): x,y.
    size (int): crop size in pixels.

    Returns
    -------
    crop (np.ndarray): final image with the new size (size, size).

    """

    cx, cy = center
    half = size // 2

    x0 = int(np.floor(cx)) - half + 1
    y0 = int(np.floor(cy)) - half + 1

    x1 = x0 + size
    y1 = y0 + size

    return image[y0:y1, x0:x1]

def rotate_images(img, center_pix, window_size, ang, reshape=False):
    """
    Rotates an image around a specified center pixel with a given angle.
    Same method as implemented in spaceKLIP

    Parameters:
        img (ndarray): The input image array.
        center_pix (tuple): The (y, x) coordinates of the center of rotation.
        window_size (float): The size of the window (in the same units as image scale).
        ang (float): The rotation angle in degrees.
        reshape (bool, optional): If True, expands the output to fit the entire rotated image.

    Returns:
        ndarray: The rotated image.
    """
    
    # Convert window size to pixels (assuming a pixel scale of 0.11 per unit)
    window_pix = int(np.rint(window_size / 0.11 / 2))
    
    # Compute offset for centering
    offset = (window_pix - window_size / 0.11 / 2) * 0.11
    
    # Generate coordinate grids
    x = np.linspace(0, img.shape[0], img.shape[0])
    y = np.linspace(0, img.shape[1], img.shape[1])
    xmesh, ymesh = np.meshgrid(x, y)
    
    # Determine the old image center (y, x)
    old_center = [img.shape[1] / 2, img.shape[0] / 2]
    
    # Adjust mesh coordinates relative to the new center
    xmesh += center_pix[1]
    ymesh += center_pix[0]
    xmesh -= old_center[1]
    ymesh -= old_center[0]
    
    # Map new coordinates onto the original image
    new_data = ndimage.map_coordinates(img, [ymesh, xmesh])
    
    # Rotate the image by the specified angle
    rot_img = ndimage.rotate(new_data, ang, reshape=reshape)
    
    return rot_img