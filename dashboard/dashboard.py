import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Fungsi bantu
def sum_order(hour_df):
    sum_order_items_df = hour_df.groupby("hours").count_cr.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def macem_season(day_df): 
    season_df = day_df.groupby(by="season").count_cr.sum().reset_index() 
    return season_df

# Load data
days_df = pd.read_csv("dashboard/day_clean.csv")
hours_df = pd.read_csv("dashboard/hour_clean.csv")

# Konversi waktu & sorting
datetime_columns = ["dteday"]
for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

days_df.sort_values("dteday", inplace=True)
hours_df.sort_values("dteday", inplace=True)

# Ambil min & max untuk date input
min_date = days_df["dteday"].min()
max_date = days_df["dteday"].max()

# Sidebar untuk filter tanggal
with st.sidebar:
    st.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image1_hH9B4gs.jpg")
    start_date, end_date = st.date_input(
        label="Pilih Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan rentang waktu
main_df_days = days_df[(days_df["dteday"] >= pd.to_datetime(start_date)) & 
                       (days_df["dteday"] <= pd.to_datetime(end_date))]
main_df_hour = hours_df[(hours_df["dteday"] >= pd.to_datetime(start_date)) & 
                        (hours_df["dteday"] <= pd.to_datetime(end_date))]

# Proses data
sum_order_items_df = sum_order(main_df_hour)
season_df = macem_season(main_df_hour)

# Header
st.header("Analisis Penyewaan Sepeda 🚲")

# 1. Visualisasi jam paling banyak & sedikit disewa
st.subheader("Jam dengan Penyewaan Tertinggi & Terendah")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.head(5),
            palette=["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"], ax=ax[0])
ax[0].set_title("Jam Terbanyak", fontsize=30)
ax[0].tick_params(axis='x', labelsize=25)
ax[0].tick_params(axis='y', labelsize=25)

sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.sort_values(by="hours").head(5),
            palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9"], ax=ax[1])
ax[1].set_title("Jam Tersedikit", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='x', labelsize=25)
ax[1].tick_params(axis='y', labelsize=25)

st.pyplot(fig)

# 2. Visualisasi musim
st.subheader("Musim dengan Penyewaan Sepeda Tertinggi")
colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9"]
fig2, ax2 = plt.subplots(figsize=(20, 10))
sns.barplot(x="season", y="count_cr", data=season_df.sort_values(by="season", ascending=False),
            palette=colors, ax=ax2)
ax2.set_title("Jumlah Penyewaan per Musim", fontsize=40)
ax2.tick_params(axis='x', labelsize=30)
ax2.tick_params(axis='y', labelsize=25)

st.pyplot(fig2)
