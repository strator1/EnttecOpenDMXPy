from ftd2xx import ftd2xx


class ConnectionNotOpen(Exception):
    def __init__(self, arg1=None, arg2=None):
        super(ConnectionNotOpen, self).__init__(arg1)


class IllegalArgument(Exception):
    def __init__(self, arg1=None, arg2=None):
        super(ConnectionNotOpen, self).__init__(arg1)


class DmxPy:
    def __init__(self, port=0):
        self._port = port
        self._buffer = [bytes([0])] * 513
        self._device = None

    def open(self):
        self._device = ftd2xx.open(self._port)

        self._device.setBaudRate(250000)
        self._device.setDataCharacteristics(8, 2, 0)
        self._device.setTimeouts(1000, 1000)
        self._device.setFlowControl(ftd2xx.FLOW_NONE)
        self._device.purge()
        self._device.clrRts()

    def set_channel(self, channel, intensity):
        if self._device is None:
            raise ConnectionNotOpen("Connection closed.")
        else:
            if 0 < channel <= 512:
                intensity = 0 if intensity < 0 else intensity
                intensity = 255 if intensity > 255 else intensity

                self._buffer[channel] = bytes([intensity])
            else:
                raise IllegalArgument("Channel number outside valid range (1 - 512): %d" % channel)

    def blackout(self):
        for channel in range(1, 513, 1):
            self.set_channel(channel, 0)

        self.render()

    def render(self):
        if self._device is None:
            raise ConnectionNotOpen("Connection closed.")
        else:
            self._device.setBreakOn()
            self._device.setBreakOff()

            self._device.write(b''.join(self._buffer))

    def close(self):
        if self._device is not None:
            self._device.close()