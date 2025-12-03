

from micropython import const

# Default I2C address for DHT12
SENSOR_ADDR = const(0x5c)

class DHT12:
    def __init__(self, i2c, addr=SENSOR_ADDR):
        self.i2c = i2c
        self.addr = addr
        self.buf = bytearray(5)

    def measure(self):
        """
        Read 5 bytes from sensor and check checksum.
        Format: [Hum_Int, Hum_Dec, Temp_Int, Temp_Dec, Checksum]
        """
        # Read 5 bytes from address 0
        self.i2c.readfrom_mem_into(self.addr, 0, self.buf)
        
        # Verify Checksum
        # Sum of first 4 bytes must match the 5th byte
        if (self.buf[0] + self.buf[1] + self.buf[2] + self.buf[3]) & 0xff != self.buf[4]:
            raise Exception("DHT12 Checksum Error")

    def humidity(self):
        """Return humidity %"""
        return self.buf[0] + self.buf[1] * 0.1

    def temperature(self):
        """Return temperature Celsius"""
        t = self.buf[2] + (self.buf[3] & 0x7f) * 0.1
        if self.buf[3] & 0x80:
            t = -t
        return t

    def read_values(self):
        """
        Perform a measurement and return (temp, hum).
        This is the method your main program calls.
        """
        self.measure()
        return self.temperature(), self.humidity()