import time
from os import remove
from os.path import splitext
from mimetypes import guess_type
from multiprocessing import Process
from subprocess import run, DEVNULL
from .optimizer_state import optimizer_queue, is_optimizing


def worker():
    while True:
        if not is_optimizing.value:
            path = optimizer_queue.get()
            optimize_video(path)

        time.sleep(5)


def optimize_video(path: str) -> None:
    try:
        is_optimizing.value = True

        media_type = guess_type(path)[0] or ""

        if not media_type.startswith("video/"):
            return

        base, ext = splitext(path)

        temp_path = f"{base}-temp{ext}"

        result = run(
            ["ffmpeg", "-i", path, "-c", "copy", "-movflags", "+faststart", "-y", temp_path],
            stdout=DEVNULL,
            stderr=DEVNULL,
        )

        if not result.returncode:
            remove(path)
            run(["mv", temp_path, path])

    except OSError as error:
        print(f"Error optimizing video: {error}")

    finally:
        is_optimizing.value = False


process = Process(target=worker, daemon=True)

process.start()
