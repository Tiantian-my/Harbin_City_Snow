import os
import threading
import datetime

def env_init():
	rs = []
	rs.append(os.system('cd /home/zhl509/code/data_collection'))
	passwd = '509001'
	command1 = 'ifconfig eno1 192.168.1.102 netmask 255.255.255.0'
	command2 = 'chmod 777 /dev/ttyUSB0'
	command3 = 'chmod 777 /dev/ttyUSB1'
	rs.append(os.system('echo %s | sudo -S %s' % (passwd, command1)))
	rs.append(os.system('echo %s | sudo -S %s' % (passwd, command2)))
	rs.append(os.system('echo %s | sudo -S %s' % (passwd, command3)))
	os.system('python -V')
	for r in rs:
		if r!=0:
			print('Initiation error!')
			return False
	print('Environment initiation done!')
	return True

def run_command(command):
	try:
		print('command %s start running %s' % (command, datetime.datetime.now()))
		os.system(command)
		print('command %s finish running %s' % (command, datetime.datetime.now()))
	except:
		print('%s\t run failed' % (command))
try:
	env_init()
	time = datetime.datetime.now()
	time = time.strftime('%Y-%m-%d-%H-%M-%S')
	print('----------------------------time----------------------------')
	print(time)
	os.mkdir('/home/zhl509/code/data_collection/data/'+time)
	os.mkdir('/home/zhl509/code/data_collection/data/'+time+'/lidar')
	os.mkdir('/home/zhl509/code/data_collection/data/'+time+'/cam0')
	os.mkdir('/home/zhl509/code/data_collection/data/'+time+'/cam1')
	os.mkdir('/home/zhl509/code/data_collection/data/'+time+'/cam2')
	os.mkdir('/home/zhl509/code/data_collection/data/'+time+'/cam3')
	os.mkdir('/home/zhl509/code/data_collection/data/'+time+'/cam4')
	os.mkdir('/home/zhl509/code/data_collection/data/'+time+'/cam5')
	os.mkdir('/home/zhl509/code/data_collection/data/'+time+'/gps_imu')
	commands = []
	commands.append('roslaunch rslidar_sdk start.launch')
	commands.append('sleep 5 && roslaunch usb_cam usb_cam-test.launch')
	commands.append('sleep 10 && roslaunch nmea_navsat_driver nmea_serial_driver.launch')
	commands.append('sleep 15 && roslaunch wit_ros_imu rviz_and_imu.launch')
	commands.append('sleep 20 && python2 topics.py ' + time)

	threads = []
	for cmd in commands:
		th = threading.Thread(target=run_command, args=(cmd,))
		th.start()
		threads.append(th)
		
finally:
	print('closing main2.py...')
	
	print('done.')
