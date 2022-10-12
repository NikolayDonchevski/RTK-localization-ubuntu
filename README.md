# **Implementing RTK GNSS in the Streetdrone**

# Introduction

This document will elaborate upon all relevant information, regarding the RTK kit&#39;s set-up, testing and implementation in the StreetDrone. In addition, key decisions and RTK-related milestones throughout the project will be detailed. Key terms and the source code for the ROS node will be placed in the appendix. Having read this report carefully, the reader should be perfectly prepared to set up, program and deploy an RTK solution for their project.

# RTK working principles – base station, moving base and rover

RTK or Real Time Kinematics is a type of localization technique, used to greatly improve the positioning accuracy of a standalone GNSS receiver. Traditionally GNSS receivers use a single antenna, placed with a clear view of the sky, in order to get the best possible satellite reception. These solutions can localize with an accuracy that could go as low as 50 cm, but update comparatively slowly and do not provide a direction of heading, which is essential for navigation.

RTK, on the other hand, uses several GNSS receivers that pull data from the satellite constellations and coordinate it, such that an accuracy of 1 cm is possible to be consistently acquired, and the direction of heading is also precisely known. An RTK system, used for mobile localization, utilizes three programmable components – a base station, moving base and rover PCBs. The base station acts as the main source of all incoming satellite messages. It essentially takes in all satellite data and transmits it to the nearest rover via a radio antenna or an NTRIP caster. The latter will not be covered in this document, as for our project, we found the 966MHz standard antenna that came with the kit to be more than enough for reliable data transmission. As with all GNSS solutions, the base station must be placed on a high point with a clear view of the sky from all directions, ideally the tallest point of a building&#39;s roof. Next up, the moving base function allows for a centimeter level xyz baseline estimate when the base station and possibly the rover are moving. It is very similar to standard RTK, with one stationary base station and a moving rover. The key difference between a moving base solution and a standard one (one base station and one rover), is that with a moving base, the directional and rotational headings of the vehicle can be acquired. Without a moving base, only a heading, relative to true north will be acquired, and only after the vehicle has moved a few meters, at a low speed. Without a constant heading, like the one provided by the moving base solution, an autonomous vehicle could never reliably start its process of navigation, as it cannot use a constantly updated reference point to know where its front is headed. Finally, the rover acts as the main receiver of RTK data from the base station and moving base. It receives correction messages from the base station and using its own antenna, and data from the base station, it can reliably localize with an accuracy of 1cm. In a moving use case, such as the StreetDrone, it is highly recommended to keep the GNSS antennas on the vehicle at least 1m apart, in order to avoid digital noise scrambling the signals and diminishing the accuracy of localization and heading.

# Setting up the Ardusimple RTK Base, Moving Base and Rover

## Setting up the physical connections in an optimal environment

The Ardusimple kit comes with three PCBs for the base station, moving base and rover, three GNSS antennas and two radio modules with 966MHz radio antennas. The PCBs for the base and moving base are equipped with a blue-colored XBee radio module, where the 966MHz radio antennas are screwed in; the antennas should optimally point straight towards the sky. The Ublox GNSS antennas are screwed in the golden sockets, marked in red. (Fig.1,2) The XBee radio antennas are screwed in the golden, marked in blue (Fig.3,4). All PCBs are powered via a micro-USB cable, inserted in the POWER+GPS slot.

 ![Shape5](RackMultipart20220121-4-qx86d8_html_39a27650aef9eaf.gif) ![Shape4](RackMultipart20220121-4-qx86d8_html_39a27650aef9eaf.gif) ![Shape3](RackMultipart20220121-4-qx86d8_html_39a27650aef9eaf.gif) ![Shape2](RackMultipart20220121-4-qx86d8_html_3bee89eac992255.gif) ![Shape1](RackMultipart20220121-4-qx86d8_html_3bee89eac992255.gif)

  ![](RackMultipart20220121-4-qx86d8_html_1bdaf5dabc80d258.jpg)                                        ![Picture 2](RackMultipart20220121-4-qx86d8_html_884e6227269f30db.gif)

Fig.1 Ardusimple  rover and moving base     Fig.2 Ardusimple base station

![](RackMultipart20220121-4-qx86d8_html_6af8d9f13d47c1bd.png) ![](RackMultipart20220121-4-qx86d8_html_202be054b99110b4.png)

Fig.3 Ublox GNSS antenna   Fig.4  XBee radio module and antenna

It is vital that all Ublox GNSS antennas are placed outside, with a clear view of the sky, preferably magnetized to a metal object, lying on a flat surface. Ideally, the surface would be a ferrous metal, as the antennas are magnetized.

## Setting up the virtual testing environment (U-center)

U-center is the software, provided by Ublox, which facilitates the testing and configuration of the PCBs. It allows for the enabling or disabling of certain functionalities, such as the ability to only track a specific satellite constellation, increase or decrease baud rate and track RTK parameters. For this project [U-center 21.09](https://www.u-blox.com/sites/default/files/u-centersetup_v21.09.zip) was used. The only prerequisite for running U-center is to download and run the [U-center Windows driver](https://www.u-blox.com/en/ubx-viewer/view/UBX-GNSS-CDC-ACM-windows_Driver_(UBX-drv-v1.2.0.8).exe.zip?url=https%3A%2F%2Fwww.u-blox.com%2Fsites%2Fdefault%2Ffiles%2Fproducts%2Ftools%2FUBX-GNSS-CDC-ACM-windows_Driver_%2528UBX-drv-v1.2.0.8%2529.exe.zip). Once both the driver and the software are installed, the PCBs are ready to be connected and set up. Currently, the base station, moving base and rover are all correctly configured to output RTK data with minimal bandwidth loss. It is not recommended to change the configurations unless a specific set of data needs to be extracted. In any case, the process to flash the PCBs with new configurations and firmware is described in the following sub-chapters.

## Configuring the base station and rover/moving base in U-center (step-by-step process)

![](RackMultipart20220121-4-qx86d8_html_664385631ab6b458.png)

1. Connect the POWER+GPS socket to a USB-A port in your computer with a micro-USB to USB-A cable. ![Shape6](RackMultipart20220121-4-qx86d8_html_14bcdee515043413.gif)
2. From the dropdown menu of the serial port connector, select the USB port you will be connecting to (the name of the port will always start with COM then a number after it)
3. ![](RackMultipart20220121-4-qx86d8_html_af6adbb23769521f.jpg)Use the handy [guide by Ardusimple](https://www.ardusimple.com/configuration-files/) that goes through the steps of how to flash new firmware and/or configuration files

When everything is set up, you can test the individual PCBs in U-center. The base station should give you the following output after about a minute of receiving satellite data:

Note that the Fix Mode is set to TIME, meaning that the base station is receiving satellite data and outputting corrections messages. Now, the nearest rover/moving base setup, equipped with a radio antenna will be able to pick up those corrections and use them to improve localization accuracy.

![](RackMultipart20220121-4-qx86d8_html_f4f72cc273f94599.jpg)Once the base station has produced a screen, identical to the image above, disconnect the base and connect the rover through the GPS+POWER slot. After several minutes at most, the rover will produce a screen, similar to this one:

Note that the Fix Mode is now 3D, meaning that longitude, latitude and altitude, relative to sea level, are sufficiently stable to localize. The only problem is the accuracy, which is sitting at 60cm on the longitude/latitude plane and 88cm when altitude is taken into account. This happens because the base station is not outputting correction data and the rover/moving base are using only their own GNSS antennas. Additionally, there is no heading data whatsoever.

T ![](RackMultipart20220121-4-qx86d8_html_fae0c87227d31ab2.jpg) o correct those errors, simply power on the base station with a power bank and set its GNSS antenna in an open space. Connect the rover/moving base to your PC and note how the data in U-center almost immediately corrects. The screen you should see within several minutes of correction data at most is the following:

The Fix Mode should now be 3D/DGNSS/FIXED, meaning that an RTK fix is achieved. If antenna placement is optimal, then the accuracy should not stray from the 1-3cm range in both 2D and 3D ranges respectively. In this case the accuracy is 2cm, but we have also achieved consistent 1cm accuracy with better antenna placement without issues.

## Testing the RTK set-up

Once set up and configured, the RTK configuration is ready to be tested. Abide by the following testing procedure:

1. Screw in all GNSS and radio antennas in their respective slots
2. Make sure the firmware and configuration files are correctly set up on all PCBs (refer to the Ardusimple configuration guide)
3. Power the base station via battery bank, through the POWER+GPS slot and wait ~2 minutes for it to start receiving corrections messages
4. Place the rover/moving base GNSS antennas at least 1m apart, in order to receive a correct heading
5. Plug in the rover/moving base to your computer and wait a minute or so to start receiving the corrections
6. Observe the number of satellites and their signal strength; it is good practice to make sure there are at least 30 satellites, 10 of which have a signal strength of 40dB or more. In case there is a fewer number of satellites with lower signal strength, adjust the positioning of the GNSS antennas in the open space.

![](RackMultipart20220121-4-qx86d8_html_6c7f9de89c0044d2.jpg)Here are examples of poor satellite reception and good satellite reception:

Pictured above: Screenshot of U-center when the RTK set-up is badly placed (inside building, GNSSantennas too close to each other)

![](RackMultipart20220121-4-qx86d8_html_54a3162fe6a3fc73.jpg)

Pictured above: Screenshot of U-center in optimal conditions (antennas are placed outside, on flat ground, pointing upwards and spaced 1.5m away from each other)

# Implementing RTK in the Streetdrone

Getting the RTK set-up to function in U-center is only a matter of flashing the PCBs and abiding by simple positioning rules. Getting the RTK set-up to function in Ubuntu and ROS however, is more complicated. The use of U-center is still extremely important, as you can enable or disable only specific messages. With the amount of messages enabled, the requirement for a higher bandwidth and baud rate increases as well. For our testing, we decided to go with a baud of 115200 and enable through message view only the following messages:

- UBX-NAV-STATUS – to extract the type of Fix Mode
- UBX-NAV-HPOSSLLH – to extract longitude, latitude and altitude
- UBX-NAV-RELPOSNED – to extract relative heading

To extract specific messages and output them in a terminal, you need to employ the use of the very handy [U-Blox Interface Manual](https://www.u-blox.com/sites/default/files/u-blox-F9-HPG-1.30_InterfaceDescription_UBX-21046737.pdf), where all messages are detailed in terms of every single parameter they carry.

## Extracting and parsing raw UBX messages in a terminal

To begin the procedure of RTK implementation in Ubuntu, a UBX message parser is the first thing, needed to read raw messages from the PCBs. The following instructions detail how that is done:

In Windows:

1. Enable or disable the messages you want to see in message view (press F9 when the PCB is connected to U-center and double click to enable or disable a message
2. Absolutely make sure to save the configuration you just made by navigating to UBX-CFG-Config, select all Devices in the top right corner and hit Send on the bottom left corner (not doing so will make the board forget all changes you&#39;ve made as soon as you close U-center or unplug it from the PC)

![](https://github.com/NikolayDonchevski/RTK-localization-ubuntu/blob/main/pictures/image028.jpg)

In Ubuntu:

1. Connect the rover/base to the computer
2. Open a terminal and run the following command to give permission for data transmission over the serial port
  ```
  sudo chmod 666 /dev/ttyACM0
  ```
3. Install the required libraries via the terminal, if you don&#39;t have them already (this is done only once)
```
  python -m pip3 install --upgrade pyubx2
  sudo apt pip3 install rospy
  sudo apt pip3 install serial
  sudo apt pip3 install transformations
  sudo apt pip3 install pyubx2
  ```
4. Run the localization.py script

The script that we have made performs the following actions:

1. Parses raw UBX messages for fix status, coordinates, heading and 3D accuracy, received from the rover/moving base
2. Translates the longitude and latitude to local x and y of the parking deck
3. Translates the heading angle into quaternion angles
4. Rotates the angle so that positive x of the parking deck is 0 degrees
5. Publishes the data to a ROS node of the type PoseWithCovarianceStamped

# Conclusion

The goals of using satellite navigation and attaining a positioning accuracy of 1 cm were achieved through the use of a Real Time Kinematic GNSS system. The system, consisting of a base station, moving base and a rover, was calibrated through the use of tuning software in Windows and adapted to work on Linux, via python script. The end result was a system, which satisfied the 5 cm accuracy requirement and allowed for localization via the provided heading.

As advice for the next group we can say to try and implement the already working RTK system in Autoware. This means that they have to remove the current localization with the lidar, but the lidar will still be used for object detection. The next step is to validate that the Streetdrone can localize itself with just RTK in Autoware. They have to look at the node ndt\_matching and understand how it is currently used to localize. Following that, they need to do some adjustment with TF to link the base\_link to RTK GNSS in Rviz. If everything is done correctly the localization part of the whole project will be complete.

# References

ArduSimple. (2022, January 4). _Configuration Files_. https://www.ardusimple.com/configuration-files/

marXact B.V. (2021, December 28). _What is the difference between RTK, FIX, and RTK Float?_ MarXact Knowledge Base. https://support.marxact.com/article/85-what-is-the-difference-between-rtk-fix-and-rtk-float

semuconsulting. (2021). _GitHub - semuconsulting/pyubx2: Python library for parsing and generating UBX GPS/GNSS protocol messages._ GitHub. https://github.com/semuconsulting/pyubx2

_u-center_. (2021, December 9). U-Blox. https://www.u-blox.com/en/product/u-center

Wikipedia contributors. (2021, November 17). _Real-time kinematic positioning_. Wikipedia. https://en.wikipedia.org/wiki/Real-time\_kinematic\_positioning

_XBee Radios_. (2015, February 16). Adafruit Learning System. https://learn.adafruit.com/xbee-radios/modules
