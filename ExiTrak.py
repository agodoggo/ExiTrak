import pyb 
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
def timed_function(f, *args, **kwargs):
    myname = str(f).split(' ')[1]
    def new_func(*args, **kwargs):
        t = utime.ticks_us()
        result = f(*args, **kwargs)
        delta = utime.ticks_diff(utime.ticks_us(), t)
        print('Function {} Time = {:6.3f}ms'.format(myname, delta/1000))
        return result
    return new_func
def main():
    myboard = ExiTrak()
    myboard.pinSetup()
    while(True):
        print(myboard.p_in.value())
        if(myboard.p_in.value() == 1):
            myboard.led.on()
            pyb.delay(1000)
            myboard.led.off()
        # else:
            
if __name__ == "__main__":
    main()