import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec
import matplotlib
from datetime import datetime
import matplotlib.colors as colors

def save_fig(data_h, data_dep, x_range, num_bin, xlabel, filename):
    fig = plt.figure(figsize=[2,2], constrained_layout=True)
    ax = fig.add_subplot(111)
    ax.hist(data_h, num_bin, color=(140./255,21./255,21./255), alpha=0.7, histtype='stepfilled', align='mid', label='Hori.')
    ax.hist(data_dep, num_bin,  alpha=0.7, histtype='stepfilled', align='mid', label='Depth')
    #ax.hist(data_h, num_bin, color=(140./255,21./255,21./255), alpha=0.7, histtype='stepfilled', align='mid', label='Hori.')
    
    ax.set_xlabel(xlabel, labelpad=0.05, fontsize=6)
    ax.legend(loc='upper right', fontsize=4)
    ax.set_ylabel('Frequency', fontsize=6, labelpad=0.3)
    ax.set_yscale('log')
    #ax.set_xlim(x_range)
    ax.xaxis.set_tick_params(labelsize=5)
    ax.yaxis.set_tick_params(labelsize=5)

    plt.savefig('./hist/'+filename, dpi=300, transparent=True)
    plt.close()
    return 0

r_h_df = pd.read_csv('relative_error_hori.csv')
r_z_df = pd.read_csv('relative_error_depth.csv')
a_h_df = pd.read_csv('absolute_error_hori.csv')
a_z_df = pd.read_csv('absolute_error_depth.csv')


# histogram of error of hypodd
save_fig(r_h_df['hypoDD'],r_z_df['hypoDD'], [0, 1.0], 20, 'Relative Error (km)', 'dd_rela_hist.pdf')
save_fig(a_h_df['hypoDD'], a_z_df['hypoDD'],[0, 2.0], 20, 'Absolute Error (km)','dd_abso_hist.pdf')

# histogram of error of gc
save_fig(r_h_df['growclust'],r_z_df['growclust'], [0, 1.0], 20, 'Relative Error (km)', 'gc_rela_hist.pdf')
save_fig(a_h_df['growclust'], a_z_df['growclust'],[0, 2.0], 20, 'Absolute Error (km)','gc_abso_hist.pdf')


# histogram of error of velest
save_fig(r_h_df['velest'], r_z_df['velest'], [0, 1.0], 20, 'Relative Error (km)', 'v_rela_hist.pdf')
save_fig(a_h_df['velest'], a_z_df['velest'], [0, 2.0], 20, 'Absolute Error (km)','v_abso_hist.pdf')


# histogram of error of hypoinverse
save_fig(r_h_df['hypoinverse'], r_z_df['hypoinverse'], [0, 1.0], 20, 'Relative Error (km)', 'h_rela_hist.pdf')
save_fig(a_h_df['hypoinverse'], a_z_df['hypoinverse'], [0, 2.0], 20, 'Absolute Error (km)','h_abso_hist.pdf')



# histogram of error of nonlinloc
save_fig(r_h_df['NonLinLoc'], r_z_df['NonLinLoc'], [0, 1.0], 20, 'Relative Error (km)', 'nll_rela_hist.pdf')
save_fig(a_h_df['NonLinLoc'], a_z_df['NonLinLoc'], [0, 2.0], 20, 'Absolute Error (km)','nll_abso_hist.pdf')
