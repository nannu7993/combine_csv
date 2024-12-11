import streamlit as st
import pandas as pd
import io

def combine_csv_files(uploaded_files):
    if not uploaded_files:
        return None
    
    # Read the first file with headers
    first_file = uploaded_files[0]
    base_df = pd.read_csv(first_file)
    
    # If there's only one file, return it
    if len(uploaded_files) == 1:
        return base_df
    
    # Process subsequent files
    all_dfs = [base_df]
    for file in uploaded_files[1:]:
        # Read each subsequent file without headers, using the column names from first file
        df = pd.read_csv(file, header=None, skiprows=1, names=base_df.columns)
        all_dfs.append(df)
    
    # Combine all dataframes
    final_df = pd.concat(all_dfs, ignore_index=True)
    return final_df

def main():
    st.title("CSV Files Combiner")
    
    # File uploader
    st.write("Upload your CSV files:")
    uploaded_files = st.file_uploader("Choose CSV files", type="csv", accept_multiple_files=True)
    
    if uploaded_files:
        st.write(f"Number of files uploaded: {len(uploaded_files)}")
        
        # Add a button to combine files
        if st.button("Combine Files"):
            with st.spinner("Combining files..."):
                try:
                    combined_df = combine_csv_files(uploaded_files)
                    
                    if combined_df is not None:
                        st.success("Files combined successfully!")
                        
                        # Display sample of combined data
                        st.write("Preview of combined data:")
                        st.dataframe(combined_df.head())
                        
                        # Show total number of rows
                        st.write(f"Total number of rows: {len(combined_df)}")
                        
                        # Add download button for combined CSV
                        csv = combined_df.to_csv(index=False)
                        st.download_button(
                            label="Download Combined CSV",
                            data=csv,
                            file_name="combined_data.csv",
                            mime="text/csv"
                        )
                    else:
                        st.error("Please upload at least one CSV file.")
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.write("Please ensure all CSV files have the same structure as the first file.")

if __name__ == "__main__":
    main()
