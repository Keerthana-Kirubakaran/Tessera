import pandas as pd
import os

print("Hello, script is running")

try:
    # ------------------------------
    # FILE PATHS (update if moved)
    # ------------------------------
    INPUT_EXCEL = r"C:\Users\user\projects\Tessera\Pixel_count\data\tess_2018_milan_cls1.xlsx"
    OUTPUT_CSV = r"C:\Users\user\projects\Tessera\Pixel_count\output\tess_milan_2018_pixelsum_cls1.csv"
    OUTPUT_EXCEL = r"C:\Users\user\projects\Tessera\Pixel_count\output\tess_milan_2018_pixelsum_cls1.xlsx"

    print("Script started")

    # ------------------------------
    # CHECK INPUT FILE
    # ------------------------------
    if not os.path.exists(INPUT_EXCEL):
        raise FileNotFoundError(f"Input Excel file not found or not local: {INPUT_EXCEL}")

    # ------------------------------
    # CREATE OUTPUT FOLDER
    # ------------------------------
    output_folder = os.path.dirname(OUTPUT_CSV)
    os.makedirs(output_folder, exist_ok=True)
    print(f"Output folder ready: {output_folder}")

    # ------------------------------
    # READ EXCEL
    # ------------------------------
    print("Reading Excel file...")
    df = pd.read_excel(INPUT_EXCEL)
    print("Excel loaded successfully")
    print("Columns:", df.columns.tolist())

    # ------------------------------
    # EXTRACT VALUES
    # ------------------------------
    total_pixel_count = df["Total Pixels"].iloc[0]
    total_area = df["Total Area"].iloc[0]
    valid_pixel_count = df["Valid Pixels"].iloc[0]
    valid_area = df["Valid Area"].iloc[0]

    # ------------------------------
    # CREATE SUMMARY TABLE
    # ------------------------------
    summary_df = pd.DataFrame({
        "Metric": ["Total Pixel Count","Total Area","Valid Pixel Count","Valid Area"],
        "Value": [total_pixel_count,total_area,valid_pixel_count,valid_area]
    })

    # ------------------------------
    # SAVE OUTPUTS
    # ------------------------------
    summary_df.to_csv(OUTPUT_CSV, index=False)
    summary_df.to_excel(OUTPUT_EXCEL, index=False, engine='openpyxl')

    # ------------------------------
    # CONFIRMATION
    # ------------------------------
    if os.path.exists(OUTPUT_CSV) and os.path.exists(OUTPUT_EXCEL):
        print("✅ Outputs generated successfully!")
        print("CSV path:", os.path.abspath(OUTPUT_CSV))
        print("Excel path:", os.path.abspath(OUTPUT_EXCEL))
    else:
        print("❌ Output files were not generated. Check folder permissions.")

except Exception as e:
    print("❌ ERROR:", e)