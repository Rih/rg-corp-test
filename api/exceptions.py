# -*- encoding: utf-8 -*-


class FrequencyException(Exception):
    
    def __init__(self, freq, message='Frequency > 0 and < 30'):
        self.freq = freq
        self.message = message
        super().__init__(self.message)


def check_frequency(freq):
    if freq and not (0 < int(freq) <= 30):
        raise FrequencyException(freq)