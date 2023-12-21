import os
import signal


class PerfectKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        self.signal = None
        self.frame = None
        print('Press Ctrl+C to exit')

    def exit_gracefully(self, signum, frame):
        self.signal = signum
        self.frame = frame
        self.kill_now = True

    def perfect_exit(self):
        if self.signal is not None:
            signal.signal(self.signal, signal.SIG_DFL)
            os.kill(os.getpid(), self.signal)
