import os
import rasterio

def load_tiles(tile_dir):
    """Load all GeoTIFF tiles in a directory"""
    tiff_files = sorted([
        os.path.join(tile_dir, f)
        for f in os.listdir(tile_dir)
        if f.lower().endswith((".tif", ".tiff"))
    ])

    if not tiff_files:
        raise FileNotFoundError("No TIFF files found")

    datasets = [rasterio.open(fp) for fp in tiff_files]
    return datasets