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

    def perform_action(self, action, parameters):
       switch = {
           MOVE: self.set_left_stick(parameters[0], parameters[1]),
           AIM: self.set_right_stick(parameters[0], parameters[1]),
           KICK: self.kick(),
           ATTACK: self.attack(),
           T_FLIGHT: self.toggle_flight(),
       }

       switch.get(action)

    def __init__(self) -> None:
        self.controller = pyvjoy.VJoyDevice(1)
        self.is_flying = False

    def set_left_stick(self, x, y):
        self.controller.set_axis(pyvjoy.HID_USAGE_X, self.scale_input(x))
        self.controller.set_axis(pyvjoy.HID_USAGE_Y, self.scale_input(y))

    def set_right_stick(self, x, y):
        self.controller.set_axis(pyvjoy.HID_USAGE_RX, self.scale_input(x))
        self.controller.set_axis(pyvjoy.HID_USAGE_RY, self.scale_input(y))

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

    def scale_input(raw_input):
        scaled_input = raw_input * (16384) + 16384

        if scaled_input != 0:
            return int(scaled_input)
        
        return int(1)
