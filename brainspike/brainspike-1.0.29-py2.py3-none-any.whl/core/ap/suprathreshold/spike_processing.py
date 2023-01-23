"""
spike_processing.py

Class for detecting spike & spiketrain features
in action potential sweepdata (depolarizing steps) + plots. 

Note: spike feature extraction modules adapted from iPFX
[https://github.com/AllenInstitute/ipfx/tree/797e677070ff161960bf72c97d70b40b91aef74a]

"""

import pandas as pd 

import numpy as np 

from ....features.ipfx.feature_extractor import (SpikeFeatureExtractor, SpikeTrainFeatureExtractor)
from ....abf.abf_obj import ABF
from ....utils.core.core_load_utils import (find_srate, find_stimuli, find_sweepdata, find_sweeptimes)
from ....curation.spike_sweepdata_qc import (drop_hyperpolsweeps, drop_unstablesweeps_rms)
from ....features.rheobase import (return_rheobase)
from ....features.spike_feature_adaptation import (spikeheight_adaptation, trough_adaptation, upstroke_adaptation, downstroke_adaptation)
from ....features.ap_types import (return_aptype)
from ....postprocessing.spike_sweep_search import (find_maxfiringsweep, find_maxampspikes, find_closestcurrentsweep)
from ....exporters.dataframes import (export_df)
from ....plots.spike_plots import (spike_plot)
from ....plots.spiketrain_plots import (spiketrain_plot, i_f_plot, spiketrain_plot_allsweeps)

###################################################################################################
###################################################################################################

class SpikeFeatures: 
    
    """ class for detecting spike features in ap sweep data across sweeps and 
    for single spikes """
    
    def __init__(self, data, dv_cutoff=5., max_interval=0.01, min_height = 2., min_peak = 0.,\
                thresh_frac = 0.2, reject_at_stim_start_interval = 0, baseline_interval = 0.05, rms_cutoff = 2,\
                burst_tol = 0.5, pause_cost = 1.0, filter = None): 
        """
        """

        self.data = data 
        self.dv_cutoff = dv_cutoff 
        self.max_interval = max_interval
        self.min_height = min_height 
        self.min_peak = min_peak 
        self.thresh_frac = thresh_frac 
        self.reject_at_stim_start_interval = reject_at_stim_start_interval
        self.rms_cutoff = rms_cutoff 
        self.burst_tol = burst_tol
        self.pause_cost = pause_cost 
        self.filter = filter 
        self.baseline_interval = baseline_interval # for rms + baseline v         
        
    @property
    def process_spikes(self): 
        """ process individual spike features for each sweep data """
        
        try: 
            isinstance(self.data, ABF)
            self.sweeptimes = find_sweeptimes(self.data)
            self.sweepdata = find_sweepdata(self.data)
            self.stimuli = find_stimuli(self.data)
            self.srate = find_srate(self.data)
            self.start = self.data.metadata['start_sec'] # start + end stimuli (seconds)
            self.end = self.data.metadata['end_sec']
            self._sweep_qc_spike # sweep qc 
            
        except AttributeError: 
            raise AttributeError("pass single data object ...")   
        
        # find spike features
        #----------------------
        # extract for all 'stable' depolarization sweeps 
        
        df_spikes = pd.DataFrame()
        df_spikes_empty = pd.DataFrame({'threshold_index':np.nan,'clipped':np.nan,\
            'threshold_t':np.nan,'threshold_v':np.nan,'threshold_i':np.nan,\
            'peak_index':np.nan,'peak_t':np.nan,'peak_v':np.nan,'peak_i':np.nan,\
            'trough_index':np.nan,'trough_t':np.nan,'trough_v':np.nan,'trough_i':np.nan,\
            'upstroke_index':np.nan,'upstroke':np.nan,'upstroke_t':np.nan,'upstroke_v':np.nan,\
            'downstroke_index':np.nan,'downstroke':np.nan,'downstroke_t':np.nan,\
            'downstroke_v':np.nan,'isi_type':np.nan,'fast_trough_index':np.nan,'fast_trough_t':np.nan,\
            'fast_trough_v':np.nan,'fast_trough_i':np.nan,'adp_index':np.nan,'adp_t':np.nan,\
            'adp_v': np.nan,'adp_i':np.nan,'slow_trough_index':np.nan,'slow_trough_t':np.nan,\
            'slow_trough_v':np.nan,'slow_trough_i':np.nan,'width':np.nan,'upstroke_downstroke_ratio':np.nan,\
            'sweep_number_supra':np.nan}, index = [0]) # empty df for group processing 
        
        if len(self.stable_sweepdata) > 0: 
            for t, v, i, sweep in zip(self.stable_sweeptimes, self.stable_sweepdata,\
                                        self.stable_stimuli, self.stable_sweepidx[0]): 

                ipfx = SpikeFeatureExtractor(start=self.start, end=self.end, filter=self.filter,
                            dv_cutoff=self.dv_cutoff, max_interval=self.max_interval, min_height=self.min_height,\
                            min_peak=self.min_peak, thresh_frac=self.thresh_frac,\
                            reject_at_stim_start_interval=self.reject_at_stim_start_interval) # ipfx src code 
                
                df = ipfx.process(t = t, v = v, i = i)

                if not df.empty:  
                    df['sweep_number_supra'] = self.adjusted_sweepnumbers[sweep] # attach sweep number 
                    df_spikes = df_spikes.append(df, ignore_index = True)
                    
            ###################
            #spike features df 
            ###################
            if not df_spikes.empty: 
                return df_spikes
            else:
                return df_spikes_empty
        else:
            return df_spikes_empty 
        
        
    @property
    def process_spiketrain(self): 
        """ process spike train features for each sweep data """
        
        try: 
            isinstance(self.data, ABF)
            self.sweeptimes = find_sweeptimes(self.data)
            self.sweepdata = find_sweepdata(self.data)
            self.stimuli = find_stimuli(self.data)
            self.srate = find_srate(self.data)
            self.start = self.data.metadata['start_sec'] 
            self.end = self.data.metadata['end_sec']
            self._sweep_qc_spike 
        except: 
            raise AttributeError("pass single data object ...")   

        df_spiketrain = pd.DataFrame()
        df_spiketrain_empty = pd.DataFrame({'adapt': np.nan, 'latency': np.nan, 'isi_cv': np.nan,\
                                            'mean_isi': np.nan, 'median_isi': np.nan,\
                                            'first_isi': np.nan, 'avg_rate': np.nan, 'v_baseline': np.nan,\
                                            'pause': np.nan, 'burst': np.nan, 'delay': np.nan, 'spike_height_adaptation': np.nan,\
                                            'trough_adaptation': np.nan, 'upstroke_adaptation': np.nan,\
                                            'downstroke_adaptation': np.nan, 'stimulus': np.nan,\
                                            'sweep_number_supra': np.nan}, index = [0]) 
        
        if len(self.stable_sweepdata) > 0: 
            for t, v, i, sweep in zip(self.stable_sweeptimes, self.stable_sweepdata,\
                                        self.stable_stimuli, self.stable_sweepidx[0]): 
                
                # spike features 
                #---------------- 
                ipfx = SpikeFeatureExtractor(start=self.start, end=self.end, filter=None,
                            dv_cutoff=self.dv_cutoff, max_interval=self.max_interval, min_height=self.min_height,\
                            min_peak=self.min_peak, thresh_frac=self.thresh_frac,\
                            reject_at_stim_start_interval=self.reject_at_stim_start_interval) # ipfx src code 
                
                df_spikes = ipfx.process(t = t, v = v, i = i) # spike df per stable sweep 
                
                # spike train features
                #----------------------
                ipfx = SpikeTrainFeatureExtractor(start = self.start, end = self.end, burst_tol=self.burst_tol,\
                    pause_cost=self.pause_cost, baseline_interval=self.baseline_interval, filter_frequency=None, srate = self.srate)
                
                spiketrain_dict = ipfx.process(t = t, v = v, i = i, spikes_df = df_spikes,\
                                    extra_features=['v_baseline', 'pause', 'burst', 'delay'], exclude_clipped=False)
                
                # + adaptation features 
                #------------------------
                # calculate changes in spk height, 
                # trough adaptation ... across sweeps 
                
                spiketrain_dict['spike_height_adaptation'] = spikeheight_adaptation(df_spikes)
                spiketrain_dict['trough_adaptation'] = trough_adaptation(df_spikes)
                spiketrain_dict['upstroke_adaptation'] = upstroke_adaptation(df_spikes)
                spiketrain_dict['downstroke_adaptation'] = downstroke_adaptation(df_spikes)
                
                # + sweep info.
                #---------------
                spiketrain_dict['stimulus'] = max(i) # only depol sweeps 
                spiketrain_dict['sweep_number_supra'] = self.adjusted_sweepnumbers[sweep]
                
                df_spiketrain = df_spiketrain.append(pd.DataFrame(spiketrain_dict, index = [0]), ignore_index = True)

            #########################
            #spike train features df 
            #########################
            if not df_spiketrain.empty: 
                return df_spiketrain
            else: 
                return df_spiketrain_empty 
        else:
            return df_spiketrain_empty 
        
        
    def df_spikes_main(self, sweep_search = 'max_firing', i_search = None, fdir = None, fname = None, file_extension = '.xlsx'): 
        """ return df for selected sweep + attach features: rheobase """ 

        df_spikes = self.process_spikes
        df_spiketrain = self.process_spiketrain
        
        # + rheobase
        # used for rheobase sweep search 
        rheobase, rheobase_sweep_number = return_rheobase(df_spiketrain)
        
        # + metadata 
        df = pd.DataFrame(self.data.metadata, index = [0])

        # + preprocessing params 
        try: 
            self.data.preprocessed_params
            df = pd.concat([df, pd.DataFrame(self.data.preprocessed_params, index = [0])], axis = 1)
        except: 
            pass 
        
        # + sweep & spike features 
        #--------------------------
        # search for sweep and max amp spike 
        # features for sweeps at max firing, rheobase 
        # or closest to a set stimuli current  
        
        if (sweep_search == 'max_firing') and (i_search is None): 
            
            # sweep: max firing sweep 
            # spikes: max amp spike features @ max firing sweep 
            #----------------------------------------------------
            df_spiketrain, max_sweep_number = find_maxfiringsweep(df_spiketrain, df_spikes)
            df_spikes = find_maxampspikes(df_spikes, max_sweep_number)
            
            # find ap type
            #---------------
            # calculated on max firing sweep

            df_spiketrain['ap_type'] = return_aptype(df_spiketrain, self.min_peak, self.dv_cutoff, self.start, self.end)
            
        elif (sweep_search == 'rheobase') and (i_search is None): 
            
            # sweep: rheobase 
            # spikes: max amp spike features @ rheobase 
            #-------------------------------------------

            df_spikes = find_maxampspikes(df_spikes, rheobase_sweep_number)
            df_spiketrain = df_spiketrain[df_spiketrain.sweep_number_supra == rheobase_sweep_number]
            
        elif (sweep_search != 'rheobase') and (i_search is not None): 
            if isinstance(i_search, float) | isinstance(i_search, int): 
            
                # sweep: closest stimuli sweep to val 
                # spikes: max amp spikes on closest stimuli sweep
                #-------------------------------------------------
                
                df_spiketrain, closest_i_sweepnumber = find_closestcurrentsweep(df_spiketrain, df_spikes, i_search = i_search)
                df_spikes = find_maxampspikes(df_spikes, closest_i_sweepnumber)
            else: 
                raise TypeError(f'i_search {i_search} to be a float or int type ...')
                
        elif (sweep_search == 'rheobase') and (i_search is not None):
            if isinstance(i_search, float) | isinstance(i_search, int): 
                
                # sweep: closest stimuli sweep to i_search + rheobase
                # spikes: max amp spikes on i_search + rheobase sweep 
                #------------------------------------------------------

                df_spiketrain, closest_i_sweepnumber = find_closestcurrentsweep(df_spiketrain, df_spikes, i_search = (rheobase + i_search))
                df_spikes = find_maxampspikes(df_spikes, closest_i_sweepnumber)
            else: 
                raise TypeError(f'i_search {i_search} to be a float or int type ...')
        else: 
            raise ValueError(f'select a sweep search | sweep_search: {sweep_search} ...') 
        
        #-----------------------
        # + detection parameters 
        df['dv_cutoff'] = self.dv_cutoff
        df['max_interval'] = self.max_interval
        df['min_height'] = self.min_height
        df['min_peak'] = self.min_peak
        df['thresh_frac'] = self.thresh_frac
        df['reject_at_stim_start_interval'] = self.reject_at_stim_start_interval
        df['rms_cutoff'] = self.rms_cutoff
        df['burst_tol'] = self.burst_tol
        df['pause_cost '] = self.pause_cost 
        df['baseline_interval'] = self.baseline_interval

        # + qc parameters
        df['i_search_supra'] = i_search
        df['sweep_search_supra'] = sweep_search
        df['total_sweep_count'] = len(self.sweepdata)
        df['analysed_sweep_count'] = len(self.stable_sweepdata)
        
        # + rheobase
        df_spiketrain['rheobase'] = rheobase

        # concat dfs 
        #------------
        df = pd.concat([df.reset_index(drop = True), df_spikes.reset_index(drop = True), df_spiketrain.reset_index(drop = True)], axis = 1)
        df = df.rename(index={0: self.data.metadata['id']})
        df = df.loc[:,~df.columns.duplicated()].copy() # sanity check :: remove dup col // better way to do this? 
        
        # export
        if None not in [fdir, fname, file_extension]:
            export_df(data = self.data, df = df_spikes,\
                        fdir = fdir, fname = fname, file_extension = '.xlsx')
        else: 
            pass
    
        return df
        
        
    def df_spiketrain_allsweeps(self, fdir = None, fname = None, file_extension = '.xlsx'): 
        """ return df of spike train features across all 'stable' sweeps """
        
        df_spiketrain = self.process_spiketrain
        
        # export
        if None not in [fdir, fname, file_extension]:
            export_df(data = self.data, df = df_spiketrain,\
                        fdir = fdir, fname = fname, file_extension = '.xlsx')
        else: 
            pass
    
        return df_spiketrain
        
        
    def df_spikes_allsweeps(self, fdir = None, fname = None, file_extension = '.xlsx'): 
        """ return df of all spikes found across all 'stable' sweeps """
        
        df_spikes = self.process_spikes
        
        # export
        if None not in [fdir, fname, file_extension]:
            export_df(data = self.data, df = df_spikes,\
                        fdir = fdir, fname = fname, file_extension = '.xlsx')
        else: 
            pass
    
        return df_spikes
    
    
    @property
    def find_aptype(self): 
        """ sanity check :: return ap type of recording """
        
        df_spikes = self.process_spikes
        df_spiketrain = self.process_spiketrain
        
        # sweep: max firing sweep 
        # spikes: max amp spike features
        #--------------------------------
        df_spiketrain, max_sweep_number = find_maxfiringsweep(df_spiketrain, df_spikes)
        df_spikes = find_maxampspikes(df_spikes, max_sweep_number)

        return return_aptype(df_spiketrain, self.min_peak, self.dv_cutoff, self.start, self.end)
        
        
    @property
    def _sweep_qc_spike(self): 
        """ qc on sweepdata for rms stability + depol steps """
        
        # check for depolarization steps :: remove sweeps < 0 pA stimuli 
        self.depol_sweepdata, self.depol_sweeptimes,\
            self.depol_stimuli, self.adjusted_sweepnumbers = drop_hyperpolsweeps(self.sweepdata, self.sweeptimes, self.stimuli,\
                                                                                start = int(self.start*self.srate), end = int(self.end*self.srate))

        # remove unstable sweeps :: remove sweeps > rms cutoff 
        if self.rms_cutoff is not None: 
            if len(self.depol_sweepdata) > 0: 
                self.stable_sweepidx, self.stable_sweepdata, self.stable_sweeptimes,\
                    self.stable_stimuli = drop_unstablesweeps_rms(self.depol_sweepdata, self.depol_sweeptimes, self.depol_stimuli,\
                                                                end = self.end, srate = self.srate, rms_cutoff = self.rms_cutoff,\
                                                                baseline_interval = self.baseline_interval)
            else: 
                self.stable_sweepidx = []; self.stable_sweepdata = []; self.stable_sweeptimes = []; self.stable_stimuli = []
        else: 
            # set >> 10 if no stability to be checked
            raise ValueError(f'remove unstable sweeps for sag calculations | pass an rms cutoff: {self.rms_cutoff}') 

    
    def plot_spiketrain(self, sweeps = None, features = None, show_all_stable = False, xlim = None,\
                ylim_v = [None, None], ylim_i = [None, None], scale_bar = True, axis = False,\
                figdir = None, figname = None, figextension = None): 
        """ plot spike train on selected sweep """
        
        # check sweeps 
        if sweeps is not None: 
            pass
        else: 
            sweeps = self.stable_sweepidx[0] # default :: collect all stable
            
        # process spiketrain + spikes 
        df_spiketrain = self.process_spiketrain
        df_spikes = self.process_spikes
        
        # collect stable sweeps 
        if show_all_stable:
            stable_sweeps = self.stable_sweepidx[0]
            print(f'plotting stable sweeps | {self.adjusted_sweepnumbers[stable_sweeps]}')
        else: 
            stable_sweeps = None 
        
        if not df_spikes[df_spikes.sweep_number_supra.isin(sweeps)].empty:  
                
            # collect features from analysed sweeps 
            # find sweepnumber, index and plot color of features 
            #----------------------------------------------------
            if features is not None: 
                
                features_dict = {'peak_index':'red', 'upstroke_index':'blue',\
                                'downstroke_index':'green', 'threshold_index':'orange',\
                                'slow_trough_index':'yellow', 'fast_trough_index':'purple', 'trough_index':'pink'}
                
                features_label = []; features_sweep = []; features_index = []; features_color = []
                for feature in features: 
                    if feature == 'max_spike_index':  
                        for sweep in sweeps: 
                            df_spikes_filt = df_spikes[df_spikes.sweep_number_supra == sweep] 
                            if not df_spikes_filt.empty: 
                                df_maxamp_spike = find_maxampspikes(df_spikes, sweep)
                                features_index.append(df_maxamp_spike.peak_index.values) 
                                features_color.append('magenta')
                                features_sweep.append(sweep)
                                features_label.append(feature)
                            else: 
                                pass 

                    elif feature != 'max_spike_index':
                        if feature in list(features_dict.keys()): 
                            for sweep in sweeps: 
                                df_spikes_filt = df_spikes[df_spikes.sweep_number_supra == sweep] 
                                if not df_spikes_filt.empty:  
                                    for val in df_spikes_filt[feature].values:
                                        features_index.append(val) 
                                        features_color.append(features_dict[feature])
                                        features_sweep.append(sweep)
                                        features_label.append(feature) 
                                    else: 
                                        pass 
                                else: 
                                    print(f'no {feature} found to plot for sweep {sweep} ... ')
                        else: 
                            print(f'feature {feature} not an option for plotting ...')
                    else: 
                        print(f'feature {feature} not an option for plotting ...')
                else: 
                    pass 
                features_info = np.column_stack((features_sweep, features_index,\
                                                    features_color, features_label)) # feature info stack 
            else: 
                features_info = None
        else: 
            features_info = None 
            
        # plot spiketrain 
        spiketrain_plot(t = self.sweeptimes, i = self.stimuli, v = self.sweepdata, sweeps = sweeps,\
                xlim = xlim, ylim_v = ylim_v, ylim_i = ylim_i, stable_sweeps = stable_sweeps,\
                scale_bar = scale_bar, axis = axis, features_info = features_info,\
                start = self.start, end = self.end, min_peak = self.min_peak, figdir = figdir, figname = figname,\
                figextension = figextension) 
        
        
    def plot_spiketrain_allsweeps(self, show_all_stable = True, figdir = None, figname = None, figextension = None): 
        """ return plot of all sweeps """
        
        df_spikes = self.process_spikes
        df_spiketrain = self.process_spiketrain
        
        if ~np.isnan(df_spiketrain['avg_rate'].values[0]): 
        
            # collect stable sweeps 
            if show_all_stable:
                stable_sweeps = self.stable_sweepidx[0]
                print(f'plotting stable sweeps | {self.adjusted_sweepnumbers[stable_sweeps]}')
            else: 
                stable_sweeps = None 
            
            if len(self.sweepdata) > 0: 
                spiketrain_plot_allsweeps(t = self.sweeptimes, v = self.sweepdata, stable_sweeps = self.adjusted_sweepnumbers[stable_sweeps],\
                                        start = self.start, end = self.end, srate = self.srate,\
                                        figdir = figdir, figname = figname, figextension = figextension)
            else: 
                fname = self.data.metadata['id']
                print(f'no sweep data to plot for {fname} ...')
        else: 
            print('no spike features found ...')
        
        
    def plot_spike(self, sweep = None, spike = 0, slice_window = [-0.008, 0.01], axis = False,\
                    ylim_phase = [None, None], xlim_phase = [None, None], scale_bar = True,\
                    ylim_v = [None, None], figdir = None, figname = None, figextension = '.pdf'): 
        """ plot spike on selected sweep """
        
        # check sweep type 
        if sweep is not None: 
            if isinstance(sweep, int): 
                pass
            else: 
                raise TypeError('pass sweep as an int type ...')
        else: 
            raise ValueError('pass a sweep number ...')
        
        # check spike type 
        if spike is not None: 
            if isinstance(spike, int): 
                pass
            elif isinstance(spike, str): 
                if spike == 'max_ap': 
                    pass
            else: 
                raise TypeError('pass spike as an int type or max_ap for max selection ...')
        else: 
            raise ValueError('pass a spike number ...')
        
        # collect spike featues 
        df_spikes = self.process_spikes

        # filter for selected sweeps 
        df_spikes = df_spikes[df_spikes.sweep_number_supra == sweep] 
        
        if len(df_spikes) > 0: 
            if spike != 'max_ap': # find spike index 
                try:  
                    peak_index = df_spikes.peak_index.values[spike] 
                except IndexError: 
                    pass
                
            elif spike == 'max_ap': 
                peak_index = df_spikes[df_spikes.peak_v == max(df_spikes.peak_v)].peak_index.values[0] # spike index 
            else: 
                raise IndexError(f'no spike {spike} found for sweep {sweep} | try a different spike and/or sweep ...')
                
            if peak_index: 
                spike_plot(i = self.stimuli, v = self.sweepdata,\
                            peak_index = peak_index, sweep = sweep, slice_window = slice_window,\
                            srate = self.srate, axis = axis, min_peak = self.min_peak, scale_bar = scale_bar,\
                            ylim_v = ylim_v, figdir = figdir, figname = figname, figextension = figextension,\
                            ylim_phase = ylim_phase, xlim_phase = xlim_phase) # spike + phase plot 
            else: 
                raise ValueError(f'peak {spike} not found ...')
        
        else: 
            print(f'no spike found for sweep {sweep} ...')
            pass 
        
        
    def plot_i_f(self, figdir = None, figname = None, figextension = None): 
        """ return plot for current vs frequency relationship """
        
        df_spikes = self.process_spikes
        df_spiketrain = self.process_spiketrain
        
        i = df_spiketrain.stimulus.values
        f = df_spiketrain.avg_rate.values
        
        # + rheobase
        rheobase, _ = return_rheobase(df_spiketrain) 
        
        # + max firing 
        df_spiketrain, max_sweep_number = find_maxfiringsweep(df_spiketrain, df_spikes)
        df_spikes = find_maxampspikes(df_spikes, max_sweep_number)
            
        if not df_spiketrain.empty: 
            i_f_plot(i = i, f = f, rheobase = rheobase, max_firing = df_spiketrain.avg_rate.values[0],\
                figdir = figdir, figname = figname, figextension = figextension)
        else: 
            fname = self.data.metadata['id']
            print(f'no i-f data to plot for {fname} ...')
        

