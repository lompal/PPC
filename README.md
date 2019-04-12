# What is the PPC?
PPC (Personal Print Cloud) - free and open source utility that implements remote control of 3D printing in real time without creating any additional connections, such as VPN, ssh-tunnels, etc. and very similar in functionality to OctoPrint Anywhere or AstroPrint Cloud - they all use OctoPrint API and based on the Socket.IO. Unlike the voiced analogs, this utility has no restrictions on the number of connected devices, functionality and is completely free.

# Features overview
  - Partial supporting functionality of the OctoPring API such as:
    - Connection handling - retrieves the current connection settings, including information regarding the available baudrates and serial ports and the current connection state with the ability to issue commands such as connect and disconnect the printer board to OctoPrint
    - Job operations - retrieves information about the current job with controls which allows starting, pausing and canceling print jobs
    - Printer operations - temperature information, sd state, general printer state
  - Unlimited number of macros that can be written as a single command and a set of commands
  - An infinite number of preheating profiles
  - Issuing any g-code command to the printer via the serial interface
  - Real-time webcam image capture (image refresh interval can be configured in account settings in the integration section on the server)
  - An adaptive mobile user interface

# Features to be implemented soon
  - Printer profiles - a printer’s physical properties (such as print volume, whether a heated bed is available, maximum speeds on its axes, etc.)
  - Slicer profiles
  - File operations - information regarding all files currently available and regarding the disk space still available locally in the system and issue a file command to an existing file (such as selecting a file for printing, slicing an STL file into GCODE, copy, move, etc.)
  - Print queuing
  - Cross-platform desktop client
  - Server-side that allows you to set up an environment on the local network without trusting third-party servers
