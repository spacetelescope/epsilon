import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
import scipy as sc
import os

Mjup = 1.898e27 #kg
Msun = 1.988e30 #kg

class DiamondbackEvolution():
    def __init__(self,clouds='nc',mh=0):
        '''
        This function initializes important variables and calls functions to load the inputs.
        '''
        self.zenodo_url = 'https://zenodo.org/records/12735103'
        self.evolution_zip_url = 'https://zenodo.org/records/12735103/files/evolution.zip'
        self.help_string = '''Evolution tables include each of the three metallicities (0.0, +0.5, -0.5) and come in three versions.
    "nc" denotes cloud-free models for the full evolution.
    "hybrid" includes clouds (fsed=2) above 1300 K and cloud-free below 1300 K (using the Sonora Bobcat models for T<900 K).
    "hybrid-grav" includes clouds (fsed=2) that clear between 1000 and 1300 K, with clouds in lower gravity models persisting to colder tempearatures, again using the Sonora Bobcat models for T<900 K.'''

        self.clouds = clouds
        self.mh = mh
        
        self.cwd = os.getcwd()
        self.source_dir = self.cwd+'/source/'
        self.pkl_dir = self.cwd+'/pkl/'

        print(self.zenodo_url)
        print(self.help_string)

        self.map_inputs()
        self.load_pkl()
        self.create_interpolator()

        self.priors = {}
        
    def data_init(self):
        '''
        Helper function to initialize the model data.
        '''
        self.download_helper()
        self.source2pkl()

    def download_helper(self):
        '''
        This function downloads and unzips the models and moves them into a directory named ./source/
        '''
        from urllib.request import urlopen
        from zipfile import ZipFile
        import shutil

        print('downloading models...')
        zipresp = urlopen(self.evolution_zip_url)
        tempzip = open(self.cwd+'/tempfile.zip', 'wb')
        tempzip.write(zipresp.read())
        tempzip.close()
        zf = ZipFile(self.cwd+'/tempfile.zip')
        zf.extractall(path = 'temp_dl')
        zf.close()
        shutil.move(self.cwd+'/temp_dl/evolution/', self.source_dir)
        shutil.rmtree(self.cwd+'/temp_dl/')
        print('done.')

    def source2pkl(self,verbose=False):
        '''
        This function transforms the formatted text files from zenodo located in ./source/* into
        Pandas DataFrames and saves them to ./pkl/*
        '''
        os.mkdir(self.pkl_dir) if not os.path.exists(self.pkl_dir) else None
        
        massheader = ['M/MSun','age(Gyr)','log L/Lsun', 'Teff(K)','log g','R/Rjup']
        ageheader = ['age(Gyr)','M/MSun','log L/Lsun', 'Teff(K)','log g','R/Rjup']
        massfnames = glob.glob(self.source_dir+'*mass')
        agefnames = glob.glob(self.source_dir+'*age')
        for idx in range(2):
            list = [massfnames,agefnames][idx]
            header = [massheader,ageheader][idx]
            for fname in list:
                file = open(fname)
                table = []
                for i,line in enumerate(file.readlines()):
                    s = line.split('\t')
                    if i == 0:
                        _header_ = line
                    elif len(s) == 8:
                        vals = [float(x) for x in s[0:-2]]
                        table.append(vals)
                df = pd.DataFrame(table,columns=header)
                pkl_fname = self.pkl_dir+fname.split('/')[-1]+'.pkl'
                df.to_pickle(pkl_fname)
                if verbose:
                    print(fname,'->',pkl_fname)
                    display(df.head())

    def map_inputs(self):
        '''
        This function maps inputs to the appropriate filenames.
        '''
        assert self.clouds in ['nc','hybrid','hybrid-grav']
        assert self.mh in [-0.5, 0, 0.0, 0.5]

        match self.clouds:
            case 'nc':
                cloud_str = 'nc_'
            case 'hybrid':
                cloud_str = 'hybrid_f2_'
            case 'hybrid-grav':
                cloud_str = 'hybrid-grav_f2_'
        match self.mh:
            case -0.5:
                mh_str = 'm-0.5'
            case 0:
                mh_str = 'm0.0'
            case 0.5:
                mh_str = 'm+0.5'
                
        end_str = '_mass'
        #end_str = '_age' #unecessary duplication?
        self.str_fname = cloud_str+mh_str+end_str
        self.pkl_fname = self.pkl_dir+self.str_fname+'.pkl'  
        self.interpDict_fname = self.cwd+'/interpDict/'+self.str_fname+'.npy'
        
    def load_pkl(self):
        '''
        This function loads the model DataFrame. It will call data_init() if the model cannot be found.
        '''
        self.data_init() if not os.path.exists(self.pkl_fname) else None 
        print('\nloading: self.df = pd.read_pickle({})'.format(self.pkl_fname))
        self.df = pd.read_pickle(self.pkl_fname)
        self.masses = np.unique(self.df['M/MSun'])

    def line_plot(self):
        '''
        Plot the model data directly.
        '''

        fig,ax = plt.subplots(1,4,figsize=(15,3),dpi=200)
        
        colors = plt.cm.plasma(np.linspace(0,1,len(self.masses)))
        
        for i,m in enumerate(self.masses):
            mdf = self.df[self.df['M/MSun']==m]
            #print(mdf.head())
            ages = mdf['age(Gyr)']
            L    = mdf['log L/Lsun']
            Teff = mdf['Teff(K)']
            logg = mdf['log g']
            R    = mdf['R/Rjup']
        
            ax[0].plot(ages,L,color=colors[i])
            ax[1].plot(ages,Teff,color=colors[i])
            ax[2].plot(ages,logg,color=colors[i])
            ax[3].plot(ages,R,color=colors[i])
        
        ax[0].set_ylabel(r'$\log$ (L/L$_\odot$)')
        ax[1].set_ylabel(r'T$_\mathrm{eff}$ (K)')
        ax[2].set_ylabel(r'$\log (\frac{g}{\mathrm{cm}/\mathrm{s}^2}$)')
        ax[3].set_ylabel(r'R$_\mathrm{p}$/R$_\mathrm{Jup}$')
        
        for a in ax:
            a.set_xlabel('Age (Gyr)')
            a.set_xscale('log')
        
        #cbar = plt.colorbar(plt.cm.ScalarMappable(norm=None, cmap=plt.cm.plasma),cax=ax[-1])
        #cbar.
        plt.subplots_adjust(wspace=0.3)
        plt.show()

    def create_interpolator(self):
        '''
        This function creates four interpolator functions from the model data using sc.interpolate.griddata.
        '''
        if os.path.exists(self.interpDict_fname):
            self.load_interpDict()
        else:
            self.create_interpDict()

        points = self.interpDict['points']
        Ls     = self.interpDict['Ls']
        Teffs  = self.interpDict['Teffs']
        loggs  = self.interpDict['loggs']
        Rs     = self.interpDict['Rs']
                
        self.interpL    = lambda x: sc.interpolate.griddata(points,Ls,x)
        self.interpTeff = lambda x: sc.interpolate.griddata(points,Teffs,x)
        self.interplogg = lambda x: sc.interpolate.griddata(points,loggs,x)
        self.interpR    = lambda x: sc.interpolate.griddata(points,Rs,x)

    def create_interpDict(self):
        '''
        This function slices the dataframes and maps pairs of inputs to outputs, saving the result in a dictionary.
        '''
        points = []
        Ls = []
        Teffs = []
        loggs = []
        Rs = []
        for i,m in enumerate(self.masses):
            mdf = self.df[self.df['M/MSun']==m]
            ages = mdf['age(Gyr)']
            L    = mdf['log L/Lsun']
            Teff = mdf['Teff(K)']
            logg = mdf['log g']
            R    = mdf['R/Rjup']
            for j,a in enumerate(ages):
                point = (a,m)
                points.append(point)
                Ls.append(L.iloc()[j])
                Teffs.append(Teff.iloc()[j])
                loggs.append(logg.iloc()[j])
                Rs.append(R.iloc()[j])

        self.interpDict = {}
        self.interpDict['points'] = points
        self.interpDict['Ls'] = Ls
        self.interpDict['Teffs'] = Teffs
        self.interpDict['loggs'] = loggs
        self.interpDict['Rs'] = Rs

        os.mkdir(self.cwd+'/interpDict/') if not os.path.exists(self.cwd+'/interpDict/') else None
        np.save(self.interpDict_fname,self.interpDict)

    def load_interpDict(self):
        '''
        Helper function to reload the dictionary from a earlier saved version.
        '''
        print('loading: {}'.format(self.interpDict_fname))
        self.interpDict = np.load(self.interpDict_fname,allow_pickle=True).item()

    def interpolate(self, points):
        '''
        This function calls the interpolator objects on the inputs and returns their values.
        '''
        Ls = self.interpL(points)
        Teffs = self.interpTeff(points)
        loggs = self.interplogg(points)
        Rs = self.interpR(points)

        return Ls, Teffs, loggs, Rs

    def interp_plot(self,ages,masses):
        '''
        A helpful plot to visualize the interpolation domain and the outputs.
        '''

        grid_x, grid_y = np.meshgrid(ages, masses)

        fig,ax=plt.subplots(1,4,figsize=(15,3),dpi=200)

        im0 = ax[0].imshow(self.interpL((grid_x,grid_y)),origin='lower',aspect='auto',cmap=plt.cm.plasma)
        im1 = ax[1].imshow(self.interpTeff((grid_x,grid_y)),origin='lower',aspect='auto',cmap=plt.cm.plasma)
        im2 = ax[2].imshow(self.interplogg((grid_x,grid_y)),origin='lower',aspect='auto',cmap=plt.cm.plasma)
        im3 = ax[3].imshow(self.interpR((grid_x,grid_y)),origin='lower',aspect='auto',cmap=plt.cm.plasma)
        
        cbar0 = fig.colorbar(im0,ax=ax[0])
        cbar1 = fig.colorbar(im1,ax=ax[1])
        cbar2 = fig.colorbar(im2,ax=ax[2])
        cbar3 = fig.colorbar(im3,ax=ax[3])
        
        cbar0.set_label('log L/Lsun',rotation=0)
        cbar1.set_label('Teff',rotation=0)
        cbar2.set_label('logg',rotation=0)
        cbar3.set_label('R/Rjup',rotation=0)
        
        for a in ax:
            a.set_xlabel('age (Gyr)')
            a.set_ylabel('Mass (Msun)')
            ds = 40
            xr = [np.round(_,2) for _ in ages]
            yr = [np.round(_,2) for _ in masses]
            a.set_xticks(np.arange(len(ages))[::ds],xr[::ds])
            a.set_yticks(np.arange(len(masses))[::ds],yr[::ds])
        
        plt.subplots_adjust(wspace=0.75)
        plt.show()

    def calc_prior(self,age_prior,mass_prior,object_name):
        '''
        Takes as inputs two distributions and maps them to the four output distributions.
        '''
        L_prior, Teff_prior, logg_prior, R_prior = self.interpolate((age_prior,mass_prior))
        self.priors[object_name] = [age_prior,mass_prior,L_prior,Teff_prior,logg_prior,R_prior]

    def prior_plot(self,object_name):
        '''
        Plots the saved priors associated with the object name.
        '''
        age_prior,mass_prior,L_prior,Teff_prior,logg_prior,R_prior = self.priors[object_name]
        
        fig,ax = plt.subplots(1,6,figsize=(12,2),dpi=200)
        
        nbins = 100
        ax[0].hist(age_prior,bins=nbins)
        ax[1].hist(mass_prior,bins=nbins)
        
        L_hist = ax[2].hist(L_prior,bins=nbins,color='orange')
        Teff_hist = ax[3].hist(Teff_prior,bins=nbins,color='orange')
        logg_hist = ax[4].hist(logg_prior,bins=nbins,color='orange')
        R_hist = ax[5].hist(R_prior,bins=nbins,color='orange')
        
        ax[0].set_xlabel('Age (Gyr)')
        ax[1].set_xlabel(r'Mass (M$_\odot$)')
        ax[2].set_xlabel(r'$\log$ (L/L$_\odot$)')
        ax[3].set_xlabel(r'T$_\mathrm{eff}$ (K)')
        ax[4].set_xlabel(r'$\log (\frac{g}{\mathrm{cm}/\mathrm{s}^2}$)')
        ax[5].set_xlabel(r'R$_\mathrm{p}$ (R$_\mathrm{Jup}$)')

        plt.suptitle('{}'.format(object_name))
        
        for a in ax:
            a.set_yticks([])
        plt.show()

    def prior_print_summary(self,object_name):
        '''
        Prints summary statistics of the priors.
        '''
        priors = self.priors[object_name]
        print_strings = ['Age (Gyr)','Mass/Mjup','log L/Lsun','Teff (K)','log g','R (Rjup)']
        for j,p in enumerate(priors):
            p = p*Msun/Mjup if j == 1 else p
            ms = np.round(np.nanmean(p),2)
            ss = np.round(np.nanstd(p),2)
            print('{} = {} +/- {}'.format(print_strings[j],ms,ss))

    def eval_prior_function(self, object_name, prior_index, points, rtol=1e-2):
        prior = self.priors[object_name][prior_index]
    
        delta_points = np.diff(points)/2.
        extended_points = np.concatenate([[points[0]],points])
        extended_dp = np.concatenate([[-delta_points[0]],delta_points,[delta_points[-1]]])
        bins = extended_points+extended_dp
        
        probability,_bins_ = np.histogram(prior,bins=bins,density=False)
        bin_centers = (_bins_[1:]+_bins_[:-1])/2.
    
        #print(bin_centers)
        #print(points)
        #print(bin_centers-points)
        assert np.allclose(bin_centers,points,rtol=rtol)
    
        #could create an interpoltor function
        #Rprior_f = lambda x: np.interp(x,points,density,left=0,right=0)
    
        #normalize probability
        Z = np.sum(probability)
        return probability/Z
