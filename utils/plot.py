# -*- coding: utf-8 -*-

# Copyright 2017 IBM RESEARCH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
# Author: Diego M. Rodríguez
"""Wrapper for displaying JS or SDK visualizations depending on environment."""

import os

from jupyter_core.paths import jupyter_config_path
from notebook.nbextensions import NBCONFIG_SECTIONS
from traitlets.config.manager import BaseJSONConfigManager

import qiskit.tools.visualization

# Try to import the Python module for the jupyter extension.
try:
    import qiskit_jupyter_visualizations
    EXTENSION_PYTHON_AVAILABLE = True
except ImportError:
    EXTENSION_PYTHON_AVAILABLE = False

# List of visualizations implemented by the jupyter extension.
EXTENSION_VISUALIZATIONS = ['bloch', 'city', 'qsphere']
EXTENSION_NAME = 'qiskit_jupyter_visualizations'

STR_NO_PYTHON = ('This visualization is available as an interactive widget '
                 'in the "%s" Jupyter extension.\n'
                 'Please install the extension via pip and activate it for '
                 'your Jupyter environment (more details at '
                 'https://github.com/QISKit/qiskit-jupyter-visualization)' %
                 EXTENSION_NAME)
STR_ACTIVATE = ('This visualization is available as an interactive widget '
                'in the "%s" Jupyter extension.\n'
                'Please activate the extension for your Jupyter environment '
                '(more details at '
                'https://github.com/QISKit/qiskit-jupyter-visualization)' %
                EXTENSION_NAME)


def plot_state(rho, method='city'):
    """Plot a visualization from JavaScript or from Python.

    Attempt to plot a visualization using the JavaScript widgets, falling back
    to the Python SDK static visualization if not possible. This function
    supports the following cases:
    1. If the visualization is not supported by the JavaScript widgets, it
       falls back to Python silently.
    2. If the visualization is supported by the JavaScript widgets, but the
       Jupyter extension is not available, it prints a message and falls back
       to Python.
    2. If the visualization is supported by the Javascript widgets and the
       extension is available, it uses the JavaScript widgets.

    Args:
        rho (numpy.array): value for the visualization.
        method (str): name of the visualization.
    """
    func = qiskit.tools.visualization.plot_state

    if method in EXTENSION_VISUALIZATIONS:
        if EXTENSION_PYTHON_AVAILABLE:
            # "jupyter-js-widgets" needs to be installed as well.
            required_names = ['%s/extension' % EXTENSION_NAME,
                              'jupyter-js-widgets/extension']
            if set(required_names).issubset(set(EXTENSIONS_INSTALLED)):
                if set(required_names).issubset(set(EXTENSIONS_ENABLED)):
                    func = qiskit_jupyter_visualizations.QWidget
                else:
                    # Extensions installed, but not enabled.
                    print(STR_ACTIVATE)
            else:
                # Extensions not installed.
                print(STR_ACTIVATE)
        else:
            # pip package not installed.
            print(STR_NO_PYTHON)

    return func(rho, method)


def _get_extensions_info():
    """Return all the nbextensions found on the Jupyter installation.

    Based on `jupyter.notebook.nbextensions.ListNBExtensionsApp`.
    Returns:
        (list(str), list(str)): list of the installed extensions on the system,
            list of enabled extensions on the system.
    """
    installed = []
    enabled = []

    config_dirs = [os.path.join(p, 'nbconfig') for p in jupyter_config_path()]

    for config_dir in config_dirs:
        # Loop through the Jupyter configuration dirs.
        config_manager = BaseJSONConfigManager(config_dir=config_dir)
        for section in NBCONFIG_SECTIONS:
            data = config_manager.get(section)
            if 'load_extensions' in data:
                for require, is_enabled in data['load_extensions'].items():
                    installed.append(require)
                    if is_enabled:
                        enabled.append(require)

    return installed, enabled


# Get the Jupyter extensions on this system.
try:
    EXTENSIONS_INSTALLED, EXTENSIONS_ENABLED = _get_extensions_info()
except:
    EXTENSIONS_INSTALLED, EXTENSIONS_ENABLED = False, False
