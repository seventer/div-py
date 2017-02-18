import json
#import time
import datetime
import psycopg2
import paho.mqtt.client as mqtt

import sys
import urllib2
from pprint import pprint

debug=False

pg_host = "db-host"
pg_db = "db-name"
pg_user = "db-user"
pg_pass = "db-passw"

fmt = "%Y-%m-%d %H:%M:%S"

global bperc

def msg_insert(in_line):
    ndx = in_line.find("{")
    gps_input = in_line[ndx:]

    #print "gps_input: ", gps_input

    decoded = json.loads(gps_input)

    # pretty printing of json-formatted string
    #print json.dumps(decoded, sort_keys=True, indent=4)

    lat = decoded['lat']
    lon = decoded['lon']
    sec = decoded['tst']
    bat = decoded['batt']
    
    global bperc 
    bperc = bat

    time = datetime.datetime.fromtimestamp(float(sec)).strftime(fmt)
   
    adres = getAdres(lat,lon)

    print "Lat : ", lat
    print "Lon : ", lon
    print "Time: ", time
    print "Batt : ", bat
    print "Adres: ", adres

    qry = "INSERT INTO live_gps (lat,lon,wanneer,batt,adres,the_geom) VALUES ('{0}','{1}',  (TIMESTAMP WITHOUT TIME ZONE 'epoch' +  '{2}' * INTERVAL '1 second'), {3}, '{4}'  ,ST_SetSRID(ST_MakePoint({1},{0}),4326));".format(str(lat),str(lon),sec,int(bat),adres)

    return qry


def pg_execute(qry_line):
    str_con = "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(pg_db,pg_user,pg_host,pg_pass)
    #print "str_con: ", str_con
    conn = psycopg2.connect(str_con)
    cur = conn.cursor()
    print "qry: ", qry_line
    cur.execute(qry_line)
    conn.commit()
    cur.close()
    conn.close()


def pub_accu():
    print "inside pub - bperc: ", bperc
    mqtmsg= "{{ \"idx\" : 278, \"nvalue\" : 0, \"svalue\" : \"{0}\", \"Battery\" : {0} }}".format(str(bperc))
    print "mqtmsq: ", mqtmsg
    client.publish("domoticz/in", mqtmsg  ,2)


def getAdres(lat,lon):
    locatieServerNGR = "http://geodata.nationaalgeoregister.nl/locatieserver"

    if debug: 
        print("Lookup adres for Lat=" + lat + "  Lon=" + lon)

    # create string
    url = locatieServerNGR + "/suggest?wt=json&q=type:adres&rows=1&lat=" + lat + "&lon=" + lon  
    urlFile = urllib2.urlopen(url)
    data = json.load(urlFile)
    

    #dumps the json object into an element
    json_str = json.dumps(data)

    #load the json to a string
    resp = json.loads(json_str)

    #extract first id in the response
    adresId = resp["response"]["docs"][0]["id"]

    if debug:
        print("Gevonden adresId=" +  adresId)
    
    # Next call
    url = locatieServerNGR + "/lookup?wt=json&id=" + adresId   
    urlFile = urllib2.urlopen(url)
    data = json.load(urlFile)
    
    if debug:
        pprint(data)

    #dumps the json object into an element
    json_str = json.dumps(data)

    #load the json to a string
    resp = json.loads(json_str)

    #get first weergavenaam from response
    weergaveNaam = resp["response"]["docs"][0]["weergavenaam"]

    return weergaveNaam


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("owntracks/otrack/+")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    try:
    	pg_execute(msg_insert(msg.payload))
    except Exception, error:
        print "Fout in on_message"
	print str(error)
    pub_accu()



bperc = "100"

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.14.24", 1883, 60)

client.loop_forever()




