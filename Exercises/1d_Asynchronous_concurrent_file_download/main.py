import time
import aiohttp
import asyncio
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

async def concurrent_request(session,uri, dir):
        async with session.get(uri) as response:
            if response.status == 200:
                content = response.content.read()
                download_path = dir / os.path.basename(uri)
                with open(download_path, 'wb') as f:
                    f.write(await content)
                with ZipFile(download_path, 'r') as zObject:
                        zObject.extractall(dir)
                os.remove(download_path)
            
async def main(uris):
    async with aiohttp.ClientSession() as session:
    
        tasks = [asyncio.ensure_future(concurrent_request(session,uri, setup_dir())) for uri in uris]

        for task in asyncio.as_completed(tasks):  
            task = await task
            if task == None:
                continue
            return task
                
if __name__ == '__main__':
    s = time.perf_counter()
    asyncio.run(main(download_uris))
    elapsed = time.perf_counter() - s
    print(f"executed in {elapsed:0.2f} seconds.")
    
    
