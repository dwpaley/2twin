# 2twin

A couple twinning scenarios are not natively handled by ShelXL:

* Combined non-merohedral and (pseudo-)merohedral twinning

* Two independent (pseudo-)merohedral twin laws

2twin generates a twinned (HKLF 5) .hkl file that correctly models these multiple
twinning situations. After running 2twin, refinement in ShelXL proceeds as
normal.

## Installation

### Binary files

Download the correct version for your operating system:

* [Windows (64-bit)](https://github.com/dwpaley/2twin/raw/master/bin/win64/2twin.exe)
* [OSX](https://github.com/dwpaley/2twin/raw/master/bin/osx/2twin)

Place the executable in the system path. The directory containing your ShelXL executable
might be convenient.


### Source code:

Copy all files and place a link to 2twin.py in your system path:

```
$ git clone https://github.com/dwpaley/2twin
$ ln -s $PWD/2twin.py /usr/local/bin/2twin
```

## Usage

To process structure.hkl, run `$ 2twin structure` and follow the prompts.
Manually duplicate structure.ins to structure-2twin.ins and ensure it has 
`HKLF 5` and the correct number of `BASF` parameters.

## Description

2twin takes an input hkl file (HKLF 4 or 5 format), applies one or
more (pseudo-)merohedral twin laws, and outputs an HKLF 5 file containing one
batch for every twin-related domain. 

For example, you might have a three-component HKLF 5 file and wish to apply 
2[110] as an additional merohedral twin law. In ShelXL, TWIN and HKLF 5 are not 
mutually compatible, so both forms of twinning cannot be refined together. 
Instead, we transform every reflection in the HKLF 5 file by the merohedral
twin law, generating a new file with twice the number of entries.

The input HKLF 5 file might contain the following group of three overlapping
reflections, where "m should be positive for the last contributing component
and negative for the remaining ones".

```
   2   2   1 89993.4 1839.96  -3
   3  -1   0 89993.4 1839.96  -2
  -1   1   2 89993.4 1839.96   1
```

After processing with 2twin, each reflection in the group has been copied and
transformed by the merohedral twin law 010/100/00-1. The hkl file contains
all merohedrally and non-merohedrally related twin components, and the 
refinement proceeds with 6 - 1 = 5 BASF parameters.

```
   2   2  -1 89993.4 1839.96  -6
   2   2   1 89993.4 1839.96  -3
  -1   3   0 89993.4 1839.96  -5
   3  -1   0 89993.4 1839.96  -2
   1  -1  -2 89993.4 1839.96  -4
  -1   1   2 89993.4 1839.96   1
```


The following combinations of twin laws are currently supported. Other
combinations may be added; contact the author or try editing compDict.
* 1 merohedral TL, order 2
* 1 merohedral TL, order 3
* 2 merohedral TLs, orders 2 and 2
* 2 merohedral TLs, orders 3 and 2
* 3 merohedral TLs, all order 2
* 1 non-merohedral and 1 merohedral, each order 2
* 1 non-merohedral and 1 merohedral, orders 3 and 2
* 1 non-merohedral and 1 merohedral, orders 2 and 3
* 1 non-merohedral and 2 merohedral, all order 2
* 1 non-merohedral and 2 merohedral; orders 3, 2, 2
* 1 non-merohedral and 3 merohedral; orders 3, 2, 2, 2


Note that your agreement factors may be artifically increased if you have
switched from TWIN/HKLF 4 refinement to HKLF 5 refinement. This is because
merging is disabled for HKLF 5 data. For a fair comparison, run your TWIN/HKLF 4
refinement with MERG 0.

## About

2twin: Multiple independent twinning in ShelXL.
Copyright 2017, Daniel W. Paley.
Contact: dwpaley@gmail.com

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

For a copy of the GPL, see <http://www.gnu.org/licenses/>.
