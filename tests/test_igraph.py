#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : test_igraph.py
# Creation  : 21 May 2018
# Time-stamp: <Mon 2018-11-05 10:39 juergen>
#
# Copyright (c) 2018 Jürgen Hackl <hackl@ibi.baug.ethz.ch>
#               http://www.ibi.ethz.ch
# $Id$
#
# Description : Test functions for converting igraph networks to tikz-networks
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================

import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import igraph as ig
from network2tikz import plot, layout


@pytest.fixture
def net():
    net = ig.Graph([(0, 1), (0, 2), (2, 3), (3, 4), (4, 2), (2, 5), (5, 0), (6, 3),
                    (5, 6), (6, 6)], directed=True)

    net.vs["name"] = ["Alice", "Bob", "Claire",
                      "Dennis", "Esther", "Frank", "George"]
    net.vs["age"] = [25, 31, 18, 47, 22, 23, 50]
    net.vs["gender"] = ["f", "m", "f", "m", "f", "m", "m"]
    net.es["is_formal"] = [False, False, True, True, True, False, True, False,
                           False, False]
    return net


@pytest.fixture
def color_dict():
    return {"m": "blue", "f": "red"}


@pytest.fixture
def shape_dict():
    return {"m": "circle", "f": "rectangle"}


@pytest.fixture
def style_dict():
    return {"m": "{shading=ball}", "f": None}


@pytest.fixture
def _layout():
    layout = {0: (4.3191, -3.5352), 1: (0.5292, -0.5292),
              2: (8.6559, -3.8008), 3: (12.4117, -7.5239),
              4: (12.7, -1.7069), 5: (6.0022, -9.0323),
              6: (9.7608, -12.7)}
    return layout


def test_plot(net, _layout, color_dict):

    # plot(net) # plot_01.png

    # plot(net,layout=layout) # plot_02.png

    # plot(net, layout=layout, canvas=(8,8), margin=1) # plot_03.png

    visual_style = {}
    visual_style['layout'] = _layout
    visual_style['vertex_size'] = .5
    visual_style['vertex_color'] = [color_dict[g] for g in net.vs['gender']]
    visual_style['vertex_opacity'] = .7
    visual_style['vertex_label'] = net.vs['name']
    visual_style['vertex_label_position'] = 'below'
    visual_style['edge_width'] = [1 + 2 * int(f) for f in net.es['is_formal']]
    visual_style['edge_curved'] = 0.1
    visual_style['canvas'] = (8, 8)
    visual_style['margin'] = 1

    plot(net, 'network.tex', **visual_style)

    plot(net, 'network.csv', **visual_style)

    plot(net, 'network.pdf', **visual_style)

    plot(net, **visual_style)


def test_plot_all_options(net, _layout, color_dict, shape_dict, style_dict):

    visual_style = {}
    # node styles
    # -----------
    visual_style['vertex_size'] = 5
    visual_style['vertex_color'] = [color_dict[g] for g in net.vs['gender']]
    visual_style['vertex_opacity'] = .7
    visual_style['vertex_label'] = net.vs['name']
    visual_style['vertex_label_position'] = 'below'
    visual_style['vertex_label_distance'] = 15
    visual_style['vertex_label_color'] = 'gray'
    visual_style['vertex_label_size'] = 3
    visual_style['vertex_shape'] = [shape_dict[g] for g in net.vs['gender']]
    visual_style['vertex_style'] = [style_dict[g] for g in net.vs['gender']]
    visual_style['vertex_label_off'] = {4: True}  # vertex e
    visual_style['vertex_math_mode'] = [True]
    visual_style['vertex_label_as_id'] = {5: True}  # vertex f
    visual_style['vertex_pseudo'] = {3: True}  # vertex d

    # edge styles
    # -----------
    visual_style['edge_width'] = [.3 + .3 * int(f) for f in net.es['is_formal']]
    visual_style['edge_color'] = 'black'
    visual_style['edge_opacity'] = .8
    visual_style['edge_curved'] = 0.1
    visual_style['edge_label'] = [i for i, e in enumerate(net.es)]
    visual_style['edge_label_position'] = 'above'
    visual_style['edge_label_distance'] = .6
    visual_style['edge_label_color'] = 'gray'
    visual_style['edge_label_size'] = {1: 5}  # edge ac
    visual_style['edge_style'] = 'dashed'
    visual_style['edge_arrow_size'] = .2
    visual_style['edge_arrow_width'] = .2
    visual_style['edge_loop_size'] = 15
    visual_style['edge_loop_position'] = 90
    visual_style['edge_loop_shape'] = 45
    visual_style['edge_directed'] = [True, True, False, True, True, False, True,
                                     True, True]
    visual_style['edge_label'][1] = '\\frac{\\alpha}{\\beta}'
    visual_style['edge_math_mode'] = {1: True}  # edge ac
    visual_style['edge_not_in_bg'] = {6: True}  # edge fa

    # general options
    # ---------------
    visual_style['unit'] = 'mm'
    visual_style['layout'] = _layout
    visual_style["margin"] = {'top': 5, 'bottom': 8, 'left': 5, 'right': 5}
    visual_style["canvas"] = (100, 60)
    visual_style['keep_aspect_ratio'] = False

    plot(net, 'network.tex', **visual_style)

    plot(net, 'network.csv', **visual_style)

    plot(net, 'network.pdf', **visual_style)

    plot(net, **visual_style)


def test_layout(net):

    layout_style = {}
    layout_style['layout'] = 'fr'
    layout_style['seed'] = 1
    _layout = layout(net, **layout_style)

    plot(net, layout=_layout)


# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 80
# End:
