import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

path = "Spectral_library_clean.xlsx"
df_clean = pd.read_excel(path)

# Normalize each spectrum column (except wavelength) to have mean=0 and std=1
df_norm = df_clean.copy()
spectrum_cols = [c for c in df_clean.columns if c != "Wavelength"]
for col in spectrum_cols:
    df_norm[col] = (df_clean[col] - df_clean[col].mean()) / df_clean[col].std()

df_for_mix = df_norm.fillna(0)

df_for_mix.to_excel("Spectral_library_clean_normalized.xlsx", index=False)

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

    # To store composition (weights) for each mixture column
    weights_records = []

    new_mixtures_dict = {}

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

                new_mixtures_dict[mix_col_name] = mix_spectrum

                # Store the weights and which species were used
                record = {"mixture_name": mix_col_name}
                for col, w in zip(comb, weights):
                    record[col] = w
                weights_records.append(record)

    new_mixtures_df = pd.DataFrame(new_mixtures_dict)
    mixtures_df = pd.concat([df, new_mixtures_df], axis=1)

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

# Not using scattering
output_spectra_path = "Spectral_library_with_mixtures.xlsx"
output_weights_path = "Spectral_library_mixture_weights.xlsx"

mixtures_df.to_excel(output_spectra_path, index=False)
weights_df.to_excel(output_weights_path, index=False)

print("Mixture spectra saved to:", output_spectra_path)
print("Mixture weights saved to:", output_weights_path)

wavelength_col = "Wavelength"
wavelengths = df_norm[wavelength_col].values

plt.figure(figsize=(8, 5))

for col in spectrum_cols:
    plt.plot(wavelengths, df_norm[col].values, label=col, alpha=0.8)

plt.xlabel("Wavelength (nm)")
plt.ylabel("Absorption (normalized)")
plt.title("Pure (one-component) spectra without scattering")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig("pure_spectra_without_scattering.png")


# Using scattering
df_for_mix_scat = pd.read_excel("Spectral_library_with_scattering.xlsx")
df_for_mix_scat[spectrum_cols] = df_for_mix_scat[spectrum_cols].replace(0, np.nan)
combination_sizes = (2, 3)      
n_mixtures_per_combination = 5

mixtures_df, weights_df = generate_mixture_spectra(
    df_for_mix_scat,
    wavelength_col="Wavelength",
    combination_sizes=combination_sizes,
    n_mixtures_per_combination=n_mixtures_per_combination,
    random_state=42
)

output_spectra_path = "Spectral_library_with_mixtures_scat.xlsx"
output_weights_path = "Spectral_library_mixture_weights_scat.xlsx"

mixtures_df.to_excel(output_spectra_path, index=False)
weights_df.to_excel(output_weights_path, index=False)

print("Mixture spectra saved to:", output_spectra_path)
print("Mixture weights saved to:", output_weights_path)

wavelength_col = "Wavelength"
wavelengths = df_for_mix_scat[wavelength_col].values

plt.figure(figsize=(8, 5))

for col in spectrum_cols:
    plt.plot(wavelengths, df_for_mix_scat[col].values, label=col, alpha=0.8)

plt.xlabel("Wavelength (nm)")
plt.ylabel("Absorption (normalized)")
plt.title("Pure (one-component) spectra with scattering")
plt.legend(fontsize=7)
plt.tight_layout()
plt.savefig("pure_spectra_with_scattering.png")