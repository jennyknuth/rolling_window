from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..rolling_window import RollingWindow

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

    def test_single_chunk(self):
        blk = RollingWindow()
        sig = [{'data': [1, 2, 3, 4, 5, 6]}]
        self.configure_block(blk, {
            'chunk_size': 1,
            'step_by': 4,
            'key': 'data'
        })
        blk.start()
        blk.process_signals(sig)
        blk.stop()
        self.assert_num_signals_notified(2)
        self.assertEqual(
            [1], self.last_notified[DEFAULT_TERMINAL][0])
        self.assertEqual(
            [5], self.last_notified[DEFAULT_TERMINAL][-1])

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
        sig = [{'data': [1, 2, 3, 4, 5, 6]}]
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

    def test_step_by_4(self):
        """step by 4"""
        blk = RollingWindow()
        sig = [{'data': [1, 2, 3, 4, 5, 6, 7]}]
        self.configure_block(blk, {
            'chunk_size': 3,
            'step_by': 4,
            'key': 'data'
        })
        blk.start()
        blk.process_signals(sig)
        blk.stop()
        self.assert_num_signals_notified(2)
        self.assertEqual(
            [5, 6, 7], self.last_notified[DEFAULT_TERMINAL][-1])
