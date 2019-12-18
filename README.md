# ExiTrak
BME 462 Project

Introduction:

This README is intended to function as a guide on how to use the ExiTrak, built on the PyBoard v1.1 by Qarch Hawk, Maddie Manning, Matthew Salvino, and Agoston Walter for Dr. Malkin's course, BME 462, in the Fall of 2019.
This is the fourth semester of work on the project. This semester our group improved the mechanical design and wrote the software for the PyBoard.
Dr. Malkin informed us that the mechanical design was lacking in protection for the electronics, so another group will finalize the mechanical design.
The software written for the boards is functional, but can also be improved, and potential improvements will be mentioned at the end of the document.

Everythign learned about the PyBoard was done online through google searches and forums, but an indispensable source of knowledge is the extensive micropython documentation.
Please visit http://docs.micropython.org/en/latest/ to learn more about the MicroPython language the PyBoard runs on.

Software Included:

There are two python files included in the folder, ExiTrak_demoVersion.py and ExiTrak_untestedVersion.py.
ExiTrak_demoVersion.py is what was used for the demonstration, and is functional for the field. 
ExiTrak_untestedVersion.py contains some of the changes to the software and hardware our group would have liked to have seen in the next iteration of the product. It does not work, but I have included it as a base to build off from using the demonstration code, if the improvements we tried to add are deemed beneficial by the next team.

Software Description:

ExiTrak_demoVersion.py runs by setting pin 'X1' to be an input pin. It is connected to a microswitch, which, when depressed, connects pin 'X1' to the 3V output of the PyBoard.
Otherwise, pin 'X1' is pulled low to ground. A stretch is registered by the device if the microswitch is depressed and pin 'X1' is pulled high. Otherwise, if no stretch is detected for more than ten minutes, the PyBoard enters a low-power standby mode.
If the microswitch is depressed while it is in sleep mode, the PyBoard wakes up and registers the stretch. Stretch data is written to a .txt file in the flash memory of the PyBoard when a stretch is made that is 24 hours since the last time data was stored.

There are three things we would like to implement in the software which we will mention in the 'Improvements Suggested' section.
One, there should be a way to suspend sleep mode to allow the community health worker to check the data stored on the device without having to depress the microswitch, which will store that as a stretch.
Two, if the first improvement is implemented, the device should always be in standby/low-power mode to conserve power. The device should come out of it only momentarily when the microswitch is depressed and a stretch is recorded, and then immediately return to sleep. If a community health worker needs to access the data on the device, they can suspend sleep mode to do it.
Three, the data should not be recorded when a stretch is registered, but should be done automatically every twenty four hours using the RTC (Real Time Clock) object. This way, data can never be lost if users do not perform stretches everyday and the device loses power.

Operation of the ExiTrak:

To operate the ExiTrak, there must be two AA batteries in the battery holder. There is no on/off switch, so the PyBoard will turn on automically.
Ideally, the battery holder should have room for three AA batteries, because the ExiTrak documentation states the board should operate on above 3.5 V of power.
However, when used with two AA batteries which together generate around 3.2 V, the pyboard turned on and was functioning, so our group decided it was enough.
The previous group also operated the PyBoard with around 3V of power using two CR2032 1.5 V batteries. We decided to use two AA batteries to extend the lifetime of the device between battery changes.

Once the batteries are in and the device is powered, switch the small black battery pack containing two CR2032 1.5 V batteries ON. This power source should also always be on.
Our group could only find a battery pack that had an ON/OFF switch, but ideally there should be no OFF switch for this power source, so there is one potential improvement for future teams.
This power source powers the Real Time Clock on the PyBoard. To conserve power, the PyBoard will enter a standby mode, and the Real Time Clock will shut off unless it is powered externally through the VBAT pin.
Having the RTC on is necessary to tell what day it is, which is how the PyBoard knows when to record the number of stretches, more on this later.

Once both battery sources are on, the PyBoard is ready for use. If the code is already on there, it should execute automatically upon power up. If not, you will have to insert the Python code yourself.
To upload the code you wish to run on the PyBoard, plug in the PyBoard to your computer using a microUSB cable. Upon plugging it in, you can access the files on the PyBoard like a flash drive, it will appear in the Devices and Drives section of File Explorer (if you're using a PC).
You will see two files on every PyBoard: boot.py and main.py. boot.py runs first on startup, generally you shouldn't touch this one. main.py runs next, this is where you will paste the code you wish to run.
After you are finished editing, make sure to eject the PyBoard using the Safely Remove Hardware option on your computer, otherwise the data on it will be corrupted when you plug it in next. 
If this happened to you and the data files on the PyBoard have turned unreadable/corrupted, follow the instructions at https://docs.micropython.org/en/latest/pyboard/tutorial/reset.html. 
You have to reset the PyBoard by first holding down the USR switch, while holding it down, pressing and releasing the RST switch. The LEDs will cycle green to orange to green+orange and back again, keep holding down USR until both the green and orange LEDs are lit, and then let go of the USR switch. The green and orange LEDs will flash 4 times, other LEDs will turn on, and the file system will be reset and the PyBoard will boot in safe mode. To boot normally, press and release the RST switch.

In the case if you wanted to run ExiTrak_demoVersion, you would plug the PyBoard in, open the main.py file, then edit it however you wished, and then safely eject the USB drive, using the eject USB safely option on your computer.
If you did this, the next time you press the RST button to turn the PyBoard on and off again, the code you edited will run.

If you want to access the stretch data, connect the PyBoard to your computer using a microUSB, and open the data.txt file. In the file, the last saved date will appear last, which means  assuming you stretched  today, yesterday will be the last line you see.
In a data.txt with ten lines containing the stretch data like so:

1
5
6

This is how you interpret it: You stretched 6 times yesterday, 5 times the day before that, and 1 time the day before that, which is the day the device was powered on.
If the device loses battery after a stretch has been performed today, it will lose all unsaved data, which means all of the data that comes today and the days after.
However, let's say the device loses battery today and the last stretch performed was 5 days ago, it will lose all the data from that day and not record zeros for the following days because the device only records the saved data when a stretch is performed on a new day.
To fix this, I think the following thing should be changed in the code. In addition to the device waking up on an external interrupt of the microswitch, the device should wake up every 24 hours and write the number of stretches to the data.txt file. The function of the stretchRegister() function writing to the .txt file can be removed, because the Real Time Clock will handle it.
This way, if the device runs out of battery and it has not been stretched in a while, the data from the days since the last stretch is not lost, the worst case is that the data from today is lost, everything yesterday and before is still there.
To implement this, you can configure a timer using the RTC (Real Time Clock) object, because that is always powered on through the VBAT. This timer should trigger an external interrupt every 24 hours that writes the current value of the stretchCounter to data.txt.

When you are developing software on the PyBoard, an indispensable tool is its REPL feature. If you connect your computer to the PyBoard, you can communicate with it serially.
We used Putty for this, but you can use any program you wish. For Putty, I will detail how to connect to the PyBoard. After you have opened Putty, select the Serial option, then type in the correct COM port which the PyBoard is in for the Serial Line (you can find which port the PyBoard is in by looking at your Device Manager), and then keep the Speed at 9600.
Click open, and then a window should open where you and the PyBoard can communicate through. The print statements I wrote in the code will print in the window, making it useful for debugging code and understanding which methods are being called, and for checking variable values.
If you want more information on REPL, please continue reading online at http://docs.micropython.org/en/latest/

After reading this, you should understand how to power the device and use it. If you have any further questions please reach out using the contact information below.

Improvements Suggested:

We have several things we felt that we could have improved on the ExiTrak. 

First, there should be a watertight housing for the electrical components that is drop-test proof.
The handle design will need a major overhaul to implement this, but it is feasible. A good way to improve drop test performance is to round edges to prevent fracture point formation.
 
Second, the ergonomics of the handle design should be examined. We designed the handle around the idea that the user will perform butterfly stretches and bicep curls using the resistance band, but the handle design may be unsuitable for other exercises.
The requirements for different stretches should be critically examined, and I think a handle redesign would make it more universal across different kinds of stretches.

Third, there should be a button that disables sleep mode on the device. This can be done using an External Interrupt similar to the one currently configured in ExiTrak_demoVersion.py. 
You can put a button connecting the 3V output of the PyBoard to pin 'X2'. You can configure an External Interrupt to occur on a rising edge to pin 'X2', and have the button be a switch that trigger the External Interrupt when turned ON, which then turns suspend sleep mode on in the code, which keeps the PyBoard on until the button is turned off.
This should be done so that there is a way for the community health worker to access the stretch data records indefinitely and to be able to do so without having to record a stretch by depressing the microswitch to turn the ExiTrak on, which is how the code is currently implemented.

Fourth, if the first improvement is implemented, the device should always be in standby/low-power mode to conserve power. The device should come out of it only momentarily when the microswitch is depressed and a stretch is recorded, and then immediately return to sleep. 
If a community health worker needs to access the data on the device, they can suspend sleep mode to do it using the suspend sleep mode button, for example. This can be done by removing the timer function from the while loop and just putting the device to sleep automatically in the while loop with no if statement to pass through.

Fifth, the data should not be recorded when a stretch is registered, but should be done automatically every twenty four hours using the RTC (Real Time Clock) object. 
This way, data can never be lost if users do not perform stretches everyday and the device loses power, as mentioned in the 'Operation of the ExiTrak' section.

We think all of these improvements are feasible and would improve the device quality. Of course, if you want more clarification on our points please feel free to reach out, we have included our contact information below.
This was a fun project to work on and we'd like to thank Dr. Malkin, Dr. Shang, and Andrea Molina for their help and enthusiasm!

If you have any questions at all or are unsure of how to move forward, please reach out to us because we spent a semester working on the exact same project with the PyBoard and Micropython, so we can help!
It took us a lot of time to get there by google searching and reading documentation, so if we can help you get to your answers faster that would be amazing! Please please please do not hesitate to ask us questions about the softare, the device, anything!
Lastly, we visited the communities we are building this device for and we believed the trip to be eye-opening in understanding the circumstances the device will be used in. If you have a chance, we think it would help you in the design process to visit Welch, WV and Williamson, WV.

Contact Information:

Agoston Walter

email: agoston@walterszanya.com
cell phone: 7575534281

You can also find me on LinkedIn, Facebook, Instagram. If you have any questions, connect with me however you can and I will help you. 



 

