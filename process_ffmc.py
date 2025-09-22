# process_ffmc.py
import pandas as pd
import geopandas as gpd
import sys

# Get the filename and province name from command-line arguments
if len(sys.argv) < 3:
    print("Error: Please provide both the CSV filename and the province name.")
    print("Usage: python3 process_ffmc.py <csv_filename> <province_name>")
    sys.exit(1)

csv_filename = sys.argv[1]
province_name = sys.argv[2]

# Path to SHP
shp_path = "Kecamatan_Indo.shp"

try:
    df = pd.read_csv(csv_filename)
    desa_gdf = gpd.read_file(shp_path)

    # Filter by the provided province name
    provinsi_desa = desa_gdf[desa_gdf['namaprovin'].str.contains(province_name, case=False, na=False)]
    
    # Check if any data for the province was found
    if provinsi_desa.empty:
        print(f"Error: No data found for the province '{province_name}'.")
        sys.exit(1)

    # Filter the DataFrame based on the province's bounding box
    minx, miny, maxx, maxy = provinsi_desa.total_bounds
    filtered_df = df[(df['X'] >= minx) & (df['X'] <= maxx) & (df['Y'] >= miny) & (df['Y'] <= maxy)]

    # Convert filtered points to GeoDataFrame
    points_gdf = gpd.GeoDataFrame(
        filtered_df,
        geometry=gpd.points_from_xy(filtered_df['X'], filtered_df['Y']),
        crs="EPSG:4326"
    )

    # Spatial join to attach administrative names
    points_with_desa = gpd.sjoin(points_gdf, provinsi_desa[['namaprovin', 'namakota_k', 'namakecama', 'geometry']], how="inner", predicate="within")

    # Group by administrative area to calculate max FFMC
    max_ffmc_by_desa = points_with_desa.groupby(['namaprovin', 'namakota_k', 'namakecama'])['EXTRACT_FFMC_1'].max().reset_index()

    # Rename columns for clarity
    max_ffmc_by_desa = max_ffmc_by_desa.rename(columns={
        'namaprovin': 'Provinsi',
        'namakota_k': 'Kabupaten/Kota',
        'namakecama': 'Kecamatan',
        'EXTRACT_FFMC_1': 'Max FFMC'
    })

    # Add Category based on FFMC value
    def get_category(ffmc):
        if ffmc < 73:
            return 'Sangat Mudah'
        elif ffmc < 78:
            return 'Mudah'
        elif ffmc < 82:
            return 'Cukup Sulit'
        else:
            return 'Sulit'

    max_ffmc_by_desa['Kategori'] = max_ffmc_by_desa['Max FFMC'].apply(get_category)

    # Save to CSV
    output_filename = f"processed_{province_name.replace(' ', '_').lower()}_{csv_filename}"
    max_ffmc_by_desa.to_csv(output_filename, index=False)

    print(f"Processing complete. Results for '{province_name}' saved to '{output_filename}'")
    
except FileNotFoundError as e:
    print(f"Error: A required file was not found: {e}")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit(1)