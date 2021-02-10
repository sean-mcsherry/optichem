# import the class model from the manual_fit module
from optichem.manual_fit import model 
s = model()

# set the refractive index of the ATR crystal
s.set_crystal_index(2.4 + 1j*1e-5)

# set the refractive index of the ATR crystal (2.4 for diamond, 4 for Ge, 3.4 for Si, or 2.4 for ZnSe)
s.set_angle_of_incidence(45)

# set the refractivde index in the visible spectrum (usually found on materials SDS)
s.set_n(1.367)

# set x-axis input units of uploaded spectra and desried output units options include: '1/m', 'Hz', 'rad/s', 'nm', 'um', 'm', 'eV'
s.set_input_units('1/cm')
s.set_output_units('um')

# upload ATR data file
s.upload('ATR_measurements/IPA_ATR_data.txt')

# set wavelength range manually
s.set_range(6.75, 12.5) 

# --- ADD MODES MANUALLY ---
s.add_mode(6.82)
s.add_mode(6.877)
s.add_mode(7)
s.add_mode(7.108)
s.add_mode(7.264)
s.add_mode(7.314)
s.add_mode(7.462)
s.add_mode(7.660)
s.add_mode(8.617)
s.add_mode(8.864)
s.add_mode(9.04)
s.add_mode(10.521)
s.add_mode(12.236)


# -- initiate 1st plot
s._init_plot()

# inital solver and plot results
s.start_solver()
s.plot_fit()

# save optical property data
s.save_optical_prop('optichem_results/IPA_optical_properties_manual.txt')

# save vibrational modes for stiching
s.save_modes('optichem_results/IPA_wL_range_2')