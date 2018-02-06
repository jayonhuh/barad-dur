import signal

class GracefulKiller:
    """
    Responds gracefully to SIGINT and SIGTERM signals.
    """

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        self.kill_now = False

    def exit_gracefully(self, signum, frame):
        self.kill_now = True
