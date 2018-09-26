#!/usr/bin/env python3

from argparse import ArgumentParser
from argparse import RawTextHelpFormatter as tefo
from idgrms.data import *
from idgrms.plotdgrms import *


argparser = ArgumentParser(prog='photometric_diagrams.py', description='>> Interactive \
CCD and CMD diagrams <<\n\n Requires Python 2.7 with:\n  * numpy\n  * argparse\n  * matplotlib\n\n',
epilog='Copyright (c) 2017 Przemysław Bruś', formatter_class=tefo)
argparser.add_argument('input_file', help='must contain columns with data and a one-line header\n\
The header must be preceded by # sign. Labels from the header \nwill be used to sign axes on charts')
argparser.add_argument('--col', help="columns which should be used to create \
the diagram\nA negative value reverses range's axis. There is no limit to the diagrams", \
nargs=2, dest='col', action='append', metavar=('col_x', 'col_y'), required=True, type=int)
argparser.add_argument('--grp', help='group of stars which can be marked by color\n\
/file/ should contain only one column with ID numbers of stars\nIf this option is used, \
also /input/ must have ID numbers of stars\nin the first column. The variable /color/ \
stores color which marks\nthe points from the /file/. The color can be specified \
by an html\nhex string ("#4f21b7") or literally (blue or b). For more details\nsee the \
matplotlib documentation. Gray and red colors are reserved\nfor plotting the background and \
selection of points, respectively', nargs=2, dest='grp', action='append', metavar=('file', 'color'))
argparser.add_argument('-t', help='talkative mode. Printing feedback with every click', \
action='store_true')
argparser.add_argument('-v', '--version', action='version', version='%(prog)s\n * Version: 2017-02-23\n \
* Licensed under the MIT license:\n   http://opensource.org/licenses/MIT\n * Copyright (c) 2017 Przemysław Bruś')
args = argparser.parse_args()
trigger_windows(args.input_file, args.col, args.grp, args.t)
