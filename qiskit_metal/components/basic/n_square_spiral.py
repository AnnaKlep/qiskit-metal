# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
"""File contains dictionary for NSquareSpiral and the make()."""

from qiskit_metal import draw, Dict
from qiskit_metal.components.base import QComponent
import numpy as np


class NSquareSpiral(QComponent):
    """A n count square spiral.

    Inherits `QComponent` class

    Description:
        A n count square spiral.
        ::

            ____________
            |   _____   |
            |  |     |  |
            |  |     |  |
            |  |________|
            |

    Options:
        Convention: Values (unless noted) are strings with units included,
        (e.g., '30um')

        * n           : number of turns of the spiral
        * width       : the width of the line of the spiral
        * radius      : the 'radius' of the inner portion of the spiral
        * gap         : the distance between each layer of the spiral
        * pos_x/_y    : the x/y position of the ground termination.
        * rotation    : the direction of the termination. 0 degrees is +x, following a
          counter-clockwise rotation (eg. 90 is +y)
        * chip        : the chip the pin should be on.
        * layer       : layer the pin is on. Does not have any practical impact to the short.

    """

    default_options = Dict(n='3',
                           width='1um',
                           radius='40um',
                           gap='4um',
                           pos_x='0um',
                           pos_y='0um',
                           rotation='0',
                           subtract='False',
                           helper='False',
                           chip='main',
                           layer='1')
    """Default drawing options"""

    def make(self):
        """
        The make function implements the logic that creates the geoemtry
        (poly, path, etc.) from the qcomponent.options dictionary of parameters,
        and the adds them to the design, using qcomponent.add_qgeometry(...),
        adding in extra needed information, such as layer, subtract, etc.
        """
        p = self.p  # p for parsed parameters. Access to the parsed options.
        n = int(p.n)
        # Create the geometry

        spiral_list = []

        for step in range(n):
            point_value = p.radius / 2 + step * (p.width + p.gap)
            spiral_list.append((-point_value, -point_value))
            spiral_list.append((point_value, -point_value))
            spiral_list.append((point_value, point_value))
            spiral_list.append((-point_value - (p.width + p.gap), point_value))

        point_value = p.radius / 2 + (step + 1) * (p.width + p.gap)
        spiral_list.append((-point_value, -point_value))
        spiral_list = draw.LineString(spiral_list)

        spiral_list = draw.rotate(spiral_list, p.rotation, origin=(0, 0))
        spiral_list = draw.translate(spiral_list, p.pos_x, p.pos_y)

        ##############################################
        # add qgeometry
        self.add_qgeometry('path', {'n_spiral': spiral_list},
                           width=p.width,
                           subtract=p.subtract,
                           helper=p.helper,
                           layer=p.layer,
                           chip=p.chip)

        points = np.array(spiral_list.coords)
        # FIX POINTS,
        self.add_pin('spiralPin',
                     points=points[-2:],
                     width=p.width,
                     input_as_norm=True)
