import pyb
from pyb import Pin,UART,Timer,ExtInt,LED
from machine import I2C

#led for instruction
led1 = LED(1)
led2 = LED(2)
led3 = LED(3)
led4 = LED(4)


#UART
uart6 = UART(6,115200)
uart6.init(baudrate = 115200,bits= 8,parity=None,stop=1)
#ano_dt = uart.ANO_DT(uart6)


#pin
p1 = Pin('X1')
p2 = Pin('X2')
p3 = Pin('X3')
p4 = Pin('X4')

p5 = Pin('X9')#ch1
p6 = Pin('X10')
p7 = Pin('Y3')#ch3
p8 = Pin('Y4')

TIM1 = Timer(2,freq = 50)
TIM2 = Timer(4,freq = 50)
ch1 = TIM1.channel(1,Timer.PWM,pin=p1)#for left front
ch2 = TIM1.channel(2,Timer.PWM,pin=p2)
ch3 = TIM1.channel(3,Timer.PWM,pin=p3)#FOR LEFT BACK
ch4 = TIM1.channel(4,Timer.PWM,pin=p4)

ch5 = TIM2.channel(1,Timer.PWM,pin=p5)
ch6 = TIM2.channel(2,Timer.PWM,pin=p6)
ch7 = TIM2.channel(3,Timer.PWM,pin=p7)
ch8 = TIM2.channel(4,Timer.PWM,pin=p8)

p0 = Pin('Y7')

TIM_TURN = Timer(12,freq = 50)
ch0 = TIM_TURN.channel(1,Timer.PWM,pin=p0)

def Zhuan(jiaodu):# 0,90,-90
    ch0.pulse_width_percent(7.5 + jiaodu * 5 / 90)

def Stop():
    ch1.pulse_width_percent(0)
    ch2.pulse_width_percent(0)
    ch3.pulse_width_percent(0)
    ch4.pulse_width_percent(0)
    ch5.pulse_width_percent(0)
    ch6.pulse_width_percent(0)
    ch7.pulse_width_percent(0)
    ch8.pulse_width_percent(0)

def Circle(turn):
    if turn == 2:#ni
        ch1.pulse_width_percent(0)# turn  two wheels
        ch2.pulse_width_percent(0)
        ch3.pulse_width_percent(0)
        ch4.pulse_width_percent(0)
        ch5.pulse_width_percent(100)
        ch6.pulse_width_percent(0)
        ch7.pulse_width_percent(100)
        ch8.pulse_width_percent(0)
    if turn == 1:#shun
        ch1.pulse_width_percent(100)# turn  two wheels
        ch2.pulse_width_percent(0)
        ch3.pulse_width_percent(100)
        ch4.pulse_width_percent(0)
        ch5.pulse_width_percent(0)
        ch6.pulse_width_percent(0)
        ch7.pulse_width_percent(0)
        ch8.pulse_width_percent(0)

def Check1():
    ch1.pulse_width_percent(40)# turn  two wheels
    ch2.pulse_width_percent(0)
    ch3.pulse_width_percent(40)
    ch4.pulse_width_percent(0)

    ch5.pulse_width_percent(0)# turn  two wheels
    ch6.pulse_width_percent(40)
    ch7.pulse_width_percent(0)
    ch8.pulse_width_percent(40)

    while 1:
        if uart6.any() != None:
            s = uart6.read(4)
            led1.toggle()
            if s == b'0x01':
                led1.on()
                break
            #if s == b'0x11':
    led4.on()

def Run(lper,rper):
    ch1.pulse_width_percent(lper)
    ch2.pulse_width_percent(0)
    ch3.pulse_width_percent(lper)
    ch4.pulse_width_percent(0)

    ch5.pulse_width_percent(rper)
    ch6.pulse_width_percent(0)
    ch7.pulse_width_percent(rper)
    ch8.pulse_width_percent(0)

def Go():
    led1.off()
    Run(100,100)
    while 1:
        uart6.write(b'0xff')
        pyb.delay(10)
        if uart6.any() != None:
            s = uart6.read(4)
            if s == b'0x02':
                led2.on()
                led3.off()
                Run(100,80)
                pyb.delay(10)
                Run(100,100)
                continue
            elif s == b'0x03':
                led3.on()
                led2.off()
                Run(80,100)
                pyb.delay(10)
                Run(100,100)
                continue
            if s == b'0x08':
                Stop()
                break
    led4.off()

def CheckColour():
    uart6.write(b'0x88')
    pyb.delay(500)
    led1.on()
    led2.on()
    led3.on()
    led4.on()
    if uart6.any() != None:
        S = uart6.read(4)
        if S == b'0x11': #green
            led3.off()
            Zhuan(90)
            Circle(2)
            pyb.delay(900)
            while 1:
                if uart6.read(4) == b'0x08':
                    Stop()
                    break
            for i in range(0,20):
                Run(100,100)
                pyb.delay(500)
                Circle(1)
                pyb.delay(500)
                while 1:
                    if uart6.any() != None:
                        Stop()
                        break

        if S == b'0x12':
            led1.off()
            Zhuan(-90)  #red
            Circle(1)
            pyb.delay(900)
            while 1:
                if uart6.read(4) == b'0x08':
                    Stop()
                    break
            for i in range(0,20):
                Run(100,100)
                pyb.delay(500)
                Circle(2)
                pyb.delay(500)
                while 1:
                    if uart6.any() != None:
                        Stop()
                        break
    Zhuan(0)
    led1.off()
    led4.off()
    led2.off()
    led3.off()

def found():
    pass

Zhuan(0)

Check1()
Go()
led2.off()
led4.off()
CheckColour()

uart6.write(b'0x09')

Check1()
Go()
led2.off()
led4.off()
CheckColour()

uart6.write(b'0x09')

Check1()
Run(100,100)



