import sys
import argparse
import httplib, urllib
import json
import os
import string

###########
# Globals #
###########

global ip
ip = "localhost"

global port
port = "8080"

#########################################################################################


#############
# Functions #
#############

#########################################################################################
# Logging #                                                                             #
#########################################################################################

def logSendRequest(url, requestType, body=None):
    """Print generic Send request to Conductor Server"""
    
    print("Sending [" + requestType + "] request to Conductor Server " + "(" + url + ")" + ":")
    if body != None:
        print("Body:")
        print(body)
    print("\n")


def logResponse(statusCode, response):
    """Print generic Response from Conductor Server"""
    
    print("Received response from Conductor Server " + "(" + ip + ")" + ":")
    print("Status: " + str(statusCode))
    print(response)
    print("\n")


#########################################################################################
# HTTP Helpers #                                                                        #
#########################################################################################

def httpRequest(url, requestType, path, headers, body=None):
    url = string.replace(url," ", "%20")
    logSendRequest(url, requestType, body)
    conn = httplib.HTTPConnection(ip, port)
    conn.request(requestType, path, body, headers)
    response = conn.getresponse()
    responseData = response.read()
    logResponse(response.status, responseData)
    return response, responseData


def httpPost(path, body='{}'):
    """HTTP POST request to Conductor Server"""
    headers = {"Content-type": "application/json"}
    url = "http://" + ip + ":" + port + path
    return httpRequest(url, "POST", path, headers, body)


def httpPut(path, body='{}'):
    """HTTP PUT request to Conductor Server"""

    headers = {"Content-type": "application/json"}
    url = "http://" + ip + ":" + port + path
    return httpRequest(url, "PUT", path, headers, body)


def httpGet(path):
    """HTTP GET request to Conductor Server"""

    headers = {"Accept": "application/json"}
    url = "http://" + ip + ":" + port + path
    return httpRequest(url, "GET", path, headers)


def httpDelete(path, body='{}'):
    """HTTP DELETE request to Conductor Server"""

    headers = {"Accept": "application/json"}
    url = "http://" + ip + ":" + port + path
    logSendRequest(url, "DELETE")
    return httpRequest(url, "DELETE", path, headers)


#########################################################################################
# Event Services #                                                                      #
#########################################################################################

def getAllEventHandlers():
    """Get all the Conductor Event Handlers
        Will invoke GET request with format http://<ip>:<port>/api/event
    """

    path = "/api/event"
    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def getEventHandler(event, activeOnly='true'):
    """Get Event Handler for given event <event>
        Will invoke GET request with format http://<ip>:<port>/api/event/<event>?activeOnly=<activeOnly>
    """

    path = "/api/event/" + event + "?activeOnly=" + activeOnly
    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def createEventHandler(body):
    """Create Event Handler definition of body passed in
        Will invoke POST request with format http://<ip>:<port>/api/event
    """

    path = "/api/event"
    response, responseData = httpPost(path, body)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def modifyEventHandler(body):
    """Modify Event Handler definition of body passed in
        Will invoke PUT request with format http://<ip>:<port>/api/event
    """

    path = "/api/event"
    response, responseData = httpPut(path, body)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def deleteEventHandler(name):
    """Delete Event Handler of <name> passed in
        Will invoke DELETE request with format http://<ip>:<port>/api/event/<name>
    """

    path = "/api/event/" + name
    response, responseData = httpDelete(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def getEventExecutions(eventHandlerName, eventName, messageId, max=100):
    """Get up to 100 Conductor Event Executions
        Will invoke GET request with format http://<ip>:<port>/api/event/executions/<eventHandlerName>/<eventName>/<messageId>?max=<max>
    """

    path = "/api/event/executions/" + eventHandlerName + "/" + eventName + "/" + messageId + "?max=" + str(max)
    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def getRegisteredQueues(verbosity="false"):
    """Get all the Conductor Registered Queues
        Will invoke GET request with format http://<ip>:<port>/api/event/queues?verbose=<verbosity>
    """

    path = "/api/event/queues?verbose=" + verbosity
    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def getRegisteredQueueProviders():
    """Get all the Conductor Registered Queue Providers
        Will invoke GET request with format http://<ip>:<port>/api/event/queues/providers
    """

    path = "/api/event/queues/providers"
    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

#########################################################################################
# Metadata Management #                                                                 #
#########################################################################################

def getAllTaskMetadata():
    """Get all the Conductor Task Definitions
        Will invoke GET request with format http://<ip>:<port>/api/metadata/taskdefs
    """

    path = "/api/metadata/taskdefs"
    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def createTaskMetadata(metadata):
    """Create Task(s) definitions of metadata passed in
        Will invoke POST request with format http://<ip>:<port>/api/metadata/taskdefs
    """

    path = "/api/metadata/taskdefs"
    response, responseData = httpPost(path, metadata)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def modifyTaskMetadata(metadata):
    """Modify Task definitions of metadata passed in
        Will invoke PUT request with format http://<ip>:<port>/api/metadata/taskdefs
    """

    path = "/api/metadata/taskdefs"
    response, responseData = httpPut(path, metadata)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def deleteTaskMetadata(taskType):
    """Delete Task definitions of taskType passed in
        Will invoke DELETE request with format http://<ip>:<port>/api/metadata/taskdefs/<tasktype>
    """

    path = "/api/metadata/taskdefs/" + taskType
    response, responseData = httpDelete(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def getTaskMetadata(taskType):
    """Get Task definition of taskType passed in
        Will invoke GET request with format http://<ip>:<port>/api/metadata/taskdefs/<tasktype>
    """

    path = "/api/metadata/taskdefs/" + taskType
    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def getAllWorkflowMetadata():
    """Get all the Conductor Workflow Definitions
        Will invoke GET request with format http://<ip>:<port>/api/metadata/workflow
    """

    path = "/api/metadata/workflow"
    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def createWorkflowMetadata(metadata):
    """Create Workflow definition of metadata passed in
        Will invoke POST request with format http://<ip>:<port>/api/metadata/workflow
    """

    path = "/api/metadata/workflow"
    response, responseData = httpPost(path, metadata)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def modifyWorkflowMetadata(metadata):
    """Modify Workflow definitions of metadata passed in
        Will invoke PUT request with format http://<ip>:<port>/api/metadata/workflow
    """

    path = "/api/metadata/workflow"
    response, responseData = httpPut(path, metadata)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def getWorkflowMetadata(name):
    """Get Workflow definition of name passed in
        Will invoke GET request with format http://<ip>:<port>/api/metadata/workflow/<name>
    """

    path = "/api/metadata/workflow/" + name
    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON


#########################################################################################
# Admin #                                                                               #
#########################################################################################

def getConfiguration():
    """Get all the Conductor Configuration Parameters
        Will invoke GET request with format http://<ip>:<port>/api/admin/config
    """

    path = "/api/admin/config"
    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def sweepWorkflow(workflowId):
    """Queue up all the running workflows for sweep
        Will invoke POST request with format http://<ip>:<port>/api/admin/sweep/requeue/<workflowId>
    """

    path = "/api/admin/sweep/requeue/" + workflowId
    response, responseData = httpPost(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def getPendingTasks(taskType, start=None, count=100):
    """Get the list of pending tasks for a given task type
        Will invoke GET request with format http://<ip>:<port>/api/admin/task/<taskType>?start=<start>&count=<count>
    """

    parameterString = "?"
    if start != None:
        parameterString += "start=" + str(start)
        parameterString += "&"

    parameterString += "count=" + str(count)

    path = "/api/admin/task/" + taskType + parameterString
    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

#########################################################################################
# Task Management #                                                                     #
#########################################################################################

def updateTask(body):
    """Update Task with information of body passed in
        Will invoke POST request with format http://<ip>:<port>/api/tasks
    """

    path = "/api/tasks"
    response, responseData = httpPost(path, body)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def getInProgressTask(taskType, startKey=None, count=100):
    """Get in progress tasks for a given task type
        Will invoke GET request with format http://<ip>:<port>/api/tasks/in_progress/<taskType>?startKey=<startKey>&count=<count>
    """

    parameterString = "?"
    if startKey != None:
        parameterString += "startKey=" + startKey
        parameterString += "&"

    parameterString += "count=" + str(count)

    path = "/api/tasks/in_progress/" + taskType + parameterString
    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def getInProgressTaskForWorkflowInstance(workflowId, taskName):
    """Get a Conductor Task Instance information with given workflowId and task name
        Will invoke GET request with format http://<ip>:<port>/api/tasks/in_progress/<workflowId>/<taskName>
    """

    path = "/api/tasks/in_progress/" + workflowId + "/" + taskName
    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def batchPollTask(taskType, workerid=None, count=1, timeout=100):
    """This method will batch poll for a given task
        Will invoke GET request with format http://<ip>:<port>/api/tasks/poll/batch/<taskType>?workerid=<workerid>&count=<count>&timeout=<timeout>
    """
    parameterString = "?"
    if workerid != None:
        parameterString += "workerid=" + workerid
        parameterString += "&"

    parameterString += "count=" + str(count)
    parameterString += "&timeout=" + str(timeout)

    path = "/api/tasks/poll/batch/" + taskType + parameterString
    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def pollTask(taskType, workerid=None):
    """This method will poll for a given task
        Will invoke GET request with format http://<ip>:<port>/api/tasks/poll/<taskType>?workerid=<workerid>&count=<count>&timeout=<timeout>
    """
    path = "/api/tasks/poll/" + taskType
    if workerid != None:
        path += "?workerid=" + workerid

    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def getTasksQueue():
    """Get details about each queue
        Will invoke GET request with format http://<ip>:<port>/api/tasks/queue/all
    """

    path = "/api/tasks/queue/all"
    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def getTasksQueueVerbose():
    """Get verbose details about each queue
        Will invoke GET request with format http://<ip>:<port>/api/tasks/queue/all/verbose
    """

    path = "/api/tasks/queue/all/verbose"
    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def requeueAllPendingTasks():
    """Requeue pending tasks for all the running workflows
        Will invoke POST request with format http://<ip>:<port>/api/tasks/queue/requeue
        Returns workflow instance id
    """

    path = "/api/tasks/queue/requeue"
    response, responseData = httpPost(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def requeuePendingTasks(taskType):
    """Requeue pending tasks for taskType
        Will invoke POST request with format http://<ip>:<port>/api/tasks/queue/requeue/<taskType>
        Returns workflow instance id
    """

    path = "/api/tasks/queue/requeue/" + taskType
    response, responseData = httpPost(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def getTaskTypeQueueSizes(body):
    """Create Workflow definition of metadata passed in
        Will invoke POST request with format http://<ip>:<port>/api/tasks/queue/sizes
    """

    path = "/api/tasks/queue/sizes"
    response, responseData = httpPost(path, body)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def deleteTaskFromQueue(taskType, taskId):
    """Delete Task of taskType with taskId from queue
        Will invoke DELETE request with format http://<ip>:<port>/api/tasks/queue/<tasktype>/<taskId>
    """

    path = "/api/tasks/queue/" + taskType + "/" + taskId
    response, responseData = httpDelete(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def getTask(taskId):
    """Get Task Instance of taskId passed in
        Will invoke GET request with format http://<ip>:<port>/api/tasks/<taskId>
    """

    path = "/api/tasks/" + taskId
    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def ackTask(taskId, workerid=None):
    """This method will ack a given task
        Will invoke POST request with format http://<ip>:<port>/api/tasks/<taskId>/ack?workerid=<workerid>
    """
    path = "/api/tasks/" + taskId + "/ack"
    if workerid != None:
        path += "?workerid=" + workerid

    response, responseData = httpPost(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

#########################################################################################
# Workflow Management #                                                                 #
#########################################################################################

def startDecision(workflowId):
    """Start Decision Task for a workflow with given id
        Will invoke PUT request with format http://<ip>:<port>/api/workflow/decide/<workflowId>
    """

    path = "/api/workflow/decide/" + workflowId
    response, responseData = httpPut(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def getRunningWorkflows(name, version=1, startTime=None, endTime=None):
    """Retrieve all the running workflows with a given name
        Will invoke GET request with format http://<ip>:<port>/api/workflow/running/<name>?version=<version>&startTime=<startTime>&endTime=<endTime>
    """

    parameterString = "?"
    if startTime != None:
        parameterString += "startTime=" + str(startTime)
        parameterString += "&"

    if endTime != None:
        parameterString += "endTime=" + str(endTime)
        parameterString += "&"

    parameterString += "version=" + str(version)

    path = "/api/workflow/running/" + name + parameterString
    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def searchWorkflows(start=None, size=100, sort=None, freeText='*', query=None):
    """Search for workloads based on parameters
        Will invoke GET request with format http://<ip>:<port>/api/workflow/search?start=<start>&size=<size>&sort=<sort>&freeText=<freeText>&query=<query>
    """

    parameterString = "?"
    if start != None:
        parameterString += "start=" + str(start)
        parameterString += "&"

    if sort != None:
        parameterString += "sort=" + sort
        parameterString += "&"

    if query != None:
        parameterString += "query=" + query
        parameterString += "&"

    parameterString += "size=" + str(size)
    parameterString += "freeText=" + freeText

    path = "/api/workflow/search" + parameterString
    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def startWorkflow(name, version=None, correlationId=None, body=None):
    """Start a Conductor Workflow with given name
        Will invoke POST request with format http://<ip>:<port>/api/workflow/<name>?version=<version>&correlationId=<correlationId>
        Returns workflow instance id
    """

    parameterString = "?"
    if version != None:
        parameterString += "version=" + str(version)
        parameterString += "&"

    if correlationId != None:
        parameterString += "sort=" + correlationId
        parameterString += "&"

    if body == None:
        body = '{}'

    path = "/api/workflow/" + name + parameterString
    response, responseData = httpPost(path, body)
    workflowInstanceId = None
    
    if response.status >= 200 and response.status < 300:
        workflowInstanceId = responseData

    return workflowInstanceId

def getWorkflowByCorrelationId(name, correlationId, includeClosed='false', includeTasks='false'):
    """Retrieve workflows with name for given correlationId
        Will invoke GET request with format http://<ip>:<port>/api/workflow/<name>/correlated/<correlationId>?includeClosed=<includeClosed>&includeTasks=<includeTasks>
    """

    parameterString = "?includeClosed=" + includeClosed
    parameterString += "&includeTasks=" + includeTasks

    path = "/api/workflow/" + name + "/correlated/" + correlationId + parameterString
    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def stopWorkflow(workflowId, reason=None):
    """Terminate/Stope Workflow of <workflowId> passed in
        Will invoke DELETE request with format http://<ip>:<port>/api/workflow/<workflowId>?reason=<reason>
    """

    path = "/api/workflow/" + workflowId

    if reason != None:
        path += "?reason=" + reason

    response, responseData = httpDelete(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def getWorkflow(workflowId, includeTasks='true'):
    """Get a Conductor Workflow Instance information with given workflowId
        Will invoke GET request with format http://<ip>:<port>/api/workflow/<workflowId>?includeTasks=<includeTasks>
    """

    path = "/api/workflow/" + workflowId + "?includeTasks=" + includeTasks
    response, responseData = httpGet(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def pauseWorkflow(workflowId):
    """Pause a Conductor Workflow Instance information with given workflowId
        Will invoke PUT request with format http://<ip>:<port>/api/workflow/<workflowId>/pause
    """

    path = "/api/workflow/" + workflowId + "/pause"
    response, responseData = httpPut(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def removeWorkflow(workflowId):
    """Remove a Conductor Workflow Instance information with given workflowId
        Will invoke DELETE request with format http://<ip>:<port>/api/workflow/<workflowId>/remove
    """

    path = "/api/workflow/" + workflowId + "/remove"
    response, responseData = httpDelete(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def rerunWorkflow(workflowId, body=None):
    """Rerun a Conductor Workflow from a specific task (passed in body)
        Will invoke POST request with format http://<ip>:<port>/api/workflow/<workflowId>/rerun
        Returns workflow instance id
    """
    if body == None:
        body = '{}'

    path = "/api/workflow/" + workflowId + "/rerun"
    response, responseData = httpPost(path, body)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def restartWorkflow(workflowId):
    """Restart a completed Conductor Workflow
        Will invoke POST request with format http://<ip>:<port>/api/workflow/<workflowId>/restart
        Returns workflow instance id
    """

    path = "/api/workflow/" + workflowId + "/restart"
    response, responseData = httpPost(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def resumeWorkflow(workflowId):
    """Resume a Conductor Workflow Instance information with given workflowId
        Will invoke PUT request with format http://<ip>:<port>/api/workflow/<workflowId>/resume
    """

    path = "/api/workflow/" + workflowId + "/resume"
    response, responseData = httpPut(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def retryWorkflow(workflowId):
    """Retries the last failed task of a Conductor Workflow
        Will invoke POST request with format http://<ip>:<port>/api/workflow/<workflowId>/retry
        Returns workflow instance id
    """

    path = "/api/workflow/" + workflowId + "/retry"
    response, responseData = httpPost(path)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON

def skipWorkflowTask(workflowId, taskReferenceName, body=None):
    """Skip a given task from a current running Conductor Workflow
        Will invoke PUT request with format http://<ip>:<port>/api/workflow/<workflowId>/skiptask/<taskReferenceName>
        Returns workflow instance id
    """
    if body == None:
        body = '{}'

    path = "/api/workflow/" + workflowId + "/skiptask/" + taskReferenceName
    response, responseData = httpPut(path, body)
    responseJSON = None
    
    if response.status >= 200 and response.status < 300:
        responseJSON = responseData

    return responseJSON


#########################################################################################
# Argument Parsing #                                                                    #
#########################################################################################

def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
         raise argparse.ArgumentTypeError("%s is not a valid positive integer value" % value)
    return ivalue

parser = argparse.ArgumentParser(description="Execute Swagger API to Conductor Server.", add_help=False)
parser.add_argument('--ip', help='IP Address of Conductor Server')
parser.add_argument('--port', help='Port of Conductor Server')
parser.add_argument('command',
                    nargs="?",
                    choices=['getAllEventHandlers', 'getEventHandler', 'createEventHandler', 'modifyEventHandler', 'deleteEventHandler', 'getEventExecutions', 'getRegisteredQueues', 'getRegisteredQueueProviders',
                    'getAllTaskMetadata', 'createTaskMetadata', 'modifyTaskMetadata', 'deleteTaskMetadata', 'getTaskMetadata', 'getAllWorkflowMetadata', 'createWorkflowMetadata', 'modifyWorkflowMetadata', 'getWorkflowMetadata',
                    'getConfiguration', 'sweepWorkflow', 'getPendingTasks',
                    'updateTask', 'getInProgressTask', 'getInProgressTaskForWorkflowInstance', 'batchPollTask', 'pollTask', 'getTasksQueue', 'getTasksQueueVerbose', 'requeueAllPendingTasks', 'requeuePendingTasks', 'getTaskTypeQueueSizes', 'deleteTaskFromQueue', 'getTask', 'ackTask',
                    'startDecision', 'getRunningWorkflows', 'searchWorkflows', 'startWorkflow', 'getWorkflowByCorrelationId', 'stopWorkflow', 'getWorkflow', 'pauseWorkflow', 'removeWorkflow', 'rerunWorkflow', 'restartWorkflow', 'resumeWorkflow', 'retryWorkflow', 'skipWorkflowTask'],
                    help="Command to execute",
                    )
parser.add_argument('-h', '--help', action='store_true')
args, sub_args = parser.parse_known_args()

if len(sys.argv) < 3:
    print(parser.format_help())
    exit(1)

# Manually handle help
if args.help:
    # If no subcommand was specified, give general help
    if args.command is None: 
        print(parser.format_help())
        sys.exit(1)
    # Otherwise pass the help option on to the subcommand
    sub_args.append('--help')

if args.ip is not None:
    ip = args.ip

if args.port is not None:
    port = args.port

parser = argparse.ArgumentParser(prog="%s %s" % (os.path.basename(sys.argv[0]), args.command))

# Event Services #
if args.command == 'getAllEventHandlers':
    args = parser.parse_args(sub_args)
    getAllEventHandlers()

elif args.command == 'getEventHandler':
    parser.add_argument('event', help='Event Name')
    parser.add_argument('--activeOnly', choices=['true','false'], help='Query only if active {true | false} (default == true)')
    args = parser.parse_args(sub_args)
    if args.activeOnly == None:
        getEventHandler(args.event)
    else:
        getEventHandler(args.event, args.activeOnly)

elif args.command == 'createEventHandler':
    parser.add_argument('body', help='Event Handler definition in JSON')
    args = parser.parse_args(sub_args)
    createEventHandler(args.body)

elif args.command == 'modifyEventHandler':
    parser.add_argument('body', help='Event Handler definition in JSON')
    args = parser.parse_args(sub_args)
    modifyEventHandler(args.body)

elif args.command == 'deleteEventHandler':
    parser.add_argument('name', help='Event Name')
    args = parser.parse_args(sub_args)
    deleteEventHandler(args.name)

elif args.command == 'getEventExecutions':
    parser.add_argument('eventHandlerName', help='Event Handler Name')
    parser.add_argument('eventName', help='Event Name')
    parser.add_argument('messageId', help='Message Id')
    parser.add_argument('--max', type=positive_int, help='Max number to query (Positive integer value, default == 100)')
    args = parser.parse_args(sub_args)
    if args.max == None:
        getEventExecutions(args.eventHandlerName, args.eventName, args.messageId)
    else:
        getEventExecutions(args.eventHandlerName, args.eventName, args.messageId, args.max)

elif args.command == 'getRegisteredQueues':
    parser.add_argument('--verbosity', choices=['true','false'], help="Verbosity {true | false} (default == false)")
    args = parser.parse_args(sub_args)
    if args.verbosity == None:
        getRegisteredQueues()
    else:
        getRegisteredQueues(args.verbosity)

elif args.command == 'getRegisteredQueueProviders':
    args = parser.parse_args(sub_args)
    getRegisteredQueueProviders()


# Metadata Management #
elif args.command == 'getAllTaskMetadata':
    args = parser.parse_args(sub_args)
    getAllTaskMetadata()

elif args.command == 'createTaskMetadata':
    parser.add_argument('metadata', help='Task Metadata definition(s) in JSON array')
    args = parser.parse_args(sub_args)
    createTaskMetadata(args.metadata)

elif args.command == 'modifyTaskMetadata':
    parser.add_argument('metadata', help='Task Metadata definition in JSON')
    args = parser.parse_args(sub_args)
    modifyTaskMetadata(args.metadata)

elif args.command == 'deleteTaskMetadata':
    parser.add_argument('taskType', help='Task Type (Name)')
    args = parser.parse_args(sub_args)
    deleteTaskMetadata(args.taskType)

elif args.command == 'getTaskMetadata':
    parser.add_argument('taskType', help='Task Type (Name)')
    args = parser.parse_args(sub_args)
    getTaskMetadata(args.taskType)

elif args.command == 'getAllWorkflowMetadata':
    args = parser.parse_args(sub_args)
    getAllWorkflowMetadata()

elif args.command == 'createWorkflowMetadata':
    parser.add_argument('metadata', help='Workflow Metadata definition in JSON')
    args = parser.parse_args(sub_args)
    createWorkflowMetadata(args.metadata)

elif args.command == 'modifyWorkflowMetadata':
    parser.add_argument('metadata', help='Workflow Metadata definition in JSON')
    args = parser.parse_args(sub_args)
    modifyWorkflowMetadata(args.metadata)

elif args.command == 'getWorkflowMetadata':
    parser.add_argument('name', help='Workflow name')
    args = parser.parse_args(sub_args)
    getWorkflowMetadata(args.name)


# Admin #
elif args.command == 'getConfiguration':
    args = parser.parse_args(sub_args)
    getConfiguration()

elif args.command == 'sweepWorkflow':
    parser.add_argument('workflowId', help='Workflow Instance Id')
    args = parser.parse_args(sub_args)
    sweepWorkflow(args.workflowId)

elif args.command == 'getPendingTasks':
    parser.add_argument('taskType', help='Task Type (Name)')
    parser.add_argument('--start', type=positive_int, help='Start time (Positive integer value)')
    parser.add_argument('--count', type=positive_int, help='Query count (Positive integer value, default == 100)')
    args = parser.parse_args(sub_args)
    if args.count == None:
        getPendingTasks(args.taskType, start=args.start)
    else:
        getPendingTasks(args.taskType, start=args.start, count=args.count)
           
# Task Managment #  
elif args.command == 'updateTask':
    parser.add_argument('body', help='Task information in JSON')
    args = parser.parse_args(sub_args)
    updateTask(args.body)

elif args.command == 'getInProgressTask':
    parser.add_argument('taskType', help='Task Type (Name)')
    parser.add_argument('--startKey', help='Start Key (String)')
    parser.add_argument('--count', type=positive_int, help='Query count (Positive integer value, default == 100)')
    args = parser.parse_args(sub_args)
    if args.count == None:
        getInProgressTask(args.taskType, startKey=args.startKey)
    else:
        getInProgressTask(args.taskType, startKey=args.startKey, count=args.count)

elif args.command == 'getInProgressTaskForWorkflowInstance':
    parser.add_argument('workflowInstanceId', help='Workflow Instance Id')
    parser.add_argument('taskRefName', help='Task Reference Name')
    args = parser.parse_args(sub_args)
    getInProgressTaskForWorkflowInstance(args.workflowInstanceId, args.taskRefName)

elif args.command == 'batchPollTask':
    parser.add_argument('taskType', help='Task Type (Name)')
    parser.add_argument('--workerid', help="Id of Worker (String)")
    parser.add_argument('--count', type=positive_int, help='Query count (Positive integer value, default == 1)')
    parser.add_argument('--timeout', type=positive_int, help='Timeout Value (Positive integer value, default == 100)')
    args = parser.parse_args(sub_args)
    if args.count == None and args.timeout == None:
        batchPollTask(args.taskType, workerid=args.workerid)
    else:
        if args.count != None and args.timeout != None:
            batchPollTask(args.taskType, workerid=args.workerid, count=args.count, timeout=args.timeout)
        elif args.count == None and args.timeout != None:
            batchPollTask(args.taskType, workerid=args.workerid, timeout=args.timeout)
        elif args.count != None and args.timeout == None:
            batchPollTask(args.taskType, workerid=args.workerid, count=args.count)

elif args.command == 'pollTask':
    parser.add_argument('taskType', help='Task Type (Name)')
    parser.add_argument('--workerid', help="Id of Worker (String)")
    args = parser.parse_args(sub_args)
    pollTask(args.taskType, args.workerid)

elif args.command == 'getTasksQueue':
    args = parser.parse_args(sub_args)
    getTasksQueue()

elif args.command == 'getTasksQueueVerbose':
    args = parser.parse_args(sub_args)
    getTasksQueueVerbose()

elif args.command == 'requeueAllPendingTasks':
    args = parser.parse_args(sub_args)
    requeueAllPendingTasks()

elif args.command == 'requeuePendingTasks':
    parser.add_argument('taskType', help='Task Type (Name)')
    args = parser.parse_args(sub_args)
    requeuePendingTasks(args.taskType)

elif args.command == 'getTaskTypeQueueSizes':
    parser.add_argument('body', help='Body in JSON array')
    args = parser.parse_args(sub_args)
    getTaskTypeQueueSizes(args.body)

elif args.command == 'deleteTaskFromQueue':
    parser.add_argument('taskType', help='Task Type (Name)')
    parser.add_argument('taskId', help='Task Instance Id')
    args = parser.parse_args(sub_args)
    deleteTaskFromQueue(args.taskType, args.taskId)

elif args.command == 'getTask':
    parser.add_argument('taskId', help='Task Instance Id')
    args = parser.parse_args(sub_args)
    getTask(args.taskId)

elif args.command == 'ackTask':
    parser.add_argument('taskId', help='Task Instance Id')
    parser.add_argument('--workerid', help="Id of Worker (String)")
    args = parser.parse_args(sub_args)
    ackTask(args.taskId, args.workerid)

# Workflow Managment #  
elif args.command == 'startDecision':
    parser.add_argument('workflowId', help='Workflow Instance Id')
    args = parser.parse_args(sub_args)
    startDecision(args.workflowId)

elif args.command == 'getRunningWorkflows':
    parser.add_argument('name', help='Workflow Name')
    parser.add_argument('--version', type=positive_int, help='Workflow Version (Positive integer value, default == 1)')
    parser.add_argument('--startTime', help='Start Time (Long value)')
    parser.add_argument('--endTime', help='End Time (Long value)')
    args = parser.parse_args(sub_args)
    if args.version == None:
        getRunningWorkflows(args.name, startTime=args.startTime, endTime=args.endTime)
    else:
        getRunningWorkflows(args.name, startTime=args.startTime, endTime=args.endTime, version=args.version)

elif args.command == 'searchWorkflows':
    parser.add_argument('--start', type=positive_int, help='Start Time (Positive integer value)')    
    parser.add_argument('--size', type=positive_int, help='Size (Positive integer value, default == 100)')
    parser.add_argument('--sort', choices=['ASC', 'DESC'], help='Sort ascending (ASC) or descending (DESC)')
    parser.add_argument('--freeText', help='Free Text (String value, default == *)')
    parser.add_argument('--query', help='Query (String value)')
    args = parser.parse_args(sub_args)
    if args.size == None and args.freeText == None:
        searchWorkflows(start=args.start, sort=args.sort, query=args.query)
    else:
        if args.size != None and args.freeText != None:
            searchWorkflows(start=args.start, sort=args.sort, query=args.query, size=args.size, freeText=args.freeText)
        elif args.size == None and args.freeText != None:
            searchWorkflows(start=args.start, sort=args.sort, query=args.query, freeText=args.freeText)
        elif args.size != None and args.freeText == None:
            searchWorkflows(start=args.start, sort=args.sort, query=args.query, size=args.size)

elif args.command == 'startWorkflow':
    parser.add_argument('name', help='Workflow Name')
    parser.add_argument('--version', type=positive_int, help='Workflow Version (Positiive integer value, default == 1)')
    parser.add_argument('--correlationId', help='Correlation Id (String value)')
    parser.add_argument('--body', help='Parameters in JSON format')
    args = parser.parse_args(sub_args)
    startWorkflow(args.name, version=args.version, correlationId=args.correlationId, body=args.body)

elif args.command == 'getWorkflowByCorrelationId':
    parser.add_argument('name', help='Workflow Name')
    parser.add_argument('correlationId', help='Correlation Id (String value)')
    parser.add_argument('--includeClosed', choices=['true','false'], help='Include Closed (Boolean value, default == false)')
    parser.add_argument('--includeTasks', choices=['true','false'], help='Include Tasks (Boolean value, default == false)')
    args = parser.parse_args(sub_args)
    if args.includeClosed == None and args.includeTasks == None:
        getWorkflowByCorrelationId(args.name, args.correlationId)
    else:
        if args.includeClosed != None and args.includeTasks != None:
            getWorkflowByCorrelationId(args.name, args.correlationId, includeClosed=args.includeClosed, includeTasks=args.includeTasks)
        elif args.includeClosed == None and args.includeTasks != None:
            getWorkflowByCorrelationId(args.name, args.correlationId, includeTasks=args.includeTasks)
        elif args.includeClosed != None and args.includeTasks == None:
            getWorkflowByCorrelationId(args.name, args.correlationId, includeClosed=args.includeClosed)

elif args.command == 'stopWorkflow':
    parser.add_argument('workflowId', help='Workflow Instance Id')
    parser.add_argument('--reason', help='Reason of termination (String value)')
    args = parser.parse_args(sub_args)
    stopWorkflow(args.workflowId, args.reason)

elif args.command == 'getWorkflow':
    parser.add_argument('workflowId', help='Workflow Instance Id')
    parser.add_argument('--includeTasks', choices=['true','false'], help='Include Tasks (Boolean value, default == true)')
    args = parser.parse_args(sub_args)
    if args.includeTasks == None:
        getWorkflow(args.workflowId)
    else:
        getWorkflow(args.workflowId, args.includeTasks)

elif args.command == 'pauseWorkflow':
    parser.add_argument('workflowId', help='Workflow Instance Id')
    args = parser.parse_args(sub_args)
    pauseWorkflow(args.workflowId)

elif args.command == 'removeWorkflow':
    parser.add_argument('workflowId', help='Workflow Instance Id')
    args = parser.parse_args(sub_args)
    removeWorkflow(args.workflowId)

elif args.command == 'rerunWorkflow':
    parser.add_argument('workflowId', help='Workflow Instance Id')
    parser.add_argument('--body', help='Parameters in JSON format {"reRunFromWorkflowId":"string", "workflowInput":{}, "reRunFromTaskId":"string", "taskInput":{}, "correlationId":"string"')
    args = parser.parse_args(sub_args)
    rerunWorkflow(args.workflowId, body=args.body)

elif args.command == 'restartWorkflow':
    parser.add_argument('workflowId', help='Workflow Instance Id')
    args = parser.parse_args(sub_args)
    restartWorkflow(args.workflowId)

elif args.command == 'resumeWorkflow':
    parser.add_argument('workflowId', help='Workflow Instance Id')
    args = parser.parse_args(sub_args)
    resumeWorkflow(args.workflowId)

elif args.command == 'retryWorkflow':
    parser.add_argument('workflowId', help='Workflow Instance Id')
    args = parser.parse_args(sub_args)
    retryWorkflow(args.workflowId)

elif args.command == 'skipWorkflowTask':
    parser.add_argument('workflowId', help='Workflow Instance Id')
    parser.add_argument('taskReferenceName', help='Task Reference Name')
    parser.add_argument('--body', help='Parameters in JSON format {"taskInput":{}, "taskOutput":{}')
    args = parser.parse_args(sub_args)
    skipWorkflowTask(args.workflowId, args.taskReferenceName, body=args.body)

