#!/usr/bin/env python

#This script gets raw UBX messages from the receivers through serial communication and parses them
#then it translates the longitude and lattitude to local X and Y of the parking deck, translates the
#heading angle to quaternion angles and publishes on a ROS node

import utm
import math
import rospy
from serial import Serial
from pyubx2 import UBXReader
from transformations import quaternion_from_euler
from std_msgs.msg import Header
from geometry_msgs.msg import PoseWithCovarianceStamped

heading = 0 
lon = 0
lat = 0

def ToLocalXY(lat, lon): #This function translates the longitude and lattitude to local x and y of the parking deck
    global x, y

    utm_coordinates = utm.from_latlon(lat, lon)  #Input the lat and lon coordinates
    angle = math.radians(221.8)     #Input the angle of rotation of the coordinates in degrees according to north

    x = (utm_coordinates[0] - 702486.199827401)*math.cos(angle) + \
        (utm_coordinates[1] - 5764080.1172225075)*math.sin(angle)
    y = (utm_coordinates[1] - 5764080.1172225075)*math.cos(angle) - \
        (utm_coordinates[0] - 702486.199827401)*math.sin(angle)

    return {'x': x, 'y': y}
    
def ToQuaternion(heading): #This function translates the heading angle into quaternion angles
    global w, z

    heading_angle = -math.radians(heading - 230.8) #rotate the angle so that positive x of the parking deck is 0 degrees
    quaternion_angle = quaternion_from_euler(0, 0, heading_angle)
    w = quaternion_angle[0]
    z = quaternion_angle[3]

    return {'z': z, 'w': w}

def main():
    stream = Serial('/dev/ttyACM0', 448000, timeout=3)
    ubr = UBXReader(stream)
    (raw_data, parsed_data) = ubr.read()
    initial_goal_publisher = rospy.Publisher('localization', PoseWithCovarianceStamped, queue_size=10)
    rospy.init_node('location_publisher', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        for (raw_data, parsed_data) in ubr:
            if parsed_data.identity == "NAV-RELPOSNED":
                global heading
                heading = parsed_data.relPosHeading
                print("Heading: {} degrees".format(heading))
            if parsed_data.identity == "NAV-HPPOSLLH":
                global lon, lat
                lon = (parsed_data.lon)
                lat = (parsed_data.lat)
                ToQuaternion(heading)
                ToLocalXY(lat, lon)
                print(x, y)
            localization_msg = PoseWithCovarianceStamped() 
            localization_msg.header = Header()
            localization_msg.header.stamp = rospy.Time.now()
            localization_msg.header.frame_id = "map"
            localization_msg.pose.pose.position.x = x
            localization_msg.pose.pose.position.y = y
            localization_msg.pose.pose.orientation.z = z
            localization_msg.pose.pose.orientation.w = w
            localization_msg.pose.covariance = [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853892326654787]
            initial_goal_publisher.publish(localization_msg)
            rate.sleep()

if __name__ == '__main__':
    main()
