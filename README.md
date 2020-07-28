# wspy
A python wrapper around libwireshark, libwiretap, and libwsutil.

This project is in early development. The goal is to create a clean python API around libwireshark that provides the full power and speed of wireshark. Instead of a wrapper around tshark (see [PyShark](https://kiminewt.github.io/pyshark/)), wspy aims to directly call the native C API and provide as much of the internal wireshark API as possible.

## Status
Currently working on importing the raw C functions. The user-friendly python interface has not started development yet.
