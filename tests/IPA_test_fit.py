# --- import and definte the class model from the optichem.peak_click module
from optichem.semi_auto_fit import model 
s = model()

# --- set the refractive index of the ATR crystal
s.set_crystal_index(2.4 + 1j*1e-5)

# --- set the angle of incidence (found in ATR manual)
s.set_angle_of_incidence(45)

# --- set the high-frequency dielectric constant (found on materials SDS)
s.set_n(1.367)

# --- set input input/output units of wavelength
s.set_input_units('1/cm')
s.set_output_units('um')

# --- upload data file
s.upload('ATR_measurements/IPA_ATR_data.txt')

# --- set wavelength range manually
s.set_range(6.75, 12.5) # range in 1/cm

# inital solver and plot results
s.start_solver()
s.plot_fit()

# save vibrational modes for stiching
s.save_modes('wL_range_3')
