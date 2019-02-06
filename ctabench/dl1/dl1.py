import numpy as np

__all__ = [
    'true_pe_cleaning',
    'signal_calibrated_image',
    'noise_calibrated_image',
]


def true_pe_cleaning(pe_image):
    """
    Return a mask selecting pixels containing signal based on the true p.e. image.

    Parameters
    ----------
    pe_image: `numpy.ndarray`

    Returns
    -------
    `numpy.ndarray`
    """
    return pe_image > 0

def noise_calibrated_image(calibrated_event, tel_id, channel=0):
    """
    This function select pixels that contain only noise based on the true pe image
    and return the masked calibrated image of these pixels

    Parameters
    ----------
    calibrated_event: `ctapipe.io.containers.DataContainer`
    tel_id: int
    channel: int - gain channel

    Returns
    -------
    `numpy.ma.array` - masked array
    """
    pe_image = calibrated_event.mc.tel[tel_id].photo_electron_image
    signal_pixels = true_pe_cleaning(pe_image)
    image = calibrated_event.dl1.tel[tel_id].image[channel]
    return np.ma.array(image, mask=signal_pixels)

def signal_calibrated_image(calibrated_event, tel_id, channel=0):
    """
    This function select pixels containing signal based on the true pe image
    and return the masked calibrated image of these pixels

    Parameters
    ----------
    calibrated_event: `ctapipe.io.containers.DataContainer`
    tel_id: int
    channel: int - gain channel

    Returns
    -------
    `numpy.ma.array` - masked array
    """
    pe_image = calibrated_event.mc.tel[tel_id].photo_electron_image
    signal_pixels = true_pe_cleaning(pe_image)
    image = calibrated_event.dl1.tel[tel_id].image[channel]
    return np.ma.array(image, mask=~signal_pixels)


def difference_calibrated_true_pe(calibrated_event, tel_id, channel=0):
    """

    Parameters
    ----------
    calibrated_event
    tel_id
    channel

    Returns
    -------

    """