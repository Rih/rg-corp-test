
class FrequencyException(Exception):
    
    def __init__(self, freq, message='Frequency > 0'):
        self.freq = freq
        self.message = message
        super().__init__(self.message)


def check_frequency(freq):
    if freq and int(freq) <= 0:
        raise FrequencyException(freq)