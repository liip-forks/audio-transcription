import subprocess
import os
DEVICE = os.getenv("DEVICE")

def get_length(filename):
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return float(result.stdout)


def time_estimate(filename, online=True):
    try:
        # For now, we don't predict the wait time for zipped files in the queue.
        if filename[-4:] == ".zip":
            return 1, 1
        run_time = get_length(filename)
        if online:
            if DEVICE == "mps":
                return run_time / 5, run_time
            else:
                return run_time / 10, run_time
        else:
            if DEVICE == "mps":
                return run_time / 3, run_time
            else:
                return run_time / 6, run_time
    except Exception as e:
        print(e)
        return -1, -1
