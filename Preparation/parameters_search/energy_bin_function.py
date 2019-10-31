"""
Module with the basics functions to set the energy bin
for the optimization of quality parameters discriminated by
the energy of the event

"""


import numpy as np
from astropy import units as u
import os


def create_energy_bin_array(minimum=1, maximum=1300, num_bins=10):

    energy_bin = np.logspace(np.log10(minimum), np.log10(maximum), num_bins)
    energy_bin = np.around(energy_bin, 2)
    energy_bin = u.Quantity(energy_bin, u.GeV)

    return energy_bin


def create_folders_energybin(path):

    dict_folders = {}

    energy_bin = create_energy_bin_array()

    for index in range(1, len(energy_bin)):

        current_folder = f"{energy_bin[index-1]}_{energy_bin[index]}".replace(" ", "")

        temp_path = path + "/" + current_folder

        # initialize dictionary_folder
        dict_folders[current_folder] = {}
        dict_folders[current_folder]['LSTCam'] = []
        dict_folders[current_folder]['NectarCam'] = []
        dict_folders[current_folder]['FlashCam'] = []
        dict_folders[current_folder]['SCTCam'] = []

        try:
            os.mkdir(temp_path)
        except FileExistsError:
            continue

    return dict_folders


def which_energybin_folder(energy_event):

    energy_bin = create_energy_bin_array()

    for index, element in enumerate(energy_bin):
        if energy_event >= element:
            if index < len(energy_bin):
                destination_folder = f"{energy_bin[index]}_{energy_bin[index+1]}"
            else:
                destination_folder = f"{energy_bin[index-1]}_{energy_bin[index]}"

    destination_folder = destination_folder.replace(" ", "")

    return destination_folder
