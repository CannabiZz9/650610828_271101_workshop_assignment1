import serial                                                             
import time        
                                                       
ArduinoUnoSerial = serial.Serial('COM3',9600)   
        
if not ArduinoUnoSerial.isOpen():
    ArduinoUnoSerial.open()
print('com3 is open', ArduinoUnoSerial.isOpen())                                               
print (ArduinoUnoSerial.readline())                             
print ("You have new message from Arduino")
bool = 1
while (bool == 1):         #Do this forever
    var = input("1 or 0?")                                             
    if (var == '1'):                                                       
        ArduinoUnoSerial.write('1'.encode())                         
        print ("LED turned ON")         
        time.sleep(0)          
    if (var == '0'): #if the value is 0         
       ArduinoUnoSerial.write('0'.encode())                
       print ("LED turned OFF")         
       time.sleep(0)
    if (var == 'fine and you'): 
       ArduinoUnoSerial.write('0'.encode()) 
       print ("I'm fine too,Are you Ready to !!!")         
       print ("Type 1 to turn ON LED and 0 to turn OFF LED")         
       time.sleep(1)
    if (var == '99'):
        ArduinoUnoSerial.close()
        bool = 0 