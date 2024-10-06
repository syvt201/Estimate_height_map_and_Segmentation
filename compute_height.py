from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import argparse
import os

def read_tiff_as_array(tiff_file):
    # Open the raster file
    dataset = gdal.Open(tiff_file, gdal.GA_ReadOnly)

    if dataset is None:
        print("Failed to open file:", tiff_file)
        return None

    # Read raster data into numpy array
    array_data = np.array(dataset.ReadAsArray())
    # Close the dataset
    dataset = None

    return array_data


def subtract_tiff_files(input_file1, input_file2, output_file):
    # Open the input TIFF files
    dataset1 = gdal.Open(input_file1, gdal.GA_ReadOnly)
    dataset2 = gdal.Open(input_file2, gdal.GA_ReadOnly)
    
    # Get the band from each dataset
    band1 = dataset1.GetRasterBand(1)
    band2 = dataset2.GetRasterBand(1)
    
    # Read the pixel values as arrays
    array1 = band1.ReadAsArray()
    array2 = band2.ReadAsArray()
    
    # Subtract pixel values
    result_array = array1 - array2
    
    # Create a new TIFF file to store the result
    driver = gdal.GetDriverByName('GTiff')
    result_dataset = driver.Create(output_file, dataset1.RasterXSize, dataset1.RasterYSize, 1, band1.DataType)
    
    # Write the result array to the new TIFF file
    result_band = result_dataset.GetRasterBand(1)
    result_band.WriteArray(result_array)
    
    # Set the geotransform and projection
    result_dataset.SetGeoTransform(dataset1.GetGeoTransform())
    result_dataset.SetProjection(dataset1.GetProjection())

def show_height(dsm_path, dtm_path):
    # Path to the .tiff file
    
    # Read the .tiff file as array
    dsm_arr = read_tiff_as_array(dsm_path)
    dtm_arr = read_tiff_as_array(dtm_path)
    data = dsm_arr - dtm_arr
    output_file = "output_data.csv"
    # Save the array to a CSV file
    np.savetxt(output_file, np.unique(data), delimiter=",")
    data[data < -20] = -20.0
    bins = [i for i in np.linspace(-20, 20, num=150)] # Define your bin edges here
    cmap = plt.cm.seismic
    # Plot the data with the specified colormap
    plt.imshow(data, cmap=cmap, interpolation='nearest')
    plt.axis('off')
    # Save the plot as an RGB image
    output_file = "output_image.png"  # Output file name with extension (e.g., .png, .jpg)
    plt.savefig(output_file, bbox_inches='tight', pad_inches=0)


def main(dsm_path, dtm_path, output_path):
    # show_height(dsm_path, dtm_path)
    subtract_tiff_files(dsm_path, dtm_path, output_path)

    return output_path

if __name__ == "__main__":

    dsm_path = 'scene/chua_kham_son_dsm.tif'
    dtm_path = 'chua_kham_son_out/chua_kham_son_dsm_dtm.tif'
    output_path = 'chua_kham_son_out/chua_kham_son_height.tif'

    main(dsm_path, dtm_path, output_path)
    print("######### HEIGHT generated at: ", output_path)
