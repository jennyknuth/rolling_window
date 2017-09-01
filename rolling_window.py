from nio.block.base import Block
from nio.properties import VersionProperty, IntProperty, StringProperty

class RollingWindow(Block):

    version = VersionProperty('0.1.0')
    chunk_size = IntProperty(title='Chunk Size', default=1)
    step_by = IntProperty(title='Step By', default=1)
    key = StringProperty(title='Key', default='')

    def process_signals(self, signals):
        out_sigs = []
        for signal in signals:
            key = self.key(signal)
            if key in signal:
                data = signal[key]
                for i in range(len(data) - (self.chunk_size(signal) * self.step_by(signal)) + 1):
                    chunk = []
                    for x in range(self.chunk_size(signal)):
                        # if ((i + self.chunk_size(signal)) * self.step_by(signal) <= len(data)):
                        chunk.append(data[(i * self.step_by(signal)) + x])
                        print(chunk)

                    # if len(chunk):
                    out_sigs.append(chunk)
        print(out_sigs)
        self.notify_signals(out_sigs)
