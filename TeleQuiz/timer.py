import time

class Timer:
    def __init__(self, duration=600):
        self.duration = duration  # Timer duration in seconds (10 minutes = 600 seconds)
        self.start_time = time.time()

    def time_left(self):
        """Return the time left until the timer reaches 0."""
        elapsed = time.time() - self.start_time
        remaining = self.duration - elapsed
        if remaining > 0:
            minutes, seconds = divmod(int(remaining), 60)
            return f"Time left: {minutes} minutes, {seconds} seconds"
        else:
            return "Time is up!"
