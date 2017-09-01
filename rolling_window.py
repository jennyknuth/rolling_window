from nio.block.base import Block
from nio.properties import VersionProperty, IntProperty, StringProperty
import math

class RollingWindow(Block):

    version = VersionProperty('0.1.0')
    chunk_size = IntProperty(title='Chunk Size', default=1)
    step_by = IntProperty(title='Step By', default=1)
    key = StringProperty(title='Key', default='')

    def process_signals(self, signals):
        out_sigs = []
        for signal in signals:
            key = self.key(signal)
            chunk_size = self.chunk_size(signal)
            step_by = self.step_by(signal)
            if key in signal:
                data = signal[key]
                for i in range(math.ceil((len(data) - chunk_size + 1) / step_by)):
                    chunk = []
                    for x in range(chunk_size):
                        chunk.append(data[(i * step_by) + x])

                    out_sigs.append(chunk)
        print(out_sigs)
        self.notify_signals(out_sigs)
