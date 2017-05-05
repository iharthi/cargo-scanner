from __future__ import print_function

import serial
import serial.tools.list_ports
import threading
import time

class LedController(object):
    def __init__(self):
        self.buffer = ''
        self.buffer_lock = threading.Lock()

    def set_mode(self, mode):
        raise NotImplementedError

    def stop_all(self):
        raise NotImplementedError


class DummyLedController(LedController):
    def set_mode(self, mode):
        print("Mode set to {}".format(mode))

    def stop_all(self):
        pass


class SerialLedController(LedController):
    @classmethod
    def port_list(cls):
        return [x[0] for x in serial.tools.list_ports.comports()]

    def __init__(self, port, speed=9600):
        super(SerialLedController, self).__init__()
        self.ser = serial.Serial(port, speed)
        self.run = True

        self.thread = threading.Thread(target=self.read_from_port)
        self.thread.start()

        self.init_port()

    def init_port(self):
        x = 0
        # Wait for Arduino to start responding
        while True:
            self.set_mode(x)
            time.sleep(0.1)
            x += 1
            if x >= 8:
                x = 0
                if len(self.buffer) > 0:
                    break

        with self.buffer_lock:
            self.buffer = ""

        self.set_mode(0)

    def read_from_port(self):
        while self.run:
            try:
                reading = self.ser.readline().decode()
                with self.buffer_lock:
                    self.buffer += reading
            except (serial.serialutil.SerialException):
                pass

    def stop_all(self):
        if self.run:
            self.run = False
            try:
                self.ser.write("{}".format(0).encode('utf-8'))
                self.ser.close()
            except (serial.serialutil.SerialException):
                pass

    def set_mode(self, mode):
        if self.run:
            self.ser.write("{}".format(mode).encode('utf-8'))
