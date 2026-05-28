This contains the project work for the project named: "Spectral Fingerprinting: Machine Learning for Identification of Freshwater Phototrophs"
for the Machine Learning for Physics & Astronomy course at Universiteit van Amsterdam (UvA)

The aim of this project is to use machine learning to find concentrations of photosynthetic microorganisms from the absorption spectra of water samples. This is useful for quickly assessing the water quality. In this project we used a couple of methods, namely an NNLS and an MLP to unmix model spectra and find the concentrations of the phototrophs.

Authors: Jochem Amesz, Mats Bannink, Dani Berndsen and Nuri Hitzelberger 
Contact: mats.bannink@student.uva.nl

Supervisors: Volha Chukhutsina (Vrije Universiteit Amsterdam) and Joy Sanghavi (UvA)

data/spectral_library_clean.xlsx
This excel contains all the pure absorption spectra of the photosynthetic microorganisms.

data/spectral_library_scattering_cyanobacteria.xlsx
This excel contains the scattered spectrum of Cyanobacteria Synechosystis

data/spectral_library_scattering_diatomp_same_sample.xlsx
This excel contains the unscattered and scattered spectra of Diatom Ptricornutum. This was measured using the exact same setup. So the influence from scattering can be analysed.

data/spectral_library_with_scattering.xlsx
This excel contains the unscattered and modeled scattering spectra for each species. This is done using the script building_spectra/scattering.ipynb


building_spectra/linear_combination.py
This script contains the function generate_mixture_spectra. This function creates a linear combination of the spectra that are put in. This can be both pure and scattered spectra. Besides the linear combination it also creates a df that stores the weights for each mixture. This can be used to test the quality of the models.

building_spectra/scattering.ipynb
This notebook adds model scattering to the pure absorption spectra from data/spectral_library_clean.xlsx and outputs these to data/spectral_library_with_scattering.xlsx
It uses an exponential fit based on the difference between the scattering data and unscattered data to model scattering. It stores the exponent. This is done for Cyanobacteria Synechosystis and Diatom Ptricornutum. 
Because the exponent depends on the size of the organism. The exponents for the other 7 species are retrieved using another exponetial fit between these two points. The results for each species are plotted at the end of the file. These results are stored in spectral_library_with_scattering.xlsx