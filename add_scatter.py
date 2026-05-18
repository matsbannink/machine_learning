import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

k = 0.5

def scattering_spectrum(wavelengths_nm, k=4.0,
                        lambda_ref=350.0, scatter_at_ref=0.2):
    """
    wavelengths_nm : array of wavelengths in nm
    k              : exponent in I = C * lambda^(-k)
    lambda_ref     : reference wavelength (nm) where you set the scale
    scatter_at_ref : desired scattering intensity at lambda_ref

    Returns:
        scattering array with same length as wavelengths_nm
    """
    lam = wavelengths_nm.astype(float)

    # Compute C so that I(lambda_ref) = scatter_at_ref
    C = scatter_at_ref * (lambda_ref ** k)

    I = C * lam**(-k)
    return I


path = "Spectral_library_clean_normalized.xlsx"
df_norm= pd.read_excel(path)

wavelength_col = "Wavelength"
species_cols = [c for c in df_norm.columns if c != wavelength_col]
wavelengths = df_norm[wavelength_col].values.astype(float) 

scattering = scattering_spectrum(wavelengths, k=k, lambda_ref=350.0, scatter_at_ref=0.2)
print("Scattering spectrum", scattering)

df_scat = df_norm.copy()
for col in species_cols:
    mask_valid = df_scat[col].notna() & (df_scat[col] != 0)

    extinction = df_scat[col].copy()

    # Add scattering only where we have a real measurement
    extinction.loc[mask_valid] = df_scat[col].loc[mask_valid] + scattering[mask_valid]

    df_scat[col] = extinction


df_scat.to_excel("Spectral_library_with_scattering.xlsx", index=False)