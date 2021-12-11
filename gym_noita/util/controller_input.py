import pyvjoy
import time

class ControllerInput():
    MOVE = 'move'
    AIM = 'aim'
    KICK = 'kick'
    ATTACK = 'attack'
    T_FLIGHT = 'toggle_flight'

    ACTION_LOOKUP = {
        0: MOVE,
        1: AIM,
        2: KICK,
        3: ATTACK,
        4: T_FLIGHT,
    }

    def perform_action(self, action):
        print("controller: ", self.controller.data)
        self.set_left_stick(action[0][0], action[0][1]),
        self.set_right_stick(action[1][0], action[1][1]),
        self.controller.update()

        if action[2]:
            self.kick(),
        if action[3]:
            self.attack(),
        if action[4]:
            self.toggle_flight(),

    def __init__(self) -> None:
        self.controller = pyvjoy.VJoyDevice(1)
        self.is_flying = False
        self.kick()
        time.sleep(1)
        self.kick()
        time.sleep(3)

    def set_left_stick(self, x, y):
        x_in = self.scale_input(x)
        y_in = self.scale_input(y)
        print("x: ", x_in, "\ny: ", y_in)
        #self.controller.set_axis(pyvjoy.HID_USAGE_X, x_in)
        #self.controller.set_axis(pyvjoy.HID_USAGE_Y, y_in)
        self.controller.data.wAxisX = x_in
        self.controller.data.wAxisY = y_in

    def set_right_stick(self, x, y):
        #self.controller.set_axis(pyvjoy.HID_USAGE_RX, self.scale_input(x))
        #self.controller.set_axis(pyvjoy.HID_USAGE_RY, self.scale_input(y))
        self.controller.data.eAxisX = self.scale_input(x)
        self.controller.data.eAxisX = self.scale_input(y)

    def kick(self):
        self.controller.set_button(2, 1)
        time.sleep(0.25)
        self.controller.set_button(2, 0)

    def attack(self):
        self.controller.set_button(11, 1)
        time.sleep(0.25)
        self.controller.set_button(11, 0)

    def toggle_flight(self):
        self.is_flying = not self.is_flying
        self.controller.set_button(11, int(self.is_flying))

    def reset(self):
        self.controller.reset()

    def scale_input(self, raw_input):
        scaled_input = raw_input * (16384) + 16384

        if scaled_input != 0:
            return int(scaled_input)
        
        return int(1)
