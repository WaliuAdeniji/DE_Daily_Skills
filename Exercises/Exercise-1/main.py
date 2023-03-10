import requests
from pathlib import Path
from zipfile import ZipFile
import os

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
def download_file(dir, uris):
    for uri in uris:
        download_path = dir / os.path.basename(uri)
        response = requests.get(uri)
        if response:
            with open(download_path, 'wb') as f:
                f.write(response.content)
            with ZipFile(download_path, 'r') as zObject:
                zObject.extractall(dir)
            os.remove(download_path) 

if __name__ == '__main__':
    download_file(setup_dir(), download_uris)
    
    
