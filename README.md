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

characterization/characterization_of_chlam.ipynb
Before characterization of all species, we tested on two species (Chlamydomonas). Here, we also tested the robustness of the MLP by seeing for which noise levels the MLP starts guessing (accuracy = 50%). It serves as a basic example of what MLPs can do with the spectra.
characterization/characterization_all_species.ipynb
This notebook characterizes the different species based on their absorption spectra using a MLP. Plots -e.g. confusion matrix -are added to show accuracy of the model.

least_squares_models/nnls.ipynb
This notebook predicts the weights using a Non-Negative Least Squares algorithm. It uses the scipy.optimize module, and an extra constraint is added, such that the weights can not sum up to more than 1. This is the standard notebook to understand the NNLS algorithm in the context of finding weights of the linear combinations of absorption spectra.
least_squares_models/nnls_with_residual_boosting.ipynb
This notebook tries to boost the output of the NNLS by fitting the residuals received from the NNLS by a MLP. Compared to nnls.ipynb, it is an add-on. This is an example of 'Ensemble Learning'. Right now, the NNLS alone performs better than this NNLS+MLP (so it does NOT WORK as wanted...)
