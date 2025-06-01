import geopandas as gpd
from geopy.geocoders import Nominatim
from time import sleep
import random

# === 1. BACA SHAPEFILE ===
print(" Membaca shapefile...")
gdf = gpd.read_file("kulinerponoogo_V1/kulinerponoogo_V1.shp")

# === 2. REVERSE GEOCODING ===
print(" Memulai reverse geocoding...")
geolocator = Nominatim(user_agent="geoapi")

alamat_list = []
jalan_list = []
no_list = []
desa_list = []
kecamatan_list = []
kabupaten_list = []

for i, row in gdf.iterrows():
    try:
        location = geolocator.reverse((row.geometry.y, row.geometry.x), language='id', addressdetails=True)
        if location and "address" in location.raw:
            address = location.raw["address"]
            jalan = address.get("road", "")
            nomor = address.get("house_number", "")
            if not nomor:
                nomor = "-"
            desa = address.get("village", "") or address.get("suburb", "")
            kecamatan = address.get("county", "")
            kabupaten = address.get("state_district", "") or address.get("state", "")

            full_alamat = f"Jl. {jalan} No. {nomor}, {desa}, {kecamatan}, {kabupaten}"
        else:
            full_alamat = "Alamat tidak ditemukan"
            jalan, nomor, desa, kecamatan, kabupaten = "", "-", "", "", ""

    except Exception as e:
        print(f"❌ Error pada index {i}: {e}")
        full_alamat = "Error"
        jalan, nomor, desa, kecamatan, kabupaten = "", "-", "", "", ""

    print(f"✅ {i+1}/{len(gdf)}: {full_alamat}")
    alamat_list.append(full_alamat)
    jalan_list.append(jalan)
    no_list.append(nomor)
    desa_list.append(desa)
    kecamatan_list.append(kecamatan)
    kabupaten_list.append(kabupaten)

    sleep(1)  # Hindari over-limit ke Nominatim

# Tambahkan hasil geocoding ke GeoDataFrame
gdf["Alamat_Lengkap"] = alamat_list
gdf["Jalan"] = jalan_list
gdf["No"] = no_list
gdf["Desa"] = desa_list
gdf["Kecamatan"] = kecamatan_list
gdf["Kabupaten"] = kabupaten_list

# === 3. TAMBAH RATING DUMMY ===
print(" Menambahkan rating dummy...")
gdf["Rating"] = [round(random.uniform(4.5, 5.0), 1) for _ in range(len(gdf))]

# === 4. SIMPAN HASIL ===
print(" Menyimpan output ke shapefile dan CSV...")
gdf.to_file("kulinerponoogo.shp", encoding='utf-8')
gdf.to_csv("kulinerponoogo.csv", index=False)

print(" Selesai! File disimpan sebagai:")
print("- kulinerponoogo_with_alamat_rating.shp")
print("- kulinerponoogo_with_alamat_rating.csv")
