import pandas as pd
import os

print("=" * 60)
print("📊 CHAPTER 1: DATA PREPROCESSING")
print("=" * 60)

# Load Excel file
file_path = "metro_database.xlsx"

# Read all sheets
excel_file = pd.ExcelFile(file_path)
print(f"\n✅ Found sheets: {excel_file.sheet_names}")

for sheet_name in excel_file.sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Remove empty rows
    df = df.dropna(how="all")
    
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # Clean text data
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()
    
    # Show info
    print(f"\n📋 {sheet_name}:")
    print(f"   Rows: {len(df)}")
    print(f"   Columns: {list(df.columns)}")
    
    # Save as CSV
    os.makedirs("csv_files", exist_ok=True)
    csv_path = f"csv_files/{sheet_name}.csv"
    df.to_csv(csv_path, index=False)
    print(f"   ✅ Saved to {csv_path}")

print("\n" + "=" * 60)
print("✅ CHAPTER 1 COMPLETE: Data Preprocessing Done!")
print("=" * 60)