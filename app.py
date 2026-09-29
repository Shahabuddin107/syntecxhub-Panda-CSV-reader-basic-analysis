import io
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Pandas CSV/Excel Reader & Analyzer",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Project - 2: Pandas CSV Reader & Basic Analysis")
st.markdown(
    "Automate data inspection, statistical computation, slicing, and exporting with Pandas."
)

# ---------------------------------------------------------
# FILE UPLOAD OR DEMO DATA
# ---------------------------------------------------------
st.sidebar.header("📁 Data Source")
uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel file", type=["csv", "xlsx", "xls"]
)

use_demo_data = st.sidebar.checkbox(
    "Use Demo Dataset", value=uploaded_file is None
)

df = None

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.sidebar.success("File uploaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error loading file: {e}")
elif use_demo_data:
    # Default sample dataset
    sample_data = {
        "Employee_ID": [101, 102, 103, 104, 105, 106, 107, 108],
        "Name": [
            "Aman",
            "Riya",
            "Karan",
            "Pooja",
            "Vikas",
            "Sneha",
            "Rahul",
            "Mehak",
        ],
        "Department": [
            "IT",
            "HR",
            "IT",
            "Finance",
            "IT",
            "HR",
            "Finance",
            "IT",
        ],
        "Salary": [45000, 38000, 62000, 55000, 72000, 42000, 61000, 68000],
        "Experience_Years": [2, 3, 5, 4, 7, 2, 5, 6],
    }
    df = pd.DataFrame(sample_data)
    st.sidebar.info("Currently running on Demo Dataset.")

# If dataset is loaded, proceed with the 4 modules
if df is not None:
    # ---------------------------------------------------------
    # 1. READ & INSPECT (Head, Tail, Types)
    # ---------------------------------------------------------
    st.subheader("1. Read CSV/Excel into DataFrame & Inspect")
    tab_head, tab_tail, tab_types = st.tabs(
        ["Head (Top Rows)", "Tail (Bottom Rows)", "Data Types & Shape"]
    )

    with tab_head:
        n_head = st.slider("Select number of top rows to view:", 1, 20, 5)
        st.dataframe(df.head(n_head), use_container_width=True)

    with tab_tail:
        n_tail = st.slider("Select number of bottom rows to view:", 1, 20, 5)
        st.dataframe(df.tail(n_tail), use_container_width=True)

    with tab_types:
        col_meta1, col_meta2 = st.columns(2)
        with col_meta1:
            st.write(f"**Total Rows:** {df.shape[0]}")
            st.write(f"**Total Columns:** {df.shape[1]}")
        with col_meta2:
            st.write("**Column Types & Non-Null Counts:**")
            info_df = pd.DataFrame(
                {
                    "Data Type": df.dtypes.astype(str),
                    "Null Values": df.isnull().sum(),
                }
            )
            st.dataframe(info_df, use_container_width=True)

    st.divider()

    # ---------------------------------------------------------
    # 2. COMPUTE SUMMARY STATS (Mean, Median, Min, Max, Count)
    # ---------------------------------------------------------
    st.subheader(
        "2. Compute Summary Stats (Mean, Median, Min, Max, Count)"
    )

    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    if numeric_columns:
        selected_stat_col = st.selectbox(
            "Select Numeric Column for Key Metrics:", numeric_columns
        )

        # Computing individual stats
        mean_v = df[selected_stat_col].mean()
        median_v = df[selected_stat_col].median()
        min_v = df[selected_stat_col].min()
        max_v = df[selected_stat_col].max()
        count_v = df[selected_stat_col].count()

        # Display metric cards
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Count", f"{count_v}")
        m2.metric("Mean", f"{mean_v:.2f}")
        m3.metric("Median", f"{median_v}")
        m4.metric("Min", f"{min_v}")
        m5.metric("Max", f"{max_v}")

        with st.expander("View Full Summary Statistics (describe())"):
            st.dataframe(df.describe(), use_container_width=True)
    else:
        st.warning("No numeric columns available to compute summary stats.")

    st.divider()

    # ---------------------------------------------------------
    # 3. FILTER ROWS, SELECT COLUMNS & SLICE SUBSETS
    # ---------------------------------------------------------
    st.subheader("3. Filter Rows, Select Columns & Slice Subsets")

    col_filter, col_select = st.columns([1, 1])

    with col_filter:
        st.markdown("**A. Row Filtering**")
        filter_column = st.selectbox(
            "Filter rows by column:", options=df.columns
        )

        if pd.api.types.is_numeric_dtype(df[filter_column]):
            min_val = float(df[filter_column].min())
            max_val = float(df[filter_column].max())
            filter_range = st.slider(
                f"Range for {filter_column}:",
                min_value=min_val,
                max_value=max_val,
                value=(min_val, max_val),
            )
            filtered_df = df[
                (df[filter_column] >= filter_range[0])
                & (df[filter_column] <= filter_range[1])
            ]
        else:
            unique_options = df[filter_column].dropna().unique().tolist()
            selected_categories = st.multiselect(
                f"Select values for {filter_column}:",
                options=unique_options,
                default=unique_options,
            )
            filtered_df = df[df[filter_column].isin(selected_categories)]

    with col_select:
        st.markdown("**B. Select Columns (Slicing)**")
        selected_cols = st.multiselect(
            "Choose columns to keep in final output:",
            options=df.columns.tolist(),
            default=df.columns.tolist(),
        )

    # Slice subset
    if selected_cols:
        final_subset = filtered_df[selected_cols]
    else:
        final_subset = filtered_df

    st.markdown(f"**Filtered Output Preview ({len(final_subset)} rows):**")
    st.dataframe(final_subset, use_container_width=True)

    st.divider()

    # ---------------------------------------------------------
    # 4. SAVE FILTERED RESULTS TO CSV / EXCEL
    # ---------------------------------------------------------
    st.subheader("4. Save Filtered Results to CSV / Excel")

    col_d1, col_d2 = st.columns(2)

    # Export to CSV
    with col_d1:
        csv_buffer = final_subset.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download as CSV",
            data=csv_buffer,
            file_name="filtered_analysis.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # Export to Excel
    with col_d2:
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            final_subset.to_excel(
                writer, index=False, sheet_name="FilteredData"
            )
        excel_data = excel_buffer.getvalue()

        st.download_button(
            label="📥 Download as Excel (.xlsx)",
            data=excel_data,
            file_name="filtered_analysis.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

else:
    st.info("Upload a file from the sidebar to start analysis.")