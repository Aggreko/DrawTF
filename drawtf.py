import sys
import time
import click
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from app.common.drawing import commonDraw
from dotenv import load_dotenv

@click.group()
def main():
    """Top level command for drawtf."""
    pass

@click.command()
@click.option('--name', help='The diagram name.')
@click.option('--state', help='The tfstate file to run against.')
@click.option('--platform', help="The platform to use 'azure' or 'aws', only 'azure' currently supported")
@click.option('--output-path', help='Output path if to debug generated json populated.')
@click.option('--json-config-path', help='Config file path if populated.')
@click.option('--verbose', is_flag=True, default=False, help='Add verbose logs.')
def draw(name: str, state: str, platform: str, output_path: str, json_config_path: str, verbose: bool):
    """Draw a single design from config and settings."""
    load_dotenv()
    return commonDraw(name, state, platform, output_path, json_config_path, verbose)

last_trigger_time = time.time()

@click.command()
@click.option('--directory', help='Directory to watch for changes in.')
def watch(directory: str):
    """Watch a directory for changes to draw."""
    load_dotenv()
    click.secho("Starting watch for *.json files...", fg='yellow')
    
    patterns = ["*.json"]
    ignore_patterns = None
    ignore_directories = True
    case_sensitive = False
    event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    event_handler.on_created = __on_created
    event_handler.on_modified = __on_modified
    event_handler.on_moved = __on_moved
    
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    
    observer.start()
    click.secho(f"Watching in {directory}...", fg='yellow')
    
    try:
        while observer.isAlive():
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        click.secho("Exiting watch...", fg='yellow')

def __on_created(event):
    global last_trigger_time
    current_time = time.time()
    if event.src_path.find('~') == -1 and (current_time - last_trigger_time) > 1:
        last_trigger_time = current_time
        click.secho(f"New file {event.src_path}, drawing...", fg='yellow')
        commonDraw(None, None, None, None, event.src_path, None)
        click.secho(f"{event.src_path} done.", fg='green')

def __on_modified(event):
    global last_trigger_time
    current_time = time.time()
    if event.src_path.find('~') == -1 and (current_time - last_trigger_time) > 1:
        last_trigger_time = current_time
        click.secho(f"Modified file {event.src_path}, drawing...", fg='yellow')
        commonDraw(None, None, None, None, event.src_path, None)
        click.secho(f"{event.src_path} done.", fg='green')
    
def __on_moved(event):
    global last_trigger_time
    current_time = time.time()
    if event.src_path.find('~') == -1 and (current_time - last_trigger_time) > 1:
        last_trigger_time = current_time
        click.secho(f"Moved file {event.dest_path}, drawing...", fg='yellow')
        commonDraw(None, None, None, None, event.dest_path, None)
        click.secho(f"{event.dest_path} done.", fg='green')


main.add_command(draw)
main.add_command(watch)

if __name__ == "__main__":
    sys.exit(draw())  # type: ignore # pragma: no cover
