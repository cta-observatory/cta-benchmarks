import numpy as np

__all__ = [
    'tel_to_impact_point_distance'
]

def tel_to_impact_point_distance(event, subarray, tel_id):
    """
    Return the distance from the shower impact point to the telescope.

    Parameters
    ----------
    event: `ctapipe.io.containers.DataContainer`
    tel_id: int

    Returns
    -------
    `astropy.units.Quantity`
    """
    return np.sqrt((event.mc.core_x - subarray.positions[tel_id][0]) ** 2
                   + (event.mc.core_y - subarray.positions[tel_id][1]) ** 2)
