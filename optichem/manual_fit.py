import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from matplotlib.backend_bases import MouseEvent
from matplotlib.widgets import SpanSelector
from scipy.signal import find_peaks
from scipy.signal import peak_widths
from scipy.optimize import curve_fit

class model:
    
    def __init__(self):
        #--- constants
        self.c = 2.9979e8
        self.h_bar = 6.582119569*1e-16
        self.h = 4.1357*1e-15
        
        #inialize boundaries and upload variables
        self.x_lim_min = []
        self.x_lim_max = []
        self.A = []
        self.wL = []
        self.A_og = []
        self.wL_og = []
        self.my_file = ''
        self.x_lim_min = []
        self.x_lim_max = []
        self.input_units = ''
        self.output_units = ''
        self.xlabel_str = ''
        
        #initalize model variables
        self.model_A = []
        self.df = pd.DataFrame({'index':[], 'w0':[], 'height':[], 'fwhm':[]})
        self.df_og = []
        self.df_new = []
        self.mode_df = []
        self.e_inf = 1
        self.fit_params = []
        self.params = []
        self.angle_of_incidence = []
        self.crystal_index = []
                
        #--- initalize interactive plotting functions
        self._figure, self._axes, self._line,self._axes_2,self._dragging_point = None, None, None, None, None
        self._points = {}
        self.span = []

    #--- setting experimental conditions ---
   
    def set_angle_of_incidence(self, angle):
        if not isinstance(angle, (int, float)):
            raise TypeError('Angle must be numeric (int,float)')
        else:
            self.angle_of_incidence = angle
            
    def set_crystal_index(self, index):
        if not isinstance(index, (int, float, complex)):
            raise TypeError('Index must be numeric (int,float, complex)')
        else:
            self.crystal_index = index      
            
    def set_n(self, index):
        if not isinstance(index, (int, float, complex)):
            raise TypeError('Index must be numeric (int,float, complex)')
        else:
            self.e_inf = index**2        
            
            
    
    #--- initiate data upload, auto peak find, and inital plot ---
    
    def set_input_units(self, units):
        self.input_units = units
        self.output_units = units
        
    def set_output_units(self, units):
        self.output_units = units
        if units == '1/cm':
            self.xlabel_str = 'Wavenumber (cm$^-1$)'
        if units == 'Hz':
            self.xlabel_str = 'Frequency (Hz)'
        if units == 'rad/s':
            self.xlabel_str = 'Frequency (rad/s)'
        if units == 'um':
            self.xlabel_str = 'Wavelength ($\mu$m)'
        if units == 'nm':
            self.xlabel_str = 'Wavelength (nm)'
        if units == 'm':
            self.xlabel_str = 'Wavelength (m)'
        if units == 'eV':
            self.xlabel_str = 'Energy (eV)'

    def upload(self, my_file= ''):
      data = np.loadtxt(my_file)
      self.wL_og = data[:,0]  
      self.A_og = data[:,1]
      self.wL = data[:,0]  
      self.A = data[:,1]
      self.wL = self.unit_conversion(self.wL, self.input_units, self.output_units)
      self.x_lim_min = np.min([self.wL[0],self.wL[len(self.wL)-1]])
      self.x_lim_max = np.max([self.wL[0], self.wL[len(self.wL)-1]])
      self.wL_og = self.unit_conversion(self.wL_og, self.input_units, self.output_units)
      self.auto_peak_find()

    def set_range(self, x_lim_min, x_lim_max):
      idx_lb = (abs(x_lim_min - self.wL_og)).argmin()
      idx_ub = (abs(x_lim_max - self.wL_og)).argmin()
      if idx_lb < idx_ub:
          self.wL = self.wL_og[idx_lb:idx_ub]
          self.A = self.A_og[idx_lb:idx_ub]
      elif idx_ub < idx_lb:
          a = idx_ub
          b = idx_lb
          idx_lb = a
          idx_ub = b
          self.wL = self.wL_og[idx_lb:idx_ub]
          self.A = self.A_og[idx_lb:idx_ub]
      self.x_lim_min = np.min([self.wL_og[idx_lb], self.wL_og[idx_ub]])
      self.x_lim_max = np.max([self.wL_og[idx_lb], self.wL_og[idx_ub]])
      plt.show()
        
    def auto_peak_find(self):
        self.df_new = []
        peaks, _ = find_peaks(self.A, height=0.01)
        width_parameters = peak_widths(self.A, peaks, rel_height=0.5)
        widths = np.empty(len(peaks))
        heights = np.empty(len(peaks))
        pks = np.empty(len(peaks))
        index = np.empty(len(peaks))
        for ii in range(0, len(peaks)):
          widths[ii] =  np.abs(self.unit_conversion(self.wL[int(width_parameters[2][ii])], self.output_units, 'eV') - self.unit_conversion(self.wL[int(width_parameters[3][ii])], self.output_units, 'eV'))
          heights[ii] = self.A[peaks[ii]]
          pks[ii] = self.wL[peaks[ii]]
          index[ii] = peaks[ii]
        self.df_new = pd.DataFrame({'index':index, 'w0': pks,'height': heights,'fwhm': widths})
        self.df_new = self.df_new.sort_values(['height'], ascending=False)
        self.df_new = self.df_new.reset_index(drop=True)
        self.df_og = self.df_new
        
    def _init_plot(self):
        self._figure = plt.figure(num='Add (left click), delete (right click), or drag (left click + drag) new peaks',figsize=(9,5))
        axes = plt.subplot(1, 1, 1)
        plt.plot(self.wL,self.A, lw = 3, color = 'k')
        axes.grid(which="both")
        self._axes = axes
        plt.xlabel(self.xlabel_str)
        plt.ylabel('Absorbance')
        if self._points:
            x, y = zip(*self._points.items())
            self._line, = self._axes.plot(x, y, "r", marker="+", markersize=10, linestyle='None')  
        self._axes.set_xlim(self.x_lim_min, self.x_lim_max)
        plt.show()
        
        def onrangeselect(xmin, xmax):
            indmin, indmax = np.searchsorted(x, (xmin, xmax))
            indmax = min(len(x) - 1, indmax)
            self.x_lim_min = np.min([xmin,xmax])
            self.x_lim_max = np.max([xmin,xmax])
            self.set_range(xmin, xmax)
        
        self.span = SpanSelector(axes, onrangeselect, 'horizontal', useblit=True,
                    rectprops=dict(alpha=0.5, facecolor='red'))
        plt.show()  
    
    
    # --- manual commands
    
    def add_mode(self, w0):
        x = w0
        idx_y = abs(w0 - self.wL).argmin()
        y = self.A[idx_y]

        gamma_df = self.df_og.iloc[(self.df_og['w0']-x).abs().argsort()[:1]]
        gamma_df = gamma_df.reset_index(drop=True)
        if (gamma_df['w0'][0] - x) <0.5:
          fwhm = gamma_df['fwhm'][0]
        else:
          gamma_df = self.df_og.iloc[(self.df_og['w0']-x).abs().argsort()[:2]]
          fwhm = gamma_df['fwhm'].mean()
        self.df = self.df.append({'index': 0,'w0': x,'height':y, 'fwhm':fwhm}, ignore_index=True)
        self.df = self.df.reset_index(drop=True)
        self._points[x] = y
        
            
        
    # --- unit conversion model ---
    
    def unit_conversion(self, wL, input_units, output_units):
        if input_units == '1/cm':
            if output_units == '1/cm':
                wL_output = wL
            if output_units == 'Hz':
                wL_output = wL*100*self.c
            if output_units == 'rad/s': 
                wL_output = 2*np.pi*wL*100*self.c
            if output_units == 'um':
                wL_output = 1e6/(wL*100)
            if output_units == 'nm':
                wL_output = 1e9/(wL*100)
            if output_units == 'm':
                wL_output = 1/(wL*100)
            if output_units == 'eV':
                wL_output = self.h*wL*100*self.c
                
        if input_units == 'Hz':
            if output_units == '1/cm':
                wL_output = wL/(100*self.c)
            if output_units == 'Hz':
                wL_output = wL
            if output_units == 'rad/s':
                wL_output = 2*np.pi*wL 
            if output_units == 'um':
                wL_output = (self.c/wL)*1e6
            if output_units == 'nm':
                wL_output = (self.c/wL)*1e9
            if output_units == 'm':
                wL_output = self.c/wL
            if output_units == 'eV':
                wL_output = wL*self.h
                
        if input_units == 'rad/s':
            if output_units == '1/cm':
                wL_output = wL/(2*np.pi*self.c*100)
            if output_units == 'Hz':
                wL_output = wL/(2*np.pi)
            if output_units == 'rad/s':
                wL_output = wL
            if output_units == 'um':
                wL_output = 1e6*(2*np.pi*self.c/wL)
            if output_units == 'nm':
                wL_output = 1e9*(2*np.pi*self.c/wL)
            if output_units == 'm':
                wL_output = (2*np.pi*self.c/wL)
            if output_units == 'eV':
                wL_output = wL*self.h_bar
                
        if input_units == 'um':
            if output_units == '1/cm':
                wL_output = 1/(wL*1e-4)
            if output_units == 'Hz':
                wL_output = self.c/(wL*1e-6)
            if output_units == 'rad/s':
                wL_output = 2*np.pi*self.c/(wL*1e-6)
            if output_units == 'um':
                wL_output = wL
            if output_units == 'nm':
                wL_output = wL*1e3
            if output_units == 'm':
                wL_output = wL*1e-6
            if output_units == 'eV':
                wL_output = self.h*(self.c/(wL*1e-6))
                
        if input_units == 'nm':
            if output_units == '1/cm':
                wL_output = 1/(wL*1e-7)
            if output_units == 'Hz':
                wL_output = self.c/(wL*1e-9)
            if output_units == 'rad/s':
                wL_output = 2*np.pi*self.c/(wL*1e-9)
            if output_units == 'um':
                wL_output = wL*1e-3
            if output_units == 'nm':
                wL_output = wL
            if output_units == 'm':
                wL_output =wL*1e-9
            if output_units == 'eV':
                wL_output = self.h*(self.c/(wL*1e-9))
                
        if input_units == 'm':
            if output_units == '1/cm':
                wL_output = wL_output = 1/(wL*1e2)
            if output_units == 'Hz':
                wL_output =self.c/wL
            if output_units == 'rad/s':
                wL_output = 2*np.pi*self.c/wL
            if output_units == 'um':
                wL_output = wL*1e6
            if output_units == 'nm':
                wL_output = wL*1e9
            if output_units == 'm':
                wL_output = wL
            if output_units == 'eV':
                wL_output =  self.h*(self.c/wL)
                
        if input_units == 'eV':
            if output_units == '1/cm':
                wL_output = (wL/(self.c*self.h*100))
            if output_units == 'Hz':
                wL_output = wL/self.h
            if output_units == 'rad/s':
                wL_output =2*np.pi*wL/self.h
            if output_units == 'um':
                wL_output = (self.h*self.c/wL)*1e6
            if output_units == 'nm':
                wL_output = (self.h*self.c/wL)*1e9
            if output_units == 'm':
                wL_output = self.h*self.c/wL
            if output_units == 'eV':
                wL_output = wL
                
        return wL_output
        
    
     #--- ATR absorbance model ---
            
    def atr_absorbance(self,wL,*params):
       
        angle = self.angle_of_incidence
        w = self.unit_conversion(wL, self.output_units,'eV')
        count = 0
        
        if isinstance(params[0], list):
            params = list(params[0])
            modes = len(params)/3
        elif params[0].dtype in [np.float32, np.float64, np.integer]:
            
            params = list(params)
            modes = len(params)/3

        e_inf = self.e_inf
        for jj in range(0, int(modes)):
                params[0+count] = self.unit_conversion(params[0+count], self.output_units,'eV')
                count = 3*(jj)+3

        a_old = 0
        ab = np.empty(len(w))
        count = 0
        
        for ii in range(0, int(modes)):
                ab = (params[1+count]*(params[0+count]**2))/((params[0+count]**2)-(w**2)-params[2+count]*w*1j)+a_old
                count = 3*ii+3
                a_old = ab
        e_p = e_inf + ab
        N_1 = np.array(self.crystal_index + 0*w)
        N_2 = np.sqrt(e_p)
        ii = []
        o = []
        R_p = np.empty(len(w))
        R_s = np.empty(len(w))
        for ii in range(0,len(w)):
            o_1 = angle*np.pi/180
            o_2 = np.arcsin(N_1[ii]/N_2[ii]*np.sin(o_1))
            rp = (N_1[ii]*np.cos(o_2) - N_2[ii]*np.cos(o_1))/(N_1[ii]*np.cos(o_2) + N_2[ii]*np.cos(o_1))
            rs = (N_1[ii]*np.cos(o_1) - N_2[ii]*np.cos(o_2))/(N_1[ii]*np.cos(o_1) + N_2[ii]*np.cos(o_2))
            R_p[ii] = (np.abs(rp))**2
            R_s[ii] = (np.abs(rs))**2

        R_tot = (1/2)*(R_p + R_s)
        self.model_A = 1 - R_tot
        return self.model_A
    
    def atr_absorbance_single(self,wL,*params):
       
        angle = self.angle_of_incidence
        w = self.unit_conversion(wL, self.output_units,'eV')
        count = 0
        
        if isinstance(params[0], list):
            params = list(params[0])
            modes = len(params)/3
        elif params[0].dtype in [np.float32, np.float64, np.integer]:
            
            params = list(params)
            modes = len(params)/3

        e_inf = self.e_inf
        for jj in range(0, int(modes)):
                params[0+count] = self.unit_conversion(params[0+count], self.output_units,'eV')
                count = 3*(jj)+3

        a_old = 0
        ab = np.empty(len(w))
        count = 0
        
        for ii in range(0, int(modes)):
                ab = (params[1+count]*(params[0+count]**2))/((params[0+count]**2)-(w**2)-params[2+count]*w*1j)+a_old
                count = 3*ii+3
                a_old = ab
        e_p = e_inf + ab
        N_1 = np.array(self.crystal_index + 0*w)
        N_2 = np.sqrt(e_p)
        ii = []
        o = []
        R_p = np.empty(len(w))
        R_s = np.empty(len(w))
        for ii in range(0,len(w)):
            o_1 = angle*np.pi/180
            o_2 = np.arcsin(N_1[ii]/N_2[ii]*np.sin(o_1))
            rp = (N_1[ii]*np.cos(o_2) - N_2[ii]*np.cos(o_1))/(N_1[ii]*np.cos(o_2) + N_2[ii]*np.cos(o_1))
            rs = (N_1[ii]*np.cos(o_1) - N_2[ii]*np.cos(o_2))/(N_1[ii]*np.cos(o_1) + N_2[ii]*np.cos(o_2))
            R_p[ii] = (np.abs(rp))**2
            R_s[ii] = (np.abs(rs))**2

        R_tot = (1/2)*(R_p + R_s)
        model_A_single = 1 - R_tot
        return model_A_single
    
    def get_optical_prop(self,wL,*params):
       
        w = self.unit_conversion(wL, self.output_units,'eV')
        count = 0
        
        if isinstance(params[0], list):
            params = list(params[0])
            modes = len(params)/3
        elif params[0].dtype in [np.float32, np.float64, np.integer]:
            
            params = list(params)
            modes = len(params)/3

        e_inf = self.e_inf
        for jj in range(0, int(modes)):
                params[0+count] = self.unit_conversion(params[0+count], self.output_units,'eV')
                count = 3*(jj)+3

        a_old = 0
        ab = np.empty(len(w))
        count = 0
        
        for ii in range(0, int(modes)):
                ab = (params[1+count]*(params[0+count]**2))/((params[0+count]**2)-(w**2)-params[2+count]*w*1j)+a_old
                count = 3*ii+3
                a_old = ab
        e_p = e_inf + ab
        N = np.sqrt(e_p)
        return N, e_p
    
    
    
    
   #--- initate solver ---     
    
    def start_solver(self, params = [],lb = [],ub = []):

        if not params:
          params = []
          for ii in range(0, len(self.df['w0'])):
            w0 = self.df['w0'][ii]
            gamma = self.df['fwhm'][ii]
            f = self.df['height'][ii]*gamma/(self.unit_conversion(self.df['w0'][ii], self.output_units,'eV'))
            params.append(w0)
            params.append(f)
            params.append(gamma)
            
        if not lb:
          lb = []
          for ii in range(int(len(params)/3)):
            w0 = params[3*ii]
            lb.append(w0 - w0*0.025)
            lb.append(0.00001)
            lb.append(0.00001)
                 
        if not ub:
          ub = []
          for ii in range(int(len(params)/3)):
            w0 = params[3*ii]
            ub.append(w0 + w0*0.025)
            ub.append(0.5)
            ub.append(0.5)
        
        best_vals, covar = curve_fit(self.atr_absorbance, self.wL, self.A, p0 = params, bounds=(lb,ub))
        self.fit_params = list(best_vals)
        self.atr_absorbance(self.wL, self.fit_params)
        return 

    
   #--- additional plotting options --- 

    def plot_fit(self, c1='k',c2='r', lw=3):     
        plt.figure(figsize=(9,12))
        ax_1 = plt.subplot(3, 1, 1)
        plt.plot(self.wL,self.A,color =c1, linewidth = lw)
        plt.plot(self.wL,self.model_A,color =c2, linewidth = lw/2)
        plt.xlabel(self.xlabel_str)
        plt.ylabel('Absorbance')
        plt.legend(('Experimental Data', 'Model'),edgecolor = 'none', facecolor = 'none')
        ax_1.set_title('Absorption Model',fontweight='bold')
        
        ax_2 = plt.subplot(3,1,2)
        plt.plot(self.wL,self.A,color =c1, linewidth = lw)
        plt.plot(self.wL,self.model_A,color =c2, linewidth = lw/2)
        plt.legend(('Experimental Data', 'Model'),edgecolor = 'none', facecolor = 'none')
        for ii in range(int(len(self.fit_params)/3)):
          A = self.atr_absorbance_single(self.wL, self.fit_params[3*ii],self.fit_params[3*ii +1],self.fit_params[3*ii+2])
          plt.plot(self.wL,A)
        plt.xlabel(self.xlabel_str)
        plt.ylabel('Absorbance')
        ax_2.set_title('Absorption Model w/ Mode Contributions', fontweight='bold')

        ax_3 = plt.subplot(3,1,3)
        N,e_p = self.get_optical_prop(self.wL,self.fit_params)
        plt.plot(self.wL,np.real(N), 'k', linewidth = lw)
        plt.plot(self.wL,np.imag(N), 'tab:gray', linewidth = lw)
        plt.xlabel(self.xlabel_str)
        plt.ylabel('Refractice Index')
        plt.legend(('n (real part)', 'k (imag part)'),edgecolor = 'none', facecolor = 'none')
        ax_3.set_title('Refractive Index Data',fontweight='bold')

        plt.subplots_adjust(hspace = 0.4,bottom =0.05, top=0.95)
        plt.show()
        
    def load_data(self, my_file= ''):
      data = np.loadtxt(my_file)
      self.wL_og = data[:,0]  
      self.A_og = data[:,1]
      self.wL = data[:,0]  
      self.A = data[:,1]
      self.wL_old = self.wL
      self.wL = self.unit_conversion(self.wL, self.input_units, self.output_units)
      self.x_lim_min = np.min([self.wL[0],self.wL[len(self.wL)-1]])
      self.x_lim_max = np.max([self.wL[0], self.wL[len(self.wL)-1]])
      self.wL_og = self.unit_conversion(self.wL_og, self.input_units, self.output_units)  
        
    def load_modes(self, *file_names):
        file_names = list(file_names)
        self.fit_params = []
        x_lim_min = []
        x_lim_max = []
        self.df = pd.DataFrame()
        for ii in range(len(file_names)):
            df = pd.read_pickle(file_names[ii])
            for jj in range(len(df['w0'])):
                self.fit_params.append(df['w0'][jj])
                self.fit_params.append(df['f'][jj])
                self.fit_params.append(df['gamma'][jj])
            x_lim_min.append(df['x_lim_min'][0]) 
            x_lim_max.append(df['x_lim_max'][0]) 
        self.x_lim_min = np.min(x_lim_min)
        self.x_lim_max = np.max(x_lim_max)
        idx_lb = (abs(self.x_lim_min - self.wL_og)).argmin()
        idx_ub = (abs(self.x_lim_max  - self.wL_og)).argmin()
        if idx_lb < idx_ub:
            self.wL = self.wL_og[idx_lb:idx_ub]
            self.A = self.A_og[idx_lb:idx_ub]
        elif idx_ub < idx_lb:
            a = idx_ub
            b = idx_lb
            idx_lb = a
            idx_ub = b
            self.wL = self.wL_og[idx_lb:idx_ub]
            self.A = self.A_og[idx_lb:idx_ub]
        self.atr_absorbance(self.wL, self.fit_params)
        self.plot_fit()
        
        
    # --- saving optical properties and vibrational modes ---
        
    def save_optical_prop(self,file_name):
        N, e_p = self.get_optical_prop(self.wL,self.fit_params)
        fmt_text = np.ones((len(self.wL),5))
        fmt_text[:,0] = self.wL
        fmt_text[:,1] = np.real(N)
        fmt_text[:,2] = np.imag(N)
        fmt_text[:,3] = np.real(e_p)
        fmt_text[:,4] = np.imag(e_p)
        np.savetxt(file_name, fmt_text, delimiter='\t')   # X is an array
        
    def save_modes(self, file_name):
        w0 = []
        f = []
        gamma = []
        x_lim_min = []
        x_lim_max = []
        for ii in range(int(len(self.fit_params)/3)):
            w0.append(self.fit_params[3*ii])
            f.append(self.fit_params[3*ii+1])
            gamma.append(self.fit_params[3*ii+2])
            x_lim_min.append(self.x_lim_min)
            x_lim_max.append(self.x_lim_max)
        d = {'w0':w0, 'f':f, 'gamma':gamma, 'x_lim_min':x_lim_min,'x_lim_max':x_lim_max}
        self.mode_df = pd.DataFrame(d)
        self.mode_df.to_pickle(file_name)
    
    
    
    
    # --- stiching ---
    
    def stich(self, *file_names):
        file_names = list(file_names)
        x_lim_min=[]
        x_lim_max = []
        self.fit_params = []
        for ii in range(len(file_names)):
            df = pd.read_pickle(file_names[ii])
            for jj in range(len(df['w0'])):
                self.fit_params.append(df['w0'][jj])
                self.fit_params.append(df['f'][jj])
                self.fit_params.append(df['gamma'][jj])
            x_lim_min.append(df['x_lim_min'][0]) 
            x_lim_max.append(df['x_lim_max'][0]) 
        self.set_range(np.min(x_lim_min), np.max(x_lim_max))
        self.start_solver(params = self.fit_params)
                
               
