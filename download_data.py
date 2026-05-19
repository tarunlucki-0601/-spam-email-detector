import os
import urllib.request
import zipfile

def download_and_extract_data():
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"
    zip_path = "smsspamcollection.zip"
    data_dir = "data"

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    print("Downloading dataset...")
    urllib.request.urlretrieve(url, zip_path)
    
    print("Extracting dataset...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(data_dir)
        
    os.remove(zip_path)
    print(f"Dataset extracted to {data_dir}/SMSSpamCollection")

if __name__ == "__main__":
    download_and_extract_data()
