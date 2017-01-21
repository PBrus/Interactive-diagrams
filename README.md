# Interactive-diagrams [![GitHub release](http://www.astro.uni.wroc.pl/ludzie/brus/img/github/ver20170108.svg "download")](https://github.com/PBrus/Interactive-diagrams/blob/master/photometric_diagrams.py) ![Written in Python](http://www.astro.uni.wroc.pl/ludzie/brus/img/github/Python.svg "language")

Allows to visualize data on astrophysical diagrams and interact with them. It was written in pure Python.

## Installation

Download `photometric_diagrams.py` wherever you want, then make the script executable. I recommend to download it to any catalog pointed by the `$PATH` variable. Moreover you should have installed *Python 2.7* with the following modules:

 * *numpy*
 * *matplotlib*
 * *argparse*

## Usage

To use the program properly you need to prepare a file with data. At the beginning call the script from the terminal window with the `-h` option:
```bash
$ photometric_diagrams.py -h
```
This will give you a description about all options. If you need to see the program in action immediately, please download three additional files from the repository to your working directory:

 * `mags.db`
 * `best.num`
 * `better.num`

A basic call:
```bash
$ photometric_diagrams.py mags.db --col 12 -10 --col 12 -4
```
More advanced call:
```bash
$ photometric_diagrams.py mags.db --col 12 -10 --col 12 -4 --grp best.num green --grp better.num yellow -t
```
In both cases try to click on any point to see changes on diagrams.

I encourage to visit my website to see more detailed description of this program. The current link can be found on my [GitHub profile](https://github.com/PBrus).

## License

**Interactive-diagrams** is licensed under the [MIT license](http://opensource.org/licenses/MIT).
