import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec
import matplotlib
from datetime import datetime
import matplotlib.colors as colors

def save_fig(data_h, data_dep, error, filename, type1):
    fig = plt.figure(figsize=[2,2], constrained_layout=True)
    ax = fig.add_subplot(111)
    ax.hist(data_h, 8, color=(140./255,21./255,21./255), alpha=0.7, histtype='stepfilled', align='mid', label='Accuracy Error')
    ax.hist(data_dep,  8, alpha=0.7, histtype='stepfilled', align='mid', label='Precision Error')
    #ax.hist(data_h, num_bin, color=(140./255,21./255,21./255), alpha=0.7, histtype='stepfilled', align='mid', label='Hori.')
    if type1 == 1: # (accuracy)
        ax.set_xlim(0, 7)

    elif type1 == 2: # (precision)
        ax.set_xlim(0,9)
        
    #ax.set_xlabel(error+'(km)', labelpad=0.05, fontsize=6,fontweight='bold')
    ax.legend(loc='upper right', prop = { "size": 6,'weight':'bold' })
    #ax.set_ylabel('Occurrence', fontsize=6, labelpad=0.3,fontweight='bold')
    ax.set_yscale('log')
    ax.set_ylim(0,1200)
    #ax.set_xlim(x_range)
    ax.xaxis.set_tick_params(labelsize=8)
    ax.yaxis.set_tick_params(labelsize=8)
    ax.set_yticklabels(ax.get_yticks(), weight='bold')
    ax.set_xticklabels(ax.get_xticks(), weight='bold')
    plt.savefig('./hist/'+filename, dpi=400, transparent=True)
    plt.close()
    return 0

r_h_df = pd.read_csv('relative_error_hori.csv')
r_z_df = pd.read_csv('relative_error_depth.csv')
a_h_df = pd.read_csv('absolute_error_hori.csv')
a_z_df = pd.read_csv('absolute_error_depth.csv')


# histogram of error of hypodd
save_fig(a_h_df['hypoDD'],r_h_df['hypoDD'], 'Horizontal Error', 'dd_hori_hist.png', 1)
save_fig(a_z_df['hypoDD'], r_z_df['hypoDD'],'Depth Error','dd_depth_hist.png', 2)

# histogram of error of gc
save_fig(a_h_df['growclust'],r_h_df['growclust'], 'Horizontal Error', 'gc_hori_hist.png', 1)
save_fig(a_z_df['growclust'], r_z_df['growclust'],'Depth Error','gc_depth_hist.png', 2)



# histogram of error of velest
save_fig(a_h_df['velest'],r_h_df['velest'], 'Horizontal Error', 'v_hori_hist.png', 1)
save_fig(a_z_df['velest'], r_z_df['velest'],'Depth Error','v_depth_hist.png', 2)


# histogram of error of hypoinverse
save_fig(a_h_df['hypoinverse'],r_h_df['hypoinverse'], 'Horizontal Error', 'h_hori_hist.png', 1)
save_fig(a_z_df['hypoinverse'], r_z_df['hypoinverse'],'Depth Error','h_depth_hist.png', 2)



# histogram of error of nonlinloc
save_fig(a_h_df['NonLinLoc'],r_h_df['NonLinLoc'], 'Horizontal Error', '_nll_hori_hist.png', 1)
save_fig(a_z_df['NonLinLoc'], r_z_df['NonLinLoc'],'Depth Error','_nll_depth_hist.png', 2)

# histogram of error of xcroloc
save_fig(a_h_df['xcorloc'],r_h_df['xcorloc'], 'Horizontal Error', 'xc_hori_hist.png', 1)
save_fig(a_z_df['xcorloc'], r_z_df['xcorloc'],'Depth Error','xc_depth_hist.png', 2)

# histogram of error of hyposvi
save_fig(a_h_df['HypoSVI'],r_h_df['HypoSVI'], 'Horizontal Error', 'svi_hori_hist.png',1)
save_fig(a_z_df['HypoSVI'],r_z_df['HypoSVI'],'Depth Error','svi_depth_hist.png',2)
