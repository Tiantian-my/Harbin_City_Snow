# Harbin_City_Snow
哈尔滨城市雪景采集系统使用源码及使用说明  
## 安装  
代码需要在ros环境下运行，请根据linux版本安装对应ros环境。  
推荐在工作目录下git clone，即可得到正确的目录结构。  
## 使用  
使用时建议删除工作目录下的build、devel和src目录下的CMakeList.txt文件夹。  
在工作目录下运行`catkin_make`重新编译，编译成功后运行`python2 main2.py`即可开始采集。  
采集顺利进行的标志是持续打印以下内容：
