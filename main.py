from Raspi_PWM_Servo_Driver import PWM      # Cabeceras del Servo
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor    # Cabeceras del Motor DC
from datetime import datetime
from datetime import date

import time
import atexit
import cv2

# create a default object, no changes to I2C address or frequency
mh = Raspi_MotorHAT(addr=0x6f)
vel=75
tiempo=1
alto=0.01
################################# DATOS DC motor test!
# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
    mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
    mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
    mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)

atexit.register(turnOffMotors)      #setea a cero los motores DC
myMotor = mh.getMotor(3)    # puerto motores DC
# set the speed to start, from 0 (off) to 255 (max speed)
myMotor.setSpeed(150)   # velocidad inicial max 255
myMotor.run(Raspi_MotorHAT.FORWARD);    # indicador ADELANTE
# turn on motor
myMotor.run(Raspi_MotorHAT.RELEASE);

########################################### Datos del Servo
pwm = PWM(0x6F)
servoMin = 270  # Min pulse length out of 4096
servoMax = 450  # Max pulse length out of 4096


def setServoPulse(channel, pulse):
    pulseLength = 1000000  # 1,000,000 us per second
    pulseLength /= 60  # 60 Hz
    print("%d us per period" % pulseLength)
    pulseLength /= 4096  # 12 bits of resolution
    print("%d us per bit" % pulseLength)
    pulse *= 1000
    pulse /= pulseLength
    pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(60)  # Set frequency to 60 Hz

def ATRAS(arg1,arg2):
    print("ATRAS")
    pwm.setPWM(1, 0, 350)
    time.sleep(1)
    myMotor.run(Raspi_MotorHAT.BACKWARD)
    myMotor.setSpeed(arg1)
    time.sleep(arg2)

def ADELANTE(arg1,arg2,arg3):
    print("ADELANTE " + str(arg3))
    pwm.setPWM(1, 0, 350)
    time.sleep(1)
    myMotor.run(Raspi_MotorHAT.FORWARD)
    myMotor.setSpeed(arg1)
    # time.sleep(arg2)

def PARAR(arg):
    print("parar")
    myMotor.run(Raspi_MotorHAT.RELEASE)
    atexit.register(turnOffMotors)
    time.sleep(arg)

def IZQUIERDA(arg1,arg2,arg3):
    print("IZQUIERDA " + str(arg3))
    pwm.setPWM(1, 0, servoMax)
    time.sleep(0.3)
    myMotor.run(Raspi_MotorHAT.FORWARD)
    myMotor.setSpeed(arg1)
    time.sleep(arg2)

def SEMIZQ(arg1,arg2,arg3):
    print("SEMI-IZQUIERDA " + str(arg3))
    pwm.setPWM(1, 0, servoMax - 40)
    time.sleep(1)
    myMotor.run(Raspi_MotorHAT.FORWARD)
    myMotor.setSpeed(arg1)
    time.sleep(arg2)

def DERECHA(arg1,arg2,arg3):
    print("DERECHA "+ str(arg3))
    pwm.setPWM(1, 0, servoMin)
    time.sleep(0.3)
    myMotor.run(Raspi_MotorHAT.FORWARD)
    myMotor.setSpeed(arg1)
    time.sleep(arg2)

def SEMIDER(arg1,arg2,arg3):
    print("SEMIDERECHA " + str(arg3))
    pwm.setPWM(1, 0, servoMin + 55)
    time.sleep(1)
    myMotor.run(Raspi_MotorHAT.FORWARD)
    myMotor.setSpeed(arg1)
    time.sleep(arg2)



def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    i_ad=0
    i_si=0
    i_iz=0
    i_de=0
    i_sd=0

    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)
        output = cv2.resize(img, (160, 120))    # Reduciendo el tamaño de la imagen
        output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)   #convirtiendo en Gris
        output = cv2.flip(output, 1)  # espejo de la imagen
        cv2.imshow('my webcam', output)

        k = cv2.waitKey(1)
        if k == 27:
            now = datetime.now()
            today = date.today()
            #     &&&&&&&&&&&&&6 Guardando en Archivo
            print(today)
            print(now)
            f = open('GENERADOS.txt', 'w')
            f.write(str(now) +" --- BD Vehiculos Auto Conduccion --- " )
            f.write("\n" + " Adelante " + str(i_ad))
            f.write("\n" + " SemIzq " + str(i_si))
            f.write("\n" + " Izq " + str(i_iz))
            f.write("\n" + " SemDer " + str(i_sd))
            f.write("\n" + " Der " + str(i_de))

            f.close()
            #       &&&& fin de guardado &&&&
            cv2.destroyAllWindows()
            quit()
        elif k == ord('i'):   # 'i' es adelante
            cv2.imwrite('BD_mov/3_AD/adelante{:>04}.png'.format(i_ad),output)
            i_ad += 1
            ADELANTE(vel,tiempo,i_ad)
            # PARAR(alto)
        elif k == ord('u'):  # 'u' es semi-izquierda
            cv2.imwrite('BD_mov/2_SI/semiz{:>04}.png'.format(i_si),output)
            i_si += 1
            SEMIZQ(vel,tiempo,i_si)
            PARAR(alto)
        elif k == ord('j'):  # 'j' es izquierda
            cv2.imwrite('BD_mov/1_IZ/izq{:>04}.png'.format(i_iz),output)
            i_iz +=1
            IZQUIERDA(vel,tiempo,i_iz)
            PARAR(alto)
        elif k == ord('o'):  # 'o' es semi-derecha
            cv2.imwrite('BD_mov/4_SD/semder{:>04}.png'.format(i_sd),output)
            i_sd +=1
            SEMIDER(vel,tiempo,i_sd)
            PARAR(alto)
        elif k == ord('l'):  # 'l' es derecha
            cv2.imwrite('BD_mov/5_DE/der{:>04}.png'.format(i_de),output)
            i_de +=1
            DERECHA(vel,tiempo,i_de)
            PARAR(alto)
        elif k == ord('k'):  # 'k' es atras
            ATRAS(vel,tiempo)
            PARAR(alto)



def main():
    show_webcam(mirror=True)

if __name__ == '__main__':
    main()


