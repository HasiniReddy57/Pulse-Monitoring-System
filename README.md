Pulse Monitoring System

Description:
Pulse monitoring system was developed to monitor the pulse of an individual. 
This system was developed using 2 Raspberry Pi's. A pulse sensor (HW 827) is connected to an Rpi which acts as client. 
Client RPi sends pulse data to server RPi over Bluetooth. A GUI was developed on server RPi using python's Tkinter library to visualize the pulse of the user. 
This GUI provides pulse in BPM, traces the pulse graph and updates every second, alerts if BPM is abnormal wrt the age of the user.

Hardware Components:
1. 2 Raspberry Pi's - Server and Client.
2. Pulse Sensor – HW827
3. ADS 7830
4. Push Button
5. Resistors
6. Connectors


Steps to execute:
1. Load BTClient.py and BTServer.py onto each of the Raspberry pi's.
2. Connect the hardware as shown in Circuit Diagram.png
3. Run the programs on Rpi's. BT connection is established between both the Pi's.
4. A small GUI screen with user name and age is asked. Fill the details and follow the on-screen instructions (Hold the sensor, push the button and submit the details).
5. Pulse rate and BPM will be calculated and displayed on GUI.
