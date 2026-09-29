import os
import pandas as pd

# ========================================================
# SCRIPT KA EXACT FOLDER DIRECTORY NIKALNA
# ========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(BASE_DIR, "data.csv")

# Agar data.csv nahi milti to script khud usi folder me bana degi
if not os.path.exists(file_name):
    print(f"Creating 'data.csv' at: {file_name}")
    sample_csv_content = """Name,Department,Salary,Experience_Years
Aman,IT,45000,2
Riya,HR,38000,3
Karan,IT,62000,5
Pooja,Finance,55000,4
Vikas,IT,70000,6
Sneha,HR,42000,2
Rahul,Finance,61000,5"""
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(sample_csv_content.strip())
    print("data.csv ready!\n")


# ========================================================
# STEP 1: READ CSV & INSPECT HEAD / TAIL / DTYPES
# ========================================================
print("=" * 60)
print("STEP 1: READ CSV & INSPECT HEAD / TAIL / DTYPES")
print("=" * 60)

df = pd.read_csv(file_name)

print("\n[head] Pehli 3 Rows:")
print(df.head(3))

print("\n[tail] Aakhiri 3 Rows:")
print(df.tail(3))

print("\n[dtypes] Column Data Types:")
print(df.dtypes)


# ========================================================
# STEP 2: SUMMARY STATISTICS
# ========================================================
print("\n" + "=" * 60)
print("STEP 2: COMPUTE SUMMARY STATS")
print("=" * 60)

target_col = "Salary"

print(f"\nStats for Column: '{target_col}'")
print(f"- Count  : {df[target_col].count()}")
print(f"- Mean   : {df[target_col].mean():.2f}")
print(f"- Median : {df[target_col].median()}")
print(f"- Min    : {df[target_col].min()}")
print(f"- Max    : {df[target_col].max()}")

print("\n[describe()] Summary of Numerical Columns:")
print(df.describe())


# ========================================================
# STEP 3: FILTER ROWS & SELECT COLUMNS
# ========================================================
print("\n" + "=" * 60)
print("STEP 3: FILTER ROWS & SELECT COLUMNS")
print("=" * 60)

condition = (df["Salary"] > 45000) & (df["Department"] == "IT")
filtered_df = df[condition]

selected_columns = ["Name", "Department", "Salary"]
final_subset = filtered_df[selected_columns]

print("\nFiltered Data (Department == 'IT' & Salary > 45000):")
print(final_subset)


# ========================================================
# STEP 4: SAVE FILTERED RESULTS
# ========================================================
print("\n" + "=" * 60)
print("STEP 4: SAVE FILTERED RESULTS")
print("=" * 60)

output_csv = os.path.join(BASE_DIR, "filtered_employees.csv")
final_subset.to_csv(output_csv, index=False)
print(f"Saved CSV  : {output_csv}")

output_excel = os.path.join(BASE_DIR, "filtered_employees.xlsx")
final_subset.to_excel(output_excel, index=False)
print(f"Saved Excel: {output_excel}")

print("\nProject execution finished successfully!")