
from machine import Pin,
from led_display import OLED_1inch3

def update_display(T, SP, OLED):
    print(str(T)+','+ str(SP))
    OLED.fill(0x0000)
    OLED.display_text('Temp  :  ' + str(T))
    OLED.draw_horizontal_line(30)
    OLED.display_text('Set Pt : ' + str(SP),y=45)
    OLED.show()


if __name__=='__main__':
    import time
    
    
    
    keyA = Pin(15,Pin.IN,Pin.PULL_UP)
    keyB = Pin(17,Pin.IN,Pin.PULL_UP)
    
    T=35
    set_pt = 25
    OLED = OLED_1inch3()

    
    update_display(T, set_pt, OLED)
    
    while True:
        if keyA.value() == 0:
            set_pt = set_pt + 1
            update_sp(T, set_pt, OLED)
        elif keyB.value() == 0:
            set_pt = set_pt - 1
            update_sp(T, set_pt, OLED)