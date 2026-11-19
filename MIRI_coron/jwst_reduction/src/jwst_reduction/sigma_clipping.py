import numpy as np


def clean_data(data_planet, sigma=3, window=2): 
    """
    Cleans the input data by replacing NaN values with the local median 
    and applying sigma clipping to remove outliers.

    Parameters:
    data_planet (numpy.ndarray): 2D array containing the input data.
    sigma (float, optional): Threshold for sigma clipping. Defaults to 3.
    window (float, optional): Size of the local window for median filtering. Default is 2.

    Returns:
    numpy.ndarray: Cleaned version of the input data.
    """
    
    size_i, size_j = np.shape(data_planet)  # Get dimensions of the input data
    
    data_corr = np.copy(data_planet)  # Create a copy to avoid modifying the original data

    # Iterate over the pixels within a valid range, avoiding edges
    for i in range(window, size_i - window):
        for j in range(window, size_j - window):
            # Extract a local window of pixels around the current pixel
            data_window = data_planet[i-window:i+window+1, j-window:j+window+1]
            
            # Select only valid (non-NaN) values in the window
            valid_data = data_window[~np.isnan(data_window)]
            
            # Proceed only if there are valid pixels in the window
            if valid_data.size > 0:
                std = np.nanstd(valid_data)  # Compute standard deviation of valid data
                median = np.nanmedian(valid_data)  # Compute median of valid data
                
                # Replace NaN values in the original data with the local median
                pixel = np.nan_to_num(data_planet[i, j], nan=median)
                
                # Apply sigma clipping: if pixel deviates significantly from median, replace it
                if abs(pixel - median) > sigma * std:
                    data_corr[i, j] = median  # Replace outlier with median

    return data_corr  # Return the cleaned data array