# SmartControl

SmartControl is a graphical interface for the smartmontools package using Enigma2 settop boxes.

## Requirements

* full HD skin
* smartmontools >= version 7.0; the plugin makes use of its JSON API
* package util-linux, more specific: the plugin makes use of the "lsblk" program

The plugin reads the self test results from connected hard disks. I do not own a defective hard disk, 
therefore I am not sure if the error log will be displayed correctly. If someone posts the output of 
"smartctl -jl" I will fix it.

## Interpretation of attributes:

Modern hard disks use internal attributes to record their health state. Attributes are displayed using three items: "Value", "Worst", "Thresh":
* "Value" is the currently saved value for the attribute
* "Worst" is the worst ever experienced value for the attribute
* "Thresh" is the threshold for which you can assume the hard disk to be in defect

These values are normalized; "Value" and "Worst" should always be above "Thresh", otherwise the hard disk probably is in defect. 
The column "State" summarizes this state: "Ok" means the hard disk thinks it is ok, otherwise the column displays the attribute's error state.

