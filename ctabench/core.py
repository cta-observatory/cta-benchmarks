import numpy as np

__all__ = [
    'tel_to_impact_point_distance'
]

def tel_to_impact_point_distance(event, tel_id):
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
    tel_index = event.inst.subarray.tel_indices[tel_id]
    return np.sqrt((event.mc.core_x - event.inst.subarray.tel_coords.x[tel_index]) ** 2
                   + (event.mc.core_y - event.inst.subarray.tel_coords.y[tel_index]) ** 2)