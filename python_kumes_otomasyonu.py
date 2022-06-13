import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import requests
import telepot
import datetime

GPIO.setwarnings(False)

DHT_SENSOR = Adafruit_DHT.DHT11



DHT_PIN = 7
pin = 21
LIGHT_PIN = 23 
led = 11 
pinMQ2 = 14 
buzzer = 24 
t1 = 0.5
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
GPIO.setup(led, GPIO.OUT) 
GPIO.setup(pinMQ2 ,GPIO.IN)
GPIO.setup(buzzer, GPIO.OUT)

GPIO.output(led, GPIO.HIGH )
GPIO.setup(LIGHT_PIN, GPIO.IN)
GPIO.setup(18,GPIO.OUT)
servo1 = GPIO.PWM(18,50)
lOld = not GPIO.input(LIGHT_PIN)


GPIO.setwarnings(False)

n_liste = [0]
s_liste = [0]
t_liste = [0]

telegram_bot = telepot.Bot("1489619748:AAEwGmJAqkYbDo_tM7cdpDEblJqOJ3UjOu0")

receive_url = 'https://api.telegram.org/bot1489619748:AAEwGmJAqkYbDo_tM7cdpDEblJqOJ3UjOu0/getUpdates'
base_url = 'https://api.telegram.org/bot1489619748:AAEwGmJAqkYbDo_tM7cdpDEblJqOJ3UjOu0/sendMessage?chat_id=-441146678&text='
photo_url = "https://api.telegram.org/bot1489619748:AAEwGmJAqkYbDo_tM7cdpDEblJqOJ3UjOu0/sendPhoto";
data = {'chat_id': "-441146678"}
servo1.start(0)

tc = ""
time.sleep(10)
print("Sistem Çalışıyor")
while 1:
    q = datetime.datetime.now().second
    if int(q) % 10 == 0:
        get_u = requests.post(receive_url).json()
        dic = get_u['result'][-1]
        tc = dic['message']['text']
    else:
        pass
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    s_liste.append(temperature)
    n_liste.append(humidity)

    if humidity is not None and temperature is not None:
        print(temperature, humidity)
if s_liste[-1] > int(22):

            try:
                if s_liste[-2] < int(22):
                    start = datetime.datetime.now()

                    GPIO.output(pin, GPIO.LOW)

                    
            except:
                pass
            if s_liste[-2] is None:
                start = datetime.datetime.now()

                GPIO.output(pin, GPIO.LOW)
                

        else:
            try:
                GPIO.output(pin, GPIO.HIGH)
                dur = datetime.datetime.now() - start
                t_liste.append(dur)

            except:

                pass
    else:
        pass
    if GPIO.input(LIGHT_PIN) != lOld:
        if GPIO.input(LIGHT_PIN):
            GPIO.output(led, GPIO.HIGH)
            print(GPIO.input(LIGHT_PIN))
        else:
            GPIO.output(led, GPIO.LOW)

    lOld = GPIO.input(LIGHT_PIN)
    time.sleep(1)
    if (GPIO.input(pinMQ2) == 0):
        print(GPIO.input(pinMQ2))
        GPIO.output(buzzer, GPIO.HIGH)
        time.sleep(t1)
        GPIO.output(buzzer, GPIO.LOW)
        time.sleep(t1)
        requests.get(base_url + "GAZ KAÇAĞI VAR !!!!!")

    else:
   
        pass
    if tc == "/Grafik Sıcaklık":
        print("Sıcaklık Grafiği Hazırlanıyor ...")
        Not_none_values = filter(None.__ne__, s_liste)

        s_liste2 = list(Not_none_values)

        plt.plot(range(0, len(s_liste2)), (s_liste2))
        plt.xlabel('Zaman')
        plt.ylabel('Sıcaklık')

        plt.savefig('t_send.png')

        plt.clf()

        time.sleep(1)
        tc = ""
        files = {'photo': open('/home/pi/t_send.png', 'rb')}
        r = requests.post(photo_url, files=files, data=data)
    if tc == "/Grafik Nem":
        print("Nem Grafiği Hazırlanıyor ...")
        Not_none_values = filter(None.__ne__, n_liste)

        n_liste2 = list(Not_none_values)

        plt.plot(range(0, len(n_liste2)), (n_liste2))
        plt.xlabel('Zaman')
        plt.ylabel('Nem')

        plt.savefig('n_send.png')
        plt.clf()
        time.sleep(1)
        tc = ""
        files = {'photo': open('/home/pi/n_send.png', 'rb')}
        r = requests.post(photo_url, files=files, data=data)
    if tc == "/Grafik iki":
        print("Sıcaklık ve Nem Grafiği Hazırlanıyor")
        Not_none_values = filter(None.__ne__, n_liste)
        n_liste2 = list(Not_none_values)

        Not_none_values = filter(None.__ne__, s_liste)
        s_liste2 = list(Not_none_values)

        plt.plot(range(0, len(s_liste2)), (s_liste2))
        plt.plot(range(0, len(n_liste2)), (n_liste2))
        plt.xlabel('Zaman')
        plt.ylabel('Sıcaklık ve Nem')

        plt.savefig('2_send.png')
        plt.clf()
        time.sleep(1)
        tc = ""
        files = {'photo': open('/home/pi/2_send.png', 'rb')}

        r = requests.post(photo_url, files=files, data=data)

    if tc == "/Çalışma Aralığı":
        print("Çalışma Aralığı Grafiği Hazırlanıyor ...")
        plt.plot(range(0, len(t_liste)), (t_liste))
        plt.xlabel('Zaman')
        plt.ylabel('Çalışma Zamanı')

        plt.savefig('t_send.png')

        time.sleep(1)
        t = ""
        files = {'photo': open('/home/pi/t_send.png', 'rb')}
        r = requests.post(photo_url, files=files, data=data)

    if tc == "/Sıcaklık":
        try:
            print("Sıcaklık : ", s_liste[-1])
            t = base_url + "Sıcaklık : " + str(s_liste[-1])

            requests.get(t)
            tc = ""
        except:
            pass

    if tc == "/Nem":
        try:
            print("Nem : ", n_liste[-1])
            q = base_url + "Nem : " + str(n_liste[-1])
            tc = ""
            requests.get(q)
        except:
            pass

    if tc == "/kapıyı aç" :
        print("kapı açıl")

        servo1.ChangeDutyCycle(2.5)
        time.sleep(0.4)
        servo1.ChangeDutyCycle(0)
        q = base_url + "Kapı açılıyor... "
        tc = ""
        requests.get(q)
        
    if tc == "/Kapı kapan":
        print("Kapı kapanıyor")
        servo1.ChangeDutyCycle(7.5)
        time.sleep(0.4)
        servo1.ChangeDutyCycle(0)
        q = base_url + "Kapı kapanıyor... "
        tc =""
        requests.get(q)
