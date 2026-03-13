import rasterio
from rasterio.merge import merge
import os
import numpy as np

def create_mosaic(tile_dir, bands=None):
    """
    Memory-efficient mosaic creation.
    tile_dir : folder containing GeoTIFF tiles
    bands : list of band indices (1-based). None = all bands
    """
    tiff_files = sorted([
        os.path.join(tile_dir, f)
        for f in os.listdir(tile_dir)
        if f.lower().endswith((".tif", ".tiff"))
    ])
    if not tiff_files:
        raise FileNotFoundError("No TIFF files found")

    # Merge one band at a time to save memory
    sample_ds = rasterio.open(tiff_files[0])
    total_bands = sample_ds.count
    sample_ds.close()

    if bands is None:
        bands = list(range(1, total_bands + 1))

    mosaics = []
    for b in bands:
        # Merge band b from all tiles
        datasets = [rasterio.open(f) for f in tiff_files]
        mosaic_band, out_transform = merge(datasets, indexes=[b])
        mosaics.append(mosaic_band[0])  # single band

        # Close datasets to free memory
        for ds in datasets:
            ds.close()

    mosaic_array = np.stack(mosaics, axis=0)
    return mosaic_array, out_transform

