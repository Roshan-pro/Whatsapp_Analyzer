# Whatsapp_Analyzer
# 📊 WhatsApp Chat Analyzer

An interactive Streamlit web app to analyze WhatsApp group chats. Upload your exported chat in `.zip` format and gain deep insights into message activity, top senders, frequent words, and message correlations.

---

## 🚀 Features

- 🔓 **Upload & Process WhatsApp ZIP Chat Files**
- 🧹 **Data Preprocessing & Feature Engineering**
  - Extracts date, day of the week, and month
- 📋 **Data Quality Checks**
  - Shows nulls, duplicates, and value distributions
- 📈 **Top Senders Visualization**
  - Interactive slider to customize top N senders
- ☁️ **Word Cloud Generator**
  - Most frequent words in the group or by a specific member
- 📅 **Weekly Message Activity**
  - Analyze message frequency by week per user
- 📬 **Daily Message Viewer**
  - View messages by member on a selected day
- 🔗 **Correlation Matrix**
  - Select up to 6 members to compare their daily messaging activity

---

## 🛠️ How It Works

### 1. Upload Chat
Upload a WhatsApp `.zip` file exported from your mobile device.

### 2. Automated Data Processing
- The file is unzipped and parsed
- Dates and days are extracted
- Data is cleaned for missing and duplicate values

### 3. Visualizations
Explore your chat through:
- Bar charts
- Word clouds
- Weekly activity lines
- Correlation heatmaps

---

## 📂 Project Structure

```bash
Whatsapp_Analyzer/
├── analysis/
│   └── Extracted_data/
│       ├── WhatsApp Chat with Group1.txt
│       ├── whatsapp_chat.csv
│       └── whatsapp.ipynb
├── src/
│   ├── __init__.py
│   ├── correlationChats.py
│   ├── data_info.py
│   ├── feature_enginnering.py
│   ├── messageActivityWeek.py
│   ├── mostfrequentwords.py
│   ├── top_senders.py
│   └── whatsapp/              # (Optional - if needed)
├── zip_data/
│   ├── __init__.py
│   ├── unzipdata.py
│   └── WhatsApp Chat with Group.zip
├── .gitignore
├── app.py
├── config.yaml
└── chat.zip

```
⚙️ Configuration (config.yaml)
```bash
data:
  extract_path: "Extracted_data"
  date_column: "Date"

wordcloud:
  width: 800
  height: 400
  background_color: "white"
  stopwords:
    - media
    - omitted
    - sticker
    - gif
    - image
    - video
    - file
  colormap: "viridis"

visuals:
  color_palette: "coolwarm"
  top_n_senders: 5

chat:
  default_zip_path: "chat.zip"
```
▶️ How to Run
1)Clone the repository:
```bash
git clone https://github.com/Roshan-pro/Whatsapp_Analyzer.git
cd Whatsapp_Analyzer
```
2)Create a virtual environment and activate it (optional but recommended):
```bash
python -m venv whatsapp
source whatsapp/bin/activate    # Linux/Mac
.\whatsapp\Scripts\activate     # Windows
```
3) Install dependencies:

```bash
pip install -r requirements.txt
```

4)Run the Streamlit app:

```bash
streamlit run app.py
```
## ✅ Dependencies
 - seaborn
 - matplotlib
 - pandas
 - numpy
 - wordcloud
 - streamlit
 - pyyaml

You can install them using:

```bash
pip install -r requirements.txt
```

## 📌 Notes
Case-sensitive sender names are required in some inputs.

Only .zip exported chat files are supported.

For best results, do not edit the exported file manually.


