#main.py -- put your code here!
import pyb
import utime
import machine
class ExiTrak:
    def __init__(self):
        print("ExiTrak.init")
        # self.led = pyb.LED(1)
        # self.sw = pyb.Switch()
        # self.PIN_ON = 1
        self.rtc = pyb.RTC()
        self.stretchCounter = 0
        self.onesecond =  0x1388 # 5000 Hz
        self.tenSeconds =  0xc350 # 50,000 
        self.twentySeconds = 0x186a0  #100,000 
        self.sixtySeconds = 0x493e0 #300,000 
        self.tenminutes =  0x2dc6c0 #3,000,000 
        self.hundredminutes = 0x1c9c380 #30,000,000 
        self.myPrescaler = 0x20cf # 8399
        self.TimerNo = 0x2 #2
        self.months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.last_saved_dateTime = [2015,1,1,4,0,0,0,0]
        self.last_savedDay = 1
        self.curr_day = 1

    def pinSetup(self):
        print("PinSetup")
        microSwitch_in = 'X1'
        self.p_in = machine.Pin(microSwitch_in, machine.Pin.IN, pyb.Pin.PULL_DOWN)
        print(self.p_in)
        print(self.p_in.value())
        self.myExtInt = pyb.ExtInt(pyb.Pin('X1'),pyb.ExtInt.IRQ_RISING,pyb.Pin.PULL_DOWN, self.callback)
        print("after enable_irq()")

    def callback(self):
        self.myExtInt.disable()
        print("Callback entered")
        self.stretchRegister()
        pyb.delay(500)
        self.toggleLED(2)
        self.myExtInt.enable()
        # self.sleep()

    def check_microSwitch(self):
        # print(self.p_in.value())
        print("Microswitch checked")
        return (self.p_in.value() == 1)
    def findDay(self,firstDate,secondDate):
        year_diff = secondDate[0] - firstDate[0]
        days = 0
        if(year_diff!=0):
            days = 365 * (year_diff - 1)
            if(firstDate[1]>secondDate[1]):
                for i in range(firstDate[1],12):
                    days = days + self.months[i]
                for i in range(1,secondDate[1]):
                    days = days + self.months[i]
                days = days + self.months[firstDate[1]]-firstDate[2] + secondDate[2]
            elif(firstDate[1]<secondDate[1]):
                days = days + 365
                if(firstDate[1]+1 < secondDate[1]-1):
                    for i in range(firstDate[1]+1,secondDate[1]-1):
                        days = days + self.months[i]
                        # print(i + "," + days)
                days = days + self.months[firstDate[1]]-firstDate[2] + secondDate[2]
            elif(firstDate[1]==secondDate[1]):
                days = days + 365 + secondDate[2]-firstDate[2]
        elif(year_diff==0):
            if(firstDate[1]<secondDate[1]):
                if(firstDate[1]+1 < secondDate[1]-1):
                    for i in range(firstDate[1]+1,secondDate[1]-1):
                        days = days + self.months[i]
                        # print(i + "," + days)
                days = days + self.months[firstDate[1]]-firstDate[2] + secondDate[2]
            elif(firstDate[1]==secondDate[1]):
                days = days + secondDate[2]-firstDate[2]
        return days
    def getDateTime(self):
        return self.rtc.datetime()
    def initTimer(self):
        print("Timer initialized")
        self.sec = pyb.Timer(self.TimerNo, prescaler = self.myPrescaler, period = self.sixtySeconds)
        self.sec.counter(0)
    def sleep(self):
        print("Machine entering sleep mode")
        self.myExtInt.enable()
        pyb.stop()
    def stretchRegister(self):
        print("entered Stretch Register")
        self.curr_dateTime = self.getDateTime()
        print("minutes elapsed" + str(self.curr_dateTime[5]-self.last_saved_dateTime[5]))
        if(self.curr_dateTime[5]-self.last_saved_dateTime[5] >= 1):
            print("wrote to flash memory")
            self.writeTime()
            self.stretchCounter = 0
            # for i in range(1,self.curr_day-self.last_savedDay):
                # self.writeTime()
            # self.last_savedDay = self.curr_day
            print("Old curr_dateTime" + str(self.curr_dateTime))
            print("Old last saved dateTime" + str(self.last_saved_dateTime))
            self.last_saved_dateTime = self.curr_dateTime
            print("New curr_dateTime" + str(self.curr_dateTime))
            print("New last saved dateTime" + str(self.last_saved_dateTime))
        # self.curr_day = self.findDay(self.last_saved_dateTime,self.curr_dateTime)
        # self.curr_day = self.last_savedDay + 1
        # if(self.curr_day == self.last_savedDay):
            # print("Curr day = last_savedDay")
            # self.last_savedDay = self.curr_day
        # elif(self.curr_day >= self.last_savedDay):
            # print("wrote to flash memory")
            # self.writeTime()
            # self.stretchCounter = 0
            # for i in range(1,self.curr_day-self.last_savedDay):
                # self.writeTime()
            # self.last_savedDay = self.curr_day
        self.stretchCounter = self.stretchCounter+1
        self.initTimer()
    def toggleLED(self, led_number):
        print("toggleLED")
        led = pyb.LED(led_number)
        led.on()
        pyb.delay(1000)
        led.off()
    def writeTime(self):
        file = open("data.txt","a+")
        file.write(str(self.stretchCounter) + "\n")
        file.close()
        stretchCounter = 0

def main():
    myboard = ExiTrak()
    myboard.pinSetup()
    myboard.initTimer()
    # pyb.delay(60000)
    while(True):
        print("seconds"+str(myboard.sec.counter()/5000))
        pyb.delay(1000)
        if(myboard.sec.counter() > myboard.tenminutes):
            print("Timer Reset")
            myboard.sec.counter(0)
            pyb.delay(1000)
            myboard.sleep()
        elif(myboard.check_microSwitch() == True):
            myboard.toggleLED(2)
            myboard.stretchRegister()
            print(myboard.stretchCounter)
            # print(myboard.last_saved_dateTime)
            # print(myboard.curr_dateTime)
            print(myboard.last_savedDay)
            print(myboard.curr_day)
            pyb.delay(1000)
    # myboard.sleep()
if __name__ == "__main__":
    main()