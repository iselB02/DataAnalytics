import pandas as pd

# Load the CSV file
file_path = "your_file.csv"
df = pd.read_csv(file_path)

# 1. Inspect the Data
print("First 5 rows of the dataset:")
print(df.head())

# Display basic statistics and information
print("\nDataset Info:")
print(df.info())

print("\nSummary Statistics:")
print(df.describe())

# 2. Handle Missing Values
# Fill missing values with a specific value or remove rows/columns
df.fillna(value={"Column_Name": "Default_Value"}, inplace=True)  # Replace missing values in a column
df.dropna(subset=["Important_Column"], inplace=True)  # Drop rows with missing values in a specific column
df.dropna(axis=0, inplace=True)  # Drop all rows with any missing values

# 3. Remove Duplicates
df.drop_duplicates(inplace=True)

# 4. Rename Columns
df.rename(columns=lambda x: x.strip().lower().replace(" ", "_"), inplace=True)

# 5. Format Data
# Convert column data types
df['numeric_column'] = pd.to_numeric(df['numeric_column'], errors='coerce')
df['date_column'] = pd.to_datetime(df['date_column'], errors='coerce')

# Remove whitespace from string columns
df['string_column'] = df['string_column'].str.strip()

# 6. Filter or Modify Data
# Example: Keep rows where 'age' > 18
df = df[df['age'] > 18]

# Example: Add a new calculated column
df['new_column'] = df['existing_column_1'] * df['existing_column_2']

# 7. Save Cleaned Data
cleaned_file_path = "cleaned_file.csv"
df.to_csv(cleaned_file_path, index=False)

print(f"\nCleaned data saved to {cleaned_file_path}")

# Load the CSV file
file_path = "your_file.csv"
df = pd.read_csv(file_path)

# Display missing value statistics
print("Missing values before imputation:")
print(df.isnull().sum())

# 1. **Impute with Mean**
df['column_name'] = df['column_name'].fillna(df['column_name'].mean())

# 2. **Impute with Median**
df['column_name'] = df['column_name'].fillna(df['column_name'].median())

# 3. **Impute with Mode**
df['column_name'] = df['column_name'].fillna(df['column_name'].mode()[0])

# 4. **Impute with a Specific Value**
df['column_name'] = df['column_name'].fillna(0)  # Replace NaN with 0

# 5. **Impute Forward/Backward (for Time-Series)**
df['column_name'] = df['column_name'].fillna(method='ffill')  # Forward fill
df['column_name'] = df['column_name'].fillna(method='bfill')  # Backward fill

# 6. **Impute with Interpolation**
df['column_name'] = df['column_name'].interpolate(method='linear')  # Linear interpolation

# 7. **Impute with Conditional Values**
# Replace missing values based on another column
df.loc[df['column_name'].isnull(), 'column_name'] = df['other_column']

# Check missing values after imputation
print("Missing values after imputation:")
print(df.isnull().sum())

# Save the cleaned dataset
cleaned_file_path = "imputed_file.csv"
df.to_csv(cleaned_file_path, index=False)

print(f"Imputed data saved to {cleaned_file_path}")
