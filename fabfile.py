
from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.context_managers import settings
from fabric.utils import fastprint


#SETTINGS_FILE_PATH = Path(__file__).ancestor(1).child('project_settings.json')

# with open(SETTINGS_FILE_PATH, 'r') as f:
#     # Load settings.
#     project_settings = json.loads(f.read())
#
# env.prompts = {
#     'Type \'yes\' to continue, or \'no\' to cancel: ': 'yes'
# }

env.hosts = ['kena@srv-dev-01']

#@task
def help():
    message = '''
    Remote updating application with fabric.

    Usage example:

    Deploy to development server:
    fab development deploy

    Deploy to production server with no tests:
    fab stable deploy:tests=no
    '''
    fastprint(message)


def test():
    with settings(warn_only=True):
        result = local("./manage.py test djangoproj")
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at the user request")


def commit(message='commit'):
    local("git add && git commit -am {}" .format(message))


def push():
    branch = 'development'
    local("git push origin {}" .format(branch))


def deploy():
    rep = 'kenaxle/djangoproj'
    branch = 'development'
    srv_code_dir = '/home/kena/djangoproj'
    with settings(warn_only=True):
        test_result = run("test -d {}" .format(srv_code_dir))
        if test_result.failed:
            run("mkdir {}" .format(srv_code_dir))
            run("git clone -b {} https://github.com/{} {}" .format( branch, rep, srv_code_dir))
        # else:
        #     with cd(srv_code_dir):
        #         run("git commit -am 'commit server changes'")
    with cd(srv_code_dir):
        run("git pull ")
        run("touch app.wsgi")


def launch():
    srv_code_dir = '/home/kena/djangoproj'
    with cd(srv_code_dir):
        run("python ./manage.py makemigrations")
        run("python ./manage.py migrate")
        run("python ./manage.py runserver 0.0.0.0:8080")





# def set_stage(stage_name='development'):
#     stages = project_settings['stages'].keys()
#     if stage_name not in stages:
#         raise KeyError('Stage name "{0}" is not a valid stage ({1})'.format(
#             ','.join(stages))
#         )
#     env.stage = stage_name
#
#
# @task
# def stable():
#     set_stage('stable')
#     set_project_settings()
#
#
# @task
# def development():
#     set_stage('development')
#     set_project_settings()
#
#
# def set_project_settings():
#     stage_settings = project_settings['stages'][env.stage]
#     if not all(project_settings.itervalues()):
#         raise KeyError('Missing values in project settings.')
#     env.settings = stage_settings
#
#
# # @task
# # def deploy(tests='yes'):
# #     '''
# #     Deploys project to previously set stage.
# #     '''
# #     require('stage', provided_by=(stable, development))
# #     require('settings', provided_by=(stable, development))
# #     # Set env.
# #     env.vcs_type = project_settings['vcs_type']
# #     env.user = env.settings['user']
# #     env.host_string = env.settings['host']
# #
# #     with hide('stderr', 'stdout', 'warnings', 'running'):
# #         if tests == 'yes':
# #             with lcd(project_settings['local']['code_src_directory']):
# #                 run_tests()
# #         with cd(env.settings['code_src_directory']):
# #             pull_repository()
# #         with virtualenv(env.settings['venv_directory']):
# #             with cd(env.settings['code_src_directory']):
# #                 collect_static()
# #                 install_requirements()
# #                 migrate_models()
# #         restart_application()
#
#
# def print_status(description):
#     def print_status_decorator(fn):
#         def print_status_wrapper():
#             now = datetime.now().strftime('%H:%M:%S')
#             fastprint('({time}) {description}{suffix}'.format(
#                 time=now,
#                 description=description.capitalize(),
#                 suffix='...\n')
#             )
#             fn()
#             now = datetime.now().strftime('%H:%M:%S')
#             fastprint('({time}) {description}{suffix}'.format(
#                 time=now,
#                 description='...finished '+description,
#                 suffix='.\n')
#             )
#         return print_status_wrapper
#     return print_status_decorator
#
# # @print_status('starting my_task')
# # def my_task():
# #     # sum job
#
# @print_status('running tests locally')
# def run_tests():
#     '''
#     Runs all tests locally. Tries to use settings.test first for sqlite db.
#     To avoid running test, use `deploy:tests=no`.
#     '''
#     python_exec = project_settings['local']['venv_python_executable']
#     test_command = python_exec + ' manage.py test'
#     with settings(warn_only=True):
#         result = local(test_command + ' --settings=settings.test')
#         if not result.failed:
#             return
#         result = local(test_command + ' --settings=settings.dev')
#         if result.failed:
#             abort('Tests failed. Use deploy:tests=no to omit tests.')
#
# def pull_repository():
#     '''
#     Updates local repository, selecting the vcs from configuration file.
#     '''
#     if env.vcs_type == 'mercurial':
#         pull_mercurial_repository
#     elif env.vcs_type == 'git':
#         pull_git_repository
#     else:
#         abort(
#             'vcs type must be either mercurial or git,'
#             ' currently is: {vcs}'.format(vcs=env.vcs_type)
#         )
#
# @print_status('pulling mercurial repository')
# def pull_mercurial_repository():
#     run('hg pull -u')
#     run('hg up {branch}'.format(branch=env.settings['vcs_branch']))
#
# @print_status('pulling git repository')
# def pull_git_repository():
#     command = 'git pull {} {}'.format(
#         env.project_settings.get('git_repository'),
#         env.settings.get('vcs_branch')
#     )
#     run(command)
#
# @print_status('collecting static files')
# def collect_static():
#     run('python manage.py collectstatic')
#
# @print_status('installing requirements')
# def install_requirements():
#     with cd(env.settings['code_src_directory']):
#         run('pip install -r {0}'.format(env.settings['requirements_file']))
#
# @print_status('migrating models')
# def migrate_models():
#     run('python manage.py migrate')
#
# @print_status('restarting application')
# def restart_application():
#     with settings(warn_only=True):
#         restart_command = env.settings['restart_command']
#         result = run(restart_command)
#     if result.failed:
#         abort('Could not restart application.')

