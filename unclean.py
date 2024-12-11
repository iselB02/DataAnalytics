import pandas as pd
import random
from faker import Faker
import numpy as np

# Initialize Faker instance
fake = Faker()

# List of possible locations (cities or neighborhoods)
locations = ['New York', 'San Francisco', 'Los Angeles', 'Chicago', 'Houston', 'Dallas', 'Miami', 'Boston', 'Seattle', 'Austin']

# List of apartment conditions
conditions = ['New', 'Renovated', 'Old', 'Needs Renovation']

withbath = ['No','Yes']

# List of possible floor levels
floor_levels = ['Ground', 'First', 'Second', 'Third', 'Penthouse']

# Function to generate uncleaned apartment sales data with missing values
def generate_uncleaned_apartment_sales_data(n):
    data = []
    
    for _ in range(n):
        # Generate random apartment ID
        apartment_id = fake.uuid4()
        
        # Random location (15% chance of missing location)
        location = random.choice(locations + [None])
        
        # Random price (10% chance of missing price)
        price = random.choice([random.randint(100000, 1000000), None])
        
        # Random size in square feet (10% chance of missing size)
        size = random.choice([random.randint(400, 4000), None])
        
        # Random number of bedrooms (with some missing values)
        bedrooms = random.choice([random.randint(1, 5), None])
        
        # Random number of bathrooms (with some missing values)
        bathrooms = random.choice([random.randint(1, 4), None])
        
        # Random number of total rooms (including bedrooms, living room, kitchen, etc.)
        rooms = random.choice([random.randint(2, 10), None])
        
        # Random balcony presence (50% chance of having a balcony)
        has_balcony = random.choice([True, False, None])
        
        # Random parking availability (50% chance of having parking)
        has_parking = random.choice([True, False, None])
        
        # Random floor level (15% chance of missing floor level)
        floor_level = random.choice(floor_levels + [None])
        
        # Random sale date (within the last 2 years)
        sale_date = fake.date_this_decade().strftime('%Y-%m-%d')
        
        # Random condition (15% chance of missing condition)
        condition = random.choice(conditions + [None])
        
        # Random owner name
        owner_name = fake.name()
        
        # Random email or None (10% chance of missing email)
        email = fake.email() if random.random() > 0.1 else None
        
        # Random phone number or None (10% chance of missing phone)
        phone = fake.phone_number() if random.random() > 0.1 else None
        
        # Random elevator presence (50% chance of having elevator)
        has_elevator = random.choice([True, False, None])
        
        # Append the row to data list
        data.append([apartment_id, location, price, size, bedrooms, bathrooms, rooms, has_balcony, has_parking, floor_level, sale_date, condition, owner_name, email, phone, has_elevator])
    
    return data

# Generate 500 rows of unclean apartment sales data
data = generate_uncleaned_apartment_sales_data(500)

# Create DataFrame
df = pd.DataFrame(data, columns=[
    'Apartment ID', 'Location', 'Price', 'Size (sqft)', 'Bedrooms', 'Bathrooms', 'Rooms', 
    'Has Balcony', 'Has Parking', 'Floor Level', 'Sale Date', 'Condition', 'Owner Name', 
    'Email', 'Phone', 'Has Elevator'
])

# Save the DataFrame to CSV file
df.to_csv('uncleaned_apartment_sales_data_with_features_500.csv', index=False)

print("CSV file 'uncleaned_apartment_sales_data_with_features_500.csv' created with 500 rows of unclean apartment sales data.")
