import RPi.GPIO as GPIO 
import smbus
import time
import socket


button = 17
bus = smbus.SMBus(1)
threshold = 128
timeBefore = time.time()
beat = 0
serverMACAddress = 'd8:3a:dd:3c:e0:7b'
port = 4
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def read_ads7830():
    bus.write_byte(0x4b, 0x84)
    time.sleep(0.5)
    return bus.read_byte(0x4b)

def BPMValues():
    global beat, timeBefore
    while True:
        BPMvalue = read_ads7830()
        print("Sensor Value:", BPMvalue)
        
        if BPMvalue > threshold:
            beat += 1
            print("Beat detected")

        if time.time() - timeBefore > 15:
            bpm = beat * 4
            beat = 0
            print("BPM:", bpm)
            timeBefore = time.time()
            text = "BPM:"+str(bpm)
            print(text)
            s.sendto(str.encode(str(text)), (serverMACAddress, port))
        s.sendto(str.encode(str(BPMvalue)), (serverMACAddress, port))
    s.close()
    time.sleep(0.5)  # Sleep for 1 second

# try:
#     BPMValues()
    
def main():
    try:
        while True:
            new_button_state = GPIO.input(button)
            if new_button_state == 0:
                print("Button Pressed")
                BPMValues()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    init()
    main()
