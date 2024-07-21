# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from loguru import logger
import my_clockify.my_clockify_api
import utils.my_utils_time
import utils.my_loguru_decorator as loguru_decorator

# ----------------------------------------------------------------------------#
class MyClockifyWorkspaceApi:
	"My clockify workspace API"

	def __init__(self, api_key, workspace_name):
		self._my_clockify_api = my_clockify.my_clockify_api.MyClockifyApi(api_key)
		self._workspace_name = workspace_name

	@loguru_decorator.logger_wraps()
	def add_task(self, project_name, task_name, assigneeId = None, estimate = None):
		"""Add task"""

		# Get my workspace id
		workspace_id = self._my_clockify_api.get_workspace_id(self._workspace_name)

		project_id = self._my_clockify_api.get_project_id(workspace_id, project_name)
		logger.debug("add_new_task - projet id: {}".format(project_id))

		self._my_clockify_api.add_new_task(workspace_id, project_id, task_name, assigneeId, estimate)
		logger.info("add_new_task - result: Done")

	@loguru_decorator.logger_wraps()
	def list_all_tasks_in_active_projects(self):
		"""List all the active projects and all tasks"""

		# Get my workspace id
		workspace_id = self._my_clockify_api.get_workspace_id(self._workspace_name)

		# List all the active projects
		projects = self._my_clockify_api.get_all_projects(workspace_id)
		for project in projects:
			if project["archived"] == False:
				print("{}:".format(project["name"]))
				tasks = self._my_clockify_api.get_all_tasks(workspace_id, project["id"])
				for task in tasks:
					task_name = task["name"]
					task_duration = utils.my_utils_time.convert_duration_to_work_days(task["duration"])
					task_estimate = utils.my_utils_time.convert_duration_to_work_days(task["estimate"])
					if (task_estimate >= 0) and (task_duration >= 0):
						if task_estimate != 0:
							task_progress = ": {} %".format(int(float(task_duration*100)/float(task_estimate)))
						else:
							task_progress = ""
						print("    * {} [{}/{}{}]".format(task_name, task_duration, task_estimate, task_progress))
					else :
						print("    * {}".format(task_name))

	@loguru_decorator.logger_wraps()
	def list_all_active_tasks_in_active_projects(self):
		"""List all the active projects and all tasks"""

		# Get my workspace id
		workspace_id = self._my_clockify_api.get_workspace_id(self._workspace_name)

		# List all the active projects
		projects = self._my_clockify_api.get_all_projects(workspace_id)
		for project in projects:
			project_printed=False
			if project["archived"] == False:
				
				tasks = self._my_clockify_api.get_all_tasks(workspace_id, project["id"])
				for task in tasks:
					if task['status'] != 'DONE':

						if not project_printed:
							print("{}:".format(project["name"]))
							project_printed = True

						task_name = task["name"]
						task_duration = utils.my_utils_time.convert_duration_to_work_days(task["duration"])
						task_estimate = utils.my_utils_time.convert_duration_to_work_days(task["estimate"])
						if (task_estimate >= 0) and (task_duration >= 0):
							if task_estimate != 0:
								task_progress = ": {} %".format(int(float(task_duration*100)/float(task_estimate)))
							else:
								task_progress = ""
							print("    * {} [{}/{}{}]".format(task_name, task_duration, task_estimate, task_progress))
						else :
							print("    * {}".format(task_name))

	@loguru_decorator.logger_wraps()
	def list_active_projects(self):
		"""List all the active projects"""

		# Get my workspace id
		workspace_id = self._my_clockify_api.get_workspace_id(self._workspace_name)

		# List all the active projects
		projects = self._my_clockify_api.get_all_projects(workspace_id)
		for project in projects:
			if project["archived"] == False:
				print("{} ({}):".format(project["name"], project["id"]))

	@loguru_decorator.logger_wraps()
	def read_summary_report(self, dateRangeStart, dateRangeEnd):
		workspace_id = self._my_clockify_api.get_workspace_id(self._workspace_name)
		summaryFilter= {"groups": ["CLIENT", "TASK"]}
		result = self._my_clockify_api.read_summary_report(workspace_id, dateRangeStart, dateRangeEnd, summaryFilter)

		for groupElement in result["groupOne"]:
			print("{}:".format(groupElement["name"]))
			for task in groupElement["children"]:
				print("  {} - {}: {} day(s)".format(task["clientName"], task["name"], task["duration"]/3600/8))

	@loguru_decorator.logger_wraps()
	def add_new_time_entry(self, project_name, task_name, dateStart, dateEnd):
		workspace_id = self._my_clockify_api.get_workspace_id(self._workspace_name)
		project_id = self._my_clockify_api.get_project_id(workspace_id, project_name)
		task_id = self._my_clockify_api.get_task_id(workspace_id, project_id, task_name)

		logger.error("project_id: {}".format(project_id))
		logger.error("task_id: {}".format(task_id))

		return self._my_clockify_api.add_new_time_entry(
			workspace_id,
			project_id,
			task_id,
			utils.my_utils_time.from_datetime_to_zulu_string(dateStart),
			utils.my_utils_time.from_datetime_to_zulu_string(dateEnd))
