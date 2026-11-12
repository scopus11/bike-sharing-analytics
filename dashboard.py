import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Bike Sharing Analytics",
    page_icon="🚲",
    layout="wide"
)
sns.set_theme(style="whitegrid", palette="Set2")

# ==========================================
# MEMUAT DATASET
# ==========================================
day_df = pd.read_csv("day_data.csv")
hour_df = pd.read_csv("hour_data.csv")

day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
weather_mapping = {
    1: "Clear",
    2: "Mist/Cloudy",
    3: "Light Rain/Snow",
    4: "Heavy Rain/Snow"
}

day_df["season_label"] = day_df["season"].map(season_mapping)
hour_df["season_label"] = hour_df["season"].map(season_mapping)
day_df["weather_label"] = day_df["weathersit"].map(weather_mapping)
hour_df["weather_label"] = hour_df["weathersit"].map(weather_mapping)

# ==========================================
# HEADER
# ==========================================
st.title("🚲 Bike Sharing Analytics Dashboard")
st.caption("Eksplorasi pola penyewaan sepeda berdasarkan waktu, musim, dan kondisi cuaca.")
st.markdown(
    "Dashboard ini menyajikan ringkasan penyewaan serta pola permintaan "
    "untuk membantu memahami kapan dan dalam kondisi apa sepeda paling banyak digunakan."
)
st.divider()

# ==========================================
# FILTER SIDEBAR
# ==========================================
st.sidebar.header("🔎 Filter Data")
years = sorted(day_df["dteday"].dt.year.unique())

selected_year = st.sidebar.selectbox(
    "Pilih Tahun", options=["Semua Tahun"] + years
)
selected_season_label = st.sidebar.selectbox(
    "Pilih Musim", options=["Semua Musim"] + list(season_mapping.values())
)
selected_weather_label = st.sidebar.selectbox(
    "Pilih Kondisi Cuaca", options=["Semua Cuaca"] + list(weather_mapping.values())
)

selected_season = next(
    (key for key, value in season_mapping.items() if value == selected_season_label),
    None
)
selected_weather = next(
    (key for key, value in weather_mapping.items() if value == selected_weather_label),
    None
)

# Helper filter agar konsisten
def apply_filters(data, include_season=True, include_weather=True):
    result = data.copy()
    if selected_year != "Semua Tahun":
        result = result[result["dteday"].dt.year == selected_year]
    if include_season and selected_season is not None:
        result = result[result["season"] == selected_season]
    if include_weather and selected_weather is not None:
        result = result[result["weathersit"] == selected_weather]
    return result

filtered_day = apply_filters(day_df)

# ==========================================
# KPI
# ==========================================
st.subheader("📌 Ringkasan Penyewaan")
k1, k2, k3 = st.columns(3)

total = filtered_day["cnt"].sum()
mean_daily = filtered_day["cnt"].mean()
n_days = len(filtered_day)

k1.metric("Total Penyewaan", f"{total:,.0f}")
k2.metric("Rata-rata per Hari", f"{mean_daily:,.0f}" if pd.notna(mean_daily) else "0")
k3.metric("Jumlah Hari", f"{n_days:,}")
st.caption("KPI mengikuti filter tahun, musim, dan kondisi cuaca yang dipilih.")
st.divider()

# ==========================================
# HOURLY ANALYSIS
# ==========================================
st.subheader("🕒 Analisis Penyewaan Berdasarkan Jam")
st.write("Perbandingan rata-rata penyewaan antara hari kerja dan akhir pekan pada setiap jam.")

hour_df["day_type"] = hour_df["weekday"].apply(
    lambda x: "Weekend" if x in [0, 6] else "Weekday"
)
filtered_hour = apply_filters(hour_df)

hourly_rentals = (
    filtered_hour.groupby(["hr", "day_type"])["cnt"]
    .mean().reset_index()
)

fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(
    data=hourly_rentals, x="hr", y="cnt", hue="day_type",
    marker="o", linewidth=2.2, ax=ax
)
ax.set_title("Average Bike Rentals by Hour", pad=14, fontsize=14)
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Average Rentals")
ax.set_xticks(range(24))
ax.legend(title="Day Type")
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

if not hourly_rentals.empty:
    peak = hourly_rentals.loc[hourly_rentals["cnt"].idxmax()]
    st.info(
        f"Insight: rata-rata penyewaan tertinggi pada data terfilter terjadi "
        f"pukul {int(peak['hr'])}:00 ({peak['day_type']}) dengan "
        f"{peak['cnt']:,.0f} penyewaan."
    )
st.divider()

# ==========================================
# SEASONAL ANALYSIS
# ==========================================
st.subheader("🌤️ Analisis Penyewaan Berdasarkan Musim")
st.write("Perbandingan rata-rata penyewaan pengguna casual dan registered pada setiap musim.")

season_df = apply_filters(day_df, include_season=False, include_weather=True)
seasonal_rentals = (
    season_df.groupby("season")[["casual", "registered"]]
    .mean().reset_index()
)
seasonal_rentals["season_label"] = seasonal_rentals["season"].map(season_mapping)
seasonal_rentals = seasonal_rentals.melt(
    id_vars="season_label",
    value_vars=["casual", "registered"],
    var_name="User Type",
    value_name="Average Rentals"
)
season_order = ["Spring", "Summer", "Fall", "Winter"]

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    data=seasonal_rentals, x="season_label", y="Average Rentals",
    hue="User Type", order=season_order, ax=ax
)
ax.set_title("Average Bike Rentals by Season", pad=14, fontsize=14)
ax.set_xlabel("Season")
ax.set_ylabel("Average Rentals")
ax.legend(title="User Type")
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

if not seasonal_rentals.empty:
    season_totals = seasonal_rentals.groupby("season_label")["Average Rentals"].sum()
    best_season = season_totals.idxmax()
    st.info(f"Insight: total rata-rata casual dan registered tertinggi terlihat pada musim {best_season}.")
st.divider()

# ==========================================
# WEATHER ANALYSIS
# ==========================================
st.subheader("🌧️ Analisis Penyewaan Berdasarkan Cuaca")
st.write("Perbandingan rata-rata jumlah penyewaan sepeda berdasarkan kondisi cuaca.")

weather_df = apply_filters(day_df, include_season=True, include_weather=False)
weather_rentals = (
    weather_df.groupby("weathersit")["cnt"]
    .mean().reset_index()
)
weather_rentals["weather_label"] = weather_rentals["weathersit"].map(weather_mapping)
weather_order = ["Clear", "Mist/Cloudy", "Light Rain/Snow", "Heavy Rain/Snow"]

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    data=weather_rentals, x="weather_label", y="cnt",
    order=weather_order, ax=ax
)
ax.set_title("Average Bike Rentals by Weather Condition", pad=14, fontsize=14)
ax.set_xlabel("Weather Condition")
ax.set_ylabel("Average Rentals")
ax.tick_params(axis="x", rotation=10)
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

if not weather_rentals.empty:
    highest = weather_rentals.loc[weather_rentals["cnt"].idxmax()]
    lowest = weather_rentals.loc[weather_rentals["cnt"].idxmin()]
    st.info(
        f"Insight: rata-rata penyewaan tertinggi terjadi saat {weather_mapping.get(int(highest['weathersit']), highest['weathersit'])}, "
        f"sedangkan terendah saat {weather_mapping.get(int(lowest['weathersit']), lowest['weathersit'])}."
    )
st.divider()

# ==========================================
# TIME GROUP ANALYSIS (ADVANCED)
# ==========================================
st.subheader("⏰ Analisis Penyewaan Berdasarkan Kelompok Waktu")
st.write("Pengelompokan jam untuk membandingkan pola permintaan pada hari kerja dan akhir pekan.")

time_df = apply_filters(hour_df)
def categorize_time(hour):
    if 0 <= hour <= 5:
        return "Early Morning"
    if 6 <= hour <= 10:
        return "Morning"
    if 11 <= hour <= 15:
        return "Midday"
    if 16 <= hour <= 19:
        return "Afternoon"
    return "Evening"

time_df["time_of_day"] = time_df["hr"].apply(categorize_time)
time_df["day_type"] = time_df["weekday"].apply(
    lambda x: "Weekend" if x in [0, 6] else "Weekday"
)
time_group_rentals = (
    time_df.groupby(["time_of_day", "day_type"])["cnt"]
    .mean().reset_index()
)
time_order = ["Early Morning", "Morning", "Midday", "Afternoon", "Evening"]

fig, ax = plt.subplots(figsize=(12, 5))
sns.barplot(
    data=time_group_rentals, x="time_of_day", y="cnt",
    hue="day_type", order=time_order, ax=ax
)
ax.set_title("Average Bike Rentals by Time Group", pad=14, fontsize=14)
ax.set_xlabel("Time Group")
ax.set_ylabel("Average Rentals")
ax.legend(title="Day Type")
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

if not time_group_rentals.empty:
    peak_group = time_group_rentals.loc[time_group_rentals["cnt"].idxmax()]
    st.info(
        f"Insight: kelompok waktu dengan rata-rata penyewaan tertinggi pada data terfilter "
        f"adalah {peak_group['time_of_day']} ({peak_group['day_type']})."
    )

st.divider()
st.caption("Data: Bike Sharing Dataset (2011–2012) | Analisis dan visualisasi untuk proyek Data Analysis.")
