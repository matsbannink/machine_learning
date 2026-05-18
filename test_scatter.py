# Test the theoretical scattering vs the actual scattering
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

theoretical_path = "Spectral_library_theoretical_scattering.xlsx"
df_theoretical = pd.read_excel(theoretical_path)

real_path = "Spectral_library_with_scattering.xlsx"
df_real = pd.read_excel(real_path)

real_wo_scat_path = "Spectral_library_clean_normalized.xlsx"
df_real_wo_scat = pd.read_excel(real_wo_scat_path)

wavelength_col = "Wavelength"
spectrum_col = "Cyanobacteria_Synechosystis"

# mask for wavelengths < 400 nm
mask_1 = df_theoretical[wavelength_col] < 400
mask_2 = df_theoretical[wavelength_col] > 750
# set all spectrum columns to NaN where mask is True
df_theoretical.loc[mask_1, spectrum_col] = np.nan
df_theoretical.loc[mask_2, spectrum_col] = np.nan
df_theoretical[spectrum_col] = (df_theoretical[spectrum_col] - df_theoretical[spectrum_col].mean()) / df_theoretical[spectrum_col].std()

df_real.loc[mask_2, spectrum_col] = np.nan
df_real[spectrum_col] = df_real[spectrum_col].replace(0, np.nan)
df_real_wo_scat.loc[mask_2, spectrum_col] = np.nan
df_real_wo_scat[spectrum_col] = df_real_wo_scat[spectrum_col].replace(0, np.nan)


real_wavelengths = df_real[wavelength_col].values
real_spectrum = df_real[spectrum_col].values

theoretical_wavelengths = df_theoretical[wavelength_col].values
theoretical_scattering = df_theoretical[spectrum_col].values

real_wo_scat_wavelengths = df_real_wo_scat[wavelength_col].values
real_wo_scat_spectrum = df_real_wo_scat[spectrum_col].values


plt.figure(figsize=(8, 5))
plt.plot(real_wavelengths, real_spectrum, label="Real with model scattering", alpha=0.8)
plt.plot(theoretical_wavelengths, theoretical_scattering, label="Theoretical scattering data Volha", alpha=0.8)
plt.plot(real_wo_scat_wavelengths, real_wo_scat_spectrum, label="Real without scatter", alpha=0.8)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Absorption (normalized)")
plt.title("Scattering: theoretical vs real")
plt.legend(fontsize=7)
plt.tight_layout()
plt.show()