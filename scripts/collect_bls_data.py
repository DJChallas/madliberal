
import requests
import json
import pandas as pd
import os
from datetime import datetime

# Configuration
BLS_API_URL = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
API_KEY = '9dd192e92c9c4989985db57deede9647'  # Your BLS registration key
DATA_DIR = 'data'
CSV_FILE = os.path.join(DATA_DIR, 'bls_data.csv')

# Series IDs to collect
SERIES_IDS = [
    # Unemployment Series
    'LNS14000006', 'LNS14000009', 'LNS14000003', 'LNS14032183',
    'LNS14000002', 'LNS14000001', 'LNS14000005', 'LNS14000004',
    # Labor Force Series
    'LNS11000004', 'LNS11000005', 'LNS11032183', 'LNS11000001',
    'LNS11000002', 'LNS11000003', 'LNS11000006', 'LNS11000009',
    # Occupation Series
    'LNU02032526', 'LNU02032468',
    'LNU02032539', 'LNU02032481',
    'LNU02032545', 'LNU02032487',
    'LNU02032490', 'LNU02032548',
    'LNU02032554', 'LNU02032496'
]

SERIES_NAME_MAPPING = {
    # Unemployment Series
    'LNS14000006': 'Unemployment - Black or African American',
    'LNS14000009': 'Unemployment - Hispanic or Latino',
    'LNS14000003': 'Unemployment - White',
    'LNS14032183': 'Unemployment - Asian',
    'LNS14000002': 'Unemployment - Women',
    'LNS14000001': 'Unemployment - Men',
    'LNS14000005': 'Unemployment - White Women',
    'LNS14000004': 'Unemployment - White Men',
    # Labor Force Series
    'LNS11000004': 'Labor Force - White Men',
    'LNS11000005': 'Labor Force - White Women',
    'LNS11032183': 'Labor Force - Asian',
    'LNS11000001': 'Labor Force - Men',
    'LNS11000002': 'Labor Force - Women',
    'LNS11000003': 'Labor Force - White',
    'LNS11000006': 'Labor Force - Black or African American',
    'LNS11000009': 'Labor Force - Hispanic or Latino',
    # Occupation Series
    'LNU02032526': 'Management, Professional, and Related Occupations - Women',
    'LNU02032468': 'Management, Professional, and Related Occupations - Men',
    'LNU02032539': 'Service Occupations - Women',
    'LNU02032481': 'Service Occupations - Men',
    'LNU02032545': 'Sales and Office Occupations - Women',
    'LNU02032487': 'Sales and Office Occupations - Men',
    'LNU02032490': 'Natural Resources, Construction, and Maintenance Occupations - Men',
    'LNU02032548': 'Natural Resources, Construction, and Maintenance Occupations - Women',
    'LNU02032554': 'Transportation and Material Moving Occupations - Women',
    'LNU02032496': 'Transportation and Material Moving Occupations - Men'
}


def period_to_month(period_str):
    """Convert BLS period format to month number."""
    if period_str.startswith('M'):
        return int(period_str[1:])
    elif period_str == 'Q01':
        return 1
    elif period_str == 'Q02':
        return 4
    elif period_str == 'Q03':
        return 7
    elif period_str == 'Q04':
        return 10
    return None


def fetch_bls_data(start_year, end_year):
    """Fetch data from BLS API for the specified year range."""
    headers = {'Content-Type': 'application/json'}
    
    data = json.dumps({
        "seriesid": SERIES_IDS,
        "startyear": str(start_year),
        "endyear": str(end_year),
        "registrationkey": API_KEY
    })
    
    try:
        response = requests.post(BLS_API_URL, data=data, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching BLS data: {e}")
        return None


def process_bls_data(json_data):
    """Process BLS API response into a pandas DataFrame."""
    all_series_data = []
    
    if 'Results' not in json_data or 'series' not in json_data['Results']:
        print("No data found in BLS response")
        return pd.DataFrame()
    
    for series in json_data['Results']['series']:
        series_id = series['seriesID']
        
        for item in series['data']:
            year = item['year']
            period = item['period']
            value = item['value']
            
            # Extract footnotes
            footnotes_list = []
            for footnote in item.get('footnotes', []):
                if footnote:
                    footnotes_list.append(footnote.get('text', ''))
            footnotes = ','.join(footnotes_list)
            
            # Only include monthly and quarterly data
            if ('M01' <= period <= 'M12') or ('Q01' <= period <= 'Q04'):
                all_series_data.append({
                    'series_id': series_id,
                    'year': int(year),
                    'period': period,
                    'value': value,
                    'footnotes': footnotes
                })
    
    if not all_series_data:
        print("No valid data found in BLS response")
        return pd.DataFrame()
    
    df = pd.DataFrame(all_series_data)
    
    # Convert period to month
    df['month'] = df['period'].apply(period_to_month)
    df = df.dropna(subset=['month'])
    df['month'] = df['month'].astype(int)
    
    # Create date column
    df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str) + '-01')
    df = df.drop(columns=['month'])
    
    # Convert value to numeric
    df['value'] = pd.to_numeric(df['value'].astype(str).replace(r'\s+\(\d+\)', '', regex=True), errors='coerce')
    
    # Apply division by 100 for unemployment series (they are percentages)
    unemployment_series = [
        'LNS14000006', 'LNS14000009', 'LNS14000003', 'LNS14032183',
        'LNS14000002', 'LNS14000001', 'LNS14000005', 'LNS14000004'
    ]
    df.loc[df['series_id'].isin(unemployment_series), 'value'] = \
        df.loc[df['series_id'].isin(unemployment_series), 'value'] / 100
    
    # Remove rows with NaN values
    df = df.dropna(subset=['value'])
    
    # Add series name
    df['series_name'] = df['series_id'].map(SERIES_NAME_MAPPING)
    
    return df


def append_or_create_data(new_df):
    """Append new data to existing CSV or create if it doesn't exist."""
    # Create data directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)
    
    if os.path.exists(CSV_FILE):
        # Load existing data
        existing_df = pd.read_csv(CSV_FILE)
        
        # Convert date columns to datetime for comparison
        existing_df['date'] = pd.to_datetime(existing_df['date'])
        new_df['date'] = pd.to_datetime(new_df['date'])
        
        # Remove duplicates: keep new data if there are overlapping dates
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        combined_df = combined_df.drop_duplicates(subset=['series_id', 'date'], keep='last')
        
        print(f"Appended {len(new_df)} new records to existing data")
    else:
        combined_df = new_df
        print(f"Created new data file with {len(new_df)} records")
    
    # Sort by date and series_id
    combined_df = combined_df.sort_values(['series_id', 'date']).reset_index(drop=True)
    
    # Save to CSV
    combined_df.to_csv(CSV_FILE, index=False)
    print(f"Data saved to {CSV_FILE}")


def main():
    """Main execution function."""
    print(f"Starting BLS data collection at {datetime.now()}")
    
    # Get current year and fetch data for last 4 years + current year
    current_year = datetime.now().year
    start_year = current_year - 4
    end_year = current_year
    
    print(f"Fetching BLS data from {start_year} to {end_year}")
    
    # Fetch data from BLS API
    json_data = fetch_bls_data(start_year, end_year)
    
    if json_data is None:
        print("Failed to fetch data from BLS API")
        return
    
    # Process the data
    new_df = process_bls_data(json_data)
    
    if new_df.empty:
        print("No data to process")
        return
    
    # Append or create the CSV file
    append_or_create_data(new_df)
    
    print(f"BLS data collection completed at {datetime.now()}")


if __name__ == '__main__':
    main()
