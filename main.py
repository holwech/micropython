# import machine
# import utime

# light_on = True
# pin22 = machine.Pin(2, machine.Pin.OUT)
# print('test')

# while True:
#     if light_on:
#         pin22.value(1)
#         light_on = False
#     else:
#         pin22.value(0)
#         light_on = True
#     print('hi')
#     utime.sleep(1)

import time
import utime
import machine, neopixel
import random

button = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)
class Light:
    def __init__(self):
        self.patterns = [self.random, self.cycle_colors, self.random2, self.cycle, self.bounce, self.fade]
        self.curr_pattern = 0
        self.np = neopixel.NeoPixel(machine.Pin(4), 8)
        self.light_idx = 0
        self.color = (0,0,0)
        self.color_idx = 0
    
    def demo(self):
        while True:
            pattern = self.patterns[self.curr_pattern]
            pattern()

    def change_pattern(self, n):
        print('Current pattern: ', self.curr_pattern)
        self.curr_pattern += 1
        self.curr_pattern = self.curr_pattern % len(self.patterns)

    def cycle(self):
        np = self.np
        n = self.np.n
        # cycle
        for i in range(4 * n):
            for j in range(n):
                np[j] = (0, 0, 0)
            np[i % n] = (255, 255, 255)
            np.write()
            time.sleep_ms(25)

    def bounce(self):
        np = self.np
        n = self.np.n
        # bounce
        for i in range(4 * n):
            for j in range(n):
                np[j] = (0, 0, 128)
            if (i // n) % 2 == 0:
                np[i % n] = (0, 0, 0)
            else:
                np[n - 1 - (i % n)] = (0, 0, 0)
            np.write()
            time.sleep_ms(60)

    def fade(self):
        np = self.np
        n = self.np.n
        # fade in/out
        for i in range(0, 4 * 256, 8):
            for j in range(n):
                if (i // 256) % 2 == 0:
                    val = i & 0xff
                else:
                    val = 255 - (i & 0xff)
                np[j] = (val, 0, 0)
            np.write()

    def random(self):
        np = self.np
        n = self.np.n
        val = (random.randint(0,160), random.randint(0,160), random.randint(0,160))
        np[random.randint(0, n - 1)] = val
        np.write()
        time.sleep_ms(40)

    def random2(self):
        np = self.np
        n = self.np.n
        val = (random.randint(0,160), random.randint(0,160), random.randint(0,160))
        np[self.light_idx] = val
        self.light_idx += 1
        self.light_idx = self.light_idx % n
        np.write()
        time.sleep_ms(40)

    def color_fade(self):
        np = self.np
        n = self.np.n
        self.cycle_colors()
        for i in range(n):
            np[i] = self.color 

    def cycle_colors(self):
        self.color_idx += 1
        self.color_idx = self.color_idx % 3
        for i, color in enumerate(self.color):
            self.color[i] += 1
            self.color[i] = color % 255



    def clear(self):
        np = self.np
        n = self.np.n
        # clear
        for i in range(n):
            np[i] = (0, 0, 0)
        np.write()
    
light = Light()


print('Program started...')
button.irq(trigger=machine.Pin.IRQ_FALLING, handler=light.change_pattern)
light.demo()
