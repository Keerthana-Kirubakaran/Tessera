import os
import rasterio
from rasterio.merge import merge
import numpy as np
import matplotlib.pyplot as plt


def create_tessera_mosaic(tile_dir, output_tif):

    # -------------------------------------------------
    # 1. Find TIFF tiles
    # -------------------------------------------------
    tiff_files = sorted([
        os.path.join(tile_dir, f)
        for f in os.listdir(tile_dir)
        if f.lower().endswith((".tif", ".tiff"))
    ])

    print(f"Found {len(tiff_files)} TIFF tiles")

    if len(tiff_files) == 0:
        raise RuntimeError("No TIFF files found in the folder!")

    # -------------------------------------------------
    # 2. Open and merge tiles
    # -------------------------------------------------
    src_files = [rasterio.open(fp) for fp in tiff_files]

    mosaic, transform = merge(src_files)

    print("Mosaic shape (bands, height, width):", mosaic.shape)

    # Close datasets
    for src in src_files:
        src.close()

    # -------------------------------------------------
    # 3. Visualization (first 3 bands)
    # -------------------------------------------------
    if mosaic.shape[0] >= 3:
        img = np.transpose(mosaic[:3], (1, 2, 0))
    else:
        img = mosaic[0]

    img = img.astype("float32")
    img = (img - np.nanmin(img)) / (np.nanmax(img) - np.nanmin(img))

    plt.figure(figsize=(10, 10))
    plt.imshow(img)
    plt.title("TESSERA Mosaic")
    plt.axis("off")
    plt.show()

    # -------------------------------------------------
    # 4. Save mosaic
    # -------------------------------------------------
    with rasterio.open(tiff_files[0]) as src:
        meta = src.meta.copy()

    meta.update({
        "driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "count": mosaic.shape[0],
        "transform": transform
    })

    with rasterio.open(output_tif, "w", **meta) as dst:
        dst.write(mosaic)

    print("Mosaic saved to:", output_tif)


# -------------------------------------------------
# MAIN PROGRAM
# -------------------------------------------------
if __name__ == "__main__":

    TILE_DIR = r"C:\Users\user\OneDrive - Politecnico di Milano\00TESSERA_Embeddings\2018"

    OUTPUT_TIF = r"C:\Users\user\OneDrive - Politecnico di Milano\00TESSERA_Embeddings\2018_mosaic.tif"

    create_tessera_mosaic(TILE_DIR, OUTPUT_TIF)