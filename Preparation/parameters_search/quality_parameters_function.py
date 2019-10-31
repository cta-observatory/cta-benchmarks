"""
Module with the basic function for the optimization of quality parameters for the image cleaning
after the calibration of the events.
(we are processing in the DL1 data level)
"""

from ctapipe.image.cleaning import tailcuts_clean
import numpy as np
from ctapipe.image import hillas_parameters
from astropy import units as u
from scipy.spatial.distance import cdist


def create_possible_parameters():
    """
    compute all the possible cleaning levels and
    does the storage in a numpy array.

    Parameters
    ----------

    Returns
    -------

    possible_cleaning_levels:
        array with all the possible cleaning levels chosen

    """
    # cleaning levels with minimum neighbors set to 0
    picture_range = np.arange(1, 10, 0.25, dtype=np.float32)
    boundary_range = np.arange(2, 20, 0.5, dtype=np.float32)
    min_neighbors_range = np.zeros(len(picture_range), dtype=np.int)
    possible_cleaning_levels_0 = np.c_[picture_range, boundary_range, min_neighbors_range]

    # cleaning levels with minimum neighbors set to 1
    min_neighbors_range = np.ones(len(picture_range), dtype=np.int)
    possible_cleaning_levels_1 = np.c_[picture_range, boundary_range, min_neighbors_range]

    # cleaning levels with minimum neighbors set to 2
    min_neighbors_range = np.multiply(min_neighbors_range, 2, dtype=np.int)
    possible_cleaning_levels_2 = np.c_[picture_range, boundary_range, min_neighbors_range]

    # cleaning levels with minimum neighbors set to 3
    min_neighbors_range = np.ones(len(picture_range), dtype=np.int)
    min_neighbors_range = np.multiply(min_neighbors_range, 3)
    possible_cleaning_levels_3 = np.c_[picture_range, boundary_range, min_neighbors_range]

    possible_cleaning_levels = np.append(possible_cleaning_levels_0, possible_cleaning_levels_1, axis=0)
    possible_cleaning_levels = np.append(possible_cleaning_levels, possible_cleaning_levels_2, axis=0)
    possible_cleaning_levels = np.append(possible_cleaning_levels, possible_cleaning_levels_3, axis=0)

    return possible_cleaning_levels


def closest_distance(center, line):
    """
    find the minimum distance between a set of points(line) and a point(center)

    Parameters
    ----------

    center :
        reference point

    line :
        a numpy array

    Returns
    -------

    distance:
        minimum distance

    """
    distance = cdist([center], line).min()
    return distance


def closest_approach_distance(hillas_container):
    """
    find the closest distance between the straight line
    corresponding to the major axis of an ellipse and the center of an image(cameraGeometry like)

    Parameters
    ----------

    hillas_container :
        dictionary with telescope IDs as key and
        HillasParametersContainer instances as values


    Returns
    -------

    close_dist:
        the closest approach calculated in meters

    """
    length = np.linspace(-1, 1, 30)
    length = u.Quantity(length, u.m, copy=False)

    y = hillas_container.y + length * np.sin(hillas_container.psi)
    x = hillas_container.x + length * np.cos(hillas_container.psi)

    center = (0, 0)

    line = np.array([x, y])
    line = line.T

    closest_approach = closest_distance(center, line)
    closest_approach = u.Quantity(closest_approach, u.m)

    return closest_approach


#  WARNING! using the sum we consider in the likelihood function the noise added to the image that remains after
#  the cleaning
def likelihood_function(event, cleaned_image, telescope_id):
    """
    returns a number that has to be compared with another likelihood to find which image has a better approximation of
    the ground truth image after the cleaning

    Parameters
    ----------

    event :
        calibrated event

    cleaned_image :
        dictionary with telescope IDs as key and
        HillasParametersContainer instances as values

    telescope_id:
        unique number for the identification of a telescope

    Returns
    -------
    likelihood:
        a scalar number that represent the sum of all the differences between ground truth and cleaned image

    """
    ground_truth_image = event.mc.tel[telescope_id].photo_electron_image

    diff = np.abs(cleaned_image - ground_truth_image)
    likelihood = diff.sum()

    return likelihood


def numbers_of_different_pixels(camera, event, cleaned_image, telescope_id, picture, boundary, min_neighbors):
    """
    find a quality parameter that is the representation of the number of pixels survived in cleaned image but
    not in cleaned ground truth image or vice versa.
    The cleaned ground truth is needed to have a logic correlation (independence from noise) between the 2 images that
    has to be compared.

    Parameters
    ----------

    camera:
        Camera geometry information

    picture:
        picture threshold for the tailcuts cleaning

    boundary:
        boundary threshold for the tailcuts cleaning

    min_neighbors:
        minimum number of neighbors in the picture for the tailcuts cleaning

    event :
        calibrated event

    cleaned_image :
        dictionary with telescope IDs as key and
        HillasParametersContainer instances as values

    telescope_id:
        unique number for the identification of a telescope

    Returns
    -------
    number_difference_pixels_survived:
        a scalar number that represent the counting of all the pixels that are in the cleaned image or
        in the cleaned ground truth BUT not in both of them

    """
    ground_truth_image = event.mc.tel[telescope_id].photo_electron_image

    clean = tailcuts_clean(
        camera,
        ground_truth_image,
        boundary_thresh=boundary,
        picture_thresh=picture,
        min_number_picture_neighbors=min_neighbors
    )
    cleaned_ground_truth = ground_truth_image.copy()
    cleaned_ground_truth[~clean] = 0.0

    pixels_survived_image_cleaning = cleaned_image > 0
    pixels_survived_ground_truth_cleaning = cleaned_ground_truth > 0

    difference_pixels_survived = np.logical_xor(pixels_survived_image_cleaning, pixels_survived_ground_truth_cleaning)
    number_difference_pixels_survived = np.count_nonzero(difference_pixels_survived)

    return number_difference_pixels_survived


def verify_size_clean_mask(clean_mask, size):
    """

    Verify that the cleaning returns an image with a size <of the size parameter

    Parameters
    ----------

    clean_mask:
        array of boolean elements that describes the pixels that have survived the cleaning

    size:
        number chosen for the minimum sum of the pixels survived

    Returns
    -------

    flag:
        boolean true or boolean false

    """
    if clean_mask.sum() < size:
        flag = True
    else:
        flag = False
    return flag


def verify_threshold(closest_approach, likelihood, difference_pixels_survived):
    """

    Verify that a set of quality parameters meets the fixed limits

    Parameters
    ----------

    closest_approach:
        quality parameter (see closest_approach_distance)


    likelihood:
        quality parameter (see likelihood_function)


    difference_pixels_survived:
        quality parameter (see numbers_of_different_pixels)

    Returns
    -------

    outcome:
        boolean true or boolean false

    """
    # TODO thresholds for the quality(adjust parameters!)
    limit_closest_approach = u.Quantity(1, u.m)
    limit_likelihood = 100
    limit_difference_pixels_survived = 5

    if (closest_approach <= limit_closest_approach) and (likelihood <= limit_likelihood) and \
            (difference_pixels_survived <= limit_difference_pixels_survived):
        outcome = True
    else:
        outcome = False

    return outcome


def optimize_param(quality_param_list, index):  # TODO test if this is enough to discriminate(may be too restrictive)
    """

    Find the index of the best parameters in the quality_param_list.
    This is the same index that define the best cleaning levels in the list of all the possible cleaning levels

    Parameters
    ----------

    quality_param_list:
        list of all the quality parameters of a cleaned image for all the possible cleaning levels chosen

    index:
        index of the current quality parameters chosen for the comparision

    Returns
    -------

    new_index:
        index of the row with the better quality parameters

    """
    if index == 0:
        return quality_param_list[index]
    else:
        closest_approach = quality_param_list[index][0]
        likelihood = quality_param_list[index][1]
        num_diff_pixels = quality_param_list[index][2]

        closest_approach_previous = quality_param_list[index - 1][0]
        likelihood_previous = quality_param_list[index - 1][1]
        num_diff_pixels_previous = quality_param_list[index - 1][2]

        if (closest_approach <= closest_approach_previous) and (likelihood <= likelihood_previous) \
                and (num_diff_pixels <= num_diff_pixels_previous):
            new_index = index
        else:
            new_index = index - 1

        return new_index


def iterate_param(possible_cleaning_levels, event, camera, image, telescope_id,
                  quality_param_list, hillas_containers, index=0):
    """

    iteration of the possible cleaning levels and research of the optimal through quality parameters

    Parameters
    ----------

    possible_cleaning_levels:
        array with all the possible cleaning levels chosen

    event:
        calibrated event

    camera:
        Camera geometry information

    image:
        pixel array that has to be cleaned

    telescope_id:
        unique number for the identification of a telescope

    quality_param_list:
        list of all the quality parameters of a cleaned image for all the possible cleaning levels chosen

    hillas_containers:
        dictionary with telescope IDs as key and
        HillasParametersContainer instances as values

    index:
        index of the current cleaning level chosen for the comparision

    Returns
    -------

    new_param:
        the better parameters for the given image

    """
    while index < len(possible_cleaning_levels):

        picture, boundary, min_neighbors = possible_cleaning_levels[index]

        clean = tailcuts_clean(
            camera,
            image,
            boundary_thresh=boundary,
            picture_thresh=picture,
            min_number_picture_neighbors=min_neighbors
        )

        # if the size of the clean mask is too little, we can't have a good ellipse reconstruction
        flag = verify_size_clean_mask(clean, 6)
        if flag:
            break

        cleaned_image = event.dl1.tel[telescope_id].image.copy()
        cleaned_image[~clean] = 0.0

        hillas_c = hillas_parameters(camera[clean], image[clean])
        hillas_containers[telescope_id] = hillas_c

        closest_approach = closest_approach_distance(hillas_containers[telescope_id])

        likelihood = likelihood_function(event, cleaned_image, telescope_id)

        num_diff_pixels = numbers_of_different_pixels(camera, event, cleaned_image, telescope_id, picture, boundary
                                                      , min_neighbors)

        quality_param_list.append([closest_approach, likelihood, num_diff_pixels])

        index_best_parameters = optimize_param(quality_param_list, index)

        index = index + 1

    new_param = possible_cleaning_levels[index_best_parameters]

    return new_param


def calc_mean_std(cleaning_levels_list, decimals=1):
    """
    calculate mean and standard deviation of a cleaning level list for a telescope type

    Parameters
    ----------

    cleaning_levels_list:
        list of the optimized cleaning levels of a telescope type for the current event

    decimals:
        the round decimal approximation needed for the rounding of the mean and std

    Returns
    -------

    mean:
        tuple of the mean for each cleaning threshold

    std:
        tuple of the standard deviation for each cleaning threshold

    """
    cleaning_levels_list = np.array(cleaning_levels_list, copy=False)

    mean_picture_threshold = cleaning_levels_list[:, [0]].mean()
    mean_boundary_threshold = cleaning_levels_list[:, [1]].mean()
    mean_min_neighbors = cleaning_levels_list[:, [2]].mean()

    mean_picture_threshold = round(mean_picture_threshold, decimals)
    mean_boundary_threshold = round(mean_boundary_threshold, decimals)
    mean_min_neighbors = round(mean_min_neighbors)

    std_picture_threshold = cleaning_levels_list[:, [0]].std()
    std_boundary_threshold = cleaning_levels_list[:, [1]].std()
    std_min_neighbors = cleaning_levels_list[:, [2]].std()

    std_picture_threshold = round(std_picture_threshold, decimals)
    std_boundary_threshold = round(std_boundary_threshold, decimals)
    std_min_neighbors = round(std_min_neighbors, decimals)

    mean = (mean_picture_threshold, mean_boundary_threshold, mean_min_neighbors)
    std = (std_picture_threshold, std_boundary_threshold, std_min_neighbors)

    return mean, std
