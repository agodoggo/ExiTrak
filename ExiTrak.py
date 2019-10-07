import pyb
class ExiTrak:
    def switchSetup(self):
        sw = pyb.Switch()
        sw.callback(lambda: pyb.LED(1).toggle())
    def pinSetup(self):
        microSwitch_in = 'X1'
        p_in = pyb.Pin(microSwitch_in, pyb.Pin.IN)
def main():
    myboard = ExiTrak()
    myboard.pinSetup()
    while(True):
        if(p_in.value() = 1):
            pyb.LED(1).on()
            pyb.delay(1000)
            pyb.LED(1).off()
        else:
            pyb.LED(1).off()
            
        
    
if __name__ == "__main__":
    main()
