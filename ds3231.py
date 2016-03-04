import smbus
from time import sleep
from datetime import datetime

# Older version of library that uses smbus, no longer updated
# For new projects use i2c_lcd

def bcd2dec(bcd, mask=0xFF):
	bcd = bcd & mask
	return (bcd & 0x0F) + (bcd//16*10)

class ds3231():
	def __init__(self, addr, port):
		self.addr = addr
		self.bus = smbus.SMBus(port)	
	
	def utcnow(self):
		data = self.bus.read_i2c_block_data(self.addr, 0, 7)
		now = {
			"second": bcd2dec(data[0], 0x7F),
			"minute": bcd2dec(data[1], 0x7F),
			"hour":   None,
			"day": 	  bcd2dec(data[4], 0x3F),
			"month":  bcd2dec(data[5], 0x1F),
			"year":   bcd2dec(data[6], 0xFF),
			}
		if data[2] & 0x40:
			#12h mode
			now["hour"] = bcd2dec(data[2], 0x1F)
			if data[2] & 0x20:
				now["hour"] += 12;
		else:
			#24h mode
			now["hour"] = bcd2dec(data[2], 0x3F)
		if data[5] & 0x80:
			now["year"] +=100
		now["year"] += 2000
		return datetime(**now)

	def now(self):
		offset = datetime.utcnow().replace(minute=0, second=0, microsecond=0) - datetime.now().replace(minute=0, second=0, microsecond=0)
		return self.utcnow() - offset

if __name__ == '__main__':
	clock = ds3231(0x68, 1);
	print(clock.now())