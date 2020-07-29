# wspy
A python wrapper around libwireshark, libwiretap, and libwsutil.

This project is in early development. The goal is to create a clean python API around libwireshark that provides the full power and speed of wireshark. Instead of a wrapper around tshark (see [PyShark](https://kiminewt.github.io/pyshark/)), wspy aims to directly call the native C API and provide as much of the internal wireshark API as possible.

## Status
Currently working on importing the raw C functions. The user-friendly python interface has not started development yet.

## Finding Libraries
By default, wspy will use whatever version of the wireshark libraries that can be found on the user's `PATH`. To use an alternative installation of wireshark, wspy can be configured to point to the desired libraries. These options can be set using either environment variables or the `wspy.config` module.

Each library can be specified individually:
```bash
$ export WSPY_LIBWIRESHARK="/my/path/to/libwireshark.so"
$ export WSPY_LIBWIRETAP="/my/path/to/libwiretap.so"
$ export WSPY_LIBWSUTIL="/my/path/to/libwsutil.so"
```
```py
import wspy_config
wspy_config.set_libwireshark('/my/path/to/libwireshark.so')
wspy_config.set_libwiretap('/my/path/to/libwiretap.so')
wspy_config.set_libwsutil('/my/path/to/libwsutil.so')

import wspy
```

Or, a single directory can be specified that contains all three libraries:
```bash
$ export WSPY_LIBDIR="/my/lib/dir"
```
```py
import wspy_config
wspy_config.set_libdir('/my/lib/dir')

import wspy
```
