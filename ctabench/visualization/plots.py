import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


__all__ = [
    'plot_binned_mean'
]

def plot_binned_mean(x, y, ax=None, errorbar=True, bins=20, **kwargs):
    """
    Plot binned statistics
    """

    ax = plt.gca() if ax is None else ax

    bin_means, bin_edges, binnumber = stats.binned_statistic(x, y, statistic='mean', bins=bins)
    bin_width = (bin_edges[1] - bin_edges[0])
    bin_centers = bin_edges[1:] - bin_width / 2

    bin_with_data = np.unique(binnumber) - 1
    bin_r68 = np.array([np.percentile(np.abs(y[binnumber == i] - bin_means[i - 1]), 68)
                        for i in set(binnumber)])

    if errorbar:
        ax.hlines(bin_means, bin_edges[:-1], bin_edges[1:], **kwargs)

        # poping label from kwargs so it does not appear twice
        if 'label' in kwargs:
            kwargs.pop('label')

        ax.vlines(bin_centers[bin_with_data],
                  bin_means[bin_with_data] - bin_r68,
                  bin_means[bin_with_data] + bin_r68,
                  **kwargs,
                  )
    else:
        ax.scatter(bin_centers[bin_with_data],
                   bin_means[bin_with_data],
                   **kwargs,
                   )
    return ax
