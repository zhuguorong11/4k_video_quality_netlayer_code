import pyhdfs

fs = pyhdfs.HdfsClient(hosts='10.149.252.106')
f = fs.listdir('/')
status = fs.list_status('/')
print f
print status
# fs.mkdirs('/zgr')
# fs.delete('/zgr')
