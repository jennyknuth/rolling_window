from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..rolling_window import RollingWindow

# foo=[1, 2, 3, 4, 5, 6]
# chunk_size=3
# bar=[[foo[i+x] for x in range(chunk_size)] for i in range(len(foo)-chunk_size)]
# bar
# [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
# [[1, 2, 3], [3,4,5]]
# [sum(b)/len(b) for b in bar]
# [2.0, 3.0, 4.0]
# for x in [sum(b)/len(b) for b in bar]:
# ...     print(x)
# ...
# 2.0
# 3.0
# 4.0

class TestRollingWindow(NIOBlockTestCase):

    def test_int_array(self):
        blk = RollingWindow()
        sig = [{'data': [1, 2, 3, 4, 5, 6]}]
        self.configure_block(blk, {
            'chunk_size': 3,
            'step_by': 1,
            'key': 'data'
        })
        blk.start()
        blk.process_signals(sig)
        blk.stop()
        self.assert_num_signals_notified(4)
        self.assertEqual(
            [1, 2, 3], self.last_notified[DEFAULT_TERMINAL][0])
        self.assertEqual(
            [4, 5, 6], self.last_notified[DEFAULT_TERMINAL][-1])
    def test_no_key(self):
        blk = RollingWindow()
        sig = [{'data': [1, 2, 3, 4, 5, 6]}]
        self.configure_block(blk, {
            'chunk_size': 3,
            'step_by': 1,
            'key': ''
        })
        blk.start()
        blk.process_signals(sig)
        blk.stop()
        self.assert_num_signals_notified(0)
        #todo raise exception
        # self.assertEqual(
        #     [1, 2, 3], self.last_notified[DEFAULT_TERMINAL][0])

    def test_step_by_2(self):
        """step by 2"""
        blk = RollingWindow()
        sig = [{'data': [1, 2, 3, 4, 5, 6, 7]}]
        self.configure_block(blk, {
            'chunk_size': 3,
            'step_by': 2,
            'key': 'data'
        })
        blk.start()
        blk.process_signals(sig)
        blk.stop()
        self.assert_num_signals_notified(2)
        self.assertEqual(
            [3, 4, 5], self.last_notified[DEFAULT_TERMINAL][-1])
