import os
import rasterio
from rasterio.mask import mask
import geopandas as gpd

# ============================
# INPUT PATHS
# ============================

RASTER_PATH = r"C:\Users\user\OneDrive - Politecnico di Milano\00LCZ\result\tessera\mosaic\2017_mosaic.tiff"
SHAPE_PATH = r"C:\Users\user\OneDrive - Politecnico di Milano\00LCZ\result\tessera\imd_2018_reclass_reproj_shp.shp"
OUTPUT_PATH = r"C:\Users\user\OneDrive - Politecnico di Milano\00LCZ\result\tessera\tessra_clip_output\clipped_2018.tif"

# ============================
# LOAD SHAPEFILE
# ============================

gdf = gpd.read_file(SHAPE_PATH)

# ============================
# OPEN RASTER
# ============================

with rasterio.open(RASTER_PATH) as src:
    
    # Reproject shapefile to raster CRS if needed
    if gdf.crs != src.crs:
        gdf = gdf.to_crs(src.crs)
    
    # Convert geometry to GeoJSON format
    shapes = gdf.geometry.values
    
    # Clip raster
    clipped_image, clipped_transform = mask(
        src,
        shapes,
        crop=True
    )
    
    # Update metadata
    clipped_meta = src.meta.copy()
    clipped_meta.update({
        "driver": "GTiff",
        "height": clipped_image.shape[1],
        "width": clipped_image.shape[2],
        "transform": clipped_transform
    })

# ============================
# SAVE OUTPUT
# ============================

with rasterio.open(OUTPUT_PATH, "w", **clipped_meta) as dest:
    dest.write(clipped_image)

print("✅ Clipping complete!")
print("Saved to:", OUTPUT_PATH)