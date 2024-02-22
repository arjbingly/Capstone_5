import textwrap
import os
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path


def wrap_text_preserve_newlines(text, width=110):
    # Split the input text into lines based on newline characters
    lines = text.split('\n')

    # Wrap each line individually
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]

    # Join the wrapped lines back together using newline characters
    wrapped_text = '\n'.join(wrapped_lines)

    return wrapped_text


def process_llm_response(llm_response):
    # print(wrap_text_preserve_newlines(llm_response['result']))
    print(llm_response['result'])
    print('\nSources:')
    for source in llm_response["source_documents"]:
        print(source.metadata['source'])


def find_project_root(current_path):
    # Traverse up until you find the config.ini file
    while not (current_path / 'CONFIG_Run' / 'config' / 'config.ini').exists():
        current_path = current_path.parent
        if current_path == current_path.parent:
            raise FileNotFoundError("config.ini not found in any parent directories.")
    return current_path


def get_config():
    # Assuming this script is somewhere inside your project directory
    script_location = Path(__file__).resolve()
    root_directory = find_project_root(script_location)

    # Path to your config file
    config_path = root_directory / 'CONFIG_Run' / 'config' / 'config.ini'
    print(config_path)
    # Initialize parser and read config
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read(config_path)

    return config
