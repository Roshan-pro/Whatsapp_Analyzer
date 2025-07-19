import streamlit as st
import pandas as pd 
import os
import zipfile
import yaml

from src.feature_enginnering import FeautreEng, SetDatesMonths
from zip_data.unzipdata import Data, UnzipData
from src.data_info import DataInformation, DataInfo, ISNULL, DuplicatePresent, ValueCounts
from src.mostfrequentwords import MostFrequentWords, MostFrequentWordsinGroups, MostFrequentWordsfromMembers
from src.messageActivityWeek import WeekMeassage, MembersWeeklyMessage
from src.top_senders import TopSenedr, Barplot
from src.correlationChats import WhatsappCorrelation,WhatsappMatrix

import matplotlib.pyplot as plt
plt.show = lambda: st.pyplot(plt.gcf())  

def load_config(path="config.yaml"):
    with open(path, "r") as file:
        return yaml.safe_load(file)

config = load_config("config.yaml")

st.set_page_config(layout="wide")
st.title("📊 WhatsApp Chat Analyzer")

uploaded_file = st.file_uploader("Upload WhatsApp ZIP file", type="zip")

if uploaded_file:
    with open(config["chat"]["default_zip_path"], "wb") as f:
        f.write(uploaded_file.read())

    try:
        # Unzip and ingest data
        data_handler = Data.get_data(".zip")
        df = data_handler.ingest(config["chat"]["default_zip_path"])

        # Feature Engineering: Add Day and Month
        fe = FeautreEng(SetDatesMonths(df, config["data"]["date_column"]))
        df = fe.apply()

        st.success("Chat loaded and preprocessed successfully!")

        # Show DataFrame
        if st.checkbox("Show raw data"):
            st.dataframe(df.head(100))

        # Info Checks
        st.subheader("📋 Data Quality Checks")

        DataInformation(DataInfo()).info(df)
        DataInformation(ISNULL()).info(df)
        DataInformation(DuplicatePresent()).info(df)
        DataInformation(ValueCounts("Sender")).info(df)

        # Top Senders
        st.subheader("📈 Top Senders")
        top_n = st.slider("Select number of top senders", 3, 20, config["visuals"]["top_n_senders"])
        TopSenedr(Barplot()).plot(df, top_n)

        # Frequent Words
        st.subheader("☁️ Word Clouds")
        freq_option = st.radio("View word cloud for:", ["Group", "Specific Member"])

        if freq_option == "Group":
            MostFrequentWords(MostFrequentWordsinGroups()).checkFreqWords(df)

        elif freq_option == "Specific Member":
            member_name = st.text_input("Enter sender name (case-sensitive):")
            if member_name:
                MostFrequentWords(MostFrequentWordsfromMembers(member_name)).checkFreqWords(df)

        # Weekly Activity
        st.subheader("📅 Weekly Message Activity by Sender")
        sender_name = st.text_input("Check weekly activity for sender:")
        if sender_name:
            WeekMeassage(MembersWeeklyMessage()).analysis(df, sender_name)

        # Day-wise message listing
        st.subheader("📬 Messages by Member on a Specific Day")
        day_choice = st.selectbox("Select a day:", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        member_input = st.text_input("Enter sender name for message listing:")

        if day_choice and member_input:
            filtered = df[(df["Sender"] == member_input) & (df["Day"] == day_choice)]
            if not filtered.empty:
                st.markdown(f"### Messages by **{member_input}** on **{day_choice}**")
                for _, row in filtered.iterrows():
                    st.markdown(f"**{row['Date'].date()}** - {row['Message']}")
            else:
                st.info(f"No messages by {member_input} on {day_choice}.")
        #Correlation Matrix
        st.subheader("🔍 Select up to 6 Members for Correlation Analysis")
        selected_members=st.multiselect(
            "Choose members (chat names):",
            options=df["Sender"].unique().tolist(),
            max_selections=6
        )
        try:
            if len(selected_members)==6:
                message_count=df[df["Sender"].isin(selected_members)]
                pivot_df = message_count.groupby(["Day", "Sender"]).size().unstack(fill_value=0)
                pivot_df=pivot_df[selected_members]
                corr=WhatsappCorrelation(WhatsappMatrix(pivot_df)).plot()
                if corr:
                    st.success("✅ Correlation matrix generated successfully!")
                    st.pyplot(corr)
                else:
                    st.error("❌ Could not generate correlation matrix.")

        except Exception as e:
            st.error(f"❌ Error generating daily activity correlation: {e}")

    except Exception as e:
        st.error(f"Error loading chat: {e}")
else:
    st.info("Please upload a WhatsApp chat ZIP file to begin.")
