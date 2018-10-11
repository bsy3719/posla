import wiringpi

class Serial(object):
    def __init__(self):
        # motor
        self.STOP = 0
        self.FORWARD = 1
        self.BACKWARD = 2

        #motor channel
        self.CH1 = 0
        self.CH2 = 1

        #PIN input & output
        self.OUTPUT = 1
        self.INPUT = 0

        #PIN setting
        self.HIGH = 1
        self.LOW = 0

        #Raspberry GPIO setting
        #PWM
        self.ENA = 4
        self.ENB = 5

        #GPIO PIN
        self.IN1 = 22
        self.IN2 = 23
        self.IN3 = 24
        self.IN4 = 25    

        wiringpi.wiringPiSetup()

        self.setPinConfig(self.ENA, self.IN1, self.IN2)
        self.setPinConfig(self.ENB, self.IN3, self.IN4)
    
    #PIN setting function
    def setPinConfig(self, EN, INA, INB):
        wiringpi.pinMode(EN, self.OUTPUT)
        wiringpi.pinMode(INA, self.OUTPUT)
        wiringpi.pinMode(INB, self.OUTPUT)
        wiringpi.softPwmCreate(EN, 0, 255)

    #motor control function
    def setMotorControl(self, PWM, INA, INB, speed, stat):
        #motor speed control PWM
        wiringpi.softPwmWrite(PWM, speed)
        
        #FORWARD
        if stat == self.FORWARD:
            wiringpi.digitalWrite(INA, self.HIGH)
            wiringpi.digitalWrite(INB, self.LOW)

        #BACKWARD
        elif stat == self.BACKWARD:
            wiringpi.digitalWrite(INA, self.LOW)
            wiringpi.digitalWrite(INB, self.HIGH)

        #STOP
        elif stat == self.STOP:
            wiringpi.digitalWrite(INA, self.LOW)
            wiringpi.digitalWrite(INB, self.LOW)
        
    #motor control function_warp
    def setMotor(self, ch, speed, stat):
        if ch == self.CH1:
            self.setMotorControl(self.ENA, self.IN1, self.IN2, speed, stat)
        else :
            self.setMotorControl(self.ENB, self.IN3, self.IN4, speed, stat)
    
    def steer(self, data):
        if data == 'w' :
            self.setMotor(self.CH1, 110, self.FORWARD)
            self.setMotor(self.CH2, 160, self.FORWARD)
        elif data == 'x' :
            self.setMotor(self.CH1, 100, self.BACKWARD)
            self.setMotor(self.CH2, 100, self.BACKWARD)
        elif data == 'a' :
            self.setMotor(self.CH1, 210, self.FORWARD)
            self.setMotor(self.CH2, 60, self.FORWARD)
        elif data == 'd' :
            self.setMotor(self.CH1, 50, self.FORWARD)
            self.setMotor(self.CH2, 210, self.FORWARD)
        elif data == 's' :
            self.setMotor(self.CH1, 0, self.STOP)
            self.setMotor(self.CH2, 0, self.STOP)
        elif data == 'z' :
            self.setMotor(self.CH1, 230, self.BACKWARD)
            self.setMotor(self.CH2, 60, self.BACKWARD)
        elif data == 'c' :
            self.setMotor(self.CH1, 60, self.BACKWARD)
            self.setMotor(self.CH2, 230, self.BACKWARD)

