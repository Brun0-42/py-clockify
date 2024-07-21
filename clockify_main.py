# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from loguru import logger
import configparser
import my_clockify.my_clockify_workspace_api
import utils.my_loguru_decorator as loguru_decorator
import click
import datetime

# ----------------------------------------------------------------------------#
@loguru_decorator.logger_wraps(level="DEBUG")
def list_all_tasks_in_active_projects():
	my_config_file_parser = configparser.ConfigParser()
	my_config_file_parser.read('config.ini')
	my_clockify_api_key = my_config_file_parser['clockify']['key']
	my_clockify_workspace_name = my_config_file_parser['clockify']['workspace_name']

	my_clockify_api = my_clockify.my_clockify_workspace_api.MyClockifyWorkspaceApi(my_clockify_api_key, my_clockify_workspace_name)
	my_clockify_api.list_all_tasks_in_active_projects()

@loguru_decorator.logger_wraps(level="DEBUG")
def list_all_active_tasks_in_active_projects():
	my_config_file_parser = configparser.ConfigParser()
	my_config_file_parser.read('config.ini')
	my_clockify_api_key = my_config_file_parser['clockify']['key']
	my_clockify_workspace_name = my_config_file_parser['clockify']['workspace_name']

	my_clockify_api = my_clockify.my_clockify_workspace_api.MyClockifyWorkspaceApi(my_clockify_api_key, my_clockify_workspace_name)
	my_clockify_api.list_all_active_tasks_in_active_projects()

# ----------------------------------------------------------------------------#
@loguru_decorator.logger_wraps(level="DEBUG")
def list_active_projects():
	my_config_file_parser = configparser.ConfigParser()
	my_config_file_parser.read('config.ini')
	my_clockify_api_key = my_config_file_parser['clockify']['key']
	my_clockify_workspace_name = my_config_file_parser['clockify']['workspace_name']

	my_clockify_api = my_clockify.my_clockify_workspace_api.MyClockifyWorkspaceApi(my_clockify_api_key, my_clockify_workspace_name)
	my_clockify_api.list_active_projects()

# ----------------------------------------------------------------------------#
@loguru_decorator.logger_wraps(level="DEBUG")
def read_summary_report(delta_days):
	my_config_file_parser = configparser.ConfigParser()
	my_config_file_parser.read('config.ini')
	my_clockify_api_key = my_config_file_parser['clockify']['key']
	my_clockify_workspace_name = my_config_file_parser['clockify']['workspace_name']

	my_clockify_api = my_clockify.my_clockify_workspace_api.MyClockifyWorkspaceApi(my_clockify_api_key, my_clockify_workspace_name)
	
	dateRangeEnd = datetime.datetime.now().replace(hour=23, minute=59, second=59, microsecond=59).isoformat()
	dateRangeStart = (datetime.datetime.now() - datetime.timedelta(days=delta_days)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
	print(f"==== Report ({dateRangeStart} / {dateRangeEnd}) ===")
	my_clockify_api.read_summary_report(dateRangeStart, dateRangeEnd)
	print("")

# ----------------------------------------------------------------------------#
@click.group()
def cli():
	"""A command line interface for the time tracker app Clockify."""
	pass

# ----------------------------------------------------------------------------#
@cli.command()
@click.argument('delta_days', type=click.INT)
def report(delta_days):
	"""Print the task time report (for example, for the last 3 weeks, delta_days=19)."""
	read_summary_report(delta_days)

# ----------------------------------------------------------------------------#
@cli.command()
@click.argument('param', type=click.Choice(['tasks', 'active_tasks','active_projects'], case_sensitive=False))
def list(param):
	"""Print the list of tasks (param='task') or active tasks (param='active_tasks') or active projects (param='active_projects')."""
	if(param.lower() == 'tasks'):
		list_all_tasks_in_active_projects()
	elif(param.lower() == 'active_tasks'):
		list_all_active_tasks_in_active_projects()
	elif(param.lower() == 'active_projects'):
		list_active_projects()

# ----------------------------------------------------------------------------#
if __name__=='__main__':
	cli()
