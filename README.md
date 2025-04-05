# vh-113_scripts

This repo contains a collection of Python scripts used to quickly configure and query the Vivid-Hosting VH-113 field access point.

## vh113.py

Quickly configures the access point for 6 robots using a pre-made template.

## vh113 module

The vh113 module is designed to be built into a wheel and installed on a system. Pre-compiled wheels are available on the [releases page](https://github.com/wildstang/vh-113_scripts/releases).

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

### status.py

Continually monitors and logs the status of the VH-113 field access point.

Usage:
```
> python3 -m vh113.status -h
usage: status.py [-h] [-a IP_ADDRESS] [-d] [-m] [-s] [-b]

Continually logs the status of a connected VH-113 field access point.

options:
  -h, --help            show this help message and exit
  -a, --ip-address IP_ADDRESS
                        VH-113 IP address
  -d, --debug           print out each received status block
  -m, --mac             print out MAC address of connected robots
  -s, --strength        print out strength of connected robots
  -b, --bandwidth       print out bandwidth of connected robots
```