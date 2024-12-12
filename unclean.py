import pandas as pd
import numpy as np

# Define sample data for testing
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Alice', 'Bob', 'Frank'],
    'Age': [23, 45, 28, 34, 41, np.nan, 55, 300],  # Includes NaN and an outlier (300)
    'Email': ['alice@example.com', 'bob@example.com', 'charlie@example.com', 
              'david@example.com', 'eve@example.com', 'alice@wrongformat', 'bob@example.com', 'frank@example.com'],  # Wrong email format for Alice
    'Salary': [50000, 60000, 70000, np.nan, 50000, 60000, 60000, 60000],  # Includes NaN
    'Country': ['USA', 'Canada', 'USA', 'UK', 'USA', 'USA', 'Canada', 'USA'],  # Duplicate 'Country'
}

# Create DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('sample_test_data.csv', index=False)

# Print DataFrame to see the result
print(df)
