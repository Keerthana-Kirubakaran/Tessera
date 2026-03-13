import rasterio
import numpy as np
import pandas as pd


def calculate_raster_statistics(input_raster, output_raster, csv_output, excel_output, nodata_value=0):

    # -------------------------------------------------
    # INITIALIZE COUNTERS
    # -------------------------------------------------
    total_pixel_count = 0
    valid_pixel_count = 0
    nodata_pixel_count = 0

    # -------------------------------------------------
    # PROCESS RASTER
    # -------------------------------------------------
    with rasterio.open(input_raster) as src:

        meta = src.meta.copy()
        meta.update({
            "dtype": "float32",
            "nodata": np.nan
        })

        # Pixel size
        pixel_width = src.transform[0]
        pixel_height = abs(src.transform[4])
        pixel_area = pixel_width * pixel_height

        # Create output raster
        with rasterio.open(output_raster, "w", **meta) as dst:

            for _, window in src.block_windows(1):

                block = src.read(window=window).astype("float32")

                band1 = block[0]

                # Count total pixels
                total_pixel_count += band1.size

                # Count nodata pixels (0)
                nodata_pixels = np.count_nonzero(band1 == nodata_value)
                nodata_pixel_count += nodata_pixels

                # Convert 0 → NaN
                band1[band1 == nodata_value] = np.nan

                # Count valid pixels
                valid_pixels = np.count_nonzero(~np.isnan(band1))
                valid_pixel_count += valid_pixels

                block[0] = band1

                # Write cleaned raster
                dst.write(block, window=window)

    # -------------------------------------------------
    # AREA CALCULATIONS
    # -------------------------------------------------
    total_area = total_pixel_count * pixel_area
    valid_area = valid_pixel_count * pixel_area
    nodata_area = nodata_pixel_count * pixel_area

    total_area_km2 = total_area / 1e6
    valid_area_km2 = valid_area / 1e6
    nodata_area_km2 = nodata_area / 1e6

    # -------------------------------------------------
    # SAVE RESULTS
    # -------------------------------------------------
    results = {
        "Metric": [
            "Total Pixels",
            "Valid Pixels",
            "NoData Pixels",
            "Pixel Area (m²)",
            "Total Area (m²)",
            "Valid Area (m²)",
            "NoData Area (m²)",
            "Total Area (km²)",
            "Valid Area (km²)",
            "NoData Area (km²)"
        ],
        "Value": [
            total_pixel_count,
            valid_pixel_count,
            nodata_pixel_count,
            pixel_area,
            total_area,
            valid_area,
            nodata_area,
            total_area_km2,
            valid_area_km2,
            nodata_area_km2
        ]
    }

    df = pd.DataFrame(results)

    df.to_csv(csv_output, index=False)
    df.to_excel(excel_output, index=False)

    # -------------------------------------------------
    # PRINT RESULTS
    # -------------------------------------------------
    print("\nRaster cleaned and saved:")
    print(output_raster)

    print("\nRaster Statistics")
    print("Total pixels:", total_pixel_count)
    print("Valid pixels:", valid_pixel_count)
    print("NoData pixels:", nodata_pixel_count)

    print("\nArea (m²)")
    print("Pixel area:", pixel_area)
    print("Total area:", total_area)
    print("Valid area:", valid_area)
    print("NoData area:", nodata_area)

    print("\nArea (km²)")
    print("Total area:", total_area_km2)
    print("Valid area:", valid_area_km2)
    print("NoData area:", nodata_area_km2)

    print("\nResults saved to:")
    print("CSV:", csv_output)
    print("Excel:", excel_output)


# -------------------------------------------------
# MAIN
# -------------------------------------------------
if __name__ == "__main__":

    INPUT_RASTER = r"C:\Users\user\OneDrive - Politecnico di Milano\00LCZ\result\tessera\tessra_clip_output\tess_2018_cls5.tif"

    OUTPUT_RASTER = r"C:\Users\user\OneDrive - Politecnico di Milano\00LCZ\result\tessera\tessra_clip_output\python\tess_2018_cls5_clean.tif"

    CSV_OUTPUT = r"C:\Users\user\OneDrive - Politecnico di Milano\00LCZ\result\tessera\tessra_clip_output\python\tess_2018_cls5_stats.csv"

    EXCEL_OUTPUT = r"C:\Users\user\OneDrive - Politecnico di Milano\00LCZ\result\tessera\tessra_clip_output\python\tess_2018_cls5_stats.xlsx"

    calculate_raster_statistics(INPUT_RASTER, OUTPUT_RASTER, CSV_OUTPUT, EXCEL_OUTPUT)