
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

class SimpleHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"MODIFIED: {event.src_path}")
    def on_created(self, event):
        print(f"CREATED: {event.src_path}")

def main():
    test_dir = Path("watch_test_dir").resolve()
    test_dir.mkdir(exist_ok=True)
    
    handler = SimpleHandler()
    observer = Observer()
    observer.schedule(handler, str(test_dir), recursive=False)
    observer.start()
    
    print(f"Watching {test_dir}...")
    try:
        time.sleep(2)
        test_file = test_dir / "test.txt"
        print(f"Creating {test_file}...")
        test_file.write_text("hello")
        time.sleep(2)
    finally:
        observer.stop()
        observer.join()
        if test_file.exists(): test_file.unlink()
        test_dir.rmdir()

if __name__ == "__main__":
    main()
