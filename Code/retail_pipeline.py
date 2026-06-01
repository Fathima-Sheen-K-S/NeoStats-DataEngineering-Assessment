import pandas as pd
import numpy as np

# Load Excel File
file_path = r"../Dataset/USECASE - Data Engineering.xlsx"

# Read Sheets
product_details = pd.read_excel(file_path, sheet_name='product_details')
retail_data1 = pd.read_excel(file_path, sheet_name='retail_data1')
retail_data2 = pd.read_excel(file_path, sheet_name='retail_data2')

# Display Basic Information
print("PRODUCT DETAILS")
print(product_details.head())

print("\nRETAIL DATA 1")
print(retail_data1.head())

print("\nRETAIL DATA 2")
print(retail_data2.head())

# Dataset Shapes
print("\nDataset Shapes:")
print("Product Details:", product_details.shape)
print("Retail Data1:", retail_data1.shape)
print("Retail Data2:", retail_data2.shape)

# Combine Retail Datasets
retail_data = pd.concat([retail_data1, retail_data2], ignore_index=True)

print("\nCOMBINED DATASET")
print(retail_data.head())

# Dataset Info
print("\nDATASET INFO")
print(retail_data.info())

# Check Missing Values
print("\nMISSING VALUES")
print(retail_data.isnull().sum())

# Check Duplicate Records
duplicates = retail_data.duplicated().sum()

print("\nDUPLICATE RECORDS:", duplicates)

# Check Unique Product Names
print("\nUNIQUE PRODUCT NAMES")
print(retail_data['product_name'].unique())

# Check Unique Categories
print("\nUNIQUE CATEGORIES")
print(retail_data['category'].unique())


# -------------------------------
# DATA CLEANING
# -------------------------------

# Standardize Product Names
retail_data['product_name'] = retail_data['product_name'].str.strip().str.title()

# Category Mapping
category_mapping = {
    'ELEC': 'Electronics',
    'electronics': 'Electronics',
    'Electronics': 'Electronics',

    'CLOTH': 'Clothing',
    'clothing': 'Clothing',
    'Clothing': 'Clothing',

    'FURN': 'Furniture',
    'furniture': 'Furniture',
    'Furniture': 'Furniture',

    'HOME': 'Home Appliances',
    'home appliances': 'Home Appliances',
    'Home Appliances': 'Home Appliances'
}

# Standardize Categories
retail_data['category'] = retail_data['category'].replace(category_mapping)

# Fill Missing Prices Using Product Table
price_mapping = product_details.set_index('product_id')['price']

retail_data['price'] = retail_data['price'].fillna(
    retail_data['product_id'].map(price_mapping)
)

# Remove Invalid Quantities
retail_data = retail_data[retail_data['quantity'] > 0]

# Convert Transaction Date
retail_data['transaction_date'] = pd.to_datetime(
    retail_data['transaction_date'],
    errors='coerce'
)

# Check Remaining Missing Values
print("\nMISSING VALUES AFTER CLEANING")
print(retail_data.isnull().sum())

# Check Clean Product Names
print("\nCLEAN PRODUCT NAMES")
print(retail_data['product_name'].unique())

# Check Clean Categories
print("\nCLEAN CATEGORIES")
print(retail_data['category'].unique())

# -------------------------------
# PII MASKING
# -------------------------------

# Mask Email Function
def mask_email(email):
    email = str(email)

    if '@' in email:
        parts = email.split('@')
        name = parts[0]
        domain = parts[1]

        if len(name) > 3:
            masked_name = name[:3] + '*' * (len(name) - 3)
        else:
            masked_name = '*' * len(name)

        return masked_name + '@' + domain

    return email

# Mask Phone Function
def mask_phone(phone):
    phone = str(phone)

    if len(phone) >= 4:
        return phone[:2] + '*' * 6 + phone[-2:]

    return phone

# Apply Masking
retail_data['masked_email'] = retail_data['email'].apply(mask_email)
retail_data['masked_phone'] = retail_data['phone'].apply(mask_phone)

print("\nPII MASKING SAMPLE")
print(retail_data[['email', 'masked_email', 'phone', 'masked_phone']].head())


# -------------------------------
# KPI CALCULATIONS
# -------------------------------

# Revenue Calculation
retail_data['revenue'] = (
    retail_data['price'] *
    retail_data['quantity']
) - retail_data['discount']

# Total Revenue
total_revenue = retail_data['revenue'].sum()

print("\nTOTAL REVENUE")
print(total_revenue)

# Revenue by Category
revenue_by_category = retail_data.groupby('category')['revenue'].sum()

print("\nREVENUE BY CATEGORY")
print(revenue_by_category)

# Revenue by City
revenue_by_city = retail_data.groupby('city')['revenue'].sum()

print("\nREVENUE BY CITY")
print(revenue_by_city.head())

# Top Selling Products
top_products = retail_data.groupby('product_name')['quantity'].sum().sort_values(ascending=False)

print("\nTOP SELLING PRODUCTS")
print(top_products)

# Most Used Payment Method
payment_method = retail_data['payment_method'].value_counts()

print("\nMOST USED PAYMENT METHOD")
print(payment_method)

# Highest Revenue Cities
top_cities = retail_data.groupby('city')['revenue'].sum().sort_values(ascending=False)

print("\nTOP REVENUE CITIES")
print(top_cities.head())

# -------------------------------
# EXPORT CLEAN DATASET
# -------------------------------

output_path = r"../Output/final_cleaned_retail_data.csv"

retail_data.to_csv(output_path, index=False)

print("\nCLEANED DATASET EXPORTED SUCCESSFULLY")