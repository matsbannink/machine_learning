import numpy as np
import pandas as pd

path = "Spectral_library.xlsx"
df_raw = pd.read_excel(path)

# Convert object columns (they contain numeric strings) to numeric
object_cols = [
    "Dinoflagellate_Symbiodiniumsp",
    "Dinoflagellate_Smicroadriaticum",
    "Dinoflagelalte_Dtrenchii",
    "Dinoflagellate_Cgoreaui",
]
for col in object_cols:
    if col in df_raw.columns:
        df_raw[col] = pd.to_numeric(df_raw[col], errors="coerce")


species_wavelength_map = {
    "Diatom_Ptricornutum":              "Wavelength",
    "Diatom_Csimplex":                  "Wavelength.1",
    "Chlamydomonas_Cpriscuii":          "Wavelengtj",
    "Chlamydomonas_Creindhardtii":      "Wavelengtj",
    "Dinoflagellate_Symbiodiniumsp":    "Wavelength.2",
    "Dinoflagellate_Smicroadriaticum":  "Wavelength.2",
    "Dinoflagellate_Dtrenchii":         "Wavelength.2",
    "Dinoflagellate_Cgoreaui":          "Wavelength.2",
    "Cyanobacteria_Synechosystis":      "Wavelength.3",
}


wl_master = np.arange(800.0, 349.0, -1.0)

df_clean = pd.DataFrame({"Wavelength": wl_master})
print(df_clean.head())


for species, wl_col in species_wavelength_map.items():
    if species not in df_raw.columns or wl_col not in df_raw.columns:
        print(f"Warning: missing column(s) for {species} / {wl_col}, skipping.")
        continue

    # Only keep rows where both wavelength and species value are present
    mask = df_raw[wl_col].notna() & df_raw[species].notna()
    wl = df_raw.loc[mask, wl_col].values
    vals = df_raw.loc[mask, species].values

    if len(wl) == 0:
        print(f"Warning: no valid data for {species}, skipping.")
        continue

    # Sort by wavelength just in case
    order = np.argsort(wl)
    wl = wl[order]
    vals = vals[order]

    # Create a Series with wavelength as index
    s = pd.Series(vals, index=wl)

    # Reindex onto the master wavelength grid
    # -> wavelengths not present become NaN
    s_aligned = s.reindex(wl_master)

    df_clean[species] = s_aligned.values


output_path = "Spectral_library_clean.xlsx"
df_clean.to_excel(output_path, index=False)

print("Cleaned spectral library saved to:", output_path)
print("Preview (top rows):")
print(df_clean.head())
print("Preview (bottom rows):")
print(df_clean.tail())