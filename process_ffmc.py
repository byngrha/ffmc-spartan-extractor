import os
import pandas as pd
import geopandas as gpd
import sys
import argparse


def get_category(ffmc:float) -> str:
    if ffmc < 73:
        return 'Aman'
    elif ffmc < 78:
        return 'Tidak Mudah'
    elif ffmc < 82:
        return 'Mudah'
    else:
        return 'Sangat Mudah'


def extract_ffmc(input: str | os.PathLike, province: str, shapefile: str | os.PathLike = "./Kecamatan_Indo.shp"):
    df = pd.read_csv(input)
    desa_gdf = gpd.read_file(shapefile)

    # Filter by the provided province name
    provinsi_desa = desa_gdf[desa_gdf['namaprovin'].str.contains(province, case=False, na=False)]

    if provinsi_desa.empty:
        print(f"Error: No data found for the province '{province}'.")
        sys.exit(1)

    minx, miny, maxx, maxy = provinsi_desa.total_bounds
    filtered_df = df[(df['X'] >= minx) & (df['X'] <= maxx) & (df['Y'] >= miny) & (df['Y'] <= maxy)]

    points_gdf = gpd.GeoDataFrame(
        filtered_df,
        geometry=gpd.points_from_xy(filtered_df['X'], filtered_df['Y']),
        crs="EPSG:4326"
    )

    # Spatial join to attach administrative names
    points_with_desa = gpd.sjoin(points_gdf, provinsi_desa[['namaprovin', 'namakota_k', 'namakecama', 'geometry']],
                                 how="inner", predicate="within")

    # Group by administrative area to calculate max FFMC
    max_ffmc_by_desa = points_with_desa.groupby(['namaprovin', 'namakota_k', 'namakecama'])['EX_FFMC_001'].max().reset_index()

    # Rename columns for clarity
    max_ffmc_by_desa = max_ffmc_by_desa.rename(columns={
        'namaprovin': 'Provinsi',
        'namakota_k': 'Kabupaten/Kota',
        'namakecama': 'Kecamatan',
        'EX_FFMC_001': 'Max FFMC'
    })

    max_ffmc_by_desa['Kategori'] = max_ffmc_by_desa['Max FFMC'].apply(get_category)
    max_ffmc_by_desa['Max FFMC'] = max_ffmc_by_desa['Max FFMC'].round(2)

    # Save to CSV
    filename = os.path.basename(input)
    output_filename = f"./processed_{province.replace(' ', '_').lower()}_{filename}"
    max_ffmc_by_desa.to_csv(output_filename, index=False)

    print(f"Processing complete. Results for '{province}' saved to '{output_filename}'")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract and categorize FFMC data by province.")
    parser.add_argument("--input", type=str,
                        help="Input CSV file containing FFMC data. Download from https://spartan.bmkg.go.id/Download-Data")
    parser.add_argument("--province", type=str, help="Province name to filter the data. E.g. 'BANTEN','JAWA BARAT'")
    parser.add_argument("--shapefile", type=str, default="Kecamatan_Indo.shp",
                        help="Path to the shapefile for administrative boundaries.")

    args = parser.parse_args()

    extract_ffmc(args.input, args.province, args.shapefile)
