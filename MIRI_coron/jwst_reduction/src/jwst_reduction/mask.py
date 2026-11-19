import numpy as np 

def create_annular_mask(h, w, center, small_radius, big_radius):
    
    if center is None: # use the middle of the image
        center = (int(w/2), int(h/2))
        
    Y, X = np.ogrid[:h,:w]
    distance_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = (small_radius <= distance_from_center) & (distance_from_center <= big_radius)
    return mask

def create_annular_mask_bkg_excluded(h, w, center, small_radius, big_radius):
    
    if center is None: # use the middle of the image
        center = (int(w/2), int(h/2))
        
    Y, X = np.ogrid[:h,:w]
    distance_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask_annular = (small_radius <= distance_from_center) & (distance_from_center <= big_radius)
    cx, cy = 139, 130
    radius = 9  # rayon du cercle en pixels

    y, x = np.ogrid[:h, :w]
    circle_mask = (x - cx)**2 + (y - cy)**2 <= radius**2

    # Exclure le cercle de l'anneau
    mask = mask_annular & ~circle_mask
    return mask