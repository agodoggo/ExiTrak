#main.py -- put your code here!
import pyb
import utime
import machine
class ExiTrak:
    def __init__(self):
        self.led = pyb.LED(1)
        self.sw = pyb.Switch()
        self.p_in = None
        self.PIN_ON = 1
    def switchSetup(self):
        sw = pyb.Switch()
        sw.callback(lambda: pyb.LED(1).toggle())
    def pinSetup(self):
        microSwitch_in = 'X1'
        self.p_in = pyb.Pin(microSwitch_in, pyb.Pin.IN, pyb.Pin.PULL_DOWN)
        self.p_in.irq(trigger=machine.Pin.IRQ_HIGH_LEVEL, handler=Functions.stretchRegister())
    def toggleLED(self):
        led = pyb.LED(1)
        led.on()
        pyb.delay(1000)
        led.off()
    def check_microSwitch(self):
        return (p_in.value() == 1)
    def Sleep:
        pyb.stop()
        
class Functions:
    def __init__(self):
        self.rtc = machine.RTC()
        self.stretchCounter = 0
        self.hundredminutes = 60000000
        self.tenminutes = 6000000
        self.myPrescaler = 8399
        self.TimerNo = 2
    def getTime(self):
        return rtc.datetime()
    def stretchRegister(self):
        if day has changed:
            writeTime the last day recorded with the counter = counter
            writeTime all the other days with the counter = 0
        else:
            stretchCounter++
        myboard.toggleLED()
        init_Timer()
    def writeTime(self):
        file = open("data.txt","a+")
        file.write(stretchCounter + "\n")
        file.close()
        stretchCounter = 0
    def init_Timer(self):
        sec = pyb.Timer(TimerNo, prescaler = myPrescaler, period = hundredminutes)
        sec.counter(0)
def main():
    myboard = ExiTrak()
    myFunctions = Functions()
    myboard.pinSetup()
    myFunction.initTimer()
    while(True):
        if(myFunctions.sec.counter() <= myFunctions.tenminutes):
            myboard.Sleep()   
        else if(myboard.check_microSwitch):
            myFunctions.stretchRegister()           
if __name__ == "__main__":
    main()