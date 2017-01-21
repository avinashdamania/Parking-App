#Libraries
import RPi.GPIO as GPIO
import time
import MySQLdb
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
A1Trig = 5
A1Echo = 6
A2Trig = 21
A2Echo = 20
B1Trig = 23
B1Echo = 24
 
#set GPIO Pin directions (IN / OUT)
GPIO.setup(A1Trig, GPIO.OUT)
GPIO.setup(A1Echo, GPIO.IN)
GPIO.setup(A2Trig, GPIO.OUT)
GPIO.setup(A2Echo, GPIO.IN)
GPIO.setup(B1Trig, GPIO.OUT)
GPIO.setup(B1Echo, GPIO.IN)
 
def distance(trigPin,echoPin):
    # set Trigger to HIGH
    GPIO.output(trigPin, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trigPin, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(echoPin) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(echoPin) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
if __name__ == '__main__':
    link = MySQLdb.connect(host ="172.20.10.3", port = 8889, passwd = "testpass", user = "testuser", db =  "ParkingSpaces") #Secure connection to mySQL Database
    m=link.cursor() #Create a cursor object to send commands
    try:
        while True:
            #obtain distances from each sensor
            dist1 = distance(A1Trig,A1Echo)
            dist2 = distance(A2Trig,A2Echo)
            dist3 = distance(B1Trig,B2Echo)
            print ("Measured Distance A1 = %.1f cm" % dist1)
            print ("Measured Distance A2 = %.1f cm" % dist2)
            print ("Measured Distance B1 = %.1f cm" % dist3)
            time.sleep(1)
            #Check whether each sensor is triggered
            if(dist1<10 || dist1>1000):
                A1Full = True
            else:
                A1Full = False
            if(dist2<10 || dist1>1000):
                A2Full = True
            else:
                A2Full = False
            if(dist3<10 || dist1>1000):
                B1Full = True
            else:
                B1Full = False
            parkSpaces = [A1Full,A2Full,B1Full]
            #Update mySQL database with live sensor data
            if(A1Full==True):
                m.execute("""UPDATE Lot1 SET filled = 1 WHERE id = 1""")
                link.commit()
            if(A1Full==False):
                m.execute("""UPDATE Lot1 SET filled = 0 WHERE id = 1""")
                link.commit()
            if(A2Full==True):
                m.execute("""UPDATE Lot1 SET filled = 1 WHERE id = 2""")
                link.commit()
            if(A2Full==False):
                m.execute("""UPDATE Lot1 SET filled = 0 WHERE id = 2""")
                link.commit()
            if(B1Full==True):
                m.execute("""UPDATE Lot1 SET filled = 1 WHERE id = 3""")
                link.commit()
            if(B1Full==False):
                m.execute("""UPDATE Lot1 SET filled = 0 WHERE id = 3""")
                link.commit()
            time.sleep(8)
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
	m.close()
	link.close()
        print("Measurement stopped by User")
        GPIO.cleanup()
