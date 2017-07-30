djangoInfo文件夹包含的是前端与后台的交互
1、其中创建数据库表 或 更改数据库表或字段：
Django 1.7.1及以上 用以下命令
# 1. 创建更改的文件
python manage.py makemigrations
# 2. 将生成的py文件应用到数据库
python manage.py migrate

2、使用开发服务器：
python manage.py runserver
 
# 当提示端口被占用的时候，可以用其它端口：
python manage.py runserver 8001
python manage.py runserver 9999




packetAnaylyze包含的是对数据包的抓取和网络层数据的分析
	进入NetInfo文件夹后运行sudo python startProcess.py即可以进行抓包分析存储
