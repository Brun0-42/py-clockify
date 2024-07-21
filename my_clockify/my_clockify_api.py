# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from loguru import logger
import utils.my_loguru_decorator as loguru_decorator

import requests
import json
import time

# ----------------------------------------------------------------------------#
class MyClockifyApi:
	"My clockify api"

	def __init__(self, api_key):
		self._api_key = api_key
		self.base_url = 'https://api.clockify.me/api/v1/'
		self.header =  {'X-Api-Key': self._api_key }

	@loguru_decorator.logger_wraps()
	def _request_get(self,url):
		while (True):
			try:
				response = requests.get(url, headers=self.header)
				return response.json()
			except Exception as e:
				logger.error("Error: {0}".format(e))
				logger.error("Try againg in 60 seconds")
				time.sleep(60)

	@loguru_decorator.logger_wraps()
	def _request_post(self,url,payload):
		while (True):
			try:
				response = requests.post(url, headers=self.header,json=payload)
				return response.json()
			except Exception as e:
				logger.error("Error: {0}".format(e))
				logger.error("Try againg in 60 seconds")
				time.sleep(60)

	@loguru_decorator.logger_wraps()
	def get_all_workspaces(self):
		try:
			url = self.base_url+'workspaces/'
			return self._request_get(url)

		except Exception as e:
			logger.error("OS error: {0}".format(e))
			logger.error(e.__dict__)

	@loguru_decorator.logger_wraps()
	def get_workspace_id(self, workspace_name):
		result = 0
		workspaces = self.get_all_workspaces()
		for workspace in workspaces:
			if workspace_name == workspace["name"]:
				result = workspace["id"]
		return result

	# returns all project from a workspace
	@loguru_decorator.logger_wraps()
	def get_all_projects(self, workspace_id):
		try:
			url = self.base_url + 'workspaces/' + workspace_id + '/projects/'
			return self._request_get(url)
		except Exception as e:
			logger.error("OS error: {0}".format(e))
			logger.error(e.__dict__)

	# returns all project from a workspace
	@loguru_decorator.logger_wraps()
	def get_all_tasks(self, workspace_id, project_id):
		try:
			url = self.base_url + 'workspaces/' + workspace_id + '/projects/' + project_id + '/tasks'
			return self._request_get(url)
		except Exception as e:
			logger.error("OS error: {0}".format(e))
			logger.error(e.__dict__)

	# returns id form project name
	@loguru_decorator.logger_wraps()
	def get_project_id(self, workspace_id, project_name):
		result = 0
		projects = self.get_all_projects(workspace_id)
		for projet in projects:
			if project_name == projet["name"]:
				result = projet["id"]
		return result

	# returns id form task name
	@loguru_decorator.logger_wraps()
	def get_task_id(self, workspace_id, project_id, task_name):
		result = 0
		tasks = self.get_all_tasks(workspace_id, project_id)
		for task in tasks:
			logger.debug(task)
			if task_name == task["name"]:
				result = task["id"]
		return result

	# returns id form task name
	@loguru_decorator.logger_wraps()
	def get_user_id(self):
		user = ""
		try:
			url = self.base_url + 'user/'
			result = self._request_get(url)
			user = result["id"]

		except Exception as e:
			logger.error("OS error: {0}".format(e))
			logger.error(e.__dict__)

		return user

	# returns project description by id
	@loguru_decorator.logger_wraps()
	def get_project_by_id(self, workspace_id, project_id):
		try:
			url = self.base_url + 'workspaces/' + workspace_id + '/projects/' + project_id
			return self._request_get(url)
		except Exception as e:
			logger.error("OS error: {0}".format(e))
			logger.error(e.__dict__)


	# returns all tasks
	@loguru_decorator.logger_wraps()
	def get_all_tasks(self, workspace_id, project_id):
		try:
			url = self.base_url+'workspaces/'+workspace_id+'/projects/'+project_id+'/tasks/'
			return self._request_get(url)

		except Exception as e:
			logger.error("OS error: {0}".format(e))
			logger.error(e.__dict__)

	# returns all active tasks
	@loguru_decorator.logger_wraps()
	def get_all_active_tasks(self, workspace_id, project_id):
		try:
			url = self.base_url+'workspaces/'+workspace_id+'/projects/'+project_id+'/tasks/?is-active=True'
			return self._request_get(url)
		except Exception as e:
			logger.error("OS error: {0}".format(e))
			logger.error(e.__dict__)

	# create a new task in a project
	@loguru_decorator.logger_wraps()
	def add_new_task(self, workspace_id, project_id, task_name, assigneeId = None, estimate = None):
		try:
			url = self.base_url+'workspaces/'+workspace_id+'/projects/'+project_id+'/tasks/'
			task = {}
			task['name'] = task_name
			#task['projectId'] = project_id
			if (assigneeId is not None):
				task['assigneeId'] = assigneeId
			if (estimate is not None):
				task['estimate'] = estimate

			return self._request_post(url, task)
		except Exception as e:
			logger.error("OS error: {0}".format(e))
			logger.error(e.__dict__)

	# read summary report (draft)
	@loguru_decorator.logger_wraps()
	def read_summary_report(self, workspace_id, dateRangeStart, dateRangeEnd, summaryFilter):
		# {
		#     "dateRangeStart": "2022-12-01T00:00:00.000Z",
		#     "dateRangeEnd": "2022-12-31T23:59:59.000Z",
		#     "summaryFilter": {"groups": ["CLIENT"]},
		#     "exportType": "JSON"

		#https://reports.api.clockify.me/v1/workspaces/602bf5a6158b7e35c8e6fb35/reports/summary
		# }
		try:
			url = 'https://reports.api.clockify.me/v1/workspaces/'+workspace_id+'/reports/summary'
			body = {"dateRangeStart": dateRangeStart, "dateRangeEnd": dateRangeEnd, "summaryFilter": summaryFilter, "exportType": "JSON"}
			
			logger.debug(url)
			logger.debug(body)

			return self._request_post(url, body)
		except Exception as e:
			logger.error("OS error: {0}".format(e))
			logger.error(e.__dict__)

	# Add a new time entry
	@loguru_decorator.logger_wraps()
	def add_new_time_entry(self, workspaceId, projectId, taskId, dateStart, dateEnd, description=""):
		try:
			userId = self.get_user_id()
			url = self.base_url+'workspaces/'+workspaceId+'/user/'+userId+'/time-entries'

			newTimeEntry = {}
			newTimeEntry['start'] = dateStart
			newTimeEntry['end'] = dateEnd
			newTimeEntry['billable'] = False
			newTimeEntry['description'] = "essai"
			newTimeEntry['projectId'] = projectId
			newTimeEntry['taskId'] = taskId
			newTimeEntry['tagIds'] = []
			newTimeEntry["type"] = "REGULAR"

			logger.debug(newTimeEntry)

			return self._request_post(url, newTimeEntry)
		except Exception as e:
			logger.error("OS error: {0}".format(e))
			logger.error(e.__dict__)