import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


sns.set(style='dark')

df_day = pd.read_csv("/dashboard/day.csv")
df_day.head()


drop_col = ['windspeed']

for i in df_day.columns:
    if i in drop_col:
        df_day.drop(labels=i, axis=1, inplace=True)


df_day.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)


df_day['month'] = df_day['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
df_day['season'] = df_day['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
df_day['weekday'] = df_day['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
df_day['weather_cond'] = df_day['weather_cond'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})


# Membuat dataframe penyewa sepeda harian (General)
def create_df_daily_rent(df):
    df_daily_rent = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return df_daily_rent


# Membuat dataframe penyewa sepeda harian kategori casual
def create_df_daily_casual_rent(df):
    df_daily_casual_rent = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return df_daily_casual_rent


# Membuat dataframe penyewa sepeda harian kategori registered
def create_df_daily_registered_rent(df):
    df_daily_registered_rent = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return df_daily_registered_rent

# Menyiapkan df_season_rent


def create_df_season_rent(df):
    df_season_rent = df.groupby(by='season')[
        ['registered', 'casual']].sum().reset_index()
    return df_season_rent

# Menyiapkan df_monthly_rent


def create_df_monthly_rent(df):
    df_monthly_rent = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    df_monthly_rent = df_monthly_rent.reindex(ordered_months, fill_value=0)
    return df_monthly_rent


# Dataframe sewa sepeda pada weekday
def create_df_weekday_rent(df):
    df_weekday_rent = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return df_weekday_rent


# Dataframe sewa sepeda pada workingday
def create_df_workingday_rent(df):
    df_workingday_rent = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return df_workingday_rent


# Dataframe sewa sepeda pada hari libur
def create_df_holiday_rent(df):
    df_holiday_rent = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return df_holiday_rent


# Dataframe penyewaan sepeda berdasarkan kondisi cuaca
def create_df_weather_rent(df):
    df_weather_rent = df.groupby(by='weather_cond').agg({
        'count': 'sum'
    })
    return df_weather_rent


# Membuat komponen filter
min_date = pd.to_datetime(df_day['dateday']).dt.date.min()
max_date = pd.to_datetime(df_day['dateday']).dt.date.max()

with st.sidebar:
    st.header('Syahrial Rizky | Proyek Analisis Data')

    # Rentang waktu data set
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df_day[(df_day['dateday'] >= str(start_date)) &
                 (df_day['dateday'] <= str(end_date))]

# Menyiapkan berbagai dataframe
df_daily_rent = create_df_daily_rent(main_df)
df_daily_casual_rent = create_df_daily_casual_rent(main_df)
df_daily_registered_rent = create_df_daily_registered_rent(main_df)
df_season_rent = create_df_season_rent(main_df)
df_monthly_rent = create_df_monthly_rent(main_df)
df_weekday_rent = create_df_weekday_rent(main_df)
df_workingday_rent = create_df_workingday_rent(main_df)
df_holiday_rent = create_df_holiday_rent(main_df)
df_weather_rent = create_df_weather_rent(main_df)


# Membuat Dashboard secara lengkap


st.header('Bike Sharing Streamlit Dashboard 🚲')


st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = df_daily_casual_rent['casual'].sum()
    st.metric('Casual User', value=daily_rent_casual)

with col2:
    daily_rent_registered = df_daily_registered_rent['registered'].sum()
    st.metric('Registered User', value=daily_rent_registered)

with col3:
    daily_rent_total = df_daily_rent['count'].sum()
    st.metric('Total User', value=daily_rent_total)

# Plotting penyewaan dalam bulan
st.subheader('Ploting rental berdasarkan bulan')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    df_monthly_rent.index,
    df_monthly_rent['count'],
    marker='o',
    linewidth=2,
    color='tab:blue'
)

for index, row in enumerate(df_monthly_rent['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

# Plotting penyewaan berdasarkan musim (season)
st.subheader('Plotting Rental berdasarkan musim')

fig, ax = plt.subplots(figsize=(16, 8))


df_melt = df_season_rent.melt(id_vars='season', value_vars=['registered', 'casual'],
                              var_name='Category', value_name='Count')


sns.barplot(
    x='season',
    y='Count',
    hue='Category',
    data=df_melt,
    palette=['tab:blue', 'tab:orange'],
    ax=ax
)


for index, row in df_season_rent.iterrows():
    ax.text(index - 0.2, row['registered'], str(row['registered']),
            ha='center', va='bottom', fontsize=12, color='tab:blue')
    ax.text(index + 0.2, row['casual'], str(row['casual']),
            ha='center', va='bottom', fontsize=12, color='tab:orange')

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend(title='Category')
st.pyplot(fig)


# Plotting penyewaan berdasarkan kondisi cuaca
st.subheader('Plotting Penyewa Sepeda berdasarkan Kondisi Cuaca')
fig, ax = plt.subplots(figsize=(16, 8))

sns.lineplot(
    x=df_weather_rent.index,
    y=df_weather_rent['count'],
    ax=ax
)

ax.set_title('Plotting Penyewa Sepeda berdasarkan Kondisi Cuaca', fontsize=16)
ax.set_xlabel('Kondisi Cuaca', fontsize=14)
ax.set_ylabel('Jumlah Pengguna Sepeda', fontsize=14)
ax.tick_params(axis='x', rotation=45)
ax.grid(True)

st.pyplot(fig)


st.subheader('Penyewaan berdasarkan Working day, Holiday, Weekday ')
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15, 10))


# Plotting Working Day
st.subheader('Penyewaan berdasarkan Working Day (Hari Kerja)')
fig1, ax1 = plt.subplots(figsize=(10, 5))

colors1 = ["tab:blue", "tab:orange"]

sns.barplot(
    x='workingday',
    y='count',
    data=df_workingday_rent,
    palette=colors1,
    ax=ax1)

for index, row in enumerate(df_workingday_rent['count']):
    ax1.text(index, row + 1, str(row),
             ha='center', va='bottom', fontsize=12)

ax1.set_title('Penyewaan berdasarkan Working Day')
ax1.set_ylabel(None)
ax1.tick_params(axis='x', labelsize=15)
ax1.tick_params(axis='y', labelsize=10)

st.pyplot(fig1)

# Plotting Holiday
st.subheader('Penyewaan berdasarkan Holiday (Hari Libur)')
fig2, ax2 = plt.subplots(figsize=(10, 5))

colors2 = ["tab:blue", "tab:orange"]

sns.barplot(
    y='count',
    data=df_holiday_rent,
    palette=colors2,
    ax=ax2)

for index, row in enumerate(df_holiday_rent['count']):
    ax2.text(index, row + 1, str(row),
             ha='center', va='bottom', fontsize=12)

ax2.set_title('Penyewaan berdasarkan Holiday')
ax2.set_ylabel(None)
ax2.tick_params(axis='x', labelsize=15)
ax2.tick_params(axis='y', labelsize=10)

st.pyplot(fig2)

# Plotting Weekday
st.subheader('Penyewaan berdasarkan Weekday (Hari dalam seminggu)')
fig3, ax3 = plt.subplots(figsize=(10, 5))

colors3 = ["tab:blue", "tab:orange", "tab:green",
           "tab:red", "tab:purple", "tab:brown", "tab:pink"]

sns.barplot(
    x='weekday',
    y='count',
    data=df_weekday_rent,
    palette=colors3,
    ax=ax3)

for index, row in enumerate(df_weekday_rent['count']):
    ax3.text(index, row + 1, str(row),
             ha='center', va='bottom', fontsize=12)

ax3.set_title('Penyewaan berdasarkan Weekday')
ax3.set_ylabel(None)
ax3.tick_params(axis='x', labelsize=15)
ax3.tick_params(axis='y', labelsize=10)

st.pyplot(fig3)


st.caption('Copyright (c) Syahrial Rizky Bangkit - Dicoding Academy 2024')
