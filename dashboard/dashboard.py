import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data with caching
@st.cache_data
def load_day_data():
    day_df = pd.read_csv("day_clean.csv")
    day_df.rename(columns={
        'dteday': 'date',
        'season': 'season_category',
        'mnth': 'month',
        'holiday': 'is_holiday',
        'weekday': 'weekday_category',
        'weathersit': 'weather_situation',
        'casual': 'casual_rentals',
        'registered': 'registered_rentals',
        'cnt': 'total_rentals'
    }, inplace=True)
    return day_df

@st.cache_data
def load_hour_data():
    hour_df = pd.read_csv("hour_clean.csv")
    hour_df.rename(columns={
        'dteday': 'date',
        'hr': 'hour',
        'season': 'season_category',
        'mnth': 'month',
        'holiday': 'is_holiday',
        'weekday': 'weekday_category',
        'weathersit': 'weather_situation',
        'casual': 'casual_rentals',
        'registered': 'registered_rentals',
        'cnt': 'total_rentals'
    }, inplace=True)
    return hour_df

# Load datasets
day_df = load_day_data()
hour_df = load_hour_data()

# Set up the Streamlit app layout
st.title("Dashboard Analisis Penyewaan Sepeda")

# Displaying dataframes
st.header("Data Penyewaan Harian")
st.dataframe(day_df)

st.header("Data Penyewaan Per Jam")
st.dataframe(hour_df)

# Sidebar for selecting analysis
st.sidebar.header("Jumlah Penyewaan Sepeda")
option = st.sidebar.selectbox("Pilih opsi:", [
    "Jumlah Penyewaan berdasarkan Musim", 
    "Jumlah Penyewaan berdasarkan Tahun",
    "Jumlah Penyewaan berdasarkan Jam",
    "Jumlah Penyewaan berdasarkan Hari dalam Minggu"
])

if option == "Jumlah Penyewaan berdasarkan Musim":
    st.subheader("Jumlah Penyewaan berdasarkan Musim")
    season_rentals = day_df.groupby('season_category')['total_rentals'].sum().sort_values(ascending=False).reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=season_rentals, x='season_category', y='total_rentals', ax=ax, palette='viridis')
    ax.set_title('Jumlah Penyewaan berdasarkan Musim', fontsize=16)
    ax.set_xlabel('Kategori Musim', fontsize=14)
    ax.set_ylabel('Jumlah Penyewaan', fontsize=14)
    st.pyplot(fig)

elif option == "Jumlah Penyewaan berdasarkan Tahun":
    st.subheader("Jumlah Penyewaan berdasarkan Tahun")
    yearly_rentals = day_df.groupby('yr')[['registered_rentals', 'casual_rentals']].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=yearly_rentals, x='yr', y='registered_rentals', label='Registered Rentals', marker='o', ax=ax)
    sns.lineplot(data=yearly_rentals, x='yr', y='casual_rentals', label='Casual Rentals', marker='o', ax=ax)
    ax.set_title('Jumlah Penyewaan berdasarkan Tahun', fontsize=16)
    ax.set_xlabel('Tahun', fontsize=14)
    ax.set_ylabel('Jumlah Penyewaan', fontsize=14)
    ax.legend(title='Jenis Penyewaan')
    st.pyplot(fig)

elif option == "Jumlah Penyewaan berdasarkan Jam":
    st.subheader("Jumlah Penyewaan berdasarkan Jam")
    hourly_rentals = hour_df.groupby('hour')['total_rentals'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=hourly_rentals, x='hour', y='total_rentals', marker='o', ax=ax)
    ax.set_title('Jumlah Penyewaan berdasarkan Jam', fontsize=16)
    ax.set_xlabel('Jam', fontsize=14)
    ax.set_ylabel('Jumlah Penyewaan', fontsize=14)
    st.pyplot(fig)

elif option == "Jumlah Penyewaan berdasarkan Hari dalam Minggu":
    st.subheader("Jumlah Penyewaan berdasarkan Hari dalam Minggu")
    weekday_rentals = day_df.groupby('weekday_category')['total_rentals'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=weekday_rentals, x='weekday_category', y='total_rentals', ax=ax, palette='magma')
    ax.set_title('Jumlah Penyewaan berdasarkan Hari dalam Minggu', fontsize=16)
    ax.set_xlabel('Hari dalam Minggu', fontsize=14)
    ax.set_ylabel('Jumlah Penyewaan', fontsize=14)
    st.pyplot(fig)

# Run the Streamlit app
if __name__ == "__main__":
    st.write("Dashboard ini menampilkan analisis interaktif penyewaan sepeda.")
