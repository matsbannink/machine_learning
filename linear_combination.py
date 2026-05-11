import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

path = "Spectral_library_clean.xlsx"
df_clean = pd.read_excel(path)

# Keep a version with NaNs as the "truth"
df_truth = df_clean.copy()

# For building linear combinations, we usually set NaN -> 0
df_for_mix = df_clean.fillna(0)

# Confirm structure
print("Columns:", df_for_mix.columns.tolist())
print(df_for_mix.head())

def generate_mixture_spectra(
    df,
    wavelength_col="Wavelength",
    combination_sizes=(2, 3),
    n_mixtures_per_combination=5,
    random_state=42
):
    """
    df: DataFrame with one wavelength column and one column per pure spectrum.
        Example columns: ['Wavelength', 'Diatom_Ptricornutum', ...]
    wavelength_col: name of the wavelength column.
    combination_sizes: tuple with sizes of combinations (e.g. (1, 2, 3, 4)).
        - 1 means single-species "mixtures" (i.e. just that pure spectrum again).
    n_mixtures_per_combination: number of random weightings per given combination.
    random_state: seed for reproducibility.

    Returns:
        mixtures_df: DataFrame with:
            - the wavelength column
            - one column per pure spectrum (copied from df)
            - additional columns for artificial mixtures
        weights_df: DataFrame that stores the weights used for each mixture column
            (so you know the exact composition).
    """
    rng = np.random.default_rng(random_state)

    # All species columns
    spectrum_cols = [c for c in df.columns if c != wavelength_col]

    # Start with a copy so we keep the pure spectra
    mixtures_df = df.copy()

    # To store composition (weights) for each mixture column
    weights_records = []

    for k in combination_sizes:
        # All k-element combinations of the spectrum columns
        for comb in itertools.combinations(spectrum_cols, k):
            comb_name_base = "_".join(comb)

            for m in range(n_mixtures_per_combination):
                # Random non-negative weights that sum to 1
                weights = rng.dirichlet(np.ones(k))

                # Linear combination: mix = sum_i w_i * spectrum_i
                mix_spectrum = np.zeros(len(df))
                for col, w in zip(comb, weights):
                    mix_spectrum += w * df[col].values

                # Unique column name for this mixture
                mix_col_name = f"mix{k}_{comb_name_base}_{m}"
                mixtures_df[mix_col_name] = mix_spectrum

                # Store the weights and which species were used
                record = {"mixture_name": mix_col_name}
                for col, w in zip(comb, weights):
                    record[col] = w
                weights_records.append(record)

    weights_df = pd.DataFrame(weights_records).fillna(0.0)

    return mixtures_df, weights_df


combination_sizes = (2, 3)      
n_mixtures_per_combination = 5

mixtures_df, weights_df = generate_mixture_spectra(
    df_for_mix,
    wavelength_col="Wavelength",
    combination_sizes=combination_sizes,
    n_mixtures_per_combination=n_mixtures_per_combination,
    random_state=42
)


output_spectra_path = "Spectral_library_with_mixtures.xlsx"
output_weights_path = "Spectral_library_mixture_weights.xlsx"

mixtures_df.to_excel(output_spectra_path, index=False)
weights_df.to_excel(output_weights_path, index=False)

print("Mixture spectra saved to:", output_spectra_path)
print("Mixture weights saved to:", output_weights_path)
print("Spectra columns example:", mixtures_df.columns[:15])
print("Weights head:")
print(weights_df.head())


# Change this to your local path if needed
file_path = "Spectral_library_clean.xlsx"
df_clean = pd.read_excel(file_path)

# Replace NaNs with 0 for mixing
df_mix = df_clean.fillna(0).copy()

wavelengths = df_mix["Wavelength"].values
species_cols = [c for c in df_mix.columns if c != "Wavelength"]

rng = np.random.default_rng(42)

# Choose some species to demonstrate (first 3 columns)
chosen_species = species_cols[:3]

# 2-species mixture (first two chosen species)
species2 = chosen_species[:2]
weights2 = rng.dirichlet(np.ones(2))
mix2 = weights2[0] * df_mix[species2[0]].values + \
       weights2[1] * df_mix[species2[1]].values

# 3-species mixture (first three chosen species)
species3 = chosen_species[:3]
weights3 = rng.dirichlet(np.ones(3))
mix3 = (weights3[0] * df_mix[species3[0]].values +
        weights3[1] * df_mix[species3[1]].values +
        weights3[2] * df_mix[species3[2]].values)

print("2-species mixture weights:")
for s, w in zip(species2, weights2):
    print(f"  {s}: {w:.3f}")

print("\n3-species mixture weights:")
for s, w in zip(species3, weights3):
    print(f"  {s}: {w:.3f}")


plt.figure(figsize=(8, 5))

# Pure spectra
for col in chosen_species:
    plt.plot(wavelengths, df_mix[col].values, label=f"Pure {col}", alpha=0.7)

# Mixtures
plt.plot(
    wavelengths, mix2,
    label=f"Mix2 {species2}",
    linewidth=2.5
)
plt.plot(
    wavelengths, mix3,
    label=f"Mix3 {species3}",
    linewidth=2.5,
    linestyle="--"
)

# Wavelengths from 800 -> 350 nm
plt.gca().invert_xaxis()

plt.xlabel("Wavelength (nm)")
plt.ylabel("Coefficient")
plt.title("Example pure spectra and linear combinations")
plt.legend(fontsize=7)
plt.tight_layout()

plt.show()

chosen_species = [
    "Diatom_Ptricornutum",
    "Diatom_Csimplex",
    "Cyanobacteria_Synechosystis",
]