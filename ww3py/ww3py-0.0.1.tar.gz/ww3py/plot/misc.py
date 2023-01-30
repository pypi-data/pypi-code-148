import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
import cartopy
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from dateutil.relativedelta import relativedelta
import pandas as pd
import math 
import matplotlib.dates as mdates
import matplotlib.colors as colors


from . import utils
from . import soft_topo_cmap
from . import init_custom

import warnings
warnings.filterwarnings("ignore")

class domain():
        def __init__(self,root_path,ini_date) -> None:
              self.data_path = f'{root_path}data/{ini_date.strftime("%Y%m%d%H")}/'
              self.plots_path = f'{root_path}data/{ini_date.strftime("%Y%m%d%H")}/plots/'
              self.bthm_path = f'{root_path}/info/plots/gebco_2021_n32.0_s8.5_w-98.0_e-58.0.nc'

        def ploting(self):
                self.bat_data=xr.open_dataset(self.bthm_path)
                self.lat_bat=self.bat_data.lat
                self.lon_bat=self.bat_data.lon
                self.elevation_bat=self.bat_data.elevation

                self.norm_topo = soft_topo_cmap.FixPointNormalize(sealevel=0)

                self.fig,self.ax1 = plt.subplots(1,1,subplot_kw={'projection': ccrs.PlateCarree()})
                self.land = cartopy.feature.NaturalEarthFeature('physical', 'land', \
                        scale='50m', edgecolor='k', facecolor=cfeature.COLORS['land'])
                self.ocean = cartopy.feature.NaturalEarthFeature('physical', 'ocean', \
                        scale='50m', edgecolor='none', facecolor=cfeature.COLORS['water'])

                self.ax1.add_feature(self.land, facecolor='gray',alpha=0.5)
                self.ax1.add_feature(self.ocean, facecolor='gainsboro',alpha=0.6)

                cf=self.ax1.contourf(self.lon_bat,self.lat_bat,self.elevation_bat[:,:],30,transform=ccrs.PlateCarree(),\
                                norm=self.norm_topo,cmap='soft_topo',extend='both',zorder=3)

                self.ax1.set(xlabel='Longitude',ylabel='Latitude',xticks=(np.arange(-98,-55,4).tolist()), \
                                yticks=(np.arange(6,35,3).tolist()),ylim=(5.5,35),xlim=(-101,-55),frame_on=False)
                lon_formatter = LongitudeFormatter(number_format='g',
                                                degree_symbol='°')
                lat_formatter = LatitudeFormatter(number_format='g',
                                                degree_symbol='°')
                self.ax1.xaxis.set_major_formatter(lon_formatter)
                self.ax1.yaxis.set_major_formatter(lat_formatter)
                self.ax1.coastlines(resolution='10m',zorder=3)

                self.ax1.add_patch(mpatches.Rectangle(xy=[-98, 8.5], width=40, height=23.5,
                                                fc='none',ec='k',ls='--',lw=1,alpha=0.8,
                                                transform=ccrs.PlateCarree(),zorder=4))    

                self.cax = self.fig.add_axes([self.ax1.get_position().x1+0.02,self.ax1.get_position().y0,\
                                        0.015,self.ax1.get_position().height])
                self.cbar=plt.colorbar(cf,cax=self.cax,orientation="vertical",pad=0.12)
                self.cbar.ax.set_ylabel('Bathimetry and orography [m]',rotation=90,labelpad=0.45)
                return self.fig,self.ax1

        def adding_buoys(self):  # It could be a decorator
                self.fig,self.ax1=self.ploting()
                self.locs_buoys = {'42057':(16.908,-81.422),'42058':(14.394,-74.816),'42059':(15.300,-67.483),
                                        '42060':(16.434,-63.329)}
                for buoy in self.locs_buoys.keys():
                        self.ax1.plot(self.locs_buoys[buoy][1],self.locs_buoys[buoy][0],'^',color='r',markersize=4,zorder=5)
                        self.ax1.text(x=self.locs_buoys[buoy][1]-3.3,y=self.locs_buoys[buoy][0]-0.3,s=buoy,transform=ccrs.PlateCarree(),\
                                        fontsize=8)
                return self.fig,self.ax1

        def sav_plot(self):
                self.fig,self.ax1=self.adding_buoys()
                self.fig.savefig(f'{self.plots_path}domain.png',dpi=1000,bbox_inches='tight',pad_inches=0.05)
                plt.show()

class results():
        def __init__(self,root_path,ini_date,end_date) -> None:
                self.data_path = f'{root_path}data/{ini_date.strftime("%Y%m%d%H")}/'
                self.run_path = f'{root_path}run/{ini_date.strftime("%Y%m%d%H")}/'
                self.plots_path = f'{root_path}data/{ini_date.strftime("%Y%m%d%H")}/plots/'
                self.idate=ini_date
                self.edate=end_date
        
        def series(self):
                data_stations=utils.read_data_int_stations(f'{self.data_path}ww3.2020_tab.nc')
                time,freqs,data_spectra = utils.read_data_src_stations(f'{self.run_path}ww3.2020_src_1d.nc','1d')

                self.buoys_id = ['42057','42058','42059','42060']
                self.myFmt = mdates.DateFormatter('%y-%m-%d')

                hs_max=[]
                for id in self.buoys_id:    
                        data_buoy = utils.ord_buoy_data(id)
                        hs_buoy=data_buoy.hs[self.idate:self.edate+relativedelta(hours=1)]
                        hs_max.append(max(hs_buoy.values))

                self.locs_buoys = {'42057':(16.908,-81.422),'42058':(14.394,-74.816),'42059':(15.300,-67.483),
                                        '42060':(16.434,-63.329)}

                self.series_era5_buoys ={}
                for buoy in self.locs_buoys.keys():
                        self.lon=self.locs_buoys[buoy][1]+360
                        self.lat=self.locs_buoys[buoy][0]
                        self.result=utils.read_era5_buoys(f'{self.run_path}/{self.idate.strftime("%Y%m%d")}_era5.nc',self.lon,self.lat)
                        self.series_era5_buoys[buoy]=self.result

                for id in self.buoys_id:    
                        data_buoy = utils.ord_buoy_data(id)
                        hs_buoy=data_buoy.hs[self.idate+relativedelta(hours=24):self.edate+relativedelta(hours=1)]
                        new_x_index=(hs_buoy.index-pd.Timedelta(minutes=40))
                        hs_model=data_stations[id].hs[new_x_index]
   
                        fig,[ax1,ax2,ax3,ax4]=plt.subplots(4,1,figsize=(12,8))
                        ax1.plot(hs_buoy,c='k',label=f'buoy')
                        ax1.plot(hs_model,c='firebrick',label='model')
                        ax1.set(ylim=(0,max(hs_max)),ylabel="$H_{s}$" +" [m]",title=f'Integral parameters for buoy {id}')
                        ax1.xaxis.set_major_formatter(self.myFmt)
                        ax1.grid('on')
                        ax1.legend()

                        wspd_buoy=data_buoy.wspd[self.idate+relativedelta(hours=24):self.edate+relativedelta(hours=1)]
                        wind_spd_buoy_era = self.series_era5_buoys[id][self.idate+relativedelta(hours=24):]
                        ax2.plot(wind_spd_buoy_era,c='olive',label='ERA5')
                        ax2.plot(wspd_buoy,c='k',label='buoy')
                        ax2.set(ylabel="Wind speed [m/s]")
                        ax2.xaxis.set_major_formatter(self.myFmt)
                        ax2.legend()

                        wvdir_buoy=data_buoy.dir[self.idate+relativedelta(hours=24):self.edate+relativedelta(hours=1)]
                        wndir_buoy=data_buoy.wndir[self.idate+relativedelta(hours=24):self.edate+relativedelta(hours=1)]
                        wvdir_model=data_stations[id].dir[new_x_index]
                        ax3.plot(wvdir_buoy,c='k',label=f'buoy')
                        ax3.plot(wvdir_model,c='firebrick',label='model')
                        ax3.plot(wndir_buoy,c='darkgreen',label='wind')
                        ax3.set(ylabel="Dir [°]")
                        ax3.xaxis.set_major_formatter(self.myFmt)
                        ax3.legend(ncol=3)

                        data_src_1d = data_spectra[id]

                        tp_buoy=data_buoy.tp[self.idate+relativedelta(hours=24):self.edate+relativedelta(hours=1)]
                        tp_model=data_stations[id].tp[new_x_index]
                        ax4.plot(data_src_1d,c='k',label=f'buoy')
                        # ax4.plot(tp_model,c='firebrick',label='model')
                        # ax4.set(ylabel="Tp [s]")
                        # ax4.xaxis.set_major_formatter(self.myFmt)
                        # ax4.legend(ncol=2)

                        plt.savefig(f'{self.plots_path}series_{id}.png',dpi=1000,bbox_inches='tight',pad_inches=0.05)

        def qqplot(self):
                data_stations=utils.read_data_int_stations(f'{self.data_path}ww3.2020_tab.nc')
                self.buoys_id = ['42057','42058','42059','42060']
                for id in self.buoys_id:    
                        data_x = utils.ord_buoy_data(id).hs[self.idate:self.edate+relativedelta(hours=1)]
                        new_x_index=(data_x.index-pd.Timedelta(minutes=40))
                        data_y = data_stations[id].hs[new_x_index]
                        fig,ax1=plt.subplots(1,1)
                        try:
                                ax1.scatter(data_x.values,data_y.values,c='k')
                                sup_lim=math.ceil(max(max(data_x.values),max(data_y.values)))
                                ax1.plot([0,sup_lim],[0,sup_lim],'--',c='k')
                        except:
                                print('doesnt match size')
                        ax1.set(xlabel="Hs [m] - Buoy",ylabel="Hs [m] - Model",xlim=(0,sup_lim),ylim=(0,sup_lim),\
                                        title=f"QQ Plot Hs [m]: Boya {id} - Model")
                        plt.savefig(f'{self.plots_path}qqplot_{id}.png',dpi=1000,bbox_inches='tight',pad_inches=0.05)
        
        def spectra(self):
                time,freqs,dics,data_spectra = utils.read_data_spec_stations(f'{self.data_path}ww3.2020_spec.nc')
                self.buoys_id = ['42057','42058','42059','42060']
                self.r,self.theta = np.meshgrid(freqs.tolist(),dics)

                for id in self.buoys_id:    
                        data_y = data_spectra[id]
                        fig,ax1=plt.subplots(1,1,subplot_kw=dict(projection='polar'))
                        plt.setp(ax1,rmin=0,rmax=1,theta_direction=(-1),theta_zero_location=('N'))

                        cf=ax1.contourf(self.theta,self.r,data_y[50,:,:].T,levels=50,cmap='magma_r')
                        ax1.set(title=f'Directional spectra - buoy {id} - {time[50]}',xticks=(np.radians(np.arange(0,360,90))))
                        utils.vert_colorbar(fig,ax1,cf,0.05,0.01,'Wave energy [m²/Hz/rad]')
                        fig.savefig(f'{self.plots_path}spectra_{id}.png',dpi=1000,bbox_inches='tight',pad_inches=0.05)

        def snl_term(self):
                time,freqs,dics,data_spectra = utils.read_data_src_stations(f'{self.data_path}ww3.2020_src.nc')
                self.buoys_id = ['42057','42058','42059','42060']
                self.r,self.theta = np.meshgrid(freqs.tolist(),dics)

                for id in self.buoys_id:    
                        data_y = data_spectra[id]
                        fig,ax1=plt.subplots(1,1,subplot_kw=dict(projection='polar'))
                        plt.setp(ax1,rmin=0,rmax=1,theta_direction=(-1),theta_zero_location=('N'))
                        norm = colors.TwoSlopeNorm(vmin=np.nanmin(data_y[50,:,:].T), vcenter=0,vmax=np.nanmax(data_y[50,:,:].T))

                        cf=ax1.contourf(self.theta,self.r,data_y[50,:,:].T,levels=50,norm=norm,cmap='seismic')
                        ax1.set(title=f'Snl 2D - buoy {id} - {time[50]}',xticks=(np.radians(np.arange(0,360,90))))
                        utils.vert_colorbar(fig,ax1,cf,0.05,0.01,'Wave energy [m²/rad]')
                        fig.savefig(f'{self.plots_path}snl_{id}.png',dpi=1000,bbox_inches='tight',pad_inches=0.05)
