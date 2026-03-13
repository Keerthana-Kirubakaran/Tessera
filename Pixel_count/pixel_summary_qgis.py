import pandas as pd
import os

# -------------------------------------------------
# FILE PATHS
# -------------------------------------------------
INPUT_EXCEL = r"C:\Users\user\OneDrive - Politecnico di Milano\00LCZ\result\tessera\tessera_grids\report\tess_2018_milan_cls1.xlsx"

OUTPUT_CSV = r"C:\Users\user\OneDrive - Politecnico di Milano\00LCZ\result\tessera\tessera_grids\python_op\tess_milan_2018_pixelsum_cls1.csv"

OUTPUT_EXCEL = r"C:\Users\user\OneDrive - Politecnico di Milano\00LCZ\result\tessera\tessera_grids\python_op\tess_milan_2018_pixelsum_cls1.xlsx"

print("Script started")

# -------------------------------------------------
# CHECK INPUT FILE
# -------------------------------------------------
if not os.path.exists(INPUT_EXCEL):
    raise FileNotFoundError(f"Input Excel file not found: {INPUT_EXCEL}")

# -------------------------------------------------
# CREATE OUTPUT FOLDER
# -------------------------------------------------
output_folder = os.path.dirname(OUTPUT_CSV)
os.makedirs(output_folder, exist_ok=True)
print(f"Output folder ready: {output_folder}")

# -------------------------------------------------
# READ EXCEL
# -------------------------------------------------
print("Reading Excel file...")
df = pd.read_excel(INPUT_EXCEL)
print("Excel loaded successfully")
print("Columns:", df.columns.tolist())

# -------------------------------------------------
# EXTRACT VALUES
# -------------------------------------------------
try:
    total_pixel_count = df["Total Pixels"].iloc[0]
    total_area = df["Total Area"].iloc[0]
    valid_pixel_count = df["Valid Pixels"].iloc[0]
    valid_area = df["Valid Area"].iloc[0]
except KeyError as e:
    raise KeyError(f"Column not found in Excel: {e}")

# -------------------------------------------------
# CREATE SUMMARY TABLE
# -------------------------------------------------
summary = {
    "Metric": [
        "Total Pixel Count",
        "Total Area",
        "Valid Pixel Count",
        "Valid Area"
    ],
    "Value": [
        total_pixel_count,
        total_area,
        valid_pixel_count,
        valid_area
    ]
}

summary_df = pd.DataFrame(summary)

# -------------------------------------------------
# SAVE OUTPUT
# -------------------------------------------------
print("Saving outputs...")

# Save CSV
summary_df.to_csv(OUTPUT_CSV, index=False)
# Save Excel
summary_df.to_excel(OUTPUT_EXCEL, index=False, engine='openpyxl')

# -------------------------------------------------
# CONFIRMATION
# -------------------------------------------------
if os.path.exists(OUTPUT_CSV) and os.path.exists(OUTPUT_EXCEL):
    print("✅ Outputs generated successfully!")
    print("CSV path:", os.path.abspath(OUTPUT_CSV))
    print("Excel path:", os.path.abspath(OUTPUT_EXCEL))
else:
    print("❌ Output files were not generated. Check permissions and folder paths.")

print("Script finished")