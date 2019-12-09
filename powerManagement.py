import machine
interruptCounter = 0
totalInterruptsCounter = 0
def callback(pin):
    machine
    print("callback pin value: " + str(p25.value()))
    machi
    print("callback entered")
    global interruptCounter
    interruptCounter = interruptCounter+1
    pyb.delay(1000)
p25 = machine.Pin('X1', machine.Pin.IN, machine.Pin.PULL_DOWN)
print("before pin.irq()")
p25.irq(trigger=machine.Pin.IRQ_RISING, handler=callback)
print("after pin.irq()")
machine.
while True:
    print("pin value: " + str(p25.value()))
    pyb.delay(1000)
    if interruptCounter>0:
        state = machine.disable_irq()
        interruptCounter = interruptCounter-1
        machine.enable_irq(state)
        totalInterruptsCounter = totalInterruptsCounter+1
        print("Interrupt has occurred: " + str(totalInterruptsCounter))