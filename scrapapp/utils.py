import pandas as pd

def fetch_kerala_cities():
    """
    Fetches all cities and towns in Kerala from Wikipedia
    and returns a list of tuples suitable for Django ChoiceField.
    Example: [('Thiruvananthapuram', 'Thiruvananthapuram'), ...]
    """
    url = "https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Kerala"
    
    try:
        # Read all tables from the Wikipedia page
        tables = pd.read_html(url)
        
        cities = []
        
        for table in tables:
            # Look for a column that contains 'City' or 'Town'
            col_candidates = [col for col in table.columns if 'City' in str(col) or 'Town' in str(col)]
            
            if col_candidates:
                # Use the first matching column
                city_col = col_candidates[0]
                cities.extend(table[city_col].tolist())
        
        # Clean the list: remove duplicates and NaN
        cities = [str(city).strip() for city in cities if pd.notna(city)]
        cities = sorted(list(set(cities)))  # optional: sorted unique list
        
        # Prepare as Django ChoiceField tuples
        city_choices = [(city, city) for city in cities]
        return city_choices

    except Exception as e:
        print("Failed to fetch Kerala cities:", e)
        return []

# Pre-fetch the choices once so forms can import
city_choices = fetch_kerala_cities()
