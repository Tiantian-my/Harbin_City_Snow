#!/usr/bin/env python2
# coding=UTF-8
'''
此程序为测试测试程序， 用以测试message_filters同时
订阅两个topic，可以同时进行数据处理。
'''
import rospy, math, random, cv_bridge, cv2, os, sys
import numpy as np
import message_filters
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image, CameraInfo, NavSatFix, PointCloud2, TimeReference, Imu
from sensor_msgs import point_cloud2

count = 0

if len(sys.argv)==1:
    print('Error: parameter lost! ')
    sys.exit()
elif len(sys.argv)>2:
    print('Error: too many parameters! ')
    sys.exit()
time = sys.argv[1]

def multi_callback(Subcriber_cam0, Subcriber_cam1, Subcriber_cam2, Subcriber_cam3, Subcriber_cam4, Subcriber_cam5, Subcriber_gps, Subcriber_imu, Subcriber_lidar):
    bridge = cv_bridge.CvBridge()
    cam0_data = bridge.imgmsg_to_cv2(Subcriber_cam0, 'bgr8')#常规操作
    cam1_data = bridge.imgmsg_to_cv2(Subcriber_cam1, 'bgr8')
    cam2_data = bridge.imgmsg_to_cv2(Subcriber_cam2, 'bgr8')
    cam3_data = bridge.imgmsg_to_cv2(Subcriber_cam3, 'bgr8')
    cam4_data = bridge.imgmsg_to_cv2(Subcriber_cam4, 'bgr8')
    cam5_data = bridge.imgmsg_to_cv2(Subcriber_cam5, 'bgr8')

    global count
    print("Frame %d saved!" % count)
    count += 1
    
    gps_data = Subcriber_gps
    imu_data = Subcriber_imu
    lidar_data = Subcriber_lidar

    # cam0_stamp = Subcriber_cam0.header.stamp.secs
    # cam1_stamp = Subcriber_cam1.header.stamp.secs
    # cam2_stamp = Subcriber_cam2.header.stamp.secs
    # gps_stamp = Subcriber_gps.header.stamp.secs
    # lidar_stamp = Subcriber_lidar.header.stamp.secs
    
    # print(cam0_stamp)
    # print(cam1_stamp)
    # print(cam2_stamp)
    # print(gps_stamp)
    # print(lidar_stamp)
    stamp = Subcriber_lidar.header.stamp.secs
    path = '/home/zhl509/code/data_collection/data/' + time + '/'
    save_cams(cam0_data, cam1_data, cam2_data, cam3_data, cam4_data, cam5_data, path, stamp)
    save_lidar(lidar_data, path, stamp)
    save_gps_imu(gps_data, imu_data, path, stamp)
    # print(gps_data)

    # save_pcd(Subcriber_lidar)
    
    # cv2.imshow("window", cam0_data)
    # cv2.imshow("window2", cam1_data)
    # cv2.imshow("window3", cam2_data)
    cv2.waitKey(1)


def save_lidar(lidar_data, path, stamp):
    points_pc2 = point_cloud2.read_points(lidar_data, skip_nans=True)
    # points = point_cloud2.read_points_numpy(PointCloud2_data, skip_nans=True)
    points_np = np.asarray(list(points_pc2), dtype=np.float32)
    path_lidar = path + 'lidar/' + str(stamp) + '.bin'
    points_np.tofile(path_lidar)

def save_cams(cam0_data, cam1_data, cam2_data, cam3_data, cam4_data, cam5_data, path, stamp):
    path0 = path + 'cam0/' + str(stamp) + '.jpg'
    path1 = path + 'cam1/' + str(stamp) + '.jpg'
    path2 = path + 'cam2/' + str(stamp) + '.jpg'
    path3 = path + 'cam3/' + str(stamp) + '.jpg'
    path4 = path + 'cam4/' + str(stamp) + '.jpg'
    path5 = path + 'cam5/' + str(stamp) + '.jpg'
    cv2.imwrite(path0, cam0_data)
    cv2.imwrite(path1, cam1_data)
    cv2.imwrite(path2, cam2_data)
    cv2.imwrite(path3, cam3_data)
    cv2.imwrite(path4, cam4_data)
    cv2.imwrite(path5, cam5_data)

def save_gps_imu(gps_data, imu_data, path, stamp):
    path_gps = path + 'gps_imu/' +str(stamp) + '.txt'
    with open(path_gps, 'w') as file:
        latitude = str(gps_data.latitude)
        file.write(latitude + '\n')
        longitude = str(gps_data.longitude)
        file.write(longitude + '\n')
        altitude = str(gps_data.altitude)
        file.write(altitude + '\n')
        pos_cov = str(gps_data.position_covariance)
        file.write(pos_cov + '\n')
        pos_cov_type = str(gps_data.position_covariance_type)
        file.write(pos_cov_type + '\n')
        orientation = str([imu_data.orientation.x, imu_data.orientation.y, imu_data.orientation.z, imu_data.orientation.w])
        file.write(orientation + '\n')
        ort_cov = str(imu_data.orientation_covariance)
        file.write(ort_cov + '\n')
        ang_vel = str([imu_data.angular_velocity.x, imu_data.angular_velocity.y, imu_data.angular_velocity.z])
        file.write(ang_vel + '\n')
        ang_cov = str(imu_data.angular_velocity_covariance)
        file.write(ang_cov + '\n')
        linear_accel = str([imu_data.linear_acceleration.x, imu_data.linear_acceleration.y, imu_data.linear_acceleration.z])
        file.write(linear_accel + '\n')
        linear_cov = str(imu_data.linear_acceleration_covariance)
        file.write(linear_cov + '\n')


if __name__ == '__main__':


    rospy.init_node('two_TOPIC', anonymous=True)#初始化节点

    print('initiation done!')
    
    subcriber_cam0 = message_filters.Subscriber('/usb_cam0/image_raw', Image)#订阅第一个话题，rgb图像
    subcriber_cam1 = message_filters.Subscriber('/usb_cam1/image_raw', Image)#订阅第二个话题，rgb图像
    subcriber_cam2 = message_filters.Subscriber('/usb_cam2/image_raw', Image)
    subcriber_cam3 = message_filters.Subscriber('/usb_cam3/image_raw', Image)
    subcriber_cam4 = message_filters.Subscriber('/usb_cam4/image_raw', Image)
    subcriber_cam5 = message_filters.Subscriber('/usb_cam5/image_raw', Image)
    print('usb_cam opened!')
    subcriber_gps = message_filters.Subscriber('/fix', NavSatFix)
    # subcriber_gps = message_filters.Subscriber('/time_reference', TimeReference)
    print('gps opened!')
    subcriber_imu = message_filters.Subscriber('/imu/data', Imu)
    print('imu opened!')
    subcriber_lidar = message_filters.Subscriber('/rslidar_points', PointCloud2)
    print('lidar opened!')
    # sync = message_filters.ApproximateTimeSynchronizer([subcriber_cam0, subcriber_cam1, subcriber_cam2, subcriber_lidar], 10,0.05)#同步时间戳，具体参数含义需要查看官方文档。
    sync = message_filters.ApproximateTimeSynchronizer([subcriber_cam0, subcriber_cam1, subcriber_cam2, subcriber_cam3, subcriber_cam4, subcriber_cam5, subcriber_gps, subcriber_imu, subcriber_lidar], 10, 0.1)#同步时间戳，具体参数含义需要查看官方文档。
    # sync = message_filters.TimeSynchronizer([subcriber_cam0, subcriber_cam1, subcriber_cam2, subcriber_gps, subcriber_lidar], 50)#同步时间戳，具体参数含义需要查看官方文档。
    print('synchronization done!')
    sync.registerCallback(multi_callback)#执行反馈函数
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("over!")
        cv2.destroyAllWindows()

