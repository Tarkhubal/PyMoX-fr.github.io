import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

# Fichiers à surveiller avec leurs commandes associées
script_path = "resources/auto/gen_hebdo.py"
FILES_TO_WATCH = {
    # os.path.abspath("main.py"): ["flet", "run", "main.py"],
    # os.path.abspath("t/hotreload.py"): [
    #     "flet",
    #     "run",
    #     "t/hotreload.py",
    # ],
    os.path.abspath("t/main.py"): [
        "flet",
        "run",
        "t/main.py",
    ],
    # os.path.abspath("resources/generate_changelog.py"): [
    #     "flet",
    #     "run",
    #     "resources/generate_changelog.py",
    # ],
    os.path.abspath("resources/auto/subs/scan_todos.py"): [
        "flet",
        "run",
        "resources/auto/gen_todos.py",
    ],
    os.path.abspath(script_path): [
        "flet",
        "run",
        script_path,
    ],
}


class ReloadHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.last_modified = {}

    def on_modified(self, event):
        if event.is_directory:
            return

        modified_file = os.path.abspath(event.src_path)
        now = time.time()

        for target_file, command in FILES_TO_WATCH.items():
            if modified_file == target_file:
                last_time = self.last_modified.get(modified_file, 0)
                if (
                    now - last_time < 0.7
                ):  # Ignore if less than 1 second since last trigger
                    return
                self.last_modified[modified_file] = now

                if self.process:
                    self.process.kill()
                self.process = subprocess.Popen(command)
                print(f"🔄 Change detected in {target_file}, restarting...")
                break


if __name__ == "__main__":
    event_handler = ReloadHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    print("👀 Watching for changes in:")
    for f in FILES_TO_WATCH:
        print("   •", f)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if event_handler.process:
            event_handler.process.kill()
    observer.join()
