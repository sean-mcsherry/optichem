# optichem - optical properties of unknown chemicals
A simple python packge that extracts the optical properties of solid and liquid chemicals by fitting Attenuated Total Reflectance (ATR) measurements. Below is an example fit of the absorption spectra of isopropyl alcohol (IPA). For a comprehensive tutorial, please refer to:[insert tutorial file name]

![](model_fit.gif)

Our model treats absorption peaks as vibrational modes that are described as simple harmonic oscillators with the Lorentz Oscillator (LO) model. Optical properties desribed with the LO model are used to calculate the Fresnel reflection coefficients at the ATR interface, and thus can be used to model absoprtion. A non-linear Scipy solver is used to determine the best fit parameters for each vibrational mode. The end result is the real and imaginary parts of the refractive index. 

This model is best used for organic and dielectric materials in the near-to-far infrared. 


<!--ts-->
   * [Installation](#installation)
   * [Usage](#usage)
<!--te-->


## Installation
===============
Some info ova here

## Usage
===============
some info ova here

