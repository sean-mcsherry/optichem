# --- import and definte the class model from the optichem.peak_click module
from optichem.manual_fit import model 
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
s.set_range(1000, 1500) # range in 1/cm

# --- ADD MODES MANUALLY ---
s.add_mode(1017.491088)
s.add_mode(1105.923417)
s.add_mode(1131.661892)
s.add_mode(1130.756507)
s.add_mode(1148.552932)
s.add_mode(1149.739504)
s.add_mode(1184.931145)
s.add_mode(1202.760276)
s.add_mode(1237.681808)
s.add_mode(1249.970088)
s.add_mode(1296.930805)
s.add_mode(1323.981365)
s.add_mode(1335.323329)
s.add_mode(1366.180953)
s.add_mode(1456.927515)
s.add_mode(1455.488015)
s.add_mode(1171)
s.add_mode(1177)
s.add_mode(1198)
s.add_mode(1437)

# -- initiate 1st plot
s._init_plot()

# inital solver and plot results
s.start_solver()
s.plot_fit()

# save optical property data
s.save_optical_prop('PFAS_test.txt')

# save vibrational modes for stiching
s.save_modes('wL_range_1000_1500')

# display modes
print(s.mode_df['w0'])


s.add_mode(1017.491088)
s.add_mode(1105.923417)
s.add_mode(1131.661892)
s.add_mode(1130.756507)
s.add_mode(1148.552932)
s.add_mode(1149.739504)
s.add_mode(1184.931145)
s.add_mode(1202.760276)
s.add_mode(1237.681808)
s.add_mode(1249.970088)
s.add_mode(1296.930805)
s.add_mode(1323.981365)
s.add_mode(1335.323329)
s.add_mode(1366.180953)
s.add_mode(1456.927515)
s.add_mode(1455.488015)
s.add_mode(1171)
s.add_mode(1177)
s.add_mode(1198)
s.add_mode(1437)