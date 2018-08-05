#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import picamera
import time
import RPi.GPIO as GPIO
import sqlite3
import datetime

PICTURE_WIDTH = 800
PICTURE_HEIGHT = 600
SAVEDIR = "/home/pi/python/static/"
INTAVAL = 10
SLEEPTIME = 5
SENSOR_PIN = 9

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

cam = picamera.PiCamera()
cam.resolution = (PICTURE_WIDTH,PICTURE_HEIGHT)
st = time.time() - INTAVAL

# データベースに書き込み
def sqlite_insert():
    dbname = '/home/pi/python/monitoring.db'
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    output_time = datetime.datetime.now()
    output_time = "{0:%Y-%m-%dT%H:%M:%SZ}".format(output_time)
    data = (output_time, (filename))
    cur.execute('insert into monitoring (date, filename) values (?,?)', (data))
    con.commit()
    con.close()

# データベースから取り出し
def sqlite_select():
    dbname = '/home/pi/python/monitoring.db'
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    cur.execute('SELECT filename FROM monitoring order by date desc limit 20')
    global fn
    fn = [(y[0]) for y in cur.fetchall()]
    con.close()

# htmlファイル生成
def html_create():
    url = "http://<IP Address>:5000/static/"
    with open("/home/pi/python/templates/monitoring.html", "w") as file:
     file.write("<!doctype html>")
     file.write("<html lang=\"en\">")
     file.write("<head>")
     file.write("<meta charset=\"utf-8\">")
     file.write("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\">")
     file.write("<link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css\" integrity=\"sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO\" crossorigin=\"anonymous\">")
     file.write("<title>Monitoring system</title>")
     file.write("</head>")
     file.write("<body>")
     file.write("<h1 class=\"display-4\">Monitoring system</h1>")
     file.write("<div class=\"alert alert-warning\" role=\"alert\"><input type=\"button\" value=\"Reload\" class=\"btn btn-info\" onclick=\"window.location.reload(true);\"> A simple warning alert—check it out!</div>")
     file.write("<table class=\"table table-striped\">")
     file.write("<thead class=\"thead-dark\">")
     file.write("<tr>")
     file.write("<th scope=\"col\">Filename</th>")
     file.write("</tr>")
     file.write("</thead>")
     file.write("<tbody>")
     for i in fn:
         file.write("<tr>")
         file.write("<th scope=\"row\"><a href=" + url + i + ">" + i + "</a></th>")
         file.write("</tr>")
     file.write("</tbody>")
     file.write("</table>")
     file.write("<script src=\"https://code.jquery.com/jquery-3.3.1.slim.min.js\" integrity=\"sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo\" crossorigin=\"anonymous\"></script>")
     file.write("<script src=\"https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js\" integrity=\"sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49\" crossorigin=\"anonymous\"></script>")
     file.write("<script src=\"https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js\" integrity=\"sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy\" crossorigin=\"anonymous\"></script>")
     file.write("</body>")
     file.write("</html>")

while True:
    if (GPIO.input(SENSOR_PIN) == GPIO.HIGH) and (st + INTAVAL < time.time()):
       st = time.time()
       filename = time.strftime("%Y%m%d-%H:%M:%S") + ".jpg"
       save_file = SAVEDIR + filename
       cam.capture(save_file)
       sqlite_insert()
       sqlite_select()
       html_create()
    time.sleep(SLEEPTIME)
