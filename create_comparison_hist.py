import os
import sys
import glob
import numpy  as np
import tables as tb
import pandas as pd

import invisible_cities.io.dst_io as dio

#path of the current file, added to pythonpath to use the functions
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

#imports of other files here
from utils_hist import *

from city_hist.pmaps_hist import pmaps_file_writer
from city_hist.kdst_hist  import kdst_file_writer
from city_hist.chits_hist   import chits_file_writer
from city_hist.tracks_hist import tracks_file_writer
from city_hist.deco_hist   import deco_file_writer

#NEEDED VARIABLES
data_path = '/analysis/14776/hdf5/prod/' #path to old and refactor prod

old_path = data_path +  'v2.1.0/20241114/irene/trigger0/'
ref_path = data_path + 'masking/20241114/irene/trigger0/'

#cities forlders should be in lower case: hypathia, penthesilea/sophronia, esmeralda, beersheba, isaura
cities = ['irene']

#FILE NAME FOR THE FIRST HISTOGRAMS
hist_file = 'hist.h5' #str filled with first 3 letters of the correspondent city
old_hist = old_path + hist_file
ref_hist = ref_path + hist_file

out_file = 'irene_comp.h5'


#STARTUP
#PICKING ALL THE FILES (OLD AND REFACTOR) TO RE-DO THE HISTOGRAMS
old_files = old_path + 'ldc1/*.h5'
ref_files = ref_path + 'ldc1/*.h5'

out_path = data_path + out_file

hist_dict = {'hypathia':    pmaps_file_writer,
             'irene':    pmaps_file_writer,
             'penthesilea': kdst_file_writer,
             'sophronia':   kdst_file_writer,
             'esmeralda':   (chits_file_writer, tracks_file_writer),
             'beersheba':   deco_file_writer,
             'isaura':      tracks_file_writer}

order_dict = {'hypathia':  hyp_order_list,
              'irene':  ire_order_list,
              'penthesilea': pen_order_list, #same for sophronia
              'esmeralda':esm_order_list,
              'beersheba':bee_order_list,
              'isaura':esm_order_list[19:]}

#START OF THE SCRIPT
if __name__ == "__main__":

    #HYPATHIA
    if np.isin(cities, 'hypathia').any():
        #We read the statistics files and search for xlims that agree in both mirror histograms
        old_hist = old_hist.format('hyp')
        ref_hist = ref_hist.format('hyp')
        out_path = out_path.format('hyp')
        xlims = common_xlims(old_hist, ref_hist, order_dict['hypathia'])
        #We now recalculate with the new lims
        hist_dict['hypathia'](old_files, out_path, city = 'hypathia', tag = 'old', xrange = xlims)
        hist_dict['hypathia'](ref_files, out_path, city = 'hypathia', tag = 'ref', xrange = xlims)

    if np.isin(cities, 'irene').any():
        #We read the statistics files and search for xlims that agree in both mirror histograms
        xlims = common_xlims(old_hist, ref_hist, order_dict['irene'])
        #We now recalculate with the new lims
        hist_dict['irene'](old_files, out_path, city = 'irene', tag = 'v2.1.0', xrange = xlims)
        hist_dict['irene'](ref_files, out_path, city = 'irene', tag = 'masking', xrange = xlims)

    #PENTHESILEA / SOPHRONIA
    if np.isin(cities, 'penthesilea').any():
        old_hist = old_hist.format('pen')
        ref_hist = ref_hist.format('sop')
        out_path = out_path.format('pen')
        xlims = common_xlims(old_hist, ref_hist, order_dict['penthesilea'])
        #no tag needed as names are different
        hist_dict['penthesilea'](old_files, out_path, city = 'penthesilea', xrange = xlims)
        hist_dict['sophronia'](ref_files, out_path, city = 'sophronia', xrange = xlims)

    #ESMERALDA
    if np.isin(cities, 'esmeralda').any():
        old_hist = old_hist.format('esm')
        ref_hist = ref_hist.format('esm')
        out_path = out_path.format('esm')
        xlims = common_xlims(old_hist, ref_hist, order_dict['esmeralda'])

        #Careful here using the xlim because there are some lims for the chits part and some for the tracks one!
        hist_dict['esmeralda'][0](old_files, out_path, 'highTh', city = 'esmeralda', tag = 'old', xrange = xlims[0:18])
        hist_dict['esmeralda'][1](old_files, out_path, city = 'esmeralda', tag = 'old', xrange = xlims[18:])
        hist_dict['esmeralda'][0](old_files, out_path, 'lowTh', city = 'esmeralda', tag = 'old')

        hist_dict['esmeralda'][0](ref_files, out_path, 'highTh', city = 'esmeralda', tag = 'ref', xrange = xlims[0:18])
        hist_dict['esmeralda'][1](ref_files, out_path, city = 'esmeralda', tag = 'ref', xrange = xlims[18:])

    #BEERSHEBA
    if np.isin(cities, 'beersheba').any():
        old_hist = old_hist.format('bee')
        ref_hist = ref_hist.format('bee')
        out_path = out_path.format('bee')
        xlims = common_xlims(old_hist, ref_hist, order_dict['beersheba'])

        hist_dict['beersheba'](old_files, out_path, city = 'beersheba', tag = 'old', xrange = xlims)
        hist_dict['beersheba'](ref_files, out_path, city = 'beersheba', tag = 'ref', xrange = xlims)

    #ISAURA
    if np.isin(cities, 'isaura').any():
        old_hist = old_hist.format('isa')
        ref_hist = ref_hist.format('isa')
        out_path = out_path.format('isa')
        xlims = common_xlims(old_hist, ref_hist, order_dict['isaura'])


        hist_dict['isaura'](old_files, out_path, city = 'isaura', tag = 'old', xrange = xlims)
        hist_dict['isaura'](ref_files, out_path, city = 'isaura', tag = 'ref', xrange = xlims)
