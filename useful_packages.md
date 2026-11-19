# Useful Packages and Software for Exoplanet High Contrast Imaging


## Coronagraphy

* **SpaceKLIP**: The core community package for JWST coronagraph data processing for NIRCam and MIRI. [Github](https://github.com/spacetelescope/spaceKLIP) [Docs](https://spaceklip.readthedocs.io/en/latest/)
* **pyKLIP**: Python implementation of KLIP/PCA-based PSF subtraction (ADI/RDI/SDI) and forward modeling, used as the engine within SpaceKLIP. [Source](https://bitbucket.org/pyKLIP/pyklip) [Docs](https://pyklip.readthedocs.io/)
* **PanCake**: The Pandeia Coronagraphy Extension, for exposure time calculations and simulated scenes for JWST coronagraphic observations. [Github](https://github.com/spacetelescope/pandeia-coronagraphy) [Docs](https://github.com/spacetelescope/pandeia-coronagraphy#readme)
* **applefy**: Tools for detection limits, contrast curves, and false-positive fraction analysis of high-contrast imaging data, with PSF subtraction by PCA. [Github](https://github.com/markusbonse/applefy) [Docs](https://applefy.readthedocs.io/)
* **pyFLIP**: Python implementation of FLIP ((Ph)ysics-based Learning for Imaging Planets). Under development as of Nov 2026 [Github](https://github.com/rferrerc/pyflip)

## Imaging Spectroscopy

* **BREADS**: Forward-modeling framework for extracting exoplanet spectra from high-contrast integral field spectrograph data, including JWST NIRSpec IFU and MIRI MRS. [Github](https://github.com/jruffio/breads) [Docs](https://breads.readthedocs.io/)


## Interferometry

* **AMIGO**: Differentiable (JAX-based) forward model and calibration pipeline for JWST NIRISS Aperture Masking Interferometry (AMI). [Github](https://github.com/LouisDesdoigts/amigo) [Docs](https://github.com/LouisDesdoigts/amigo#readme)
* **ExoGRAVITY**: Data reduction code for extracting astrometry and spectra of exoplanets from VLTI/GRAVITY interferometric observations. [Source](https://gitlab.obspm.fr/mnowak/exoGravity) [Docs](https://github.com/wbalmer/exogravity#readme)


## Atmospheres and Modeling

* **species**: Toolkit for atmospheric characterization of directly imaged planets and brown dwarfs, including model grids, retrievals, and photometry/spectra handling. [Github](https://github.com/tomasstolker/species) [Docs](https://species.readthedocs.io/)
* **MADYS**: Toolit for isochronal fitting, age/mass estimation, detection probability map estimates. [Github](https://github.com/vsquicciarini/madys) [Docs](https://madys.readthedocs.io/en/latest/)
* **spectres**: Resampling of spectra onto a new wavelength grid. [Github](https://github.com/ACCarnall/SpectRes) [Docs](https://spectres.readthedocs.io/en/latest/)
* **picaso**: Modelling and retrieval suite for exoplanet atmospehres [Github](https://github.com/natashabatalha/picaso) [Docs](https://natashabatalha.github.io/picaso/)
* **petitRADTRANS**: Package for calculating spectra of exoplanets and for running retrievals.[Github](https://github.com/nborsato/petitRADTRANS) [Docs](https://petitradtrans.readthedocs.io/en/latest/)

## Orbits and Dynamics

* **whereistheplanet**: Predicts the position of known directly imaged planets and companions at a given date from published orbit fits, via a web tool and Python package. [Github](https://github.com/semaphoreP/whereistheplanet) [Docs](http://whereistheplanet.com/)
* **orbitize**: Bayesian orbit-fitting package for directly imaged companions using sparse astrometry, with MCMC and OFTI samplers. [Github](https://github.com/sblunt/orbitize) [Docs](https://orbitize.readthedocs.io/)
* **octofitter**: Bayesian modeling framework for orbits and companions combining direct imaging, RV, and astrometry (note, written in Julia, not Python). [Github](https://github.com/sefffal/Octofitter.jl) [Docs](https://sefffal.github.io/Octofitter.jl/)
* **orvara**: Orbit fitting code combining radial velocity, Hipparcos–Gaia astrometry, and relative astrometry to measure companion masses and orbits. [Github](https://github.com/t-brandt/orvara) [Docs](https://github.com/t-brandt/orvara#readme)


## JWST systems and operations

* **pysiaf**: Access and manipulate Science Instrument Aperture File (SIAF) data, i.e. precise aperture geometry and coordinate transforms for JWST and other missions. [Github](https://github.com/spacetelescope/pysiaf) [Docs](https://pysiaf.readthedocs.io/)
* **jwst_gtvt**: JWST General Target Visibility Tool, for computing target visibility windows and position angle ranges. [Github](https://github.com/spacetelescope/jwst_gtvt) [Docs](https://jwst-docs.stsci.edu/jwst-other-tools/jwst-target-visibility-tools)
* **jwst_mast_query**: Scripts to query MAST for JWST observations and download data by program, instrument, or filter. [Github](https://github.com/spacetelescope/jwst_mast_query) [Docs](https://github.com/spacetelescope/jwst_mast_query#readme)
* **pandeia.engine**: The JWST (and Roman) exposure time calculator engine, which performs 3D simulation-based signal-to-noise calculations; scriptable for running local ETC calculations. [PyPI](https://pypi.org/project/pandeia.engine/) [Docs](https://jwst-docs.stsci.edu/display/Latest/Pandeia+Quickstart)

## Optical Modeling and Simulations
* **STPSF**: Simulates JWST (and Roman) point spread functions for all instruments, the successor to WebbPSF. [Github](https://github.com/spacetelescope/stpsf) [Docs](https://stpsf.readthedocs.io/)
* **POPPY**: Physical optics propagation (Fresnel/Fraunhofer) in Python, the engine underlying STPSF. [Github](https://github.com/spacetelescope/poppy) [Docs](https://poppy-optics.readthedocs.io/)
* **HCIPy**: Framework for simulating high-contrast imaging systems, including optics propagation, coronagraphs, and adaptive optics. [Github](https://github.com/ehpor/hcipy) [Docs](https://hcipy.org/)

## Other
* **WHIPPOT**: A tool for simulating JWST observing scenes and planning position angles and offsets. Some example notebooks are found in the [observation_planning](observation_planning) folder, with more available on the github. [Github](https://github.com/STScI-MIRI/whippot)
