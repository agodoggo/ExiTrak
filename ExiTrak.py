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
    myboard.switchSetup()
    
if __name__ == "__main__":
    main()
