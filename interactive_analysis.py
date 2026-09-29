import os
import pandas as pd

# Folder ka exact path nikalna
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "data.csv")

# Agar data.csv na ho to auto-create karein
if not os.path.exists(FILE_PATH):
    sample_csv_content = """Name,Department,Salary,Experience_Years
Aman,IT,45000,2
Riya,HR,38000,3
Karan,IT,62000,5
Pooja,Finance,55000,4
Vikas,IT,70000,6
Sneha,HR,42000,2
Rahul,Finance,61000,5"""
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(sample_csv_content.strip())

# DataFrame load karna
df = pd.read_csv(FILE_PATH)
filtered_data = None


def show_menu():
    print("\n" + "=" * 45)
    print("      📊 PANDAS DATA ANALYSIS MENU")
    print("=" * 45)
    print("1. View Head & Tail (Top/Bottom Rows)")
    print("2. View Data Types & Null Values")
    print("3. View Summary Stats (Mean, Median, Min, Max)")
    print("4. Filter Data (By Condition)")
    print("5. Export Filtered Data to CSV / Excel")
    print("6. Exit")
    print("=" * 45)


while True:
    show_menu()
    choice = input("Enter option (1-6): ").strip()

    if choice == "1":
        n = input("Kitni rows dekhni hain? (default 3): ").strip()
        n = int(n) if n.isdigit() else 3
        print("\n--- [HEAD] FIRST ROWS ---")
        print(df.head(n))
        print("\n--- [TAIL] LAST ROWS ---")
        print(df.tail(n))

    elif choice == "2":
        print("\n--- DATA TYPES ---")
        print(df.dtypes)
        print("\n--- MISSING / NULL VALUES ---")
        print(df.isnull().sum())

    elif choice == "3":
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        print(f"\nAvailable Numeric Columns: {numeric_cols}")
        col = input("Stats ke liye column name enter karein: ").strip()

        if col in numeric_cols:
            print(f"\n--- Statistics for '{col}' ---")
            print(f"Total Count : {df[col].count()}")
            print(f"Mean (Avg)  : {df[col].mean():.2f}")
            print(f"Median      : {df[col].median()}")
            print(f"Min Value   : {df[col].min()}")
            print(f"Max Value   : {df[col].max()}")
        else:
            print("❌ Invalid numeric column name!")

    elif choice == "4":
        print(f"\nAvailable Columns: {df.columns.tolist()}")
        print("Example condition: Salary > 50000  ya  Department == 'IT'")
        condition = input("Enter filter condition: ").strip()

        try:
            filtered_data = df.query(condition)
            print(f"\n✅ Result ({len(filtered_data)} rows matched):")
            print(filtered_data)
        except Exception as e:
            print(f"❌ Condition error: {e}")

    elif choice == "5":
        if filtered_data is None or filtered_data.empty:
            print(
                "❌ Pehle Option 4 use karke data filter karein, tabhi save hoga!"
            )
            continue

        file_format = (
            input("Export format chuniye (csv / excel): ").strip().lower()
        )
        file_name = input("Output file ka naam likhein: ").strip()

        if file_format == "csv":
            save_path = os.path.join(BASE_DIR, f"{file_name}.csv")
            filtered_data.to_csv(save_path, index=False)
            print(f"✅ Saved successfully: {save_path}")
        elif file_format == "excel":
            save_path = os.path.join(BASE_DIR, f"{file_name}.xlsx")
            filtered_data.to_excel(save_path, index=False)
            print(f"✅ Saved successfully: {save_path}")
        else:
            print("❌ Invalid format! Sirf 'csv' ya 'excel' likhein.")

    elif choice == "6":
        print("Program closed.")
        break

    else:
        print("❌ Invalid choice, dobara try karein (1 to 6).")