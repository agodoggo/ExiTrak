import pyb
import utime
import machine
class ExiTrak:
    def __init__(self):
        self.led = pyb.LED(1)
        self.sw = pyb.Switch()
        self.p_in = None
    def switchSetup(self):
        sw = pyb.Switch()
        sw.callback(lambda: pyb.LED(1).toggle())
    def pinSetup(self):
        microSwitch_in = 'X1'
        self.p_in = pyb.Pin(microSwitch_in, pyb.Pin.IN, pyb.Pin.PULL_UP)
    def toggleLED(self):
        led = pyb.LED(1)
        led.on()
        pyb.delay(1000)
        led.off()
    def check_microSwitch(self):
        return (p_in.value() == 1)
class Functions:
    def __init__(self):
        self.rtc = machine.RTC()
        self.file = open("data.txt","a+")
    def getTime(self):
        rtc = machine.RTC()
        # rtc.init([(2019, 10, 8, 2, 14, 46, 36, 104])
        return rtc.datetime()
    
def main():
    myboard = ExiTrak()
    myFunctions = Functions()
    myboard.pinSetup()
    while(True):
        print(myboard.p_in.value())
        if(myboard.p_in.value() == 1):
            print("past if statement")
            time = myFunctions.getTime()
            print(str(time))
            myFunctions.file.write(str(time))
            myboard.toggleLED()
        # else:
            
if __name__ == "__main__":
    main()