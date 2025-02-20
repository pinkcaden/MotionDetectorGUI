
import threading
from time import sleep
import tkinter as tk

#from pygame import mixer



##from gpiozero import LED
##from gpiozero import MotionSensor
YELLOW_GPIO = 6
WHITE_GPIO = 7

armedRed = '#f0493a'
disarmedGreen = '#88de43'
controlBlue = '#8ec7ed'
detectionYellow = '#f9fc30'

stausFont = ("Roboto", 20, "bold")
controlFont = ("Roboto", 14, "bold")
detectionFont = ("Roboto", 24, "bold")

NESW = (tk.N + tk.E + tk.S + tk.W)

BLINK_SPEED = 1 ## Blinks Per Minute

class LED():
    def __init__(self, pin):
        pass
    def on(self):
        print('led on')
    def off(self):
        print('led off')        

class MotionSensor():
    def __init__(self, pin):
        pass



class Interface(tk.Tk):



    ## control button has two functions that swap everytime its clicked

    def armClick(self): ## C PINK
        

        self.statusLabel.config(bg = armedRed, text = 'ARMED')
        self.controlButton.config(command = self.disarmClick, text = 'DISARM')
        
        
        self.detectionOn = True
        self.status_light()
        
        alarm = threading.Thread(target = self.soundAlarm)
        self.detector.when_motion = alarm.start()
            


    def disarmClick(self): ## C PINK
        

        
        self.detector.when_motion = None
        self.detectionOn = False       
        self.status_light()            
        self.statusLabel.config(bg = disarmedGreen, text = 'DISARMED')        
        self.detectionLabel.config(bg = 'white', text = '')
        
        self.controlButton.config(command = self.armClick, text = 'ARM')
        

        

    ## self.soundAlarm() is a wrapper method that is responsible for coordinating outputs when motion is detected

    def soundAlarm(self): ## C PINK
        
        self.detectionLabel.config(bg = detectionYellow, text = "MOTION DETECTED")
         
        while self.detectionOn:
            
            lightsT = threading.Thread(target = self.urgent, args = (2.5, .5))
        
            soundT = threading.Thread(target = self.playSound)

            lightsT.start()
            soundT.start()
        
            lightsT.join()
            soundT.join()


        



    ## playSound should play a sound to the speaker.
    ## It's called when motion is detected.

    def playSound(self): 
        ## If necessary, edit the parameters in this method, and the variables in the __init__ method
        return

     

    


    ## urgent should rapidly blink an LED
    ## It's called when motion is detected.          

    def urgent(self, totalTime, blinkTime): # CHRIS C

        numberBlinks = int(totalTime / blinkTime) # mention rounding from classroom


        for _ in range(0,numberBlinks):
            print('yellowLed.on()')         
            sleep(blinkTime/2)
            print('yellowLed.off()')
            sleep(blinkTime/2)        
            
    def status_light(self): # CHRIS C
        if self.detectionOn == True:
            self.whiteLight.on()  
        elif self.detectionOn == False:
            self.whiteLight.off()
     

        
       
        
        
        
        
    
    

    ## for all variables in the def __init__ section, remember to put "self." before the name.
    ## this denotes that it belongs to the instance, not to the class
    def __init__(self):
        
    ##############################################

        ## Initializing Tkinter window
        tk.Tk.__init__(self)
        
        ## screen title and size
        self.title('Alarm System')
        self.geometry(str(self.winfo_screenwidth() - 150) + 'x' + str(self.winfo_screenheight() - 150) + '+75+50')
        
    ##############################################        
        ## variable to signal that the detector should stop detecting
        
        self.stopDetecting = False
            
    ##############################################
        ## area for making variables related to playing sound
            
        self.motionDetector_SwitchingOnAudioPath = None
        self.motionDetector_SwitchingOffAudioPath = None
        self.motionDetector_IntruderAlertAudioPath = None
        self.motionDetector_AlarmOffAudioPath = None
    ##############################################
        ## area for making variables related to LEDs



        self.yellowLed= LED(YELLOW_GPIO)
        self.whiteLight = LED(WHITE_GPIO)


    ##############################################
        ## area for making variables related to motion detection


        SENSOR_GPIO = 15
        self.detector = MotionSensor(SENSOR_GPIO)
        self.detectionOn = True        


    ##############################################
        

    ## set up grid to place components ## CP

        self.grid_rowconfigure(0, weight = 2)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_rowconfigure(2, weight= 2)
        self.columnconfigure(0, weight = 6)        
        

        
        self.detectionLabel = tk.Label(self, bg = 'white', font = detectionFont)
        self.detectionLabel.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = NESW)
        self.controlButton = tk.Button(self, bg = controlBlue, font = controlFont, command = self.armClick, text = 'ARM')
        self.controlButton.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = NESW)
        self.statusLabel = tk.Label(self, bg = disarmedGreen, font = detectionFont, text = 'DISARMED')
        self.statusLabel.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = NESW)        

    ##############################################


        self.mainloop()



    

w = Interface()