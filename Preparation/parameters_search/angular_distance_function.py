"""
Module with basics function to calculate angular distance between the array that points to the origin
of the proton's shower and the array reconstructed with the hillas_dictionary

"""

from astropy.coordinates import SkyCoord, AltAz
from ctapipe.reco import HillasReconstructor
from ctapipe.reco.reco_algorithms import TooFewTelescopesException, InvalidWidthException


def angular_distance(event, hillas_containers):
    """
    find the angular distance between the true array that point to the origin of
    the shower of protons and the predicted point.

    Parameters
    ----------

    event :
        calibrated event

    hillas_containers :
        dictionary with telescope IDs as key and
        HillasParametersContainer instances as values

    Returns
    -------

    angular_distance:
        angular distance(in degrees) or False if the reconstruction can't be done due
        TooFewTelescopesException or InvalidWidthException

    """
    horizon_frame = AltAz()
    reco = HillasReconstructor()

    # SkyCoord
    array_pointing_event = SkyCoord(
        az=event.mcheader.run_array_direction[0],
        alt=event.mcheader.run_array_direction[1],
        frame=horizon_frame
    )

    try:

        reconstruction_cleaned = reco.predict(
            hillas_containers,
            event.inst,
            array_pointing_event,
        )

    except TooFewTelescopesException:
        return False

    except InvalidWidthException:
        return False

    array_pointing_reconstruction = SkyCoord(
        az=reconstruction_cleaned.az,
        alt=reconstruction_cleaned.alt,
        frame=horizon_frame
    )

    # angular distance between reconstructed and event image
    ang_dist = array_pointing_event.separation(array_pointing_reconstruction)
    return ang_dist
