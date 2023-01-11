import time
import requests
from pathlib import Path
from zipfile import ZipFile
import os
import concurrent.futures


download_uris = [
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip'
]

def setup_dir():
    download_dir = Path('downloads')
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir

def download_file(dir, uri):
    download_path = dir / os.path.basename(uri)
    response = requests.get(uri)
    if response.status_code==200:
        with open(download_path, 'wb') as f:
            f.write(response.content)
        with ZipFile(download_path, 'r') as zObject:
            zObject.extractall(dir)
        os.remove(download_path) 

def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(download_file, dir=setup_dir(), uri=uri) for uri in download_uris]

        for val in concurrent.futures.as_completed(results):
            return (val.result())


if __name__ == '__main__':
    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"executed in {elapsed:0.2f} seconds")
