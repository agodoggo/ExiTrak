#main.py -- put your code here!
import pyb
import utime
import machine #This can be removed and the initialization of self.p_in can be done using 'pyb' in the place of 'machine', line 29 
class ExiTrak:
    def __init__(self):
        print("ExiTrak.init") # Used for debugging: prints statement when the method is called
        # self.led = pyb.LED(1)
        # self.sw = pyb.Switch()
        # self.PIN_ON = 1
        self.rtc = pyb.RTC() # Instantiates the Real Time Clock Class from the pyb module
        self.stretchCounter = 0 # Initializes the Stretch Counter to 0 on startup
        self.onesecond =  0x1388 # 5000 in Hexadecimal, equivalent to one second when used with the timer created in initTimer
        self.tenSeconds =  0xc350 # 50,000 in Hexadecimal, equivalent to ten seconds when used with the timer created in initTimer
        self.twentySeconds = 0x186a0  #100,000 in Hexadecimal, equivalent to twenty seconds when used with the timer created in initTimer
        self.sixtySeconds = 0x493e0 #300,000 in Hexadecimal, equivalent to sixty seconds when used with the timer created in initTimer
        self.tenminutes =  0x2dc6c0 #3,000,000 in Hexadecimal, equivalent to ten minutes when used with the timer created in initTimer
        self.hundredminutes = 0x1c9c380 #30,000,000 in Hexadecimal, equivalent to one hundred minutes when used with the timer created in initTimer
        self.myPrescaler = 0x20cf # 8399 in Hexadecimal, used with the timer in initTimer to run at a frequency of 5000 Hz. 
        self.TimerNo = 0x2 # 2 in Hexadecimal, used to select the second timer for use
        self.months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] # an array of the number of days in each month, each index is one month, starting from January
        self.last_saved_dateTime = [2015,1,1,4,0,0,0,0] # Sets the first date saved, values are [year, month, day, weekday, hours, minutes, seconds, subseconds], where weekdays is 1-7 for Monday through Sunday, and subseconds counts down from 255 to 0
        self.last_savedDay = 0 # Sets the last saved day as day zero
        self.curr_day = 0 # Sets the current saved day as zero

    def pinSetup(self):
        print("PinSetup") # Used for debugging: prints statement when the method is called
        microSwitch_in = 'X1' # sets the microSwitch_in to be pin 'X1' on the board
        self.p_in = machine.Pin(microSwitch_in, machine.Pin.IN, pyb.Pin.PULL_DOWN) # initializes the pin 'X1' to be an input pin, with the voltage pulled low. This pin's value will be 0 if connected to ground and 1 if connected to a 3V voltage source.
        print(self.p_in) # Used for debugging: for checking if the microswitch pin 'X1' was instantiated properly
        print(self.p_in.value()) # Used for debugging: prints a 0 if pin 'X1' is pulled to ground, and prints a 1 if pin 'X1' is pulled high to 3V
        self.myExtInt = pyb.ExtInt(pyb.Pin('X1'),pyb.ExtInt.IRQ_RISING,pyb.Pin.PULL_DOWN, self.callback) # Initializes the pin 'X1' to be a pin that triggers an external interrupt that will be triggered by a rising voltage edge, the pin is pulled to ground otherwise, and the external interrupt will call the 'callback' method. Used to wake the pyboard from sleep.
        print("after enable_irq()") # Used for debugging: Checks if code ran past the initializing of the external interrupt to 'X1'

    def callback(self):
        self.myExtInt.disable() # Disables the triggering of any external interrupts to pin 'X1'
        print("Callback entered") # Used for debugging: prints statement when the callback method is called
        self.stretchRegister() # Calls the stretchRegister method from the ExiTrak class
        pyb.delay(500) # delays for 500 seconds, to give time between 
        self.toggleLED(2) # Calls the toggleLED method for LED 2, the green LED
        self.myExtInt.enable() # Enables the triggering of external interrupts to pin 'X1'
        # self.sleep()

    def check_microSwitch(self):
        # print(self.p_in.value())
        print("Microswitch checked") # Used for debugging: prints statement if this method is entered
        return (self.p_in.value() == 1) #returns True or False boolean, depending on the state of pin 'X1'. If pin 'X1' is pulled to 3V, then it returns True, if it is pulled to ground, it returns False.
    def findDay(self,firstDate,secondDate): #This method is used to find the number of days between two given dates, it uses the self.months array initialized in the __init__ method
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
        return self.rtc.datetime() #returns a tuple organized in the following manner, [year, month, day, weekday, hours, minutes, seconds, subseconds], using the datetime function of the RTC class, part of the pyb module
    def initTimer(self):
        print("Timer initialized") #Used for debugging: prints statement when method initTimer is called
        self.sec = pyb.Timer(self.TimerNo, prescaler = self.myPrescaler, period = self.hundredminutes) #initializes the internal timer using the timer number, prescaler, and the period. Please see the documentation on pyb.Timer to see how to select the correct prescaler, period and the timerNo. The prescaler sets how many Hz are in one second, timer 2 operates on 84 Mhz per second, and the timer rolls over back to 0 seconds after one hundred minutes.
        self.sec.counter(0) #Sets the timer counter to 0 seconds.
    def sleep(self):
        print("Machine entering sleep mode") #Used for debugging: prints statement before the PyBoard enters sleep mode
        self.myExtInt.enable() #Enables the external interrupt to ensure the PyBoard can be woken up if the external interrupt is triggered on pin 'X1'
        pyb.stop() # Puts the PyBoard into standby mode, see Pyb.stop() documentation from Micropython for more information about power consumption, etc.
    def stretchRegister(self):
        print("entered Stretch Register") #Used for debugging: prints statement when method has been entered
        self.curr_dateTime = self.getDateTime() # Gets the current dateTime tuple using the getDateTime() method
        self.curr_day = self.findDay(self.last_saved_dateTime,self.curr_dateTime) # Finds the number of days since the last saved day using the findDay() method
        if(self.curr_day == self.last_savedDay): # If the condition is that the current day is the same as the last saved Day, which is set to 0
            print("Curr day = last_savedDay") # Debugging statement: Verifies that the if statement has been passed
            self.last_savedDay = self.curr_day # changes the last saved day to be equal to the current day, this is actually unnecessary. I think the whole if statement can be removed and the elif can be turned into an if statement. The whole reason this if statement is entered is because the two variables are equal, equating them is unnecessary
        elif(self.curr_day > self.last_savedDay): # If the current day is greater than the last saved day, which is set to 0, then the number of saved stretches should be written to the data.txt file
            print("wrote to flash memory") # Debugging statement: prints statement if the function enters the elif statement
            self.writeTime() #Calls the writeTime() method to write the saved number of stretches to the flash memory in the form of a .txt file
            self.stretchCounter = 0 #Sets the stretch counter to zero, resetting the daily stretch count
            for i in range(1,self.curr_day-self.last_savedDay): # for the number of days in between the current day and the last saved day, it will print a 0 for the number of stretches recorded for that day.
                self.writeTime() # Calls the writeTime() method from the ExiTrak class
            self.last_saved_dateTime = self.curr_dateTime # Saves the current dateTime as the last saved dateTime, allowing the next number of days to be accurately calculated for the next time the number of stretches must be written to memory
        self.stretchCounter = self.stretchCounter+1 # Increments the stretchCounter by 1, this should always happen if pin 'X1' is pulled high by the microswitch being pressed
        self.initTimer() #Restarts the timer, in the case of a stretch, the timer should always be restarted
    def toggleLED(self, led_number): #method to flash an LED given an LED_number, turning it on for one second and then turning it off. This is used for user feedback to show the device recognized that they pressed down the microswitch.
        print("toggleLED") #Debugging statement: prints statement if the method has been entered
        led = pyb.LED(led_number) #instantiates an LED object using the pyb module, using the LED number provided
        led.on() # LED turned on
        pyb.delay(1000) # delay for one second
        led.off() # LED turned off
    def writeTime(self):
        file = open("data.txt","a+") #opens a text file. If not there, creates one called data.txt. If data.txt is found, opens it and appends to it.
        file.write(str(self.stretchCounter) + "\n") #Writes the current stretchCounter, and prints a newline using "\n"
        file.close() #closes the file, preventing from any further editing
        stretchCounter = 0 # changes the stretchCounter to 0, preventing the same stretch count from being recorded multiple times

def main():
    myboard = ExiTrak() # initializes the ExiTrak class in myboard
    myboard.pinSetup() #sets the microswitch pin up as an input pin and a pin that triggers an External Interrupt
    myboard.initTimer() # begins the timer
    # pyb.delay(60000)
    while(True): #while loop that runs continuously
        print("seconds"+str(myboard.sec.counter()/5000)) #Debugging statement: Used to print out the current seconds the timer is at.
        pyb.delay(1000) # delays the pyboard by 1 second, this is useful for debugging, because then the number of seconds can be seen clearly. For actual function it is problematic, because it sets a sampling rate of 1 Hz for the microswitch. This can be removed for a version of the code where debugging is unnecessary, however I have left it in for ease of use of any future users. For actual use of the device, however, it is useful because the microswitch is set off by a light pressure, allowing the users to potentially stretch under the threshold necessary to complete a proper stretch. With the 1 second delay, users will only be notified of a completed stretch 1 second after the microswitch is depressed, improving the overall quality of the stretches recorded.
        if(myboard.sec.counter() > myboard.tenminutes): # If the timer has exceeded ten minutes, then the PyBoard will be set to sleep
            print("Timer Reset") # Print statement that verifies the code entered the if statement
            myboard.sec.counter(0) # resets the timer to 0 seconds
            pyb.delay(1000) # delays for 1 second, I am unsure of if this line is necessary, may be removed
            myboard.sleep() # Calls the sleep() method in the ExiTrak class. PyBoard will be in a low-power standby mode, with all of the local variable values saved. It will power on when an External Interrupt will be triggered, in this case it is 'X1' being triggered by a rising voltag edge.
        elif(myboard.check_microSwitch() == True): # If the microswitch has been pushed down, uses the check_microSwitch method in the ExiTrak class
            myboard.toggleLED(2) # Toggles the green LED for 1 s
            myboard.stretchRegister() # calls the stretchRegister method from the ExiTrak class
            print(myboard.stretchCounter) # Debugging Statement: prints the value of the current stretchCounter variable
            # print(myboard.last_saved_dateTime)
            # print(myboard.curr_dateTime)
            print(myboard.last_savedDay) # Debugging Statement: prints the last_savedDay dateTime, which is modified by the stretchRegister class
            print(myboard.curr_day) # Debugging Statement: prints the current day, which is calculated from subtracting the curr_dateTime from the last_saved_dateTime using the findDay() method in the ExiTrak class.
            pyb.delay(1000) # delays for 1 s, allowing the user to read the debug statements onscreen. This and the other delay should potentially be removed from a final user version of the code, because the delays increase the sampling time, which may/may not be undesirable.
    # myboard.sleep()
if __name__ == "__main__":
    main() # calls the main method