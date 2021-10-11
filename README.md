# How to Use

1. Connect PC to the STM32 DCMB Emulator using the USB to TTL adaptor over the serial port
2. In Windows device manager or MAC equivalent, find the serial port connected to the adaptor and set the baud rate to 115200
3. In main.py, line 11: ser = serial.Serial('com3', 115200, timeout=1), replace 'com3' with the com# you see in the device manager. 

4. Run the Python script and use the buttons and sliders to control the motor. 
