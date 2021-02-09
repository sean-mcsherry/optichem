# --- import and definte the class model from the optichem.peak_click module
from optichem.peak_click2 import model 
s = model()

# --- set the refractive index of the ATR crystal
s.set_crystal_index(2.4 + 1j*1e-5)

# --- set the angle of incidence (found in ATR manual)
s.set_angle_of_incidence(45)

# --- set the high-frequency dielectric constant (found on materials SDS)
s.set_n(1.2)

# --- set input input/output units of wavelength
s.set_input_units('um')
s.set_output_units('1/cm')

# --- upload data file
s.upload('PFOA.txt')

# --- set wavelength range manually
#s.set_range(1000, 1500) # range in 1/cm

# inital solver and plot results
s.start_solver()
s.plot_fit()

# save vibrational modes for stiching
s.save_modes('wL_range_3')