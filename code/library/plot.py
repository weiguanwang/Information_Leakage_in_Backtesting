
import matplotlib.pyplot as plt
from pandas.tseries.offsets import BDay

from .bs import simulate_geometric_bm


#plots in-sample path and multiple out-of-sample paths for simulation data
def plot_stock_test_prices(
        path,
        underlying_params,
        n_ofTestDays,
        date_break,
        index_end_date):
    fig_sim, ax_sim = plt.subplots()
    path['S0'].plot(ax=ax_sim, legend=False)
    underlying_params['s0'] = path['S0'].iloc[-1]
    underlying_params['start_date'] = underlying_params['end_date'] + BDay()
    underlying_params['end_date'] = underlying_params['end_date'] + n_ofTestDays

    
    for i in range(10):
        simulate_geometric_bm(underlying_params).plot(
            ax=ax_sim,
            legend=False,
            alpha=0.5
        )  

    ax_sim.annotate(
        'Training',
        xy=(0.4, 0.05),
        xytext=(0.4, 0),
        xycoords='axes fraction',
        ha='center',
        va='bottom')
    #  arrowprops=dict(arrowstyle='-[, widthB=11.0, lengthB=.5', lw=1.5)
    ax_sim.annotate(
        'Validation',
        xy=(0.75, 0.05),
        xytext=(0.75, 0),
        xycoords='axes fraction',
        ha='center',
        va='bottom')
    ax_sim.annotate(
        'Test',
        xy=(0.91, 0.05),
        xytext=(0.91, 0),
        xycoords='axes fraction',
        ha='center',
        va='bottom')
    ax_sim.axvline(index_end_date, color='black', linestyle='dashed', alpha=0.6)
    ax_sim.axvline(date_break, color='black', linestyle='dashed', alpha=0.6)

