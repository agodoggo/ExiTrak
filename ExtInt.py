# main.py -- put your code here!
def callback(line):
    # ExtInt.disable()
    print("toggleLED")
    print("line =" + line)
    # print(ExtInt.line())
    led = pyb.LED(2)
    led.on()
    pyb.delay(1000)
    led.off()
    # ExtInt.enable()
p_in = pyb.Pin('X1', pyb.Pin.IN, pyb.Pin.PULL_DOWN)
ExtInt = pyb.ExtInt('X1',pyb.ExtInt.IRQ_RISING_FALLING,pyb.Pin.PULL_DOWN,callback('X1'))
while(True):
    print(p_in.value())
    pyb.delay(1000)