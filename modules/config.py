import re
from configparser import ConfigParser
from pathlib import Path


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / 'config.ini'
DIRECTORY_SETTING_KEYS = ('SERVER_SIDE', 'CLIENT_SIDE')


def load_config(config_path=None):
    """Read rDec's config file, independent of the current working directory."""
    config_parser = ConfigParser(inline_comment_prefixes=('#', ';'))
    config_parser.read(config_path or DEFAULT_CONFIG_PATH, encoding='utf-8')
    return config_parser


def get_directory_settings(config_path=None):
    config_parser = load_config(config_path)
    return {
        setting_name: config_parser.get('DIRECTORY', setting_name, fallback='').strip()
        for setting_name in DIRECTORY_SETTING_KEYS
    }


def set_directory_setting(setting_name, directory_path, config_path=None):
    """Update one directory setting while keeping existing config comments."""
    setting_name = setting_name.upper()
    if setting_name not in DIRECTORY_SETTING_KEYS:
        raise ValueError(f'Unknown directory setting: {setting_name!r}.')

    config_file_path = Path(config_path or DEFAULT_CONFIG_PATH)
    if config_file_path.exists():
        with config_file_path.open('r', encoding='utf-8', newline='') as config_file:
            config_lines = config_file.readlines()
    else:
        config_lines = []

    line_ending = '\r\n' if any(line.endswith('\r\n') for line in config_lines) else '\n'
    section_start = None
    section_end = len(config_lines)
    for index, line in enumerate(config_lines):
        section = re.match(r'^\s*\[([^]]+)\]', line)
        if section:
            if section_start is not None:
                section_end = index
                break
            if section.group(1).strip().lower() == 'directory':
                section_start = index

    if section_start is None:
        if config_lines and not config_lines[-1].endswith(('\n', '\r')):
            config_lines[-1] += line_ending
        if config_lines and config_lines[-1].strip():
            config_lines.append(line_ending)
        config_lines.extend((f'[DIRECTORY]{line_ending}', f'{setting_name} = {directory_path}{line_ending}'))
    else:
        setting_pattern = re.compile(rf'^(\s*{re.escape(setting_name)}\s*=)(.*?)(\r?\n)?$', re.IGNORECASE)
        for index in range(section_start + 1, section_end):
            match = setting_pattern.match(config_lines[index])
            if not match:
                continue
            remainder = match.group(2)
            comment = re.search(r'\s+[;#].*$', remainder)
            suffix = f' {comment.group(0).lstrip()}' if comment else ''
            ending = match.group(3) or ''
            config_lines[index] = f'{match.group(1)} {directory_path}{suffix}{ending}'
            break
        else:
            config_lines.insert(section_end, f'{setting_name} = {directory_path}{line_ending}')

    config_file_path.parent.mkdir(parents=True, exist_ok=True)
    with config_file_path.open('w', encoding='utf-8', newline='') as config_file:
        config_file.writelines(config_lines)
