from modules import *

cwd = os.getcwd()
project_name_regexs = [
    re.compile(r'[/\\]scraping(?P<project_name>_[^/\\]+)$'),
    re.compile(r'[/\\](?P<project_name>[^/\\]+)$'),
]

# todo: project_name
project_name = ''
for project_name_regex in project_name_regexs:
    found = project_name_regex.search(cwd)
    if found:
        project_name = try_excetp_re(found, 'project_name')
        break

# todo: parent_dir
parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

# todo: others
except_dir = 'except'
except_values_dir = 'except_values'
except_points_dir = 'except_points'
server_dir = '/mnt/volume_nyc1_05'
download_dir = os.path.join(parent_dir, 'download') if 'Users' in cwd else f'{server_dir}/download'
cache_dir = os.path.join(parent_dir, f'cache{project_name}') if 'Users' in cwd else f'{server_dir}/cache{project_name}'
session_dir = os.path.join(parent_dir, f'session{project_name}')
