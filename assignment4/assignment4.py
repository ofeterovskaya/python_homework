import pandas as pd

# Task 1: Introduction to Pandas - Creating and Manipulating DataFrames

# Create a DataFrame from a dictionary
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}

task1_data_frame = pd.DataFrame(data)
print("Task 1 DataFrame:")
print(task1_data_frame)

# Add a new column 'Salary'
task1_with_salary = task1_data_frame.copy()
task1_with_salary['Salary'] = [70000, 80000, 90000]
print("\nTask 1 with Salary:")
print(task1_with_salary)

# Increment the Age column
task1_older = task1_with_salary.copy()
task1_older['Age'] = task1_older['Age'] + 1
print("\nTask 1 Older (Age + 1):")
print(task1_older)

# Write to CSV (without index)
task1_older.to_csv('employees.csv', index=False)

# Task 2: Loading Data from CSV and JSON
# Read data from CSV file
task2_employees = pd.read_csv('employees.csv')
print("\nTask 2 - Loaded from CSV:")
print(task2_employees)

# Create and save JSON file with additional employees
import json
additional_employees_data = {
    'Name': ['Eve', 'Frank'],
    'Age': [28, 40],
    'City': ['Miami', 'Seattle'],
    'Salary': [60000, 95000]
}

# Save to JSON file
with open('additional_employees.json', 'w') as f:
    json.dump(additional_employees_data, f, indent=2)

# Read data from JSON file
json_employees = pd.read_json('additional_employees.json')
print("\nTask 2 - Loaded from JSON:")
print(json_employees)

# Combine DataFrames
more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)
print("\nTask 2 - Combined DataFrame:")
print(more_employees)


# Task 3: Data Inspection - Using Head, Tail, and Info Methods

# Use head() to get first three rows
first_three = more_employees.head(3)
print("\nTask 3 - First three rows:")
print(first_three)

# Use tail() to get last two rows
last_two = more_employees.tail(2)
print("\nTask 3 - Last two rows:")
print(last_two)

# Get the shape of the DataFrame
employee_shape = more_employees.shape
print("\nTask 3 - DataFrame shape:")
print(employee_shape)

# Use info() method
print("\nTask 3 - DataFrame info:")
more_employees.info()

# Task 4: Data Cleaning - Handling Missing Values and Standardizing Data

# Read dirty_data.csv
dirty_data = pd.read_csv('dirty_data.csv')
print("\nTask 4 - Dirty Data:")
print(dirty_data)

# Create a copy for cleaning
clean_data = dirty_data.copy()

# Remove duplicate rows
clean_data.drop_duplicates(inplace=True)
print("\nTask 4 - After removing duplicates:")
print(clean_data)

# Convert Age to numeric and handle missing values
clean_data['Age'] = pd.to_numeric(clean_data['Age'], errors='coerce')
print("\nTask 4 - After converting Age to numeric:")
print(clean_data)

# Convert Salary to numeric and replace known placeholders with NaN
clean_data['Salary'] = clean_data['Salary'].replace(['unknown', 'n/a'], pd.NA)
clean_data['Salary'] = pd.to_numeric(clean_data['Salary'], errors='coerce')
print("\nTask 4 - After converting Salary to numeric:")
print(clean_data)

# Fill missing numeric values: Age with mean, Salary with median
clean_data['Age'] = clean_data['Age'].fillna(clean_data['Age'].mean())
clean_data['Salary'] = clean_data['Salary'].fillna(clean_data['Salary'].median())
print("\nTask 4 - After filling missing values:")
print(clean_data)

# Convert Hire Date to datetime
clean_data['Hire Date'] = pd.to_datetime(clean_data['Hire Date'], format='mixed', errors='coerce')
print("\nTask 4 - After converting Hire Date to datetime:")
print(clean_data)

# Strip extra whitespace and standardize Name and Department as uppercase
clean_data['Name'] = clean_data['Name'].str.strip()
clean_data['Department'] = clean_data['Department'].str.strip().str.upper()
print("\nTask 4 - Final cleaned data:")
print(clean_data)

