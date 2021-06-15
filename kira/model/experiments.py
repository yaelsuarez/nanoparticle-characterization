from typing import List, Tuple
import os
import yaml
import csv
import numpy as np
import matplotlib.pyplot as plt
import logging
from copy import deepcopy

class Annealing:
    """
    :param temperature: Temperature (ºC) of annealing
    :param time: Time (hours) of annealing
    """
    def __init__(self, temperature: float, time: float):
        self.temperature = temperature
        self.time = time
    @classmethod
    def from_metadata(cls, metadata):
        temp = metadata['annealing_temp']
        time = metadata['annealing_time']
        temp = float(temp) if temp is not None else None
        time = float(time) if time is not None else None
        return cls(temperature=temp, time=time)

class Measurement:
    """
    :param spectrum: List of x axis values (Wavelength (nm))
    :param luminescence: List of y axis values (Intensity (a.u.))
    """
    def __init__(self, spectrum: List[float], luminescence: List[float], std: List[float]):
        self.spectrum = spectrum
        self.luminescence = luminescence
        self.std = std

    @classmethod
    def read_laser_scan(cls, filename):
        """get spectrum and luminescence from a single document"""
        with open(filename, 'r') as f:
            l=next(f)
            while l != ">>>>>Begin Spectral Data<<<<<\n":
                l=next(f)
            reader=csv.reader(f,delimiter="\t")
            x=[]
            y=[]
            for row in reader:
                x.append(float(row[0]))
                y.append(float(row[1]))
        return cls(spectrum=np.array(x), luminescence=np.array(y), std=None)

    @classmethod
    def mean_laser_scan(cls, filenames):
        """
        Get mean of x and y data,
        All files must always have the same x range.
        """
        y_all = []
        y_mean = []
        x_all = []
        x_mean = []
        std = []
        for filename in filenames:
            meas = cls.read_laser_scan(filename)
            y_all.append(meas.luminescence)
            x_all.append(meas.spectrum)
        y_all = np.array(y_all)
        y_mean = np.mean(y_all, axis=0)
        std = np.std(y_all, axis=0)
        x_all = np.array(x_all)
        x_mean = np.mean(x_all, axis=0)
        return cls(spectrum=x_mean, luminescence=y_mean, std=std)

    @classmethod
    def mean_laser_scan_from_folder(cls, folder_path):
        """
        Scan a folder for txt files,
        read them and get the mean for every x
        """
        txt_files = [os.path.join(folder_path,f)
            for f in os.listdir(folder_path) if f.endswith('txt') and not f.startswith("._")]
        return cls.mean_laser_scan(txt_files)

    def crop(self, low:float, high:float):
        """crops the meas to the specified range"""
        mask_low = self.spectrum >= low
        mask_high = self.spectrum <= high
        mask = np.logical_and(mask_low, mask_high)
        self.spectrum = self.spectrum[mask]
        self.luminescence = self.luminescence[mask]
        self.std = self.std[mask]

    def plot(self, **kwargs):
        plt.errorbar(self.spectrum, self.luminescence, **kwargs)

    def auc(self, low:float, high:float):
        """
        Find AUC of the selected the spectra.
        :param low: inclusive lower limit.
        :param high: inclusive higher limit.
        """
        temp_self = deepcopy(self)
        temp_self.crop(low, high)
        max_luminescence = temp_self.luminescence + temp_self.std
        min_luminescence = temp_self.luminescence - temp_self.std
        max_auc = np.trapz(max_luminescence, temp_self.spectrum)
        min_auc = np.trapz(min_luminescence, temp_self.spectrum)
        mean_std = (max_auc-min_auc)/2
        return np.trapz(temp_self.luminescence, temp_self.spectrum), mean_std


class Nanoparticle:
    """
    A Nanoparticle models all the required information in order 
    to make an easy analysis of the experiments.
    :param identity: Nanoparticle base compound.
    :param dopant: Dopant type.
    :param dopant_concentration: Concentration of dopant (%).
    :param annealing: Annealing characteristics.
    :param d_xrd: Diameter size (nm) by XRD peak method.
    :param meas: Mesurement of luminescence for the np.
    :param ref: the measurement of the control. It is used to compare the nanoparticle measurements against 
    """
    def __init__(self,
                identity: str,
                dopant: str,
                dopant_concentration:float,
                annealing: Annealing,
                d_xrd: float,
                meas: Measurement,
                ref: Measurement):
        self.identity = identity
        self.dopant = dopant
        self.dopant_concentration = dopant_concentration
        self.annealing = annealing
        self.d_xrd = d_xrd
        self.meas = meas
        self.ref = ref

    @classmethod
    def from_folder(cls, meas_folder:str):
        """Loads a Nanoparticle from a measurements folder.
        :param meas_folder: A folder that contains all the txt files with
            measurements that will be averaged. The folder also contains
            a "metadata.yaml" that specifies all other values for the nanoparticle.
            The YAML template is the following.
                identity: NaYF₄
                dopant: Ln
                dopant_concentration: 1
                # folder where the reference lives in the parent directory to the meas_folder
                reference: NaYF4_Yb
                annealing_time: 0
                annealing_temp: 0
                d_xrd: 40.2
        """
        metadata_path = os.path.join(meas_folder, "metadata.yaml")
        with open(metadata_path) as file:
            metadata = yaml.safe_load(file)
        mean_meas = Measurement.mean_laser_scan_from_folder(meas_folder)
        annealing = Annealing.from_metadata(metadata)
        ref_folder_name = metadata['reference']
        ref_path = os.path.join(
            os.path.abspath(os.path.join(meas_folder, os.pardir)),
            ref_folder_name)
        ref_meas = Measurement.mean_laser_scan_from_folder(ref_path)
        if not np.isclose(ref_meas.spectrum, mean_meas.spectrum).all():
            logging.warning("the spectrum of the reference is different")
        return cls(identity=metadata['identity'], dopant=metadata['dopant'],
                    dopant_concentration=metadata['dopant_concentration'],
                    d_xrd = metadata['d_xrd'], annealing=annealing,
                    meas=mean_meas, ref=ref_meas)

    def plot(self, plot_ref: bool = False, **kwargs):
        plt.errorbar(self.meas.spectrum, self.meas.luminescence, **kwargs)
        if plot_ref:
            if "label" in kwargs.keys():
                kwargs["label"] += "_ref"
            if "yerr" in kwargs.keys():
                kwargs['yerr'] = self.ref.std
            plt.errorbar(self.ref.spectrum, self.ref.luminescence, **kwargs)

    def crop(self, low:float, high:float):
        """crop the meas and ref to the specified range"""
        self.meas.crop(low, high)
        self.ref.crop(low, high)

    def crop_rescale_to_new_ref(self, new_ref:Measurement, lims:Tuple[float, float]):
        """Modify the meas so that the reference matches the new_ref,
        it assumes that all measurements have exaclty the same spectrum
        :param lims: (lower, upper) inclusive limits of the spectrum for getting the
            factors of the resizing"""
        new_ref.crop(low=lims[0], high=lims[1])
        self.crop(low=lims[0], high=lims[1])
        if not np.isclose(new_ref.spectrum, self.ref.spectrum).all():
            logging.warning("The spectra of the references are different")
            logging.warning(f"new_ref spectrum:{new_ref.spectrum}")
            logging.warning(f"new_ref spectrum:{self.ref.spectrum}")
        factors = new_ref.luminescence / self.ref.luminescence
        self.meas.luminescence = self.meas.luminescence * factors
        self.ref.luminescence = self.ref.luminescence * factors
        self.meas.std = self.meas.std * factors
        self.ref.std = self.ref.std * factors
        return factors
