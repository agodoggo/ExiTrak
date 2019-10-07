import pyb
class ExiTrak:
    def switchSetup(self):
        sw = pyb.Switch()
        sw.callback(lambda: pyb.LED(1).toggle())
        
def main():
    myboard = ExiTrak()
    myboard.switchSetup()
    
if __name__ == "__main__":
    main()
