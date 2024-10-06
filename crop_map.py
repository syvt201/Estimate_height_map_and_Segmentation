import geopandas as gpd
import rasterio
from rasterio.mask import mask
from shapely.geometry import box
import argparse
import cv2
import os
def crop_map(input_tiff_path, output_tiff_path, crs, minx, miny, maxx, maxy):
    print(f"Crop {minx}, {maxx}, {miny}, {maxy}")
    bbox = box(minx, miny, maxx, maxy)
    bbox_gdf = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs=crs)

    with rasterio.open(input_tiff_path) as src:
        out_image, out_transform = mask(src, bbox_gdf.geometry, crop=True)
        out_meta = src.meta.copy()

    out_meta.update({"driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform})

    with rasterio.open(output_tiff_path, "w", **out_meta) as dest:
        dest.write(out_image)

def crop_mask(input_mask_path, output_mask_path, left, right, top, bottom):
    map = cv2.imread(input_mask_path, cv2.IMREAD_GRAYSCALE)
    height, width = map.shape
    cropped = map[top:min(bottom+1, height), left:min(right+1, width)]
    cv2.imwrite(output_mask_path, cropped)

def main(input_tiff_path, output_tiff_path, left, right, top, bottom):
    dataset = rasterio.open(input_tiff_path)
    img_width = dataset.width
    img_height = dataset.height

    minx, miny = dataset.xy(top, left)
    maxx, maxy = dataset.xy(min(bottom, img_height), min(right, img_width))

    crop_map(input_tiff_path, output_tiff_path, dataset.crs, minx, miny, maxx, maxy)


if __name__ == "__main__":
    input_tiff_path = 'scene/sun_hoa_binh_cuoi_ha.tif'
    out_dir = 'out'
    out_path = 'out/sun_hoa_binh_cuoi_ha_2.tif'
    left, right, top, bottom = 3500, 5000, 8000, 11000

    if not os.path.exists(out_dir):
        # If not, create the folder
        os.makedirs(out_dir)

    dtm_path = main(input_tiff_path, out_path, left, right, top, bottom)


    input_mask_path = 'scene/sun_hoa_binh_cuoi_ha_tree.tif'
    out_path = 'out/sun_hoa_binh_cuoi_ha_tree_2.tif'
    crop_mask(input_mask_path, out_path, left, right, top, bottom)



    
