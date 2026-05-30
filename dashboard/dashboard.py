import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import matplotlib.patches as mpatches
sns.set(style='whitegrid')

#Membuat fungsi untuk mengolah data
def create_penyewa_bulanan_df(df):
    penyewa_bulanan_df = df.resample(rule='ME', on='dteday').agg({
        "casual": "sum",
        "registered": "sum"
    })
    
    penyewa_bulanan_df = penyewa_bulanan_df.reset_index()
    
    penyewa_bulanan_df['bulan'] = penyewa_bulanan_df['dteday'].dt.month
    penyewa_bulanan_df['tahun'] = penyewa_bulanan_df['dteday'].dt.year

    penyewa_bulanan_df.rename(columns={
        "casual": "penyewa_baru",
        "registered": "penyewa_terdaftar"
    }, inplace=True)
    
    return penyewa_bulanan_df

def create_penyewa_harian_df(df):
    penyewa_harian_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum",
        "casual": "sum",
        "registered": "sum"
    })
    penyewa_harian_df = penyewa_harian_df.reset_index()
    penyewa_harian_df.rename(columns={
        "cnt": "total_penyewa",
        "casual": "penyewa_baru",
        "registered": "penyewa_terdaftar"
    }, inplace=True)
    return penyewa_harian_df

def create_cuaca_terbaik_df(df):
    weather_map = {
        1: 'Cerah',
        2: 'Berawan',
        3: 'Hujan Ringan',
        4: 'Hujan Berat'
        }
    df['kondisi_cuaca'] = df['weathersit'].map(weather_map)

    cuaca_terbaik_df = df.groupby('kondisi_cuaca')['cnt'].mean().sort_values(ascending=False).reset_index()
    cuaca_terbaik_df.rename(columns={
        "cnt": "Rata_rata_penyewa"
    }, inplace=True)
    return cuaca_terbaik_df

def create_rata_harian_penyewa_df(df):
    day_map = {
        0: 'Minggu',
        1: 'Senin',
        2: 'Selasa',
        3: 'Rabu',
        4: 'Kamis',
        5: 'Jumat',
        6: 'Sabtu'
    }
    df['nama_hari'] = df['weekday'].map(day_map)

    rataharian_penyewa_df = df.groupby('nama_hari')['cnt'].mean().reset_index()
    rataharian_penyewa_df.rename(columns={"cnt": "Rata_rata_penyewa"}, inplace=True)

    hari_pemesanan = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    rataharian_penyewa_df['nama_hari'] = pd.Categorical(rataharian_penyewa_df['nama_hari'], categories=hari_pemesanan, ordered=True)
    rataharian_penyewa_df = rataharian_penyewa_df.sort_values('nama_hari')
    return rataharian_penyewa_df

def create_musim_df(df):
    season_map = {
        1: 'Semi', 
        2: 'Panas', 
        3: 'Gugur', 
        4: 'Dingin'
        }
    df['nama_musim'] = df['season'].map(season_map)

    musim_df = df.groupby('nama_musim')['cnt'].mean().reset_index()
    musim_df.rename(columns={"cnt": "Rata_rata_penyewa"}, inplace=True)
    return musim_df

def create_cluster_temperatur_df(df):
    def temp_binning(temp):
        if temp < 0.2: return 'Sangat Dingin'
        elif temp < 0.4: return 'Dingin'
        elif temp < 0.6: return 'Hangat'
        elif temp < 0.8: return 'Panas'
        else: return 'Sangat Panas'

    df['kategori_temperatur'] = df['temp'].apply(temp_binning)

    cluster_temperatur_df = df.groupby('kategori_temperatur')['cnt'].mean().reset_index()
    cluster_temperatur_df.rename(columns={"cnt": "Rata_rata_penyewa"}, inplace=True)

    kondisi_temperatur = ['Sangat Dingin', 'Dingin', 'Hangat', 'Panas', 'Sangat Panas']
    cluster_temperatur_df['kategori_temperatur'] = pd.Categorical(cluster_temperatur_df['kategori_temperatur'], categories = kondisi_temperatur, ordered=True)
    cluster_temperatur_df = cluster_temperatur_df.sort_values('kategori_temperatur')
    return cluster_temperatur_df

#Mengubah file csv menjadi DataFrame
dayall_df = pd.read_csv("day_data.csv")

#Mengatur rentang waktu
dayall_df['dteday'] = pd.to_datetime(dayall_df['dteday'])
dayall_df.sort_values(by="dteday", inplace=True)
dayall_df.reset_index(drop=True, inplace=True)
tanggal_min = dayall_df["dteday"].min()
tanggal_max = dayall_df["dteday"].max()

#Membuat salinan dari DataFrame ke inti dashboard
main_df = dayall_df.copy() 

#Membuat fitur pilihan pada sidebar
with st.sidebar:
    st.image("logo_analisis_data.png")
    st.header("Filter Data")
    
    #fitur tanggal
    st.subheader("📅 Rentang Waktu")
    start_date = st.date_input(
        "Tanggal mulai",
        min_value=tanggal_min,
        max_value=tanggal_max,
        value=tanggal_min
    )

    end_date = st.date_input(
        "Tanggal akhir",
        min_value=tanggal_min,
        max_value=tanggal_max,
        value=tanggal_max
    )

    #fitur musim
    st.subheader("☃️ Musim")
    selected_musim = st.multiselect(
        'Pilih musim',
        options=[1, 2, 3, 4],
        format_func=lambda x: {1: 'Semi', 2: 'Panas', 3: 'Gugur', 4: 'Dingin'}[x],
        default=[1, 2, 3, 4]
    )
    
    #fitur cuaca
    st.subheader("🌤️ Kondisi Cuaca")
    selected_cuaca = st.multiselect(
        'Pilih cuaca',
        options=[1, 2, 3],
        format_func=lambda x: {1: 'Cerah', 2: 'Berawan', 3: 'Hujan Ringan'}[x],
        default=[1, 2, 3]
    )
    
    #fitur hari
    st.subheader("📆 Hari")
    selected_hari = st.multiselect(
        'Pilih hari',
        options=[0, 1, 2, 3, 4, 5, 6],
        format_func=lambda x: ['Minggu','Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'][x],
        default=[0, 1, 2, 3, 4, 5, 6]
    )

#Fitur interaktif
main_df = dayall_df[
    (dayall_df["dteday"] >= pd.to_datetime(start_date)) & 
    (dayall_df["dteday"] <= pd.to_datetime(end_date)) &
    (dayall_df["season"].isin(selected_musim)) &
    (dayall_df["weathersit"].isin(selected_cuaca)) &
    (dayall_df["weekday"].isin(selected_hari))
]
#Tampilan jumlah data
with st.sidebar:
    st.divider()
    st.caption(f"📊 Data tersedia: {len(main_df)} hari")

#Mengubah data hasil filter menjadi ringkasan sesuai fungsi
penyewa_bulanan_df = create_penyewa_bulanan_df(main_df)
penyewa_harian_df = create_penyewa_harian_df(main_df)  # ← pakai main_df
rata_harian_penyewa_df = create_rata_harian_penyewa_df(main_df)  # ← pakai main_df
cuaca_terbaik_df = create_cuaca_terbaik_df(main_df)  # ← pakai main_df
musim_df = create_musim_df(main_df)  # ← pakai main_df
cluster_temperatur_df = create_cluster_temperatur_df(main_df)

#Judul dashboard
st.header('Bike Sharing Dashboard', divider='rainbow')
st.subheader('Analisis Penyewaan Sepeda pada Tahun 2011-2012')

#Analisis jumlah data 
col1, col2, col3, col4 = st.columns(4)
with col1:
    total_sewa = penyewa_harian_df.total_penyewa.sum()
    st.metric("Total Penyewa", value=f"{total_sewa:,}")

with col2:
    ratarata_harian = penyewa_harian_df.total_penyewa.mean()
    st.metric("Rata-rata Harian", value=f"{ratarata_harian:.0f}")

with col3:
    total_casual = penyewa_harian_df.penyewa_baru.sum()
    st.metric("Total Pengguna Casual", value=f"{total_casual:,}")

with col4:
    total_registered = penyewa_harian_df.penyewa_terdaftar.sum()
    st.metric("Total Pengguna User", value=f"{total_registered:,}")

#visualisasi tren pengguna casual dan registered
st.subheader('Tren Pengguna Casual dan Registered per Bulan', divider='gray')
fig, ax = plt.subplots(figsize=(14, 6))
df_plot = penyewa_bulanan_df.copy()
df_plot['bulan_tahun'] = df_plot['dteday'].dt.strftime('%b %Y')
#grafik casual
ax.plot(
    df_plot["bulan_tahun"],
    df_plot["penyewa_baru"],
    marker='o',
    label='Casual User',
    color="#1E8B84",
    linewidth=2
)
#grafik registered
ax.plot(
    df_plot["bulan_tahun"],
    df_plot["penyewa_terdaftar"],
    marker='o',
    label='Registered User',
    color="#72036C",
    linewidth=2
)
ax.set_title("Tren Penyewaan Sepeda per Bulan", fontsize=16)
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewa")
ax.legend()
ax.grid(alpha=0.3)
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

#visualisasi penyewa berdasarkan rata-rata harian
st.subheader('Rata-Rata Penyewaan Berdasarkan Hari', divider='gray')
fig, ax = plt.subplots(figsize=(12, 6))
df_plot = rata_harian_penyewa_df.copy()
#cari hari dengan penyewa tertinggi
max_hari = df_plot.loc[df_plot['Rata_rata_penyewa'].idxmax(), 'nama_hari']
colors = [
    "#FF6B6B" if hari == max_hari else "#D3D3D3"
    for hari in df_plot['nama_hari']
]
sns.barplot(
    x="nama_hari",
    y="Rata_rata_penyewa",
    data=df_plot,
    palette=colors,
    order=df_plot['nama_hari'], 
    ax=ax
)
for p in ax.patches:
    ax.annotate(
        f'{p.get_height():,.0f}',
        (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center',
        va='bottom',
        fontsize=9
    )
ax.set_title("Rata-rata Penyewa per Hari", fontsize=14)
ax.set_ylabel("Rata-rata Penyewa")
ax.set_xlabel(None)
merah = mpatches.Patch(color='#FF6B6B', label='Tertinggi')
abu = mpatches.Patch(color='#D3D3D3', label='Lainnya')
ax.legend(
    handles=[merah, abu],
    loc='upper right'
)
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

#visualisasi rata-rata penyewa berdasarkan cuaca dan musim
st.subheader('Rata-Rata Penyewaan Berdasarkan Cuaca dan Musim', divider='gray')
column1, column2 = st.columns(2)
#berdasarkan cuaca (kolom 1)
with column1:
    fig, ax = plt.subplots(figsize=(10, 6))
    df_plot = cuaca_terbaik_df.copy()
    max_cuaca = df_plot.loc[df_plot['Rata_rata_penyewa'].idxmax(), 'kondisi_cuaca']
    colors = [
        "#FF6B6B" if cuaca == max_cuaca else "#D3D3D3"
        for cuaca in df_plot['kondisi_cuaca']
    ]
    sns.barplot(
        x="kondisi_cuaca",
        y="Rata_rata_penyewa",
        data=df_plot,
        palette=colors,
        order=df_plot['kondisi_cuaca'],
        ax=ax
    )
    for p in ax.patches:
        ax.annotate(
            f'{p.get_height():,.0f}',
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha='center',
            va='bottom',
            fontsize=9
        )
    ax.set_title("Rata-rata Penyewa Berdasarkan Cuaca", fontsize=14)
    ax.set_ylabel("Rata-rata Penyewa")
    ax.set_xlabel(None)
    merah = mpatches.Patch(color='#FF6B6B', label='Tertinggi')
    abu = mpatches.Patch(color='#D3D3D3', label='Lainnya')
    ax.legend(
        handles=[merah, abu],
        loc='upper right'
    )
    ax.tick_params(axis='x', labelsize=11, rotation=15)
    st.pyplot(fig)
#berdasarkan musim (kolom 2)
with column2:
    fig, ax = plt.subplots(figsize=(10, 6))
    df_plot = musim_df.sort_values('Rata_rata_penyewa', ascending=False).reset_index(drop=True)
    max_musim = df_plot.loc[df_plot['Rata_rata_penyewa'].idxmax(), 'nama_musim']
    colors = [
        "#FF6B6B" if musim == max_musim else "#D3D3D3"
        for musim in df_plot['nama_musim']
    ]
    sns.barplot(
        x="nama_musim",
        y="Rata_rata_penyewa",
        data=df_plot,
        palette=colors,
        order=df_plot['nama_musim'],
        ax=ax
    )
    for p in ax.patches:
        ax.annotate(
            f'{p.get_height():,.0f}',
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha='center',
            va='bottom',
            fontsize=9
        )
    ax.set_title("Rata-rata Penyewa Berdasarkan Musim", fontsize=14)
    ax.set_ylabel("Rata-rata Penyewa")
    ax.set_xlabel(None)
    merah = mpatches.Patch(color='#FF6B6B', label='Tertinggi')
    abu = mpatches.Patch(color='#D3D3D3', label='Lainnya')
    ax.legend(
        handles=[merah, abu],
        loc='upper right'
    )
    ax.tick_params(axis='x', labelsize=11, rotation=15)
    st.pyplot(fig)
    

#visualisasi binning temperature
st.subheader('Rata-Rata Penyewa Berdasarkan Temperatur', divider='gray')
fig, ax = plt.subplots(figsize=(10, 6))
df_plot = cluster_temperatur_df.copy()
max_kategori = df_plot.loc[
    df_plot['Rata_rata_penyewa'].idxmax(),
    'kategori_temperatur'
]
colors = [
    "#FF6B6B" if kategori == max_kategori else "#D3D3D3"
    for kategori in df_plot['kategori_temperatur']
]
sns.barplot(
    x="kategori_temperatur",
    y="Rata_rata_penyewa",
    data=df_plot,
    palette=colors,
    order=df_plot['kategori_temperatur'],
    ax=ax
)
for p in ax.patches:
    ax.annotate(
        f'{p.get_height():,.0f}',
        (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center',
        va='bottom',
        fontsize=9
    )
ax.set_title("Rata-rata Penyewa Berdasarkan Kategori Temperatur", fontsize=14)
ax.set_xlabel("Kategori Temperatur")
ax.set_ylabel("Rata-rata Penyewa")
merah = mpatches.Patch(color='#FF6B6B', label='Tertinggi')
abu = mpatches.Patch(color='#D3D3D3', label='Lainnya')
ax.legend(
    handles=[merah, abu],
    loc='upper right'
)
ax.tick_params(axis='x', rotation=15)
st.pyplot(fig)

#Membuat kesimpulan keseluruhan analisis
st.markdown("""
<div style="
    background-color:#f0f2f6;
    padding:15px;
    border-radius:10px;
    border-left:5px solid #FF6B6B;
">
<b>📊 Insight:</b><br><br>
<ul>
Berdasarkan analisis keseluruhan dataset dari tahun 2011-2012, diperoleh kesimpulan:
<li> Jumlah penyewa terbanyak terdapat pada pengguna registered (terdaftar).
<li> Jumlah penyewa mengalami puncak penyewaan pada bulan Mei-September.
<li> Rata-rata pengguna lebih sering menyewa pada hari kerja, dari pada hari weekend (sabtu-minggu).
<li> Jumlah penyewa tertinggi terjadi pada saat kondisi temperatur Hangat-Panas.
<li> Jumlah penyewa menurun pada saat kondisi ekstrem (terlalu dingin / terlalu panas).
</ul>
</div>
""", unsafe_allow_html=True)

#Membuat caption dashboard
st.caption('Copyright © Angelika Revalina Rismawati | Proyek Analisis Data')