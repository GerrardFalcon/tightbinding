import numpy as np
from cmath import exp

"""
Author: Jack Baker

Date: 15/11/2016

Description: Some free floating functions and a dictinaory of lambda fucntions
used in the implementation of the Slater-Koster tables.
"""

#eta_dict = {"s_s_sigma": -1.40,
#            "s_p_sigma": 1.84,
#            "p_s_sigma": 1.84,
#            "p_p_sigma": 3.24,
#            "p_p_pi": -0.81  }
# Dave's parameters
eta_dict = {"s_s_sigma": -1.938,
            "s_p_sigma": 1.745,
            "p_s_sigma": 1.745,
            "p_p_sigma": 3.050,
            "p_p_pi": -1.075}

def eta_coeff(l_i, l_j, bond_type):
    """
    Retrieves the correct eta coefficient from eta_dict.
    input: l_i => Angular momentum state for the ith orbital. String.
    input: l_j => Angular momentum state for the jth orbital. String.
    input: bond_type => The type of bond (sigma, pi...) from the orbital overlap.
    String.
    returns: eta_dict[eta_string] => the correct eta coefficient. Float64
    """
    return eta_dict["_".join([l_i, l_j, bond_type])]


def V_coeff(eta, internuclear_distance):
    """
    input: eta => Returned from the function eta_coeff (dict look
                  up from eta_dict.). Float64.
    input: internuclear_distance => Distance separating centers of nuclei.
                                    enters function in angstroms. Float64.
    returns: V => The bond coefficient including the distance dependence in eV.
                  Float.
    """
    # Daves suggestion for bulk -> distance dependecne should be 1
    #V = 7.619964162248216*eta
    V = 7.619964162248216 * eta * (1/(internuclear_distance*internuclear_distance))
    return V



orb_dict = {
"ssss": lambda x_dir_cos, y_dir_cos, z_dir_cos, dist_ij:
        V_coeff(eta_coeff("s", "s", "sigma"), dist_ij),
"sspx": lambda x_dir_cos, y_dir_cos, z_dir_cos, dist_ij:
        x_dir_cos * V_coeff(eta_coeff("s", "p", "sigma"), dist_ij),
"pxss": lambda x_dir_cos, y_dir_cos, z_dir_cos, dist_ij:
        -x_dir_cos * V_coeff(eta_coeff("s", "p", "sigma"), dist_ij),
"sspy": lambda x_dir_cos, y_dir_cos, z_dir_cos, dist_ij:
        y_dir_cos * V_coeff(eta_coeff("s", "p", "sigma"), dist_ij),
"pyss": lambda x_dir_cos, y_dir_cos, z_dir_cos, dist_ij:
        -y_dir_cos * V_coeff(eta_coeff("s", "p", "sigma"), dist_ij),
"sspz": lambda x_dir_cos, y_dir_cos, z_dir_cos, dist_ij:
        z_dir_cos * V_coeff(eta_coeff("s", "p", "sigma"), dist_ij),
"pzss": lambda x_dir_cos, y_dir_cos, z_dir_cos, dist_ij:
        -z_dir_cos * V_coeff(eta_coeff("s", "p", "sigma"), dist_ij),
"pxpx": lambda x_dir_cos, y_dir_cos, z_dir_cos, dist_ij:
        x_dir_cos ** 2 * V_coeff(eta_coeff("p", "p", "sigma"), dist_ij) +\
        (1 - x_dir_cos ** 2) * V_coeff(eta_coeff("p", "p", "pi"), dist_ij),
"pzpz": lambda x_dir_cos, y_dir_cos, z_dir_cos, dist_ij:
        z_dir_cos ** 2 * V_coeff(eta_coeff("p", "p", "sigma"), dist_ij) +\
        (1 - z_dir_cos ** 2) * V_coeff(eta_coeff("p", "p", "pi"), dist_ij),
"pypy": lambda x_dir_cos, y_dir_cos, z_dir_cos, dist_ij:
        y_dir_cos ** 2 * V_coeff(eta_coeff("p", "p", "sigma"), dist_ij) +\
        (1 - y_dir_cos ** 2) * V_coeff(eta_coeff("p", "p", "pi"), dist_ij),
"pxpy": lambda x_dir_cos, y_dir_cos, z_dir_cos, dist_ij:
        (x_dir_cos * y_dir_cos *V_coeff(eta_coeff("p", "p", "sigma"), dist_ij)) -\
        (x_dir_cos * y_dir_cos *V_coeff(eta_coeff("p", "p", "pi"), dist_ij)),
"pypx": lambda x_dir_cos, y_dir_cos, z_dir_cos, dist_ij:
        (x_dir_cos * y_dir_cos *V_coeff(eta_coeff("p", "p", "sigma"), dist_ij)) -\
        (x_dir_cos * y_dir_cos *V_coeff(eta_coeff("p", "p", "pi"), dist_ij)),
"pypz": lambda x_dir_cos, y_dir_cos, z_dir_cos, dist_ij:
        (z_dir_cos * y_dir_cos *V_coeff(eta_coeff("p", "p", "sigma"), dist_ij)) -\
        (z_dir_cos * y_dir_cos *V_coeff(eta_coeff("p", "p", "pi"), dist_ij)),
"pzpy": lambda x_dir_cos, y_dir_cos, z_dir_cos, dist_ij:
        (z_dir_cos * y_dir_cos *V_coeff(eta_coeff("p", "p", "sigma"), dist_ij)) -\
        (z_dir_cos * y_dir_cos *V_coeff(eta_coeff("p", "p", "pi"), dist_ij)),
"pzpx": lambda x_dir_cos, y_dir_cos, z_dir_cos, dist_ij:
        (x_dir_cos * z_dir_cos *V_coeff(eta_coeff("p", "p", "sigma"), dist_ij)) - \
        (x_dir_cos * z_dir_cos *V_coeff(eta_coeff("p", "p", "pi"), dist_ij)),
"pxpz": lambda x_dir_cos, y_dir_cos, z_dir_cos, dist_ij:
        (x_dir_cos * z_dir_cos *V_coeff(eta_coeff("p", "p", "sigma"), dist_ij)) - \
        (x_dir_cos * z_dir_cos *V_coeff(eta_coeff("p", "p", "pi"), dist_ij))
}

def slater_koster_table(orb_i, orb_j, x_dir_cos, y_dir_cos, z_dir_cos, dist_ij):
    """
    Calculates the interatomic matrix elements using the Slater-Koster table.
    string: orb_i, orb_j: ss, px, py, pz...
    remaining arguments are float64.
    """
    return orb_dict["".join([orb_i, orb_j])](x_dir_cos, y_dir_cos,
                                             z_dir_cos, dist_ij)


on_site_dict = {"Cp": -8.97,
                "Cs": -17.52,
                "Hs": -13.61,
                "Sip": -5.75, #-6.52
                "Sis": -12.2}

def on_site_energy_table(species, orbital):
    """
    Gets the on site element from the on_site_dict.
    input: species => the element the orbitak belongs to. String.
    input: orbital => the text representations of the magnetic quantum number.
                      i.e, py, pz... String
    returns: on_site_dict["".join([species, orbital[0:1]])] => The correct on
             site element from dict look up. Float64.
    """
    return on_site_dict["".join([species, orbital[0:1]])]


def bloch_phase_factor(k_point, r_ij):
    """
    The Bloch plane wave phase factor.
    """
    return exp(1J*(k_point[0]*r_ij[0] + k_point[1]*r_ij[1] + k_point[2]*r_ij[2]))
