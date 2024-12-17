import streamlit as st
import pandas as pd
import os
from datetime import datetime

def save_split_files(df: pd.DataFrame, split_column: str, output_directory: str):
    """
    Save the DataFrame as multiple Excel files based on a split column.

    Args:
        df (pd.DataFrame): The DataFrame to be split and saved.
        split_column (str): The column to split the DataFrame by.
        output_directory (str): The directory where to save the files.
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    for value in df[split_column].unique():
        df_split = df[df[split_column] == value]
        output_path = os.path.join(output_directory, f"{str(value).replace(':', '_')}-{timestamp}.xlsx")
        df_split.to_excel(output_path, index=False)

def main():
    st.title("Excel Processor")

    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "csv"])

    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.write("Preview of Data")
        st.write(df.head())

        selected_columns = st.multiselect("Select Columns to Keep", df.columns.tolist(), default=df.columns.tolist())

        if not selected_columns:
            st.warning("No columns selected. Keeping all columns.")
        
        df = df[selected_columns]

        add_teaching_weeks = st.checkbox("Add Teaching Weeks Column")
        add_staff = st.checkbox("Add Staff Column")
        add_phd = st.checkbox("Add PhD Yes/No Column")
        custom_column = st.text_input("Add Custom Column")

        if add_teaching_weeks:
            df["teaching_weeks"] = "Enter value here"
        if add_staff:
            df["Staff Name"] = "Enter Name here"
        if add_phd:
            df["PhD Yes/No"] = "Enter Yes or No here"
        if custom_column:
            df[custom_column] = "Enter value here"

        split_column = st.selectbox("Select Column to Split By", [None] + df.columns.tolist())

        if split_column:
            output_directory = st.text_input("Output Directory", value=os.path.expanduser("~"))

            if st.button("Save Files"):
                save_split_files(df, split_column, output_directory)
                st.success("Files saved successfully")

if __name__ == "__main__":
    main()