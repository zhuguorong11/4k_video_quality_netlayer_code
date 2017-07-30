import ConfigParser
config = ConfigParser.ConfigParser()
config.readfp(open("config.ini","rb"))
ip = config.get("global","ip")
config.set("global","name","liumeiti")
print ip
parses = config.items("global")
print parses
print ip+"asdasd"

client = config.get("clinetIP","ip")
client = client.split(',')
print client