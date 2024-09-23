import argparse
import urllib.request  
import logging
from datetime import datetime
import csv
import re
from collections import Counter

def downloadData(url):
    """
    Downloads the contents from the provided URL and returns it.
    """
    try:
        response = urllib.request.urlopen(url)
        csvData = response.read().decode('utf-8')  # Decode byte content to string
        return csvData
    except Exception as e:
        logging.error(f"Error downloading data from URL: {url}")
        raise

def processData(csvData):
    """
    Processes the CSV file contents and returns a dictionary mapping information about each hit.
"""
    log_entries = []
    reader = csv.reader(csvData.splitlines())
    
    # Read each row and parse it
    for row in reader:
        log_entry = {
            'path': row[0],
            'datetime': row[1],
            'browser': row[2],
            'status': row[3],
            'size': row[4]
        }
        log_entries.append(log_entry)
    
    return log_entries

def imageRequestStats(log_entries):
    """
    Calculates the percentage of requests that are for image files.
    """
    image_extensions = re.compile(r'.*\.(jpg|gif|png)$')
    total_requests = len(log_entries)
    image_requests = 0
    
    for entry in log_entries:
        if image_extensions.match(entry['path']):
            image_requests += 1
    
    image_percentage = (image_requests / total_requests) * 100
    print(f"Image requests account for {image_percentage:.1f}% of all requests.")

def mostPopularBrowser(log_entries):
    """
    Determines the most popular browser based on log entries.
    """
    browser_pattern = re.compile(r'(Firefox|Chrome|MSIE|Safari)')
    browser_count = Counter()
    
    for entry in log_entries:
        match = browser_pattern.search(entry['browser'])
        if match:
            browser_name = match.group(1)
            if browser_name == 'MSIE':
                browser_count['Internet Explorer'] += 1
            else:
                browser_count[browser_name] += 1
    
    most_common_browser = browser_count.most_common(1)[0]
    print(f"The most popular browser is {most_common_browser[0]} with {most_common_browser[1]} hits.")

def main(url):
    """
    Main function that orchestrates downloading, processing, and analyzing data.
"""
    print(f"Running main with URL = {url}...")
    
    # Download and process the data
    try:
        csvData = downloadData(url)
        log_entries = processData(csvData)
        
        # Part III: Image request stats
        imageRequestStats(log_entries)
        
        # Part IV: Most popular browser
        mostPopularBrowser(log_entries)
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
