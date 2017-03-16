# conductor-tools
Tools to integrate with Netflix Conductor Workflow Engine

Netflix Conductor Engine:
Documentation: https://netflix.github.io/conductor/
github repo: https://github.com/Netflix/conductor

conductor.py is a python script to invoke the Conductor Server swagger REST API's.

python conductor.py
usage: conductor.py [--ip IP] [--port PORT] [-h]

                    [{getAllEventHandlers,getEventHandler,createEventHandler,modifyEventHandler,deleteEventHandler,getEventExecutions,getRegisteredQueues,getRegisteredQueueProviders,getAllTaskMetadata,createTaskMetadata,modifyTaskMetadata,deleteTaskMetadata,getTaskMetadata,getAllWorkflowMetadata,createWorkflowMetadata,modifyWorkflowMetadata,getWorkflowMetadata,getConfiguration,sweepWorkflow,getPendingTasks,updateTask,getInProgressTask,getInProgressTaskForWorkflowInstance,batchPollTask,pollTask,getTasksQueue,getTasksQueueVerbose,requeueAllPendingTasks,requeuePendingTasks,getTaskTypeQueueSizes,deleteTaskFromQueue,getTask,ackTask,startDecision,getRunningWorkflows,searchWorkflows,startWorkflow,getWorkflowByCorrelationId,stopWorkflow,getWorkflow,pauseWorkflow,removeWorkflow,rerunWorkflow,restartWorkflow,resumeWorkflow,retryWorkflow,skipWorkflowTask}]

Execute Swagger API to Conductor Server.

positional arguments:
  {getAllEventHandlers,getEventHandler,createEventHandler,modifyEventHandler,deleteEventHandler,getEventExecutions,getRegisteredQueues,getRegisteredQueueProviders,getAllTaskMetadata,createTaskMetadata,modifyTaskMetadata,deleteTaskMetadata,getTaskMetadata,getAllWorkflowMetadata,createWorkflowMetadata,modifyWorkflowMetadata,getWorkflowMetadata,getConfiguration,sweepWorkflow,getPendingTasks,updateTask,getInProgressTask,getInProgressTaskForWorkflowInstance,batchPollTask,pollTask,getTasksQueue,getTasksQueueVerbose,requeueAllPendingTasks,requeuePendingTasks,getTaskTypeQueueSizes,deleteTaskFromQueue,getTask,ackTask,startDecision,getRunningWorkflows,searchWorkflows,startWorkflow,getWorkflowByCorrelationId,stopWorkflow,getWorkflow,pauseWorkflow,removeWorkflow,rerunWorkflow,restartWorkflow,resumeWorkflow,retryWorkflow,skipWorkflowTask}
                        Command to execute

optional arguments:
  --ip IP               IP Address of Conductor Server
  --port PORT           Port of Conductor Server
  -h, --help
  


For any specific command, the -h or --help can be used for help:
  
python conductor.py startWorkflow --help
usage: conductor.py startWorkflow [-h] [--version VERSION]
                                  [--correlationId CORRELATIONID]
                                  [--body BODY]
                                  name

positional arguments:
  name                  Workflow Name

optional arguments:
  -h, --help            show this help message and exit
  --version VERSION     Workflow Version (Positiive integer value, default ==
                        1)
  --correlationId CORRELATIONID
                        Correlation Id (String value)
  --body BODY           Parameters in JSON format
  






Example usage:
$ python conductor.py startWorkflow corey_flow_1 --ip localhost --port 8080
Sending [POST] request to Conductor Server (http://localhost:8080/api/workflow/corey_flow_1?):
Body:
{}


Received response from Conductor Server (localhost):
Status: 200
24f7b62e-16d1-4f76-b807-3641c1faa881
  
