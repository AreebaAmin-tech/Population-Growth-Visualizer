import pandas as pd

def load_data(file_path=r"C:\Users\megazone\Documents\world_population_data.csv"):
    """
    Load the population data from the specified CSV file.
    """
    try:
        data = pd.read_csv(file_path)
        print("Data loaded successfully!")
        
        # Print the columns of the loaded data to verify
        print("Columns in the data:", data.columns)
        
        return data
    except FileNotFoundError:
        print(f"File not found at path: {file_path}")
        return None

def filter_data(data, country, start_year, end_year):
    """
    Filter data based on the selected country and year range.
    """
    if 'country' not in data.columns:
        print("The column 'country' does not exist in the data.")
        return None
    
    # Filter data for the specified country
    filtered_data = data[data['country'] == country]
    
    if filtered_data.empty:
        print(f"No data found for country: {country}")
        return None
    
    # Generate valid year columns dynamically based on the data
    years_columns = [f"{year} population" for year in range(start_year, end_year + 1)]
    
    # Check which year columns exist in the data
    valid_columns = [col for col in years_columns if col in data.columns]
    
    if not valid_columns:
        print(f"No valid population data found for {country} in the selected year range.")
        return None
    
    # Filter data by selected years
    filtered_data = filtered_data[valid_columns]
    
    return filtered_data

def calculate_growth_rate(data):
    """
    Calculate the population growth rate based on the available year columns.
    """
    if data is None:
        return None
    
    year_columns = [col for col in data.columns if 'population' in col]
    
    # Add growth rate calculations to data for each year
    for i in range(1, len(year_columns)):
        prev_year = year_columns[i-1]
        curr_year = year_columns[i]
        growth_rate_column = f"{curr_year} Growth Rate"
        
        data[growth_rate_column] = ((data[curr_year] - data[prev_year]) / data[prev_year]) * 100
    
    return data
