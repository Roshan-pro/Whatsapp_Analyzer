import zipfile
import pandas as pd
import os
from abc import ABC, abstractmethod
import re
import shutil

class DataIngester(ABC):
    @abstractmethod
    def ingest(self, file_path: str) -> pd.DataFrame:
        pass

class UnzipData(DataIngester):
    def ingest(self, file_path: str = None) -> pd.DataFrame:
        data = []

        if not file_path.endswith(".zip"):
            raise ValueError("The provided file path is not a ZIP file!")

        extract_dir = "Extracted_data"

        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
        os.makedirs(extract_dir)

        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        extracted_files = os.listdir(extract_dir)
        txt_files = [f for f in extracted_files if f.endswith(".txt")]

        if len(txt_files) == 0:
            raise ValueError("❌ No .txt file found inside the ZIP!")

        # Pick the first .txt file
        txt_file_path = os.path.join(extract_dir, txt_files[0])
        print(f"📂 Using file: {txt_file_path}")

        # ✅ Correct regex pattern
        pattern = r"(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}\s[APMapm]{2}) - (.*?): (.*)"

        with open(txt_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                match = re.match(pattern, line)
                if match:
                    date, time, sender, message = match.groups()
                    data.append({
                        "Date": date,
                        "Time": time,
                        "Sender": sender,
                        "Message": message
                    })
                else:
                    if data:
                        data[-1]["Message"] += " " + line

        df = pd.DataFrame(data)
        df.to_csv("whatsapp_chat.csv", index=False)
        print("✅ Chat saved as 'whatsapp_chat.csv'")
        return df

class Data:
    @staticmethod
    def get_data(file_extension: str) -> DataIngester:
        if file_extension == ".zip":
            return UnzipData()
        else:
            raise ValueError("Unsupported file extension.")
