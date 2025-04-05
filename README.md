# vh-113_scripts

This repo contains a collection of Python scripts used to quickly configure and query the Vivid-Hosting VH-113 field access point.

## vh113.py

Quickly configures the access point for 6 robots using a pre-made template.

## vh113 module

TODO: build a wheel to install these scripts

### config.py

An updated version of `vh113.py`. Adds command line arguments to configure the most common settings and error checking.

Usage:
```
> python3 -m vh113/config -h
usage: config.py [-h] [-d] [-a IP_ADDRESS] [-p PASSWORD] [-c {5,13,21,29,37,45,53,61,69,77,85,93,101,109,117}] ...

Configures a connected VH-113 field access point for up to 6 robots.

positional arguments:
  teams                 team numbers in order: red1 blue1 red2 blue2 red3 blue3

options:
  -h, --help            show this help message and exit
  -d, --debug           print out data before sending
  -a, --ip-address IP_ADDRESS
                        VH-113 IP address
  -p, --password PASSWORD
                        password for all SSIDs
  -c, --channel {5,13,21,29,37,45,53,61,69,77,85,93,101,109,117}
                        Wi-Fi 6 GHz channel
```