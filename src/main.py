from globals import *
import tkinter as tk
import serial
import threading, time
from os import path

# Creating the root (window)
root = tk.Tk()

# Create serial port
ser = serial.Serial('com3', 115200, timeout=1)

class MotorUI():
    def __init__(self) -> None:
        self.buttonWidth1 = 100
        self.labelWidth1 = 40
        self.motorOn = False
        self.forward = True
        self.accelVal = 0
        self.regenVal = 0
        self.accelTurn = True
        self.vfmCount = 1
        # self.mainTime = time.time()
        # self.forRevTime = time.time()
        # self.accelTime = time.time()
        # self.regenTime = time.time()
        # self.vfmUpTime = time.time()
        # self.vfmDownTime = time.time()
        self.buttonTime = time.time()
        
        self.mainButton = tk.Button(root, text='MAIN', command=self.mainButtonCallBack, 
            background=lightBlue2, foreground='white', font=('Fixedsys', 12), borderwidth=3)
        self.mainLabel = tk.Label(root, text="OFF", font=('Fixedsys', 12), bg='black', foreground='yellow')
        
        self.forRevButton = tk.Button(root, text='FwdRev', command=self.forRevButtonCallBack, 
            background=lightBlue1, foreground='white', font=('Fixedsys', 12), borderwidth=3)
        self.forRevLabel = tk.Label(root, text="FWD", font=('Fixedsys', 12), bg='black', foreground='yellow')

        self.accelSlider = tk.Scale(root, from_=255, to=0, bg=lightBlue1, foreground='black', command=self.accelSliderCallback)
        self.accelLabel = tk.Label(root, text="Accel", font=('Fixedsys', 12), bg=blueish, foreground='white')
        self.accelButton = tk.Button(root, text='Send', command=self.accelButtonCallback) 
        self.regenSlider = tk.Scale(root, from_=255, to=0, bg=lightBlue1, foreground='black', command=self.regenSliderCallback)
        self.regenButton = tk.Button(root, text='Send', command=self.regenButtonCallback) 
        self.regenLabel = tk.Label(root, text="Regen", font=('Fixedsys', 12), bg=blueish, foreground='white')

        self.vfmUpButton = tk.Button(root, text='VFM \n\nUP  ', command=self.vfmUpButtonCallback, 
            background=greenBlue, foreground='white', font=('Fixedsys', 12), borderwidth=3)
        self.vfmDownButton = tk.Button(root, text='VFM \n\nDOWN', command=self.vfmDownButtonCallback, 
            background=greenBlue, foreground='white', font=('Fixedsys', 12), borderwidth=3)
        self.vfmLabel = tk.Label(root, text="1", font=('Fixedsys', 14), bg='black', foreground='yellow')

        # Send initial serial data to DCMB emulator
        off = "MOff"
        ser.write(off.encode('utf8'))

        # fwd = "Forward"
        # ser.write(fwd.encode("utf8"))

       


    def show(self):
        leftX = 40
        rightX = leftX + self.buttonWidth1 + 10

        self.mainButton.place(x=leftX, y=50, width=self.buttonWidth1)
        self.mainLabel.place(x=rightX, y=50, width=self.labelWidth1+5)

        self.forRevButton.place(x=leftX, y=100, width=self.buttonWidth1)
        self.forRevLabel.place(x=rightX, y=100, width=self.labelWidth1+5)

        sliderX = 250
        sliderW = 45
        self.accelSlider.place(x=sliderX, y=50, width=sliderW)
        self.accelButton.place(x=sliderX, y=170, width=sliderW)
        self.accelLabel.place(x=sliderX, y=200)
        sliderX2 = 340
        self.regenSlider.place(x=sliderX2, y=50, width=sliderW)
        self.regenButton.place(x=sliderX2, y=170, width=sliderW)
        self.regenLabel.place(x=sliderX2, y=200)

        self.vfmDownButton.place(x=leftX, y=155)
        self.vfmLabel.place(x=(rightX-leftX), y=165)
        self.vfmUpButton.place(x=rightX, y=155)
        

    def mainButtonCallBack(self):
        if time.time() - self.buttonTime < 1:
            return
        self.buttonTime = time.time()
        if not self.motorOn:
            self.motorOn = True
            self.mainLabel.config(text="ON")
            # Send serial data to DCMB-Emulator
            on = "M On"
            ser.write(on.encode('utf8'))
            print(on)
            
        elif self.motorOn:
            self.motorOn = False
            self.mainLabel.config(text="OFF")
            # Send serial data to DCMB emulator
            off = "MOff"
            ser.write(off.encode('utf8'))
            print(off)
    
    def forRevButtonCallBack(self):
        if time.time() - self.buttonTime < 1:
            return
        self.buttonTime = time.time()
        if not self.forward:
            self.forward = True
            self.forRevLabel.config(text="FWD")
            # Send serial data to DCMB emulator
            fwd = "F wd"
            ser.write(fwd.encode("utf8"))
                
        elif self.forward:
            self.forward = False
            self.forRevLabel.config(text="REV")
            # Send serial data to DCMB emulator
            rev = "R ev"
            ser.write(rev.encode("utf8"))


    def accelButtonCallback(self):
        if time.time() - self.buttonTime < 1:
            return
        self.buttonTime = time.time()
        accelInt = self.accelSlider.get()
        if accelInt < 10:
            accel = "A" + "  " + str(accelInt)
        elif accelInt < 100:
            accel = "A" + " " + str(accelInt)
        else:
            accel = "A" + str(accelInt)
        print(accel)
        ser.write(accel.encode("utf8"))


    def regenButtonCallback(self):
        if time.time() - self.buttonTime < 1:
            return
        self.buttonTime = time.time()
        regenInt = self.regenSlider.get()
        if regenInt < 10:
            regen = "R" + "  " + str(regenInt)
        elif regenInt < 100:
            regen = "R" + " " + str(regenInt)
        else:
            regen = "R" + str(regenInt)
        ser.write(regen.encode('utf8'))
        print(regen.encode('utf8'))

    def accelSliderCallback(self, var): # Note: var is needed due to some tkinter bug?
        # accelValue = str(self.accelSlider.get())
        # accel = "Accel: " + accelValue
        # print(accel)
        # ser.write(accel.encode("utf8"))
        pass
    
    def regenSliderCallback(self, var):
        pass
        # regenValue = str(self.regenSlider.get())
        # regen = "Regen: " + regenValue
        # print(regen)
        # ser.write(regen.encode("utf8"))

    def vfmUpButtonCallback(self):
        if time.time() - self.buttonTime < 1:
            return
        if self.vfmCount >= 4:
            return
        self.buttonTime = time.time()
        self.vfmCount += 1
        self.vfmLabel.config(text=str(self.vfmCount))
        # Send to DCMB emulator
        up = "V" + "  " + str(self.vfmCount)
        ser.write(up.encode("utf8"))
        print(up.encode("utf8"))


    def vfmDownButtonCallback(self):
        if time.time() - self.buttonTime < 1:
            return
        if self.vfmCount <= 1:
            return
        self.buttonTime = time.time()
        self.vfmCount -= 1
        self.vfmLabel.config(text=str(self.vfmCount))
        # Send to DCMB emulator
        down = "V" + "  " + str(self.vfmCount)
        ser.write(down.encode("utf8"))
        print(down.encode("utf8"))
    # not used
    def sendAccelOrRegen(self):
        accelInt = self.accelSlider.get()
        regenInt = self.regenSlider.get()

        if self.accelTurn:
            self.accelTurn = False
            accel = "Accel: " + str(accelInt)
            # print(accel)
            ser.write(accel.encode("utf8"))
        elif not self.accelTurn:
            self.accelTurn = True
            regen = "Regen: " + str(regenInt)
            # print(regen)
            ser.write(regen.encode("utf8"))
        root.after(1000, self.sendAccelOrRegen)

        
# recCounter = 0
'''def receiveData():
    
    stmData1 = ser.readline().decode('ascii').strip()
    stmData2 = ser.readline().decode('ascii').strip()

    # if (receiveData.recCounter % 10) == 0:
    print(stmData1)
    # print()
    print(stmData2)
    print()
    receiveData.recCounter = 0

    receiveData.recCounter += 1
    root.after(500, receiveData) 
    # Note this cycle must be equal or faster than the UART transmission from the microcontroller
    # in order to avoid buffer building up and overflow
receiveData.recCounter = 0'''

# This function shall run in another thread
def receive():
    while 1:
        stmData1 = ser.readline().decode('ascii').strip()
        stmData2 = ser.readline().decode('ascii').strip()

        print(stmData1)
        print(stmData2)
        print()
 

def main():
    root.title('MotorControl')
    root.geometry(str(windowWidth) + "x" + str(windowHeight))
    root['background'] = blueish
    thisFilePath = __file__
    # print("This is the file path:", thisFilePath)
    parentPath = path.dirname(thisFilePath).replace("\\", "/")
    root.iconbitmap(parentPath + '/icon.ico')
    
    motor_ui = MotorUI()
    motor_ui.show()
    # motor_ui.sendAccelOrRegen()

    # receiveData() 
    # Not calling this since receive is now a separate thread
    root.mainloop()
    

if __name__ == "__main__":
    receiveThread = threading.Thread(target=receive)
    receiveThread.daemon = True
    receiveThread.start()
    main()