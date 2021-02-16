"""
# Tasks for AWS Step Functions

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

[AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) is a web service that enables you to coordinate the
components of distributed applications and microservices using visual workflows.
You build applications from individual components that each perform a discrete
function, or task, allowing you to scale and change applications quickly.

A [Task](https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-task-state.html) state represents a single unit of work performed by a state machine.
All work in your state machine is performed by tasks.

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## Table Of Contents

* [Task](#task)
* [Paths](#paths)

  * [InputPath](#inputpath)
  * [OutputPath](#outputpath)
  * [ResultPath](#resultpath)
* [Parameters](#task-parameters-from-the-state-json)
* [Evaluate Expression](#evaluate-expression)
* [Athena](#athena)

  * [StartQueryExecution](#startQueryExecution)
  * [GetQueryExecution](#getQueryExecution)
  * [GetQueryResults](#getQueryResults)
  * [StopQueryExecution](#stopQueryExecution)
* [Batch](#batch)

  * [SubmitJob](#submitjob)
* [CodeBuild](#codebuild)

  * [StartBuild](#startbuild)
* [DynamoDB](#dynamodb)

  * [GetItem](#getitem)
  * [PutItem](#putitem)
  * [DeleteItem](#deleteitem)
  * [UpdateItem](#updateitem)
* [ECS](#ecs)

  * [RunTask](#runtask)

    * [EC2](#ec2)
    * [Fargate](#fargate)
* [EMR](#emr)

  * [Create Cluster](#create-cluster)
  * [Termination Protection](#termination-protection)
  * [Terminate Cluster](#terminate-cluster)
  * [Add Step](#add-step)
  * [Cancel Step](#cancel-step)
  * [Modify Instance Fleet](#modify-instance-fleet)
  * [Modify Instance Group](#modify-instance-group)
* [Glue](#glue)
* [Glue DataBrew](#glue-databrew)
* [Lambda](#lambda)
* [SageMaker](#sagemaker)

  * [Create Training Job](#create-training-job)
  * [Create Transform Job](#create-transform-job)
  * [Create Endpoint](#create-endpoint)
  * [Create Endpoint Config](#create-endpoint-config)
  * [Create Model](#create-model)
  * [Update Endpoint](#update-endpoint)
* [SNS](#sns)
* [Step Functions](#step-functions)

  * [Start Execution](#start-execution)
  * [Invoke Activity Worker](#invoke-activity)
* [SQS](#sqs)

## Task

A Task state represents a single unit of work performed by a state machine. In the
CDK, the exact work to be done is determined by a class that implements `IStepFunctionsTask`.

AWS Step Functions [integrates](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-service-integrations.html) with some AWS services so that you can call API
actions, and coordinate executions directly from the Amazon States Language in
Step Functions. You can directly call and pass parameters to the APIs of those
services.

## Paths

In the Amazon States Language, a [path](https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-paths.html) is a string beginning with `$` that you
can use to identify components within JSON text.

Learn more about input and output processing in Step Functions [here](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-input-output-filtering.html)

### InputPath

Both `InputPath` and `Parameters` fields provide a way to manipulate JSON as it
moves through your workflow. AWS Step Functions applies the `InputPath` field first,
and then the `Parameters` field. You can first filter your raw input to a selection
you want using InputPath, and then apply Parameters to manipulate that input
further, or add new values. If you don't specify an `InputPath`, a default value
of `$` will be used.

The following example provides the field named `input` as the input to the `Task`
state that runs a Lambda function.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
submit_job = tasks.LambdaInvoke(stack, "Invoke Handler",
    lambda_function=submit_job_lambda,
    input_path="$.input"
)
```

### OutputPath

Tasks also allow you to select a portion of the state output to pass to the next
state. This enables you to filter out unwanted information, and pass only the
portion of the JSON that you care about. If you don't specify an `OutputPath`,
a default value of `$` will be used. This passes the entire JSON node to the next
state.

The [response](https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html#API_Invoke_ResponseSyntax) from a Lambda function includes the response from the function
as well as other metadata.

The following example assigns the output from the Task to a field named `result`

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
submit_job = tasks.LambdaInvoke(stack, "Invoke Handler",
    lambda_function=submit_job_lambda,
    output_path="$.Payload.result"
)
```

### ResultPath

The output of a state can be a copy of its input, the result it produces (for
example, output from a Task state’s Lambda function), or a combination of its
input and result. Use [`ResultPath`](https://docs.aws.amazon.com/step-functions/latest/dg/input-output-resultpath.html) to control which combination of these is
passed to the state output. If you don't specify an `ResultPath`, a default
value of `$` will be used.

The following example adds the item from calling DynamoDB's `getItem` API to the state
input and passes it to the next state.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
tasks.DynamoGetItem(self, "PutItem",
    item={"MessageId": {"s": "12345"}},
    table_name="my-table",
    result_path="$.Item"
)
```

⚠️ The `OutputPath` is computed after applying `ResultPath`. All service integrations
return metadata as part of their response. When using `ResultPath`, it's not possible to
merge a subset of the task output to the input.

## Task parameters from the state JSON

Most tasks take parameters. Parameter values can either be static, supplied directly
in the workflow definition (by specifying their values), or a value available at runtime
in the state machine's execution (either as its input or an output of a prior state).
Parameter values available at runtime can be specified via the `JsonPath` class,
using methods such as `JsonPath.stringAt()`.

The following example provides the field named `input` as the input to the Lambda function
and invokes it asynchronously.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
submit_job = tasks.LambdaInvoke(stack, "Invoke Handler",
    lambda_function=submit_job_lambda,
    payload=sfn.JsonPath.StringAt("$.input"),
    invocation_type=tasks.InvocationType.EVENT
)
```

Each service integration has its own set of parameters that can be supplied.

## Evaluate Expression

Use the `EvaluateExpression` to perform simple operations referencing state paths. The
`expression` referenced in the task will be evaluated in a Lambda function
(`eval()`). This allows you to not have to write Lambda code for simple operations.

Example: convert a wait time from milliseconds to seconds, concat this in a message and wait:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
convert_to_seconds = tasks.EvaluateExpression(self, "Convert to seconds",
    expression="$.waitMilliseconds / 1000",
    result_path="$.waitSeconds"
)

create_message = tasks.EvaluateExpression(self, "Create message",
    # Note: this is a string inside a string.
    expression="`Now waiting ${$.waitSeconds} seconds...`",
    runtime=lambda_.Runtime.NODEJS_10_X,
    result_path="$.message"
)

publish_message = tasks.SnsPublish(self, "Publish message",
    topic=topic,
    message=sfn.TaskInput.from_data_at("$.message"),
    result_path="$.sns"
)

wait = sfn.Wait(self, "Wait",
    time=sfn.WaitTime.seconds_path("$.waitSeconds")
)

sfn.StateMachine(self, "StateMachine",
    definition=convert_to_seconds.next(create_message).next(publish_message).next(wait)
)
```

The `EvaluateExpression` supports a `runtime` prop to specify the Lambda
runtime to use to evaluate the expression. Currently, the only runtime
supported is `lambda.Runtime.NODEJS_10_X`.

## Athena

Step Functions supports [Athena](https://docs.aws.amazon.com/step-functions/latest/dg/connect-athena.html) through the service integration pattern.

### StartQueryExecution

The [StartQueryExecution](https://docs.aws.amazon.com/athena/latest/APIReference/API_StartQueryExecution.html) API runs the SQL query statement.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_stepfunctions as sfn
import ??? as tasks

start_query_execution_job = tasks.AthenaStartQueryExecution(stack, "Start Athena Query",
    query_string=sfn.JsonPath.string_at("$.queryString"),
    query_execution_context={
        "database": "mydatabase"
    },
    result_configuration={
        "encryption_configuration": {
            "encryption_option": tasks.EncryptionOption.S3_MANAGED
        },
        "output_location": sfn.JsonPath.string_at("$.outputLocation")
    }
)
```

### GetQueryExecution

The [GetQueryExecution](https://docs.aws.amazon.com/athena/latest/APIReference/API_GetQueryExecution.html) API gets information about a single execution of a query.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_stepfunctions as sfn
import ??? as tasks

get_query_execution_job = tasks.AthenaGetQueryExecution(stack, "Get Query Execution",
    query_execution_id=sfn.JsonPath.string_at("$.QueryExecutionId")
)
```

### GetQueryResults

The [GetQueryResults](https://docs.aws.amazon.com/athena/latest/APIReference/API_GetQueryResults.html) API that streams the results of a single query execution specified by QueryExecutionId from S3.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_stepfunctions as sfn
import ??? as tasks

get_query_results_job = tasks.AthenaGetQueryResults(stack, "Get Query Results",
    query_execution_id=sfn.JsonPath.string_at("$.QueryExecutionId")
)
```

### StopQueryExecution

The [StopQueryExecution](https://docs.aws.amazon.com/athena/latest/APIReference/API_StopQueryExecution.html) API that stops a query execution.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_stepfunctions as sfn
import ??? as tasks

stop_query_execution_job = tasks.AthenaStopQueryExecution(stack, "Stop Query Execution",
    query_execution_id=sfn.JsonPath.string_at("$.QueryExecutionId")
)
```

## Batch

Step Functions supports [Batch](https://docs.aws.amazon.com/step-functions/latest/dg/connect-batch.html) through the service integration pattern.

### SubmitJob

The [SubmitJob](https://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html) API submits an AWS Batch job from a job definition.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_batch as batch
import aws_cdk.aws_stepfunctions_tasks as tasks

batch_queue = batch.JobQueue(self, "JobQueue",
    compute_environments=[JobQueueComputeEnvironment(
        order=1,
        compute_environment=batch.ComputeEnvironment(self, "ComputeEnv",
            compute_resources=ComputeResources(vpc=vpc)
        )
    )
    ]
)

batch_job_definition = batch.JobDefinition(self, "JobDefinition",
    container=JobDefinitionContainer(
        image=ecs.ContainerImage.from_asset(path.resolve(__dirname, "batchjob-image"))
    )
)

task = tasks.BatchSubmitJob(self, "Submit Job",
    job_definition=batch_job_definition,
    job_name="MyJob",
    job_queue=batch_queue
)
```

## CodeBuild

Step Functions supports [CodeBuild](https://docs.aws.amazon.com/step-functions/latest/dg/connect-codebuild.html) through the service integration pattern.

### StartBuild

[StartBuild](https://docs.aws.amazon.com/codebuild/latest/APIReference/API_StartBuild.html) starts a CodeBuild Project by Project Name.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_stepfunctions_tasks as tasks
import aws_cdk.aws_stepfunctions as sfn

codebuild_project = codebuild.Project(stack, "Project",
    project_name="MyTestProject",
    build_spec=codebuild.BuildSpec.from_object({
        "version": "0.2",
        "phases": {
            "build": {
                "commands": ["echo \"Hello, CodeBuild!\""
                ]
            }
        }
    })
)

task = tasks.CodeBuildStartBuild(stack, "Task",
    project=codebuild_project,
    integration_pattern=sfn.IntegrationPattern.RUN_JOB,
    environment_variables_override={
        "ZONE": BuildEnvironmentVariable(
            type=codebuild.BuildEnvironmentVariableType.PLAINTEXT,
            value=sfn.JsonPath.string_at("$.envVariables.zone")
        )
    }
)
```

## DynamoDB

You can call DynamoDB APIs from a `Task` state.
Read more about calling DynamoDB APIs [here](https://docs.aws.amazon.com/step-functions/latest/dg/connect-ddb.html)

### GetItem

The [GetItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html) operation returns a set of attributes for the item with the given primary key.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
tasks.DynamoGetItem(self, "Get Item",
    key={"message_id": tasks.DynamoAttributeValue.from_string("message-007")},
    table=table
)
```

### PutItem

The [PutItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html) operation creates a new item, or replaces an old item with a new item.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
tasks.DynamoPutItem(self, "PutItem",
    item={
        "MessageId": tasks.DynamoAttributeValue.from_string("message-007"),
        "Text": tasks.DynamoAttributeValue.from_string(sfn.JsonPath.string_at("$.bar")),
        "TotalCount": tasks.DynamoAttributeValue.from_number(10)
    },
    table=table
)
```

### DeleteItem

The [DeleteItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_DeleteItem.html) operation deletes a single item in a table by primary key.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_stepfunctions as sfn
import aws_cdk.aws_stepfunctions_tasks as tasks

tasks.DynamoDeleteItem(self, "DeleteItem",
    key={"MessageId": tasks.DynamoAttributeValue.from_string("message-007")},
    table=table,
    result_path=sfn.JsonPath.DISCARD
)
```

### UpdateItem

The [UpdateItem](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html) operation edits an existing item's attributes, or adds a new item
to the table if it does not already exist.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
tasks.DynamoUpdateItem(self, "UpdateItem",
    key={"MessageId": tasks.DynamoAttributeValue.from_string("message-007")},
    table=table,
    expression_attribute_values={
        ":val": tasks.DynamoAttributeValue.number_from_string(sfn.JsonPath.string_at("$.Item.TotalCount.N")),
        ":rand": tasks.DynamoAttributeValue.from_number(20)
    },
    update_expression="SET TotalCount = :val + :rand"
)
```

## ECS

Step Functions supports [ECS/Fargate](https://docs.aws.amazon.com/step-functions/latest/dg/connect-ecs.html) through the service integration pattern.

### RunTask

[RunTask](https://docs.aws.amazon.com/step-functions/latest/dg/connect-ecs.html) starts a new task using the specified task definition.

#### EC2

The EC2 launch type allows you to run your containerized applications on a cluster
of Amazon EC2 instances that you manage.

When a task that uses the EC2 launch type is launched, Amazon ECS must determine where
to place the task based on the requirements specified in the task definition, such as
CPU and memory. Similarly, when you scale down the task count, Amazon ECS must determine
which tasks to terminate. You can apply task placement strategies and constraints to
customize how Amazon ECS places and terminates tasks. Learn more about [task placement](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement.html)

The latest ACTIVE revision of the passed task definition is used for running the task.

The following example runs a job from a task definition on EC2

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_stepfunctions_tasks as tasks
import aws_cdk.aws_stepfunctions as sfn

vpc = ec2.Vpc.from_lookup(stack, "Vpc",
    is_default=True
)

cluster = ecs.Cluster(stack, "Ec2Cluster", vpc=vpc)
cluster.add_capacity("DefaultAutoScalingGroup",
    instance_type=ec2.InstanceType("t2.micro"),
    vpc_subnets=SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
)

task_definition = ecs.TaskDefinition(stack, "TD",
    compatibility=ecs.Compatibility.EC2
)

task_definition.add_container("TheContainer",
    image=ecs.ContainerImage.from_registry("foo/bar"),
    memory_limit_mi_b=256
)

run_task = tasks.EcsRunTask(stack, "Run",
    integration_pattern=sfn.IntegrationPattern.RUN_JOB,
    cluster=cluster,
    task_definition=task_definition,
    launch_target=tasks.EcsEc2LaunchTarget(
        placement_strategies=[
            ecs.PlacementStrategy.spread_across_instances(),
            ecs.PlacementStrategy.packed_by_cpu(),
            ecs.PlacementStrategy.randomly()
        ],
        placement_constraints=[
            ecs.PlacementConstraint.member_of("blieptuut")
        ]
    )
)
```

#### Fargate

AWS Fargate is a serverless compute engine for containers that works with Amazon
Elastic Container Service (ECS). Fargate makes it easy for you to focus on building
your applications. Fargate removes the need to provision and manage servers, lets you
specify and pay for resources per application, and improves security through application
isolation by design. Learn more about [Fargate](https://aws.amazon.com/fargate/)

The Fargate launch type allows you to run your containerized applications without the need
to provision and manage the backend infrastructure. Just register your task definition and
Fargate launches the container for you. The latest ACTIVE revision of the passed
task definition is used for running the task. Learn more about
[Fargate Versioning](https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_DescribeTaskDefinition.html)

The following example runs a job from a task definition on Fargate

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_ecs as ecs
import aws_cdk.aws_stepfunctions_tasks as tasks
import aws_cdk.aws_stepfunctions as sfn

vpc = ec2.Vpc.from_lookup(stack, "Vpc",
    is_default=True
)

cluster = ecs.Cluster(stack, "FargateCluster", vpc=vpc)

task_definition = ecs.TaskDefinition(stack, "TD",
    memory_mi_b="512",
    cpu="256",
    compatibility=ecs.Compatibility.FARGATE
)

container_definition = task_definition.add_container("TheContainer",
    image=ecs.ContainerImage.from_registry("foo/bar"),
    memory_limit_mi_b=256
)

run_task = tasks.EcsRunTask(stack, "RunFargate",
    integration_pattern=sfn.IntegrationPattern.RUN_JOB,
    cluster=cluster,
    task_definition=task_definition,
    assign_public_ip=True,
    container_overrides=[ContainerOverride(
        container_definition=container_definition,
        environment=[TaskEnvironmentVariable(name="SOME_KEY", value=sfn.JsonPath.string_at("$.SomeKey"))]
    )],
    launch_target=tasks.EcsFargateLaunchTarget()
)
```

## EMR

Step Functions supports Amazon EMR through the service integration pattern.
The service integration APIs correspond to Amazon EMR APIs but differ in the
parameters that are used.

[Read more](https://docs.aws.amazon.com/step-functions/latest/dg/connect-emr.html) about the differences when using these service integrations.

### Create Cluster

Creates and starts running a cluster (job flow).
Corresponds to the [`runJobFlow`](https://docs.aws.amazon.com/emr/latest/APIReference/API_RunJobFlow.html) API in EMR.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster_role = iam.Role(stack, "ClusterRole",
    assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
)

service_role = iam.Role(stack, "ServiceRole",
    assumed_by=iam.ServicePrincipal("elasticmapreduce.amazonaws.com")
)

auto_scaling_role = iam.Role(stack, "AutoScalingRole",
    assumed_by=iam.ServicePrincipal("elasticmapreduce.amazonaws.com")
)

auto_scaling_role.assume_role_policy.add_statements(
    iam.PolicyStatement(
        effect=iam.Effect.ALLOW,
        principals=[
            iam.ServicePrincipal("application-autoscaling.amazonaws.com")
        ],
        actions=["sts:AssumeRole"
        ]
    ))

tasks.EmrCreateCluster(stack, "Create Cluster",
    instances={},
    cluster_role=cluster_role,
    name=sfn.TaskInput.from_data_at("$.ClusterName").value,
    service_role=service_role,
    auto_scaling_role=auto_scaling_role,
    integration_pattern=sfn.ServiceIntegrationPattern.FIRE_AND_FORGET
)
```

### Termination Protection

Locks a cluster (job flow) so the EC2 instances in the cluster cannot be
terminated by user intervention, an API call, or a job-flow error.

Corresponds to the [`setTerminationProtection`](https://docs.aws.amazon.com/step-functions/latest/dg/connect-emr.html) API in EMR.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
tasks.EmrSetClusterTerminationProtection(stack, "Task",
    cluster_id="ClusterId",
    termination_protected=False
)
```

### Terminate Cluster

Shuts down a cluster (job flow).
Corresponds to the [`terminateJobFlows`](https://docs.aws.amazon.com/emr/latest/APIReference/API_TerminateJobFlows.html) API in EMR.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
tasks.EmrTerminateCluster(stack, "Task",
    cluster_id="ClusterId"
)
```

### Add Step

Adds a new step to a running cluster.
Corresponds to the [`addJobFlowSteps`](https://docs.aws.amazon.com/emr/latest/APIReference/API_AddJobFlowSteps.html) API in EMR.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
tasks.EmrAddStep(stack, "Task",
    cluster_id="ClusterId",
    name="StepName",
    jar="Jar",
    action_on_failure=tasks.ActionOnFailure.CONTINUE
)
```

### Cancel Step

Cancels a pending step in a running cluster.
Corresponds to the [`cancelSteps`](https://docs.aws.amazon.com/emr/latest/APIReference/API_CancelSteps.html) API in EMR.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
tasks.EmrCancelStep(stack, "Task",
    cluster_id="ClusterId",
    step_id="StepId"
)
```

### Modify Instance Fleet

Modifies the target On-Demand and target Spot capacities for the instance
fleet with the specified InstanceFleetName.

Corresponds to the [`modifyInstanceFleet`](https://docs.aws.amazon.com/emr/latest/APIReference/API_ModifyInstanceFleet.html) API in EMR.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
sfn.EmrModifyInstanceFleetByName(stack, "Task",
    cluster_id="ClusterId",
    instance_fleet_name="InstanceFleetName",
    target_on_demand_capacity=2,
    target_spot_capacity=0
)
```

### Modify Instance Group

Modifies the number of nodes and configuration settings of an instance group.

Corresponds to the [`modifyInstanceGroups`](https://docs.aws.amazon.com/emr/latest/APIReference/API_ModifyInstanceGroups.html) API in EMR.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
tasks.EmrModifyInstanceGroupByName(stack, "Task",
    cluster_id="ClusterId",
    instance_group_name=sfn.JsonPath.string_at("$.InstanceGroupName"),
    instance_group={
        "instance_count": 1
    }
)
```

## Glue

Step Functions supports [AWS Glue](https://docs.aws.amazon.com/step-functions/latest/dg/connect-glue.html) through the service integration pattern.

You can call the [`StartJobRun`](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-jobs-runs.html#aws-glue-api-jobs-runs-StartJobRun) API from a `Task` state.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
GlueStartJobRun(stack, "Task",
    glue_job_name="my-glue-job",
    arguments={
        "key": "value"
    },
    timeout=cdk.Duration.minutes(30),
    notify_delay_after=cdk.Duration.minutes(5)
)
```

## Glue DataBrew

Step Functions supports [AWS Glue DataBrew](https://docs.aws.amazon.com/step-functions/latest/dg/connect-databrew.html) through the service integration pattern.

You can call the [`StartJobRun`](https://docs.aws.amazon.com/databrew/latest/dg/API_StartJobRun.html) API from a `Task` state.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
GlueDataBrewStartJobRun(stack, "Task",
    Name="databrew-job"
)
```

## Lambda

[Invoke](https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html) a Lambda function.

You can specify the input to your Lambda function through the `payload` attribute.
By default, Step Functions invokes Lambda function with the state input (JSON path '$')
as the input.

The following snippet invokes a Lambda Function with the state input as the payload
by referencing the `$` path.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_stepfunctions as sfn
import aws_cdk.aws_stepfunctions_tasks as tasks

my_lambda = lambda_.Function(self, "my sample lambda",
    code=Code.from_inline("exports.handler = async () => {\n    return {\n      statusCode: '200',\n      body: 'hello, world!'\n    };\n  };"),
    runtime=Runtime.NODEJS_12_X,
    handler="index.handler"
)

tasks.LambdaInvoke(self, "Invoke with state input",
    lambda_function=my_lambda
)
```

When a function is invoked, the Lambda service sends  [these response
elements](https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html#API_Invoke_ResponseElements)
back.

⚠️ The response from the Lambda function is in an attribute called `Payload`

The following snippet invokes a Lambda Function by referencing the `$.Payload` path
to reference the output of a Lambda executed before it.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
tasks.LambdaInvoke(self, "Invoke with empty object as payload",
    lambda_function=my_lambda,
    payload=sfn.TaskInput.from_object()
)

# use the output of myLambda as input
tasks.LambdaInvoke(self, "Invoke with payload field in the state input",
    lambda_function=my_other_lambda,
    payload=sfn.TaskInput.from_data_at("$.Payload")
)
```

The following snippet invokes a Lambda and sets the task output to only include
the Lambda function response.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
tasks.LambdaInvoke(self, "Invoke and set function response as task output",
    lambda_function=my_lambda,
    payload=sfn.TaskInput.from_data_at("$"),
    output_path="$.Payload"
)
```

If you want to combine the input and the Lambda function response you can use
the `payloadResponseOnly` property and specify the `resultPath`. This will put the
Lambda function ARN directly in the "Resource" string, but it conflicts with the
integrationPattern, invocationType, clientContext, and qualifier properties.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
tasks.LambdaInvoke(self, "Invoke and combine function response with task input",
    lambda_function=my_lambda,
    payload_response_only=True,
    result_path="$.myLambda"
)
```

You can have Step Functions pause a task, and wait for an external process to
return a task token. Read more about the [callback pattern](https://docs.aws.amazon.com/step-functions/latest/dg/callback-task-sample-sqs.html#call-back-lambda-example)

To use the callback pattern, set the `token` property on the task. Call the Step
Functions `SendTaskSuccess` or `SendTaskFailure` APIs with the token to
indicate that the task has completed and the state machine should resume execution.

The following snippet invokes a Lambda with the task token as part of the input
to the Lambda.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
tasks.LambdaInvoke(stack, "Invoke with callback",
    lambda_function=my_lambda,
    integration_pattern=sfn.IntegrationPattern.WAIT_FOR_TASK_TOKEN,
    payload=sfn.TaskInput.from_object(
        token=sfn.JsonPath.task_token,
        input=sfn.JsonPath.string_at("$.someField")
    )
)
```

⚠️ The task will pause until it receives that task token back with a `SendTaskSuccess` or `SendTaskFailure`
call. Learn more about [Callback with the Task
Token](https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token).

AWS Lambda can occasionally experience transient service errors. In this case, invoking Lambda
results in a 500 error, such as `ServiceException`, `AWSLambdaException`, or `SdkClientException`.
As a best practive, the `LambdaInvoke` task will retry on those errors with an interval of 2 seconds,
a back-off rate of 2 and 6 maximum attempts. Set the `retryOnServiceExceptions` prop to `false` to
disable this behavior.

## SageMaker

Step Functions supports [AWS SageMaker](https://docs.aws.amazon.com/step-functions/latest/dg/connect-sagemaker.html) through the service integration pattern.

### Create Training Job

You can call the [`CreateTrainingJob`](https://docs.aws.amazon.com/sagemaker/latest/dg/API_CreateTrainingJob.html) API from a `Task` state.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
sfn.SagemakerTrainTask(self, "TrainSagemaker",
    training_job_name=sfn.JsonPath.string_at("$.JobName"),
    role=role,
    algorithm_specification={
        "algorithm_name": "BlazingText",
        "training_input_mode": tasks.InputMode.FILE
    },
    input_data_config=[{
        "channel_name": "train",
        "data_source": {
            "s3_data_source": {
                "s3_data_type": tasks.S3DataType.S3_PREFIX,
                "s3_location": tasks.S3Location.from_json_expression("$.S3Bucket")
            }
        }
    }],
    output_data_config={
        "s3_output_location": tasks.S3Location.from_bucket(s3.Bucket.from_bucket_name(stack, "Bucket", "mybucket"), "myoutputpath")
    },
    resource_config={
        "instance_count": 1,
        "instance_type": ec2.InstanceType.of(ec2.InstanceClass.P3, ec2.InstanceSize.XLARGE2),
        "volume_size": cdk.Size.gibibytes(50)
    },
    stopping_condition={
        "max_runtime": cdk.Duration.hours(1)
    }
)
```

### Create Transform Job

You can call the [`CreateTransformJob`](https://docs.aws.amazon.com/sagemaker/latest/dg/API_CreateTransformJob.html) API from a `Task` state.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
sfn.SagemakerTransformTask(self, "Batch Inference",
    transform_job_name="MyTransformJob",
    model_name="MyModelName",
    model_client_options={
        "invocation_max_retries": 3, # default is 0
        "invocation_timeout": cdk.Duration.minutes(5)
    },
    role=role,
    transform_input={
        "transform_data_source": {
            "s3_data_source": {
                "s3_uri": "s3://inputbucket/train",
                "s3_data_type": S3DataType.S3Prefix
            }
        }
    },
    transform_output={
        "s3_output_path": "s3://outputbucket/TransformJobOutputPath"
    },
    transform_resources={
        "instance_count": 1,
        "instance_type": ec2.InstanceType.of(ec2.InstanceClass.M4, ec2.InstanceSize.XLarge)
    }
)
```

### Create Endpoint

You can call the [`CreateEndpoint`](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateEndpoint.html) API from a `Task` state.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
sfn.SageMakerCreateEndpoint(self, "SagemakerEndpoint",
    endpoint_name=sfn.JsonPath.string_at("$.EndpointName"),
    endpoint_config_name=sfn.JsonPath.string_at("$.EndpointConfigName")
)
```

### Create Endpoint Config

You can call the [`CreateEndpointConfig`](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateEndpointConfig.html) API from a `Task` state.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
sfn.SageMakerCreateEndpointConfig(self, "SagemakerEndpointConfig",
    endpoint_config_name="MyEndpointConfig",
    production_variants=[{
        "initial_instance_count": 2,
        "instance_type": ec2.InstanceType.of(ec2.InstanceClass.M5, ec2.InstanceSize.XLARGE),
        "model_name": "MyModel",
        "variant_name": "awesome-variant"
    }]
)
```

### Create Model

You can call the [`CreateModel`](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateModel.html) API from a `Task` state.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
sfn.SageMakerCreateModel(self, "Sagemaker",
    model_name="MyModel",
    primary_container=tasks.ContainerDefinition(
        image=tasks.DockerImage.from_json_expression(sfn.JsonPath.string_at("$.Model.imageName")),
        mode=tasks.Mode.SINGLE_MODEL,
        model_s3_location=tasks.S3Location.from_json_expression("$.TrainingJob.ModelArtifacts.S3ModelArtifacts")
    )
)
```

### Update Endpoint

You can call the [`UpdateEndpoint`](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_UpdateEndpoint.html) API from a `Task` state.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
sfn.SageMakerUpdateEndpoint(self, "SagemakerEndpoint",
    endpoint_name=sfn.JsonPath.string_at("$.Endpoint.Name"),
    endpoint_config_name=sfn.JsonPath.string_at("$.Endpoint.EndpointConfig")
)
```

## SNS

Step Functions supports [Amazon SNS](https://docs.aws.amazon.com/step-functions/latest/dg/connect-sns.html) through the service integration pattern.

You can call the [`Publish`](https://docs.aws.amazon.com/sns/latest/api/API_Publish.html) API from a `Task` state to publish to an SNS topic.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_sns as sns
import aws_cdk.aws_stepfunctions as sfn
import aws_cdk.aws_stepfunctions_tasks as tasks

# ...

topic = sns.Topic(self, "Topic")

# Use a field from the execution data as message.
task1 = tasks.SnsPublish(self, "Publish1",
    topic=topic,
    integration_pattern=sfn.IntegrationPattern.REQUEST_RESPONSE,
    message=sfn.TaskInput.from_data_at("$.state.message")
)

# Combine a field from the execution data with
# a literal object.
task2 = tasks.SnsPublish(self, "Publish2",
    topic=topic,
    message=sfn.TaskInput.from_object({
        "field1": "somedata",
        "field2": sfn.JsonPath.string_at("$.field2")
    })
)
```

## Step Functions

### Start Execution

You can manage [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/connect-stepfunctions.html) executions.

AWS Step Functions supports it's own [`StartExecution`](https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartExecution.html) API as a service integration.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Define a state machine with one Pass state
child = sfn.StateMachine(stack, "ChildStateMachine",
    definition=sfn.Chain.start(sfn.Pass(stack, "PassState"))
)

# Include the state machine in a Task state with callback pattern
task = StepFunctionsStartExecution(stack, "ChildTask",
    state_machine=child,
    integration_pattern=sfn.IntegrationPattern.WAIT_FOR_TASK_TOKEN,
    input=sfn.TaskInput.from_object(
        token=sfn.JsonPath.task_token,
        foo="bar"
    ),
    name="MyExecutionName"
)

# Define a second state machine with the Task state above
sfn.StateMachine(stack, "ParentStateMachine",
    definition=task
)
```

### Invoke Activity

You can invoke a [Step Functions Activity](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-activities.html) which enables you to have
a task in your state machine where the work is performed by a *worker* that can
be hosted on Amazon EC2, Amazon ECS, AWS Lambda, basically anywhere. Activities
are a way to associate code running somewhere (known as an activity worker) with
a specific task in a state machine.

When Step Functions reaches an activity task state, the workflow waits for an
activity worker to poll for a task. An activity worker polls Step Functions by
using GetActivityTask, and sending the ARN for the related activity.

After the activity worker completes its work, it can provide a report of its
success or failure by using `SendTaskSuccess` or `SendTaskFailure`. These two
calls use the taskToken provided by GetActivityTask to associate the result
with that task.

The following example creates an activity and creates a task that invokes the activity.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
submit_job_activity = sfn.Activity(self, "SubmitJob")

tasks.StepFunctionsInvokeActivity(self, "Submit Job",
    activity=submit_job_activity
)
```

## SQS

Step Functions supports [Amazon SQS](https://docs.aws.amazon.com/step-functions/latest/dg/connect-sqs.html)

You can call the [`SendMessage`](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SendMessage.html) API from a `Task` state
to send a message to an SQS queue.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_stepfunctions as sfn
import aws_cdk.aws_stepfunctions_tasks as tasks
import aws_cdk.aws_sqs as sqs

# ...

queue = sqs.Queue(self, "Queue")

# Use a field from the execution data as message.
task1 = tasks.SqsSendMessage(self, "Send1",
    queue=queue,
    message_body=sfn.TaskInput.from_data_at("$.message")
)

# Combine a field from the execution data with
# a literal object.
task2 = tasks.SqsSendMessage(self, "Send2",
    queue=queue,
    message_body=sfn.TaskInput.from_object({
        "field1": "somedata",
        "field2": sfn.JsonPath.string_at("$.field2")
    })
)
```
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.assets
import aws_cdk.aws_batch
import aws_cdk.aws_codebuild
import aws_cdk.aws_dynamodb
import aws_cdk.aws_ec2
import aws_cdk.aws_ecr
import aws_cdk.aws_ecr_assets
import aws_cdk.aws_ecs
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.aws_sns
import aws_cdk.aws_sqs
import aws_cdk.aws_stepfunctions
import aws_cdk.core
import constructs


class AcceleratorClass(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.AcceleratorClass",
):
    """(experimental) The generation of Elastic Inference (EI) instance.

    :see: https://docs.aws.amazon.com/sagemaker/latest/dg/ei.html
    :stability: experimental
    """

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, version: builtins.str) -> "AcceleratorClass":
        """(experimental) Custom AcceleratorType.

        :param version: - Elastic Inference accelerator generation.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "of", [version])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="EIA1")
    def EIA1(cls) -> "AcceleratorClass":
        """(experimental) Elastic Inference accelerator 1st generation.

        :stability: experimental
        """
        return jsii.sget(cls, "EIA1")

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="EIA2")
    def EIA2(cls) -> "AcceleratorClass":
        """(experimental) Elastic Inference accelerator 2nd generation.

        :stability: experimental
        """
        return jsii.sget(cls, "EIA2")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        """(experimental) - Elastic Inference accelerator generation.

        :stability: experimental
        """
        return jsii.get(self, "version")


class AcceleratorType(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.AcceleratorType",
):
    """(experimental) The size of the Elastic Inference (EI) instance to use for the production variant.

    EI instances provide on-demand GPU computing for inference

    :see: https://docs.aws.amazon.com/sagemaker/latest/dg/ei.html
    :stability: experimental
    """

    def __init__(self, instance_type_identifier: builtins.str) -> None:
        """
        :param instance_type_identifier: -

        :stability: experimental
        """
        jsii.create(AcceleratorType, self, [instance_type_identifier])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls,
        accelerator_class: AcceleratorClass,
        instance_size: aws_cdk.aws_ec2.InstanceSize,
    ) -> "AcceleratorType":
        """(experimental) AcceleratorType.

        This class takes a combination of a class and size.

        :param accelerator_class: -
        :param instance_size: -

        :stability: experimental
        """
        return jsii.sinvoke(cls, "of", [accelerator_class, instance_size])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        """(experimental) Return the accelerator type as a dotted string.

        :stability: experimental
        """
        return jsii.invoke(self, "toString", [])


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.ActionOnFailure")
class ActionOnFailure(enum.Enum):
    """(experimental) The action to take when the cluster step fails.

    :default: CONTINUE

    :see:

    https://docs.aws.amazon.com/emr/latest/APIReference/API_StepConfig.html

    Here, they are named as TERMINATE_JOB_FLOW, TERMINATE_CLUSTER, CANCEL_AND_WAIT, and CONTINUE respectively.
    :stability: experimental
    """

    TERMINATE_CLUSTER = "TERMINATE_CLUSTER"
    """(experimental) Terminate the Cluster on Step Failure.

    :stability: experimental
    """
    CANCEL_AND_WAIT = "CANCEL_AND_WAIT"
    """(experimental) Cancel Step execution and enter WAITING state.

    :stability: experimental
    """
    CONTINUE = "CONTINUE"
    """(experimental) Continue to the next Step.

    :stability: experimental
    """


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.AlgorithmSpecification",
    jsii_struct_bases=[],
    name_mapping={
        "algorithm_name": "algorithmName",
        "metric_definitions": "metricDefinitions",
        "training_image": "trainingImage",
        "training_input_mode": "trainingInputMode",
    },
)
class AlgorithmSpecification:
    def __init__(
        self,
        *,
        algorithm_name: typing.Optional[builtins.str] = None,
        metric_definitions: typing.Optional[typing.List["MetricDefinition"]] = None,
        training_image: typing.Optional["DockerImage"] = None,
        training_input_mode: typing.Optional["InputMode"] = None,
    ) -> None:
        """(experimental) Specify the training algorithm and algorithm-specific metadata.

        :param algorithm_name: (experimental) Name of the algorithm resource to use for the training job. This must be an algorithm resource that you created or subscribe to on AWS Marketplace. If you specify a value for this parameter, you can't specify a value for TrainingImage. Default: - No algorithm is specified
        :param metric_definitions: (experimental) List of metric definition objects. Each object specifies the metric name and regular expressions used to parse algorithm logs. Default: - No metrics
        :param training_image: (experimental) Registry path of the Docker image that contains the training algorithm. Default: - No Docker image is specified
        :param training_input_mode: (experimental) Input mode that the algorithm supports. Default: 'File' mode

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if algorithm_name is not None:
            self._values["algorithm_name"] = algorithm_name
        if metric_definitions is not None:
            self._values["metric_definitions"] = metric_definitions
        if training_image is not None:
            self._values["training_image"] = training_image
        if training_input_mode is not None:
            self._values["training_input_mode"] = training_input_mode

    @builtins.property
    def algorithm_name(self) -> typing.Optional[builtins.str]:
        """(experimental) Name of the algorithm resource to use for the training job.

        This must be an algorithm resource that you created or subscribe to on AWS Marketplace.
        If you specify a value for this parameter, you can't specify a value for TrainingImage.

        :default: - No algorithm is specified

        :stability: experimental
        """
        result = self._values.get("algorithm_name")
        return result

    @builtins.property
    def metric_definitions(self) -> typing.Optional[typing.List["MetricDefinition"]]:
        """(experimental) List of metric definition objects.

        Each object specifies the metric name and regular expressions used to parse algorithm logs.

        :default: - No metrics

        :stability: experimental
        """
        result = self._values.get("metric_definitions")
        return result

    @builtins.property
    def training_image(self) -> typing.Optional["DockerImage"]:
        """(experimental) Registry path of the Docker image that contains the training algorithm.

        :default: - No Docker image is specified

        :stability: experimental
        """
        result = self._values.get("training_image")
        return result

    @builtins.property
    def training_input_mode(self) -> typing.Optional["InputMode"]:
        """(experimental) Input mode that the algorithm supports.

        :default: 'File' mode

        :stability: experimental
        """
        result = self._values.get("training_input_mode")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlgorithmSpecification(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.AssembleWith")
class AssembleWith(enum.Enum):
    """(experimental) How to assemble the results of the transform job as a single S3 object.

    :stability: experimental
    """

    NONE = "NONE"
    """(experimental) Concatenate the results in binary format.

    :stability: experimental
    """
    LINE = "LINE"
    """(experimental) Add a newline character at the end of every transformed record.

    :stability: experimental
    """


class AthenaGetQueryExecution(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.AthenaGetQueryExecution",
):
    """(experimental) Get an Athena Query Execution as a Task.

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-athena.html
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        query_execution_id: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param query_execution_id: (experimental) Query that will be retrieved.
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        :stability: experimental
        """
        props = AthenaGetQueryExecutionProps(
            query_execution_id=query_execution_id,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(AthenaGetQueryExecution, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.AthenaGetQueryExecutionProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "query_execution_id": "queryExecutionId",
    },
)
class AthenaGetQueryExecutionProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        query_execution_id: builtins.str,
    ) -> None:
        """(experimental) Properties for getting a Query Execution.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param query_execution_id: (experimental) Query that will be retrieved.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "query_execution_id": query_execution_id,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def query_execution_id(self) -> builtins.str:
        """(experimental) Query that will be retrieved.

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "adfsaf-23trf23-f23rt23"
        """
        result = self._values.get("query_execution_id")
        assert result is not None, "Required property 'query_execution_id' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AthenaGetQueryExecutionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AthenaGetQueryResults(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.AthenaGetQueryResults",
):
    """(experimental) Get an Athena Query Results as a Task.

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-athena.html
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        query_execution_id: builtins.str,
        max_results: typing.Optional[jsii.Number] = None,
        next_token: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param query_execution_id: (experimental) Query that will be retrieved.
        :param max_results: (experimental) Max number of results. Default: 1000
        :param next_token: (experimental) Pagination token. Default: - No next token
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        :stability: experimental
        """
        props = AthenaGetQueryResultsProps(
            query_execution_id=query_execution_id,
            max_results=max_results,
            next_token=next_token,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(AthenaGetQueryResults, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.AthenaGetQueryResultsProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "query_execution_id": "queryExecutionId",
        "max_results": "maxResults",
        "next_token": "nextToken",
    },
)
class AthenaGetQueryResultsProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        query_execution_id: builtins.str,
        max_results: typing.Optional[jsii.Number] = None,
        next_token: typing.Optional[builtins.str] = None,
    ) -> None:
        """(experimental) Properties for getting a Query Results.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param query_execution_id: (experimental) Query that will be retrieved.
        :param max_results: (experimental) Max number of results. Default: 1000
        :param next_token: (experimental) Pagination token. Default: - No next token

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "query_execution_id": query_execution_id,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if max_results is not None:
            self._values["max_results"] = max_results
        if next_token is not None:
            self._values["next_token"] = next_token

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def query_execution_id(self) -> builtins.str:
        """(experimental) Query that will be retrieved.

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "adfsaf-23trf23-f23rt23"
        """
        result = self._values.get("query_execution_id")
        assert result is not None, "Required property 'query_execution_id' is missing"
        return result

    @builtins.property
    def max_results(self) -> typing.Optional[jsii.Number]:
        """(experimental) Max number of results.

        :default: 1000

        :stability: experimental
        """
        result = self._values.get("max_results")
        return result

    @builtins.property
    def next_token(self) -> typing.Optional[builtins.str]:
        """(experimental) Pagination token.

        :default: - No next token

        :stability: experimental
        """
        result = self._values.get("next_token")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AthenaGetQueryResultsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AthenaStartQueryExecution(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.AthenaStartQueryExecution",
):
    """(experimental) Start an Athena Query as a Task.

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-athena.html
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        query_string: builtins.str,
        client_request_token: typing.Optional[builtins.str] = None,
        query_execution_context: typing.Optional["QueryExecutionContext"] = None,
        result_configuration: typing.Optional["ResultConfiguration"] = None,
        work_group: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param query_string: (experimental) Query that will be started.
        :param client_request_token: (experimental) Unique string string to ensure idempotence. Default: - No client request token
        :param query_execution_context: (experimental) Database within which query executes. Default: - No query execution context
        :param result_configuration: (experimental) Configuration on how and where to save query. Default: - No result configuration
        :param work_group: (experimental) Configuration on how and where to save query. Default: - No work group
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        :stability: experimental
        """
        props = AthenaStartQueryExecutionProps(
            query_string=query_string,
            client_request_token=client_request_token,
            query_execution_context=query_execution_context,
            result_configuration=result_configuration,
            work_group=work_group,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(AthenaStartQueryExecution, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.AthenaStartQueryExecutionProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "query_string": "queryString",
        "client_request_token": "clientRequestToken",
        "query_execution_context": "queryExecutionContext",
        "result_configuration": "resultConfiguration",
        "work_group": "workGroup",
    },
)
class AthenaStartQueryExecutionProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        query_string: builtins.str,
        client_request_token: typing.Optional[builtins.str] = None,
        query_execution_context: typing.Optional["QueryExecutionContext"] = None,
        result_configuration: typing.Optional["ResultConfiguration"] = None,
        work_group: typing.Optional[builtins.str] = None,
    ) -> None:
        """(experimental) Properties for starting a Query Execution.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param query_string: (experimental) Query that will be started.
        :param client_request_token: (experimental) Unique string string to ensure idempotence. Default: - No client request token
        :param query_execution_context: (experimental) Database within which query executes. Default: - No query execution context
        :param result_configuration: (experimental) Configuration on how and where to save query. Default: - No result configuration
        :param work_group: (experimental) Configuration on how and where to save query. Default: - No work group

        :stability: experimental
        """
        if isinstance(query_execution_context, dict):
            query_execution_context = QueryExecutionContext(**query_execution_context)
        if isinstance(result_configuration, dict):
            result_configuration = ResultConfiguration(**result_configuration)
        self._values: typing.Dict[str, typing.Any] = {
            "query_string": query_string,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if client_request_token is not None:
            self._values["client_request_token"] = client_request_token
        if query_execution_context is not None:
            self._values["query_execution_context"] = query_execution_context
        if result_configuration is not None:
            self._values["result_configuration"] = result_configuration
        if work_group is not None:
            self._values["work_group"] = work_group

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def query_string(self) -> builtins.str:
        """(experimental) Query that will be started.

        :stability: experimental
        """
        result = self._values.get("query_string")
        assert result is not None, "Required property 'query_string' is missing"
        return result

    @builtins.property
    def client_request_token(self) -> typing.Optional[builtins.str]:
        """(experimental) Unique string string to ensure idempotence.

        :default: - No client request token

        :stability: experimental
        """
        result = self._values.get("client_request_token")
        return result

    @builtins.property
    def query_execution_context(self) -> typing.Optional["QueryExecutionContext"]:
        """(experimental) Database within which query executes.

        :default: - No query execution context

        :stability: experimental
        """
        result = self._values.get("query_execution_context")
        return result

    @builtins.property
    def result_configuration(self) -> typing.Optional["ResultConfiguration"]:
        """(experimental) Configuration on how and where to save query.

        :default: - No result configuration

        :stability: experimental
        """
        result = self._values.get("result_configuration")
        return result

    @builtins.property
    def work_group(self) -> typing.Optional[builtins.str]:
        """(experimental) Configuration on how and where to save query.

        :default: - No work group

        :stability: experimental
        """
        result = self._values.get("work_group")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AthenaStartQueryExecutionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AthenaStopQueryExecution(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.AthenaStopQueryExecution",
):
    """(experimental) Stop an Athena Query Execution as a Task.

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-athena.html
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        query_execution_id: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param query_execution_id: (experimental) Query that will be stopped.
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        :stability: experimental
        """
        props = AthenaStopQueryExecutionProps(
            query_execution_id=query_execution_id,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(AthenaStopQueryExecution, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.AthenaStopQueryExecutionProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "query_execution_id": "queryExecutionId",
    },
)
class AthenaStopQueryExecutionProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        query_execution_id: builtins.str,
    ) -> None:
        """(experimental) Properties for stoping a Query Execution.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param query_execution_id: (experimental) Query that will be stopped.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "query_execution_id": query_execution_id,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def query_execution_id(self) -> builtins.str:
        """(experimental) Query that will be stopped.

        :stability: experimental
        """
        result = self._values.get("query_execution_id")
        assert result is not None, "Required property 'query_execution_id' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AthenaStopQueryExecutionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.BatchContainerOverrides",
    jsii_struct_bases=[],
    name_mapping={
        "command": "command",
        "environment": "environment",
        "gpu_count": "gpuCount",
        "instance_type": "instanceType",
        "memory": "memory",
        "vcpus": "vcpus",
    },
)
class BatchContainerOverrides:
    def __init__(
        self,
        *,
        command: typing.Optional[typing.List[builtins.str]] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        gpu_count: typing.Optional[jsii.Number] = None,
        instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        memory: typing.Optional[aws_cdk.core.Size] = None,
        vcpus: typing.Optional[jsii.Number] = None,
    ) -> None:
        """The overrides that should be sent to a container.

        :param command: The command to send to the container that overrides the default command from the Docker image or the job definition. Default: - No command overrides
        :param environment: The environment variables to send to the container. You can add new environment variables, which are added to the container at launch, or you can override the existing environment variables from the Docker image or the job definition. Default: - No environment overrides
        :param gpu_count: The number of physical GPUs to reserve for the container. The number of GPUs reserved for all containers in a job should not exceed the number of available GPUs on the compute resource that the job is launched on. Default: - No GPU reservation
        :param instance_type: The instance type to use for a multi-node parallel job. This parameter is not valid for single-node container jobs. Default: - No instance type overrides
        :param memory: Memory reserved for the job. Default: - No memory overrides. The memory supplied in the job definition will be used.
        :param vcpus: The number of vCPUs to reserve for the container. This value overrides the value set in the job definition. Default: - No vCPUs overrides
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if command is not None:
            self._values["command"] = command
        if environment is not None:
            self._values["environment"] = environment
        if gpu_count is not None:
            self._values["gpu_count"] = gpu_count
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if memory is not None:
            self._values["memory"] = memory
        if vcpus is not None:
            self._values["vcpus"] = vcpus

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        """The command to send to the container that overrides the default command from the Docker image or the job definition.

        :default: - No command overrides
        """
        result = self._values.get("command")
        return result

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """The environment variables to send to the container.

        You can add new environment variables, which are added to the container
        at launch, or you can override the existing environment variables from
        the Docker image or the job definition.

        :default: - No environment overrides
        """
        result = self._values.get("environment")
        return result

    @builtins.property
    def gpu_count(self) -> typing.Optional[jsii.Number]:
        """The number of physical GPUs to reserve for the container.

        The number of GPUs reserved for all containers in a job
        should not exceed the number of available GPUs on the compute
        resource that the job is launched on.

        :default: - No GPU reservation
        """
        result = self._values.get("gpu_count")
        return result

    @builtins.property
    def instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        """The instance type to use for a multi-node parallel job.

        This parameter is not valid for single-node container jobs.

        :default: - No instance type overrides
        """
        result = self._values.get("instance_type")
        return result

    @builtins.property
    def memory(self) -> typing.Optional[aws_cdk.core.Size]:
        """Memory reserved for the job.

        :default: - No memory overrides. The memory supplied in the job definition will be used.
        """
        result = self._values.get("memory")
        return result

    @builtins.property
    def vcpus(self) -> typing.Optional[jsii.Number]:
        """The number of vCPUs to reserve for the container.

        This value overrides the value set in the job definition.

        :default: - No vCPUs overrides
        """
        result = self._values.get("vcpus")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchContainerOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.BatchJobDependency",
    jsii_struct_bases=[],
    name_mapping={"job_id": "jobId", "type": "type"},
)
class BatchJobDependency:
    def __init__(
        self,
        *,
        job_id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        """An object representing an AWS Batch job dependency.

        :param job_id: The job ID of the AWS Batch job associated with this dependency. Default: - No jobId
        :param type: The type of the job dependency. Default: - No type
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if job_id is not None:
            self._values["job_id"] = job_id
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def job_id(self) -> typing.Optional[builtins.str]:
        """The job ID of the AWS Batch job associated with this dependency.

        :default: - No jobId
        """
        result = self._values.get("job_id")
        return result

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        """The type of the job dependency.

        :default: - No type
        """
        result = self._values.get("type")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchJobDependency(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.BatchStrategy")
class BatchStrategy(enum.Enum):
    """(experimental) Specifies the number of records to include in a mini-batch for an HTTP inference request.

    :stability: experimental
    """

    MULTI_RECORD = "MULTI_RECORD"
    """(experimental) Fits multiple records in a mini-batch.

    :stability: experimental
    """
    SINGLE_RECORD = "SINGLE_RECORD"
    """(experimental) Use a single record when making an invocation request.

    :stability: experimental
    """


class BatchSubmitJob(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.BatchSubmitJob",
):
    """Task to submits an AWS Batch job from a job definition.

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-batch.html
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        job_definition: aws_cdk.aws_batch.IJobDefinition,
        job_name: builtins.str,
        job_queue: aws_cdk.aws_batch.IJobQueue,
        array_size: typing.Optional[jsii.Number] = None,
        attempts: typing.Optional[jsii.Number] = None,
        container_overrides: typing.Optional[BatchContainerOverrides] = None,
        depends_on: typing.Optional[typing.List[BatchJobDependency]] = None,
        payload: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param job_definition: The job definition used by this job.
        :param job_name: The name of the job. The first character must be alphanumeric, and up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.
        :param job_queue: The job queue into which the job is submitted.
        :param array_size: The array size can be between 2 and 10,000. If you specify array properties for a job, it becomes an array job. For more information, see Array Jobs in the AWS Batch User Guide. Default: - No array size
        :param attempts: The number of times to move a job to the RUNNABLE status. You may specify between 1 and 10 attempts. If the value of attempts is greater than one, the job is retried on failure the same number of attempts as the value. Default: 1
        :param container_overrides: A list of container overrides in JSON format that specify the name of a container in the specified job definition and the overrides it should receive. Default: - No container overrides
        :param depends_on: A list of dependencies for the job. A job can depend upon a maximum of 20 jobs. Default: - No dependencies
        :param payload: The payload to be passed as parameters to the batch job. Default: - No parameters are passed
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        """
        props = BatchSubmitJobProps(
            job_definition=job_definition,
            job_name=job_name,
            job_queue=job_queue,
            array_size=array_size,
            attempts=attempts,
            container_overrides=container_overrides,
            depends_on=depends_on,
            payload=payload,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(BatchSubmitJob, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.BatchSubmitJobProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "job_definition": "jobDefinition",
        "job_name": "jobName",
        "job_queue": "jobQueue",
        "array_size": "arraySize",
        "attempts": "attempts",
        "container_overrides": "containerOverrides",
        "depends_on": "dependsOn",
        "payload": "payload",
    },
)
class BatchSubmitJobProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        job_definition: aws_cdk.aws_batch.IJobDefinition,
        job_name: builtins.str,
        job_queue: aws_cdk.aws_batch.IJobQueue,
        array_size: typing.Optional[jsii.Number] = None,
        attempts: typing.Optional[jsii.Number] = None,
        container_overrides: typing.Optional[BatchContainerOverrides] = None,
        depends_on: typing.Optional[typing.List[BatchJobDependency]] = None,
        payload: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
    ) -> None:
        """Properties for RunBatchJob.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param job_definition: The job definition used by this job.
        :param job_name: The name of the job. The first character must be alphanumeric, and up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.
        :param job_queue: The job queue into which the job is submitted.
        :param array_size: The array size can be between 2 and 10,000. If you specify array properties for a job, it becomes an array job. For more information, see Array Jobs in the AWS Batch User Guide. Default: - No array size
        :param attempts: The number of times to move a job to the RUNNABLE status. You may specify between 1 and 10 attempts. If the value of attempts is greater than one, the job is retried on failure the same number of attempts as the value. Default: 1
        :param container_overrides: A list of container overrides in JSON format that specify the name of a container in the specified job definition and the overrides it should receive. Default: - No container overrides
        :param depends_on: A list of dependencies for the job. A job can depend upon a maximum of 20 jobs. Default: - No dependencies
        :param payload: The payload to be passed as parameters to the batch job. Default: - No parameters are passed
        """
        if isinstance(container_overrides, dict):
            container_overrides = BatchContainerOverrides(**container_overrides)
        self._values: typing.Dict[str, typing.Any] = {
            "job_definition": job_definition,
            "job_name": job_name,
            "job_queue": job_queue,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if array_size is not None:
            self._values["array_size"] = array_size
        if attempts is not None:
            self._values["attempts"] = attempts
        if container_overrides is not None:
            self._values["container_overrides"] = container_overrides
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if payload is not None:
            self._values["payload"] = payload

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def job_definition(self) -> aws_cdk.aws_batch.IJobDefinition:
        """The job definition used by this job."""
        result = self._values.get("job_definition")
        assert result is not None, "Required property 'job_definition' is missing"
        return result

    @builtins.property
    def job_name(self) -> builtins.str:
        """The name of the job.

        The first character must be alphanumeric, and up to 128 letters (uppercase and lowercase),
        numbers, hyphens, and underscores are allowed.
        """
        result = self._values.get("job_name")
        assert result is not None, "Required property 'job_name' is missing"
        return result

    @builtins.property
    def job_queue(self) -> aws_cdk.aws_batch.IJobQueue:
        """The job queue into which the job is submitted."""
        result = self._values.get("job_queue")
        assert result is not None, "Required property 'job_queue' is missing"
        return result

    @builtins.property
    def array_size(self) -> typing.Optional[jsii.Number]:
        """The array size can be between 2 and 10,000.

        If you specify array properties for a job, it becomes an array job.
        For more information, see Array Jobs in the AWS Batch User Guide.

        :default: - No array size
        """
        result = self._values.get("array_size")
        return result

    @builtins.property
    def attempts(self) -> typing.Optional[jsii.Number]:
        """The number of times to move a job to the RUNNABLE status.

        You may specify between 1 and 10 attempts.
        If the value of attempts is greater than one,
        the job is retried on failure the same number of attempts as the value.

        :default: 1
        """
        result = self._values.get("attempts")
        return result

    @builtins.property
    def container_overrides(self) -> typing.Optional[BatchContainerOverrides]:
        """A list of container overrides in JSON format that specify the name of a container in the specified job definition and the overrides it should receive.

        :default: - No container overrides

        :see: https://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html#Batch-SubmitJob-request-containerOverrides
        """
        result = self._values.get("container_overrides")
        return result

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[BatchJobDependency]]:
        """A list of dependencies for the job.

        A job can depend upon a maximum of 20 jobs.

        :default: - No dependencies

        :see: https://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html#Batch-SubmitJob-request-dependsOn
        """
        result = self._values.get("depends_on")
        return result

    @builtins.property
    def payload(self) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskInput]:
        """The payload to be passed as parameters to the batch job.

        :default: - No parameters are passed
        """
        result = self._values.get("payload")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BatchSubmitJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.Channel",
    jsii_struct_bases=[],
    name_mapping={
        "channel_name": "channelName",
        "data_source": "dataSource",
        "compression_type": "compressionType",
        "content_type": "contentType",
        "input_mode": "inputMode",
        "record_wrapper_type": "recordWrapperType",
        "shuffle_config": "shuffleConfig",
    },
)
class Channel:
    def __init__(
        self,
        *,
        channel_name: builtins.str,
        data_source: "DataSource",
        compression_type: typing.Optional["CompressionType"] = None,
        content_type: typing.Optional[builtins.str] = None,
        input_mode: typing.Optional["InputMode"] = None,
        record_wrapper_type: typing.Optional["RecordWrapperType"] = None,
        shuffle_config: typing.Optional["ShuffleConfig"] = None,
    ) -> None:
        """(experimental) Describes the training, validation or test dataset and the Amazon S3 location where it is stored.

        :param channel_name: (experimental) Name of the channel.
        :param data_source: (experimental) Location of the channel data.
        :param compression_type: (experimental) Compression type if training data is compressed. Default: - None
        :param content_type: (experimental) The MIME type of the data. Default: - None
        :param input_mode: (experimental) Input mode to use for the data channel in a training job. Default: - None
        :param record_wrapper_type: (experimental) Specify RecordIO as the value when input data is in raw format but the training algorithm requires the RecordIO format. In this case, Amazon SageMaker wraps each individual S3 object in a RecordIO record. If the input data is already in RecordIO format, you don't need to set this attribute. Default: - None
        :param shuffle_config: (experimental) Shuffle config option for input data in a channel. Default: - None

        :stability: experimental
        """
        if isinstance(data_source, dict):
            data_source = DataSource(**data_source)
        if isinstance(shuffle_config, dict):
            shuffle_config = ShuffleConfig(**shuffle_config)
        self._values: typing.Dict[str, typing.Any] = {
            "channel_name": channel_name,
            "data_source": data_source,
        }
        if compression_type is not None:
            self._values["compression_type"] = compression_type
        if content_type is not None:
            self._values["content_type"] = content_type
        if input_mode is not None:
            self._values["input_mode"] = input_mode
        if record_wrapper_type is not None:
            self._values["record_wrapper_type"] = record_wrapper_type
        if shuffle_config is not None:
            self._values["shuffle_config"] = shuffle_config

    @builtins.property
    def channel_name(self) -> builtins.str:
        """(experimental) Name of the channel.

        :stability: experimental
        """
        result = self._values.get("channel_name")
        assert result is not None, "Required property 'channel_name' is missing"
        return result

    @builtins.property
    def data_source(self) -> "DataSource":
        """(experimental) Location of the channel data.

        :stability: experimental
        """
        result = self._values.get("data_source")
        assert result is not None, "Required property 'data_source' is missing"
        return result

    @builtins.property
    def compression_type(self) -> typing.Optional["CompressionType"]:
        """(experimental) Compression type if training data is compressed.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("compression_type")
        return result

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        """(experimental) The MIME type of the data.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("content_type")
        return result

    @builtins.property
    def input_mode(self) -> typing.Optional["InputMode"]:
        """(experimental) Input mode to use for the data channel in a training job.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("input_mode")
        return result

    @builtins.property
    def record_wrapper_type(self) -> typing.Optional["RecordWrapperType"]:
        """(experimental) Specify RecordIO as the value when input data is in raw format but the training algorithm requires the RecordIO format.

        In this case, Amazon SageMaker wraps each individual S3 object in a RecordIO record.
        If the input data is already in RecordIO format, you don't need to set this attribute.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("record_wrapper_type")
        return result

    @builtins.property
    def shuffle_config(self) -> typing.Optional["ShuffleConfig"]:
        """(experimental) Shuffle config option for input data in a channel.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("shuffle_config")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Channel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodeBuildStartBuild(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.CodeBuildStartBuild",
):
    """Start a CodeBuild Build as a task.

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-codebuild.html
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        project: aws_cdk.aws_codebuild.IProject,
        environment_variables_override: typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_codebuild.BuildEnvironmentVariable]] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param project: CodeBuild project to start.
        :param environment_variables_override: A set of environment variables to be used for this build only. Default: - the latest environment variables already defined in the build project.
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        """
        props = CodeBuildStartBuildProps(
            project=project,
            environment_variables_override=environment_variables_override,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(CodeBuildStartBuild, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.CodeBuildStartBuildProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "project": "project",
        "environment_variables_override": "environmentVariablesOverride",
    },
)
class CodeBuildStartBuildProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        project: aws_cdk.aws_codebuild.IProject,
        environment_variables_override: typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_codebuild.BuildEnvironmentVariable]] = None,
    ) -> None:
        """Properties for CodeBuildStartBuild.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param project: CodeBuild project to start.
        :param environment_variables_override: A set of environment variables to be used for this build only. Default: - the latest environment variables already defined in the build project.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "project": project,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if environment_variables_override is not None:
            self._values["environment_variables_override"] = environment_variables_override

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def project(self) -> aws_cdk.aws_codebuild.IProject:
        """CodeBuild project to start."""
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return result

    @builtins.property
    def environment_variables_override(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_codebuild.BuildEnvironmentVariable]]:
        """A set of environment variables to be used for this build only.

        :default: - the latest environment variables already defined in the build project.
        """
        result = self._values.get("environment_variables_override")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeBuildStartBuildProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.CommonEcsRunTaskProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "task_definition": "taskDefinition",
        "container_overrides": "containerOverrides",
        "integration_pattern": "integrationPattern",
    },
)
class CommonEcsRunTaskProps:
    def __init__(
        self,
        *,
        cluster: aws_cdk.aws_ecs.ICluster,
        task_definition: aws_cdk.aws_ecs.TaskDefinition,
        container_overrides: typing.Optional[typing.List["ContainerOverride"]] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern] = None,
    ) -> None:
        """Basic properties for ECS Tasks.

        :param cluster: The topic to run the task on.
        :param task_definition: Task Definition used for running tasks in the service. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions
        :param container_overrides: Container setting overrides. Key is the name of the container to override, value is the values you want to override. Default: - No overrides
        :param integration_pattern: The service integration pattern indicates different ways to call RunTask in ECS. The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET
        """
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
            "task_definition": task_definition,
        }
        if container_overrides is not None:
            self._values["container_overrides"] = container_overrides
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern

    @builtins.property
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """The topic to run the task on."""
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return result

    @builtins.property
    def task_definition(self) -> aws_cdk.aws_ecs.TaskDefinition:
        """Task Definition used for running tasks in the service.

        Note: this must be TaskDefinition, and not ITaskDefinition,
        as it requires properties that are not known for imported task definitions
        """
        result = self._values.get("task_definition")
        assert result is not None, "Required property 'task_definition' is missing"
        return result

    @builtins.property
    def container_overrides(self) -> typing.Optional[typing.List["ContainerOverride"]]:
        """Container setting overrides.

        Key is the name of the container to override, value is the
        values you want to override.

        :default: - No overrides
        """
        result = self._values.get("container_overrides")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """The service integration pattern indicates different ways to call RunTask in ECS.

        The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN.

        :default: FIRE_AND_FORGET
        """
        result = self._values.get("integration_pattern")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonEcsRunTaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.CompressionType")
class CompressionType(enum.Enum):
    """(experimental) Compression type of the data.

    :stability: experimental
    """

    NONE = "NONE"
    """(experimental) None compression type.

    :stability: experimental
    """
    GZIP = "GZIP"
    """(experimental) Gzip compression type.

    :stability: experimental
    """


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.ContainerDefinitionConfig",
    jsii_struct_bases=[],
    name_mapping={"parameters": "parameters"},
)
class ContainerDefinitionConfig:
    def __init__(
        self,
        *,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        """Configuration options for the ContainerDefinition.

        :param parameters: Additional parameters to pass to the base task. Default: - No additional parameters passed
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        """Additional parameters to pass to the base task.

        :default: - No additional parameters passed
        """
        result = self._values.get("parameters")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerDefinitionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.ContainerDefinitionOptions",
    jsii_struct_bases=[],
    name_mapping={
        "container_host_name": "containerHostName",
        "environment_variables": "environmentVariables",
        "image": "image",
        "mode": "mode",
        "model_package_name": "modelPackageName",
        "model_s3_location": "modelS3Location",
    },
)
class ContainerDefinitionOptions:
    def __init__(
        self,
        *,
        container_host_name: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
        image: typing.Optional["DockerImage"] = None,
        mode: typing.Optional["Mode"] = None,
        model_package_name: typing.Optional[builtins.str] = None,
        model_s3_location: typing.Optional["S3Location"] = None,
    ) -> None:
        """(experimental) Properties to define a ContainerDefinition.

        :param container_host_name: (experimental) This parameter is ignored for models that contain only a PrimaryContainer. When a ContainerDefinition is part of an inference pipeline, the value of the parameter uniquely identifies the container for the purposes of logging and metrics. Default: - None
        :param environment_variables: (experimental) The environment variables to set in the Docker container. Default: - No variables
        :param image: (experimental) The Amazon EC2 Container Registry (Amazon ECR) path where inference code is stored. Default: - None
        :param mode: (experimental) Defines how many models the container hosts. Default: - Mode.SINGLE_MODEL
        :param model_package_name: (experimental) The name or Amazon Resource Name (ARN) of the model package to use to create the model. Default: - None
        :param model_s3_location: (experimental) The S3 path where the model artifacts, which result from model training, are stored. This path must point to a single gzip compressed tar archive (.tar.gz suffix). The S3 path is required for Amazon SageMaker built-in algorithms, but not if you use your own algorithms. Default: - None

        :see: https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_ContainerDefinition.html
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if container_host_name is not None:
            self._values["container_host_name"] = container_host_name
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if image is not None:
            self._values["image"] = image
        if mode is not None:
            self._values["mode"] = mode
        if model_package_name is not None:
            self._values["model_package_name"] = model_package_name
        if model_s3_location is not None:
            self._values["model_s3_location"] = model_s3_location

    @builtins.property
    def container_host_name(self) -> typing.Optional[builtins.str]:
        """(experimental) This parameter is ignored for models that contain only a PrimaryContainer.

        When a ContainerDefinition is part of an inference pipeline,
        the value of the parameter uniquely identifies the container for the purposes of logging and metrics.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("container_host_name")
        return result

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskInput]:
        """(experimental) The environment variables to set in the Docker container.

        :default: - No variables

        :stability: experimental
        """
        result = self._values.get("environment_variables")
        return result

    @builtins.property
    def image(self) -> typing.Optional["DockerImage"]:
        """(experimental) The Amazon EC2 Container Registry (Amazon ECR) path where inference code is stored.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("image")
        return result

    @builtins.property
    def mode(self) -> typing.Optional["Mode"]:
        """(experimental) Defines how many models the container hosts.

        :default: - Mode.SINGLE_MODEL

        :stability: experimental
        """
        result = self._values.get("mode")
        return result

    @builtins.property
    def model_package_name(self) -> typing.Optional[builtins.str]:
        """(experimental) The name or Amazon Resource Name (ARN) of the model package to use to create the model.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("model_package_name")
        return result

    @builtins.property
    def model_s3_location(self) -> typing.Optional["S3Location"]:
        """(experimental) The S3 path where the model artifacts, which result from model training, are stored.

        This path must point to a single gzip compressed tar archive (.tar.gz suffix).
        The S3 path is required for Amazon SageMaker built-in algorithms, but not if you use your own algorithms.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("model_s3_location")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerDefinitionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.ContainerOverride",
    jsii_struct_bases=[],
    name_mapping={
        "container_definition": "containerDefinition",
        "command": "command",
        "cpu": "cpu",
        "environment": "environment",
        "memory_limit": "memoryLimit",
        "memory_reservation": "memoryReservation",
    },
)
class ContainerOverride:
    def __init__(
        self,
        *,
        container_definition: aws_cdk.aws_ecs.ContainerDefinition,
        command: typing.Optional[typing.List[builtins.str]] = None,
        cpu: typing.Optional[jsii.Number] = None,
        environment: typing.Optional[typing.List["TaskEnvironmentVariable"]] = None,
        memory_limit: typing.Optional[jsii.Number] = None,
        memory_reservation: typing.Optional[jsii.Number] = None,
    ) -> None:
        """A list of container overrides that specify the name of a container and the overrides it should receive.

        :param container_definition: Name of the container inside the task definition.
        :param command: Command to run inside the container. Default: - Default command from the Docker image or the task definition
        :param cpu: The number of cpu units reserved for the container. Default: - The default value from the task definition.
        :param environment: The environment variables to send to the container. You can add new environment variables, which are added to the container at launch, or you can override the existing environment variables from the Docker image or the task definition. Default: - The existing environment variables from the Docker image or the task definition
        :param memory_limit: The hard limit (in MiB) of memory to present to the container. Default: - The default value from the task definition.
        :param memory_reservation: The soft limit (in MiB) of memory to reserve for the container. Default: - The default value from the task definition.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "container_definition": container_definition,
        }
        if command is not None:
            self._values["command"] = command
        if cpu is not None:
            self._values["cpu"] = cpu
        if environment is not None:
            self._values["environment"] = environment
        if memory_limit is not None:
            self._values["memory_limit"] = memory_limit
        if memory_reservation is not None:
            self._values["memory_reservation"] = memory_reservation

    @builtins.property
    def container_definition(self) -> aws_cdk.aws_ecs.ContainerDefinition:
        """Name of the container inside the task definition."""
        result = self._values.get("container_definition")
        assert result is not None, "Required property 'container_definition' is missing"
        return result

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        """Command to run inside the container.

        :default: - Default command from the Docker image or the task definition
        """
        result = self._values.get("command")
        return result

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units reserved for the container.

        :default: - The default value from the task definition.
        """
        result = self._values.get("cpu")
        return result

    @builtins.property
    def environment(self) -> typing.Optional[typing.List["TaskEnvironmentVariable"]]:
        """The environment variables to send to the container.

        You can add new environment variables, which are added to the container at launch,
        or you can override the existing environment variables from the Docker image or the task definition.

        :default: - The existing environment variables from the Docker image or the task definition
        """
        result = self._values.get("environment")
        return result

    @builtins.property
    def memory_limit(self) -> typing.Optional[jsii.Number]:
        """The hard limit (in MiB) of memory to present to the container.

        :default: - The default value from the task definition.
        """
        result = self._values.get("memory_limit")
        return result

    @builtins.property
    def memory_reservation(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        :default: - The default value from the task definition.
        """
        result = self._values.get("memory_reservation")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerOverride(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.ContainerOverrides",
    jsii_struct_bases=[],
    name_mapping={
        "command": "command",
        "environment": "environment",
        "gpu_count": "gpuCount",
        "instance_type": "instanceType",
        "memory": "memory",
        "vcpus": "vcpus",
    },
)
class ContainerOverrides:
    def __init__(
        self,
        *,
        command: typing.Optional[typing.List[builtins.str]] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        gpu_count: typing.Optional[jsii.Number] = None,
        instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        memory: typing.Optional[jsii.Number] = None,
        vcpus: typing.Optional[jsii.Number] = None,
    ) -> None:
        """The overrides that should be sent to a container.

        :param command: The command to send to the container that overrides the default command from the Docker image or the job definition. Default: - No command overrides
        :param environment: The environment variables to send to the container. You can add new environment variables, which are added to the container at launch, or you can override the existing environment variables from the Docker image or the job definition. Default: - No environment overrides
        :param gpu_count: The number of physical GPUs to reserve for the container. The number of GPUs reserved for all containers in a job should not exceed the number of available GPUs on the compute resource that the job is launched on. Default: - No GPU reservation
        :param instance_type: The instance type to use for a multi-node parallel job. This parameter is not valid for single-node container jobs. Default: - No instance type overrides
        :param memory: The number of MiB of memory reserved for the job. This value overrides the value set in the job definition. Default: - No memory overrides
        :param vcpus: The number of vCPUs to reserve for the container. This value overrides the value set in the job definition. Default: - No vCPUs overrides
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if command is not None:
            self._values["command"] = command
        if environment is not None:
            self._values["environment"] = environment
        if gpu_count is not None:
            self._values["gpu_count"] = gpu_count
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if memory is not None:
            self._values["memory"] = memory
        if vcpus is not None:
            self._values["vcpus"] = vcpus

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        """The command to send to the container that overrides the default command from the Docker image or the job definition.

        :default: - No command overrides
        """
        result = self._values.get("command")
        return result

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """The environment variables to send to the container.

        You can add new environment variables, which are added to the container
        at launch, or you can override the existing environment variables from
        the Docker image or the job definition.

        :default: - No environment overrides
        """
        result = self._values.get("environment")
        return result

    @builtins.property
    def gpu_count(self) -> typing.Optional[jsii.Number]:
        """The number of physical GPUs to reserve for the container.

        The number of GPUs reserved for all containers in a job
        should not exceed the number of available GPUs on the compute
        resource that the job is launched on.

        :default: - No GPU reservation
        """
        result = self._values.get("gpu_count")
        return result

    @builtins.property
    def instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        """The instance type to use for a multi-node parallel job.

        This parameter is not valid for single-node container jobs.

        :default: - No instance type overrides
        """
        result = self._values.get("instance_type")
        return result

    @builtins.property
    def memory(self) -> typing.Optional[jsii.Number]:
        """The number of MiB of memory reserved for the job.

        This value overrides the value set in the job definition.

        :default: - No memory overrides
        """
        result = self._values.get("memory")
        return result

    @builtins.property
    def vcpus(self) -> typing.Optional[jsii.Number]:
        """The number of vCPUs to reserve for the container.

        This value overrides the value set in the job definition.

        :default: - No vCPUs overrides
        """
        result = self._values.get("vcpus")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.DataSource",
    jsii_struct_bases=[],
    name_mapping={"s3_data_source": "s3DataSource"},
)
class DataSource:
    def __init__(self, *, s3_data_source: "S3DataSource") -> None:
        """(experimental) Location of the channel data.

        :param s3_data_source: (experimental) S3 location of the data source that is associated with a channel.

        :stability: experimental
        """
        if isinstance(s3_data_source, dict):
            s3_data_source = S3DataSource(**s3_data_source)
        self._values: typing.Dict[str, typing.Any] = {
            "s3_data_source": s3_data_source,
        }

    @builtins.property
    def s3_data_source(self) -> "S3DataSource":
        """(experimental) S3 location of the data source that is associated with a channel.

        :stability: experimental
        """
        result = self._values.get("s3_data_source")
        assert result is not None, "Required property 's3_data_source' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DockerImage(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.DockerImage",
):
    """(experimental) Creates ``IDockerImage`` instances.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _DockerImageProxy

    def __init__(self) -> None:
        jsii.create(DockerImage, self, [])

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(
        cls,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        directory: builtins.str,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file: typing.Optional[builtins.str] = None,
        repository_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        extra_hash: typing.Optional[builtins.str] = None,
        exclude: typing.Optional[typing.List[builtins.str]] = None,
        follow: typing.Optional[aws_cdk.assets.FollowMode] = None,
        ignore_mode: typing.Optional[aws_cdk.core.IgnoreMode] = None,
    ) -> "DockerImage":
        """(experimental) Reference a Docker image that is provided as an Asset in the current app.

        :param scope: the scope in which to create the Asset.
        :param id: the ID for the asset in the construct tree.
        :param directory: (experimental) The directory where the Dockerfile is stored.
        :param build_args: (experimental) Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param file: (experimental) Path to the Dockerfile (relative to the directory). Default: 'Dockerfile'
        :param repository_name: (deprecated) ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - the default ECR repository for CDK assets
        :param target: (experimental) Docker target to build to. Default: - no target
        :param extra_hash: (deprecated) Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param exclude: (deprecated) Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: (deprecated) The ignore behavior to use for exclude patterns. Default: - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the '

        :stability: experimental
        """
        props = aws_cdk.aws_ecr_assets.DockerImageAssetProps(
            directory=directory,
            build_args=build_args,
            file=file,
            repository_name=repository_name,
            target=target,
            extra_hash=extra_hash,
            exclude=exclude,
            follow=follow,
            ignore_mode=ignore_mode,
        )

        return jsii.sinvoke(cls, "fromAsset", [scope, id, props])

    @jsii.member(jsii_name="fromEcrRepository")
    @builtins.classmethod
    def from_ecr_repository(
        cls,
        repository: aws_cdk.aws_ecr.IRepository,
        tag: typing.Optional[builtins.str] = None,
    ) -> "DockerImage":
        """(experimental) Reference a Docker image stored in an ECR repository.

        :param repository: the ECR repository where the image is hosted.
        :param tag: an optional ``tag``.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromEcrRepository", [repository, tag])

    @jsii.member(jsii_name="fromJsonExpression")
    @builtins.classmethod
    def from_json_expression(
        cls,
        expression: builtins.str,
        allow_any_ecr_image_pull: typing.Optional[builtins.bool] = None,
    ) -> "DockerImage":
        """(experimental) Reference a Docker image which URI is obtained from the task's input.

        :param expression: the JSON path expression with the task input.
        :param allow_any_ecr_image_pull: whether ECR access should be permitted (set to ``false`` if the image will never be in ECR).

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromJsonExpression", [expression, allow_any_ecr_image_pull])

    @jsii.member(jsii_name="fromRegistry")
    @builtins.classmethod
    def from_registry(cls, image_uri: builtins.str) -> "DockerImage":
        """(experimental) Reference a Docker image by it's URI.

        When referencing ECR images, prefer using ``inEcr``.

        :param image_uri: the URI to the docker image.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromRegistry", [image_uri])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, task: "ISageMakerTask") -> "DockerImageConfig":
        """(experimental) Called when the image is used by a SageMaker task.

        :param task: -

        :stability: experimental
        """
        ...


class _DockerImageProxy(DockerImage):
    @jsii.member(jsii_name="bind")
    def bind(self, task: "ISageMakerTask") -> "DockerImageConfig":
        """(experimental) Called when the image is used by a SageMaker task.

        :param task: -

        :stability: experimental
        """
        return jsii.invoke(self, "bind", [task])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.DockerImageConfig",
    jsii_struct_bases=[],
    name_mapping={"image_uri": "imageUri"},
)
class DockerImageConfig:
    def __init__(self, *, image_uri: builtins.str) -> None:
        """(experimental) Configuration for a using Docker image.

        :param image_uri: (experimental) The fully qualified URI of the Docker image.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "image_uri": image_uri,
        }

    @builtins.property
    def image_uri(self) -> builtins.str:
        """(experimental) The fully qualified URI of the Docker image.

        :stability: experimental
        """
        result = self._values.get("image_uri")
        assert result is not None, "Required property 'image_uri' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerImageConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DynamoAttributeValue(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoAttributeValue",
):
    """Represents the data for an attribute.

    Each attribute value is described as a name-value pair.
    The name is the data type, and the value is the data itself.

    :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_AttributeValue.html
    """

    @jsii.member(jsii_name="booleanFromJsonPath")
    @builtins.classmethod
    def boolean_from_json_path(cls, value: builtins.str) -> "DynamoAttributeValue":
        """Sets an attribute of type Boolean from state input through Json path.

        For example:  "BOOL": true

        :param value: Json path that specifies state input to be used.
        """
        return jsii.sinvoke(cls, "booleanFromJsonPath", [value])

    @jsii.member(jsii_name="fromBinary")
    @builtins.classmethod
    def from_binary(cls, value: builtins.str) -> "DynamoAttributeValue":
        """Sets an attribute of type Binary.

        For example:  "B": "dGhpcyB0ZXh0IGlzIGJhc2U2NC1lbmNvZGVk"

        :param value: base-64 encoded string.
        """
        return jsii.sinvoke(cls, "fromBinary", [value])

    @jsii.member(jsii_name="fromBinarySet")
    @builtins.classmethod
    def from_binary_set(
        cls,
        value: typing.List[builtins.str],
    ) -> "DynamoAttributeValue":
        """Sets an attribute of type Binary Set.

        For example:  "BS": ["U3Vubnk=", "UmFpbnk=", "U25vd3k="]

        :param value: -
        """
        return jsii.sinvoke(cls, "fromBinarySet", [value])

    @jsii.member(jsii_name="fromBoolean")
    @builtins.classmethod
    def from_boolean(cls, value: builtins.bool) -> "DynamoAttributeValue":
        """Sets an attribute of type Boolean.

        For example:  "BOOL": true

        :param value: -
        """
        return jsii.sinvoke(cls, "fromBoolean", [value])

    @jsii.member(jsii_name="fromList")
    @builtins.classmethod
    def from_list(
        cls,
        value: typing.List["DynamoAttributeValue"],
    ) -> "DynamoAttributeValue":
        """Sets an attribute of type List.

        For example:  "L": [ {"S": "Cookies"} , {"S": "Coffee"}, {"N", "3.14159"}]

        :param value: -
        """
        return jsii.sinvoke(cls, "fromList", [value])

    @jsii.member(jsii_name="fromMap")
    @builtins.classmethod
    def from_map(
        cls,
        value: typing.Mapping[builtins.str, "DynamoAttributeValue"],
    ) -> "DynamoAttributeValue":
        """Sets an attribute of type Map.

        For example:  "M": {"Name": {"S": "Joe"}, "Age": {"N": "35"}}

        :param value: -
        """
        return jsii.sinvoke(cls, "fromMap", [value])

    @jsii.member(jsii_name="fromNull")
    @builtins.classmethod
    def from_null(cls, value: builtins.bool) -> "DynamoAttributeValue":
        """Sets an attribute of type Null.

        For example:  "NULL": true

        :param value: -
        """
        return jsii.sinvoke(cls, "fromNull", [value])

    @jsii.member(jsii_name="fromNumber")
    @builtins.classmethod
    def from_number(cls, value: jsii.Number) -> "DynamoAttributeValue":
        """Sets a literal number.

        For example: 1234
        Numbers are sent across the network to DynamoDB as strings,
        to maximize compatibility across languages and libraries.
        However, DynamoDB treats them as number type attributes for mathematical operations.

        :param value: -
        """
        return jsii.sinvoke(cls, "fromNumber", [value])

    @jsii.member(jsii_name="fromNumberSet")
    @builtins.classmethod
    def from_number_set(cls, value: typing.List[jsii.Number]) -> "DynamoAttributeValue":
        """Sets an attribute of type Number Set.

        For example:  "NS": ["42.2", "-19", "7.5", "3.14"]
        Numbers are sent across the network to DynamoDB as strings,
        to maximize compatibility across languages and libraries.
        However, DynamoDB treats them as number type attributes for mathematical operations.

        :param value: -
        """
        return jsii.sinvoke(cls, "fromNumberSet", [value])

    @jsii.member(jsii_name="fromString")
    @builtins.classmethod
    def from_string(cls, value: builtins.str) -> "DynamoAttributeValue":
        """Sets an attribute of type String.

        For example:  "S": "Hello"
        Strings may be literal values or as JsonPath.

        :param value: -

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            "DynamoAttributeValue.fromString(JsonPath.stringAt('$.bar'))"
        """
        return jsii.sinvoke(cls, "fromString", [value])

    @jsii.member(jsii_name="fromStringSet")
    @builtins.classmethod
    def from_string_set(
        cls,
        value: typing.List[builtins.str],
    ) -> "DynamoAttributeValue":
        """Sets an attribute of type String Set.

        For example:  "SS": ["Giraffe", "Hippo" ,"Zebra"]

        :param value: -
        """
        return jsii.sinvoke(cls, "fromStringSet", [value])

    @jsii.member(jsii_name="mapFromJsonPath")
    @builtins.classmethod
    def map_from_json_path(cls, value: builtins.str) -> "DynamoAttributeValue":
        """Sets an attribute of type Map.

        For example:  "M": {"Name": {"S": "Joe"}, "Age": {"N": "35"}}

        :param value: Json path that specifies state input to be used.
        """
        return jsii.sinvoke(cls, "mapFromJsonPath", [value])

    @jsii.member(jsii_name="numberFromString")
    @builtins.classmethod
    def number_from_string(cls, value: builtins.str) -> "DynamoAttributeValue":
        """Sets an attribute of type Number.

        For example:  "N": "123.45"
        Numbers are sent across the network to DynamoDB as strings,
        to maximize compatibility across languages and libraries.
        However, DynamoDB treats them as number type attributes for mathematical operations.

        Numbers may be expressed as literal strings or as JsonPath

        :param value: -
        """
        return jsii.sinvoke(cls, "numberFromString", [value])

    @jsii.member(jsii_name="numberSetFromStrings")
    @builtins.classmethod
    def number_set_from_strings(
        cls,
        value: typing.List[builtins.str],
    ) -> "DynamoAttributeValue":
        """Sets an attribute of type Number Set.

        For example:  "NS": ["42.2", "-19", "7.5", "3.14"]
        Numbers are sent across the network to DynamoDB as strings,
        to maximize compatibility across languages and libraries.
        However, DynamoDB treats them as number type attributes for mathematical operations.

        Numbers may be expressed as literal strings or as JsonPath

        :param value: -
        """
        return jsii.sinvoke(cls, "numberSetFromStrings", [value])

    @jsii.member(jsii_name="toObject")
    def to_object(self) -> typing.Any:
        """Returns the DynamoDB attribute value."""
        return jsii.invoke(self, "toObject", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attributeValue")
    def attribute_value(self) -> typing.Any:
        """Represents the data for the attribute.

        Data can be
        i.e. "S": "Hello"
        """
        return jsii.get(self, "attributeValue")


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoConsumedCapacity")
class DynamoConsumedCapacity(enum.Enum):
    """Determines the level of detail about provisioned throughput consumption that is returned."""

    INDEXES = "INDEXES"
    """The response includes the aggregate ConsumedCapacity for the operation, together with ConsumedCapacity for each table and secondary index that was accessed."""
    TOTAL = "TOTAL"
    """The response includes only the aggregate ConsumedCapacity for the operation."""
    NONE = "NONE"
    """No ConsumedCapacity details are included in the response."""


class DynamoDeleteItem(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoDeleteItem",
):
    """A StepFunctions task to call DynamoDeleteItem."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        key: typing.Mapping[builtins.str, DynamoAttributeValue],
        table: aws_cdk.aws_dynamodb.ITable,
        condition_expression: typing.Optional[builtins.str] = None,
        expression_attribute_names: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        expression_attribute_values: typing.Optional[typing.Mapping[builtins.str, DynamoAttributeValue]] = None,
        return_consumed_capacity: typing.Optional[DynamoConsumedCapacity] = None,
        return_item_collection_metrics: typing.Optional["DynamoItemCollectionMetrics"] = None,
        return_values: typing.Optional["DynamoReturnValues"] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param key: Primary key of the item to retrieve. For the primary key, you must provide all of the attributes. For example, with a simple primary key, you only need to provide a value for the partition key. For a composite primary key, you must provide values for both the partition key and the sort key.
        :param table: The name of the table containing the requested item.
        :param condition_expression: A condition that must be satisfied in order for a conditional DeleteItem to succeed. Default: - No condition expression
        :param expression_attribute_names: One or more substitution tokens for attribute names in an expression. Default: - No expression attribute names
        :param expression_attribute_values: One or more values that can be substituted in an expression. Default: - No expression attribute values
        :param return_consumed_capacity: Determines the level of detail about provisioned throughput consumption that is returned in the response. Default: DynamoConsumedCapacity.NONE
        :param return_item_collection_metrics: Determines whether item collection metrics are returned. If set to SIZE, the response includes statistics about item collections, if any, that were modified during the operation are returned in the response. If set to NONE (the default), no statistics are returned. Default: DynamoItemCollectionMetrics.NONE
        :param return_values: Use ReturnValues if you want to get the item attributes as they appeared before they were deleted. Default: DynamoReturnValues.NONE
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        """
        props = DynamoDeleteItemProps(
            key=key,
            table=table,
            condition_expression=condition_expression,
            expression_attribute_names=expression_attribute_names,
            expression_attribute_values=expression_attribute_values,
            return_consumed_capacity=return_consumed_capacity,
            return_item_collection_metrics=return_item_collection_metrics,
            return_values=return_values,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(DynamoDeleteItem, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoDeleteItemProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "key": "key",
        "table": "table",
        "condition_expression": "conditionExpression",
        "expression_attribute_names": "expressionAttributeNames",
        "expression_attribute_values": "expressionAttributeValues",
        "return_consumed_capacity": "returnConsumedCapacity",
        "return_item_collection_metrics": "returnItemCollectionMetrics",
        "return_values": "returnValues",
    },
)
class DynamoDeleteItemProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        key: typing.Mapping[builtins.str, DynamoAttributeValue],
        table: aws_cdk.aws_dynamodb.ITable,
        condition_expression: typing.Optional[builtins.str] = None,
        expression_attribute_names: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        expression_attribute_values: typing.Optional[typing.Mapping[builtins.str, DynamoAttributeValue]] = None,
        return_consumed_capacity: typing.Optional[DynamoConsumedCapacity] = None,
        return_item_collection_metrics: typing.Optional["DynamoItemCollectionMetrics"] = None,
        return_values: typing.Optional["DynamoReturnValues"] = None,
    ) -> None:
        """Properties for DynamoDeleteItem Task.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param key: Primary key of the item to retrieve. For the primary key, you must provide all of the attributes. For example, with a simple primary key, you only need to provide a value for the partition key. For a composite primary key, you must provide values for both the partition key and the sort key.
        :param table: The name of the table containing the requested item.
        :param condition_expression: A condition that must be satisfied in order for a conditional DeleteItem to succeed. Default: - No condition expression
        :param expression_attribute_names: One or more substitution tokens for attribute names in an expression. Default: - No expression attribute names
        :param expression_attribute_values: One or more values that can be substituted in an expression. Default: - No expression attribute values
        :param return_consumed_capacity: Determines the level of detail about provisioned throughput consumption that is returned in the response. Default: DynamoConsumedCapacity.NONE
        :param return_item_collection_metrics: Determines whether item collection metrics are returned. If set to SIZE, the response includes statistics about item collections, if any, that were modified during the operation are returned in the response. If set to NONE (the default), no statistics are returned. Default: DynamoItemCollectionMetrics.NONE
        :param return_values: Use ReturnValues if you want to get the item attributes as they appeared before they were deleted. Default: DynamoReturnValues.NONE
        """
        self._values: typing.Dict[str, typing.Any] = {
            "key": key,
            "table": table,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if condition_expression is not None:
            self._values["condition_expression"] = condition_expression
        if expression_attribute_names is not None:
            self._values["expression_attribute_names"] = expression_attribute_names
        if expression_attribute_values is not None:
            self._values["expression_attribute_values"] = expression_attribute_values
        if return_consumed_capacity is not None:
            self._values["return_consumed_capacity"] = return_consumed_capacity
        if return_item_collection_metrics is not None:
            self._values["return_item_collection_metrics"] = return_item_collection_metrics
        if return_values is not None:
            self._values["return_values"] = return_values

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def key(self) -> typing.Mapping[builtins.str, DynamoAttributeValue]:
        """Primary key of the item to retrieve.

        For the primary key, you must provide all of the attributes.
        For example, with a simple primary key, you only need to provide a value for the partition key.
        For a composite primary key, you must provide values for both the partition key and the sort key.

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html#DDB-GetItem-request-Key
        """
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return result

    @builtins.property
    def table(self) -> aws_cdk.aws_dynamodb.ITable:
        """The name of the table containing the requested item."""
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return result

    @builtins.property
    def condition_expression(self) -> typing.Optional[builtins.str]:
        """A condition that must be satisfied in order for a conditional DeleteItem to succeed.

        :default: - No condition expression

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_DeleteItem.html#DDB-DeleteItem-request-ConditionExpression
        """
        result = self._values.get("condition_expression")
        return result

    @builtins.property
    def expression_attribute_names(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """One or more substitution tokens for attribute names in an expression.

        :default: - No expression attribute names

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_DeleteItem.html#DDB-DeleteItem-request-ExpressionAttributeNames
        """
        result = self._values.get("expression_attribute_names")
        return result

    @builtins.property
    def expression_attribute_values(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, DynamoAttributeValue]]:
        """One or more values that can be substituted in an expression.

        :default: - No expression attribute values

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_DeleteItem.html#DDB-DeleteItem-request-ExpressionAttributeValues
        """
        result = self._values.get("expression_attribute_values")
        return result

    @builtins.property
    def return_consumed_capacity(self) -> typing.Optional[DynamoConsumedCapacity]:
        """Determines the level of detail about provisioned throughput consumption that is returned in the response.

        :default: DynamoConsumedCapacity.NONE

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_DeleteItem.html#DDB-DeleteItem-request-ReturnConsumedCapacity
        """
        result = self._values.get("return_consumed_capacity")
        return result

    @builtins.property
    def return_item_collection_metrics(
        self,
    ) -> typing.Optional["DynamoItemCollectionMetrics"]:
        """Determines whether item collection metrics are returned.

        If set to SIZE, the response includes statistics about item collections, if any,
        that were modified during the operation are returned in the response.
        If set to NONE (the default), no statistics are returned.

        :default: DynamoItemCollectionMetrics.NONE
        """
        result = self._values.get("return_item_collection_metrics")
        return result

    @builtins.property
    def return_values(self) -> typing.Optional["DynamoReturnValues"]:
        """Use ReturnValues if you want to get the item attributes as they appeared before they were deleted.

        :default: DynamoReturnValues.NONE

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_DeleteItem.html#DDB-DeleteItem-request-ReturnValues
        """
        result = self._values.get("return_values")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DynamoDeleteItemProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DynamoGetItem(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoGetItem",
):
    """A StepFunctions task to call DynamoGetItem."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        key: typing.Mapping[builtins.str, DynamoAttributeValue],
        table: aws_cdk.aws_dynamodb.ITable,
        consistent_read: typing.Optional[builtins.bool] = None,
        expression_attribute_names: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        projection_expression: typing.Optional[typing.List["DynamoProjectionExpression"]] = None,
        return_consumed_capacity: typing.Optional[DynamoConsumedCapacity] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param key: Primary key of the item to retrieve. For the primary key, you must provide all of the attributes. For example, with a simple primary key, you only need to provide a value for the partition key. For a composite primary key, you must provide values for both the partition key and the sort key.
        :param table: The name of the table containing the requested item.
        :param consistent_read: Determines the read consistency model: If set to true, then the operation uses strongly consistent reads; otherwise, the operation uses eventually consistent reads. Default: false
        :param expression_attribute_names: One or more substitution tokens for attribute names in an expression. Default: - No expression attributes
        :param projection_expression: An array of DynamoProjectionExpression that identifies one or more attributes to retrieve from the table. These attributes can include scalars, sets, or elements of a JSON document. Default: - No projection expression
        :param return_consumed_capacity: Determines the level of detail about provisioned throughput consumption that is returned in the response. Default: DynamoConsumedCapacity.NONE
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        """
        props = DynamoGetItemProps(
            key=key,
            table=table,
            consistent_read=consistent_read,
            expression_attribute_names=expression_attribute_names,
            projection_expression=projection_expression,
            return_consumed_capacity=return_consumed_capacity,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(DynamoGetItem, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoGetItemProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "key": "key",
        "table": "table",
        "consistent_read": "consistentRead",
        "expression_attribute_names": "expressionAttributeNames",
        "projection_expression": "projectionExpression",
        "return_consumed_capacity": "returnConsumedCapacity",
    },
)
class DynamoGetItemProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        key: typing.Mapping[builtins.str, DynamoAttributeValue],
        table: aws_cdk.aws_dynamodb.ITable,
        consistent_read: typing.Optional[builtins.bool] = None,
        expression_attribute_names: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        projection_expression: typing.Optional[typing.List["DynamoProjectionExpression"]] = None,
        return_consumed_capacity: typing.Optional[DynamoConsumedCapacity] = None,
    ) -> None:
        """Properties for DynamoGetItem Task.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param key: Primary key of the item to retrieve. For the primary key, you must provide all of the attributes. For example, with a simple primary key, you only need to provide a value for the partition key. For a composite primary key, you must provide values for both the partition key and the sort key.
        :param table: The name of the table containing the requested item.
        :param consistent_read: Determines the read consistency model: If set to true, then the operation uses strongly consistent reads; otherwise, the operation uses eventually consistent reads. Default: false
        :param expression_attribute_names: One or more substitution tokens for attribute names in an expression. Default: - No expression attributes
        :param projection_expression: An array of DynamoProjectionExpression that identifies one or more attributes to retrieve from the table. These attributes can include scalars, sets, or elements of a JSON document. Default: - No projection expression
        :param return_consumed_capacity: Determines the level of detail about provisioned throughput consumption that is returned in the response. Default: DynamoConsumedCapacity.NONE
        """
        self._values: typing.Dict[str, typing.Any] = {
            "key": key,
            "table": table,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if consistent_read is not None:
            self._values["consistent_read"] = consistent_read
        if expression_attribute_names is not None:
            self._values["expression_attribute_names"] = expression_attribute_names
        if projection_expression is not None:
            self._values["projection_expression"] = projection_expression
        if return_consumed_capacity is not None:
            self._values["return_consumed_capacity"] = return_consumed_capacity

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def key(self) -> typing.Mapping[builtins.str, DynamoAttributeValue]:
        """Primary key of the item to retrieve.

        For the primary key, you must provide all of the attributes.
        For example, with a simple primary key, you only need to provide a value for the partition key.
        For a composite primary key, you must provide values for both the partition key and the sort key.

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html#DDB-GetItem-request-Key
        """
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return result

    @builtins.property
    def table(self) -> aws_cdk.aws_dynamodb.ITable:
        """The name of the table containing the requested item."""
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return result

    @builtins.property
    def consistent_read(self) -> typing.Optional[builtins.bool]:
        """Determines the read consistency model: If set to true, then the operation uses strongly consistent reads;

        otherwise, the operation uses eventually consistent reads.

        :default: false
        """
        result = self._values.get("consistent_read")
        return result

    @builtins.property
    def expression_attribute_names(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """One or more substitution tokens for attribute names in an expression.

        :default: - No expression attributes

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html#DDB-GetItem-request-ExpressionAttributeNames
        """
        result = self._values.get("expression_attribute_names")
        return result

    @builtins.property
    def projection_expression(
        self,
    ) -> typing.Optional[typing.List["DynamoProjectionExpression"]]:
        """An array of DynamoProjectionExpression that identifies one or more attributes to retrieve from the table.

        These attributes can include scalars, sets, or elements of a JSON document.

        :default: - No projection expression

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html#DDB-GetItem-request-ProjectionExpression
        """
        result = self._values.get("projection_expression")
        return result

    @builtins.property
    def return_consumed_capacity(self) -> typing.Optional[DynamoConsumedCapacity]:
        """Determines the level of detail about provisioned throughput consumption that is returned in the response.

        :default: DynamoConsumedCapacity.NONE

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html#DDB-GetItem-request-ReturnConsumedCapacity
        """
        result = self._values.get("return_consumed_capacity")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DynamoGetItemProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoItemCollectionMetrics")
class DynamoItemCollectionMetrics(enum.Enum):
    """Determines whether item collection metrics are returned."""

    SIZE = "SIZE"
    """If set to SIZE, the response includes statistics about item collections, if any, that were modified during the operation."""
    NONE = "NONE"
    """If set to NONE, no statistics are returned."""


class DynamoProjectionExpression(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoProjectionExpression",
):
    """Class to generate projection expression."""

    def __init__(self) -> None:
        jsii.create(DynamoProjectionExpression, self, [])

    @jsii.member(jsii_name="atIndex")
    def at_index(self, index: jsii.Number) -> "DynamoProjectionExpression":
        """Adds the array literal access for passed index.

        :param index: array index.
        """
        return jsii.invoke(self, "atIndex", [index])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        """converts and return the string expression."""
        return jsii.invoke(self, "toString", [])

    @jsii.member(jsii_name="withAttribute")
    def with_attribute(self, attr: builtins.str) -> "DynamoProjectionExpression":
        """Adds the passed attribute to the chain.

        :param attr: Attribute name.
        """
        return jsii.invoke(self, "withAttribute", [attr])


class DynamoPutItem(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoPutItem",
):
    """A StepFunctions task to call DynamoPutItem."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        item: typing.Mapping[builtins.str, DynamoAttributeValue],
        table: aws_cdk.aws_dynamodb.ITable,
        condition_expression: typing.Optional[builtins.str] = None,
        expression_attribute_names: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        expression_attribute_values: typing.Optional[typing.Mapping[builtins.str, DynamoAttributeValue]] = None,
        return_consumed_capacity: typing.Optional[DynamoConsumedCapacity] = None,
        return_item_collection_metrics: typing.Optional[DynamoItemCollectionMetrics] = None,
        return_values: typing.Optional["DynamoReturnValues"] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param item: A map of attribute name/value pairs, one for each attribute. Only the primary key attributes are required; you can optionally provide other attribute name-value pairs for the item.
        :param table: The name of the table where the item should be written .
        :param condition_expression: A condition that must be satisfied in order for a conditional PutItem operation to succeed. Default: - No condition expression
        :param expression_attribute_names: One or more substitution tokens for attribute names in an expression. Default: - No expression attribute names
        :param expression_attribute_values: One or more values that can be substituted in an expression. Default: - No expression attribute values
        :param return_consumed_capacity: Determines the level of detail about provisioned throughput consumption that is returned in the response. Default: DynamoConsumedCapacity.NONE
        :param return_item_collection_metrics: The item collection metrics to returned in the response. Default: DynamoItemCollectionMetrics.NONE
        :param return_values: Use ReturnValues if you want to get the item attributes as they appeared before they were updated with the PutItem request. Default: DynamoReturnValues.NONE
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        """
        props = DynamoPutItemProps(
            item=item,
            table=table,
            condition_expression=condition_expression,
            expression_attribute_names=expression_attribute_names,
            expression_attribute_values=expression_attribute_values,
            return_consumed_capacity=return_consumed_capacity,
            return_item_collection_metrics=return_item_collection_metrics,
            return_values=return_values,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(DynamoPutItem, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoPutItemProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "item": "item",
        "table": "table",
        "condition_expression": "conditionExpression",
        "expression_attribute_names": "expressionAttributeNames",
        "expression_attribute_values": "expressionAttributeValues",
        "return_consumed_capacity": "returnConsumedCapacity",
        "return_item_collection_metrics": "returnItemCollectionMetrics",
        "return_values": "returnValues",
    },
)
class DynamoPutItemProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        item: typing.Mapping[builtins.str, DynamoAttributeValue],
        table: aws_cdk.aws_dynamodb.ITable,
        condition_expression: typing.Optional[builtins.str] = None,
        expression_attribute_names: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        expression_attribute_values: typing.Optional[typing.Mapping[builtins.str, DynamoAttributeValue]] = None,
        return_consumed_capacity: typing.Optional[DynamoConsumedCapacity] = None,
        return_item_collection_metrics: typing.Optional[DynamoItemCollectionMetrics] = None,
        return_values: typing.Optional["DynamoReturnValues"] = None,
    ) -> None:
        """Properties for DynamoPutItem Task.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param item: A map of attribute name/value pairs, one for each attribute. Only the primary key attributes are required; you can optionally provide other attribute name-value pairs for the item.
        :param table: The name of the table where the item should be written .
        :param condition_expression: A condition that must be satisfied in order for a conditional PutItem operation to succeed. Default: - No condition expression
        :param expression_attribute_names: One or more substitution tokens for attribute names in an expression. Default: - No expression attribute names
        :param expression_attribute_values: One or more values that can be substituted in an expression. Default: - No expression attribute values
        :param return_consumed_capacity: Determines the level of detail about provisioned throughput consumption that is returned in the response. Default: DynamoConsumedCapacity.NONE
        :param return_item_collection_metrics: The item collection metrics to returned in the response. Default: DynamoItemCollectionMetrics.NONE
        :param return_values: Use ReturnValues if you want to get the item attributes as they appeared before they were updated with the PutItem request. Default: DynamoReturnValues.NONE
        """
        self._values: typing.Dict[str, typing.Any] = {
            "item": item,
            "table": table,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if condition_expression is not None:
            self._values["condition_expression"] = condition_expression
        if expression_attribute_names is not None:
            self._values["expression_attribute_names"] = expression_attribute_names
        if expression_attribute_values is not None:
            self._values["expression_attribute_values"] = expression_attribute_values
        if return_consumed_capacity is not None:
            self._values["return_consumed_capacity"] = return_consumed_capacity
        if return_item_collection_metrics is not None:
            self._values["return_item_collection_metrics"] = return_item_collection_metrics
        if return_values is not None:
            self._values["return_values"] = return_values

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def item(self) -> typing.Mapping[builtins.str, DynamoAttributeValue]:
        """A map of attribute name/value pairs, one for each attribute.

        Only the primary key attributes are required;
        you can optionally provide other attribute name-value pairs for the item.

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html#DDB-PutItem-request-Item
        """
        result = self._values.get("item")
        assert result is not None, "Required property 'item' is missing"
        return result

    @builtins.property
    def table(self) -> aws_cdk.aws_dynamodb.ITable:
        """The name of the table where the item should be written ."""
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return result

    @builtins.property
    def condition_expression(self) -> typing.Optional[builtins.str]:
        """A condition that must be satisfied in order for a conditional PutItem operation to succeed.

        :default: - No condition expression

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html#DDB-PutItem-request-ConditionExpression
        """
        result = self._values.get("condition_expression")
        return result

    @builtins.property
    def expression_attribute_names(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """One or more substitution tokens for attribute names in an expression.

        :default: - No expression attribute names

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html#DDB-PutItem-request-ExpressionAttributeNames
        """
        result = self._values.get("expression_attribute_names")
        return result

    @builtins.property
    def expression_attribute_values(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, DynamoAttributeValue]]:
        """One or more values that can be substituted in an expression.

        :default: - No expression attribute values

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html#DDB-PutItem-request-ExpressionAttributeValues
        """
        result = self._values.get("expression_attribute_values")
        return result

    @builtins.property
    def return_consumed_capacity(self) -> typing.Optional[DynamoConsumedCapacity]:
        """Determines the level of detail about provisioned throughput consumption that is returned in the response.

        :default: DynamoConsumedCapacity.NONE

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html#DDB-PutItem-request-ReturnConsumedCapacity
        """
        result = self._values.get("return_consumed_capacity")
        return result

    @builtins.property
    def return_item_collection_metrics(
        self,
    ) -> typing.Optional[DynamoItemCollectionMetrics]:
        """The item collection metrics to returned in the response.

        :default: DynamoItemCollectionMetrics.NONE

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/LSI.html#LSI.ItemCollections
        """
        result = self._values.get("return_item_collection_metrics")
        return result

    @builtins.property
    def return_values(self) -> typing.Optional["DynamoReturnValues"]:
        """Use ReturnValues if you want to get the item attributes as they appeared before they were updated with the PutItem request.

        :default: DynamoReturnValues.NONE

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_PutItem.html#DDB-PutItem-request-ReturnValues
        """
        result = self._values.get("return_values")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DynamoPutItemProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoReturnValues")
class DynamoReturnValues(enum.Enum):
    """Use ReturnValues if you want to get the item attributes as they appear before or after they are changed."""

    NONE = "NONE"
    """Nothing is returned."""
    ALL_OLD = "ALL_OLD"
    """Returns all of the attributes of the item."""
    UPDATED_OLD = "UPDATED_OLD"
    """Returns only the updated attributes."""
    ALL_NEW = "ALL_NEW"
    """Returns all of the attributes of the item."""
    UPDATED_NEW = "UPDATED_NEW"
    """Returns only the updated attributes."""


class DynamoUpdateItem(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoUpdateItem",
):
    """A StepFunctions task to call DynamoUpdateItem."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        key: typing.Mapping[builtins.str, DynamoAttributeValue],
        table: aws_cdk.aws_dynamodb.ITable,
        condition_expression: typing.Optional[builtins.str] = None,
        expression_attribute_names: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        expression_attribute_values: typing.Optional[typing.Mapping[builtins.str, DynamoAttributeValue]] = None,
        return_consumed_capacity: typing.Optional[DynamoConsumedCapacity] = None,
        return_item_collection_metrics: typing.Optional[DynamoItemCollectionMetrics] = None,
        return_values: typing.Optional[DynamoReturnValues] = None,
        update_expression: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param key: Primary key of the item to retrieve. For the primary key, you must provide all of the attributes. For example, with a simple primary key, you only need to provide a value for the partition key. For a composite primary key, you must provide values for both the partition key and the sort key.
        :param table: The name of the table containing the requested item.
        :param condition_expression: A condition that must be satisfied in order for a conditional DeleteItem to succeed. Default: - No condition expression
        :param expression_attribute_names: One or more substitution tokens for attribute names in an expression. Default: - No expression attribute names
        :param expression_attribute_values: One or more values that can be substituted in an expression. Default: - No expression attribute values
        :param return_consumed_capacity: Determines the level of detail about provisioned throughput consumption that is returned in the response. Default: DynamoConsumedCapacity.NONE
        :param return_item_collection_metrics: Determines whether item collection metrics are returned. If set to SIZE, the response includes statistics about item collections, if any, that were modified during the operation are returned in the response. If set to NONE (the default), no statistics are returned. Default: DynamoItemCollectionMetrics.NONE
        :param return_values: Use ReturnValues if you want to get the item attributes as they appeared before they were deleted. Default: DynamoReturnValues.NONE
        :param update_expression: An expression that defines one or more attributes to be updated, the action to be performed on them, and new values for them. Default: - No update expression
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        """
        props = DynamoUpdateItemProps(
            key=key,
            table=table,
            condition_expression=condition_expression,
            expression_attribute_names=expression_attribute_names,
            expression_attribute_values=expression_attribute_values,
            return_consumed_capacity=return_consumed_capacity,
            return_item_collection_metrics=return_item_collection_metrics,
            return_values=return_values,
            update_expression=update_expression,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(DynamoUpdateItem, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.DynamoUpdateItemProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "key": "key",
        "table": "table",
        "condition_expression": "conditionExpression",
        "expression_attribute_names": "expressionAttributeNames",
        "expression_attribute_values": "expressionAttributeValues",
        "return_consumed_capacity": "returnConsumedCapacity",
        "return_item_collection_metrics": "returnItemCollectionMetrics",
        "return_values": "returnValues",
        "update_expression": "updateExpression",
    },
)
class DynamoUpdateItemProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        key: typing.Mapping[builtins.str, DynamoAttributeValue],
        table: aws_cdk.aws_dynamodb.ITable,
        condition_expression: typing.Optional[builtins.str] = None,
        expression_attribute_names: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        expression_attribute_values: typing.Optional[typing.Mapping[builtins.str, DynamoAttributeValue]] = None,
        return_consumed_capacity: typing.Optional[DynamoConsumedCapacity] = None,
        return_item_collection_metrics: typing.Optional[DynamoItemCollectionMetrics] = None,
        return_values: typing.Optional[DynamoReturnValues] = None,
        update_expression: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for DynamoUpdateItem Task.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param key: Primary key of the item to retrieve. For the primary key, you must provide all of the attributes. For example, with a simple primary key, you only need to provide a value for the partition key. For a composite primary key, you must provide values for both the partition key and the sort key.
        :param table: The name of the table containing the requested item.
        :param condition_expression: A condition that must be satisfied in order for a conditional DeleteItem to succeed. Default: - No condition expression
        :param expression_attribute_names: One or more substitution tokens for attribute names in an expression. Default: - No expression attribute names
        :param expression_attribute_values: One or more values that can be substituted in an expression. Default: - No expression attribute values
        :param return_consumed_capacity: Determines the level of detail about provisioned throughput consumption that is returned in the response. Default: DynamoConsumedCapacity.NONE
        :param return_item_collection_metrics: Determines whether item collection metrics are returned. If set to SIZE, the response includes statistics about item collections, if any, that were modified during the operation are returned in the response. If set to NONE (the default), no statistics are returned. Default: DynamoItemCollectionMetrics.NONE
        :param return_values: Use ReturnValues if you want to get the item attributes as they appeared before they were deleted. Default: DynamoReturnValues.NONE
        :param update_expression: An expression that defines one or more attributes to be updated, the action to be performed on them, and new values for them. Default: - No update expression
        """
        self._values: typing.Dict[str, typing.Any] = {
            "key": key,
            "table": table,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if condition_expression is not None:
            self._values["condition_expression"] = condition_expression
        if expression_attribute_names is not None:
            self._values["expression_attribute_names"] = expression_attribute_names
        if expression_attribute_values is not None:
            self._values["expression_attribute_values"] = expression_attribute_values
        if return_consumed_capacity is not None:
            self._values["return_consumed_capacity"] = return_consumed_capacity
        if return_item_collection_metrics is not None:
            self._values["return_item_collection_metrics"] = return_item_collection_metrics
        if return_values is not None:
            self._values["return_values"] = return_values
        if update_expression is not None:
            self._values["update_expression"] = update_expression

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def key(self) -> typing.Mapping[builtins.str, DynamoAttributeValue]:
        """Primary key of the item to retrieve.

        For the primary key, you must provide all of the attributes.
        For example, with a simple primary key, you only need to provide a value for the partition key.
        For a composite primary key, you must provide values for both the partition key and the sort key.

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_GetItem.html#DDB-GetItem-request-Key
        """
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return result

    @builtins.property
    def table(self) -> aws_cdk.aws_dynamodb.ITable:
        """The name of the table containing the requested item."""
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return result

    @builtins.property
    def condition_expression(self) -> typing.Optional[builtins.str]:
        """A condition that must be satisfied in order for a conditional DeleteItem to succeed.

        :default: - No condition expression

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html#DDB-UpdateItem-request-ConditionExpression
        """
        result = self._values.get("condition_expression")
        return result

    @builtins.property
    def expression_attribute_names(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """One or more substitution tokens for attribute names in an expression.

        :default: - No expression attribute names

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html#DDB-UpdateItem-request-ExpressionAttributeNames
        """
        result = self._values.get("expression_attribute_names")
        return result

    @builtins.property
    def expression_attribute_values(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, DynamoAttributeValue]]:
        """One or more values that can be substituted in an expression.

        :default: - No expression attribute values

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html#DDB-UpdateItem-request-ExpressionAttributeValues
        """
        result = self._values.get("expression_attribute_values")
        return result

    @builtins.property
    def return_consumed_capacity(self) -> typing.Optional[DynamoConsumedCapacity]:
        """Determines the level of detail about provisioned throughput consumption that is returned in the response.

        :default: DynamoConsumedCapacity.NONE

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html#DDB-UpdateItem-request-ReturnConsumedCapacity
        """
        result = self._values.get("return_consumed_capacity")
        return result

    @builtins.property
    def return_item_collection_metrics(
        self,
    ) -> typing.Optional[DynamoItemCollectionMetrics]:
        """Determines whether item collection metrics are returned.

        If set to SIZE, the response includes statistics about item collections, if any,
        that were modified during the operation are returned in the response.
        If set to NONE (the default), no statistics are returned.

        :default: DynamoItemCollectionMetrics.NONE
        """
        result = self._values.get("return_item_collection_metrics")
        return result

    @builtins.property
    def return_values(self) -> typing.Optional[DynamoReturnValues]:
        """Use ReturnValues if you want to get the item attributes as they appeared before they were deleted.

        :default: DynamoReturnValues.NONE

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html#DDB-UpdateItem-request-ReturnValues
        """
        result = self._values.get("return_values")
        return result

    @builtins.property
    def update_expression(self) -> typing.Optional[builtins.str]:
        """An expression that defines one or more attributes to be updated, the action to be performed on them, and new values for them.

        :default: - No update expression

        :see: https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html#DDB-UpdateItem-request-UpdateExpression
        """
        result = self._values.get("update_expression")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DynamoUpdateItemProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EcsEc2LaunchTargetOptions",
    jsii_struct_bases=[],
    name_mapping={
        "placement_constraints": "placementConstraints",
        "placement_strategies": "placementStrategies",
    },
)
class EcsEc2LaunchTargetOptions:
    def __init__(
        self,
        *,
        placement_constraints: typing.Optional[typing.List[aws_cdk.aws_ecs.PlacementConstraint]] = None,
        placement_strategies: typing.Optional[typing.List[aws_cdk.aws_ecs.PlacementStrategy]] = None,
    ) -> None:
        """Options to run an ECS task on EC2 in StepFunctions and ECS.

        :param placement_constraints: Placement constraints. Default: - None
        :param placement_strategies: Placement strategies. Default: - None
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if placement_constraints is not None:
            self._values["placement_constraints"] = placement_constraints
        if placement_strategies is not None:
            self._values["placement_strategies"] = placement_strategies

    @builtins.property
    def placement_constraints(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ecs.PlacementConstraint]]:
        """Placement constraints.

        :default: - None
        """
        result = self._values.get("placement_constraints")
        return result

    @builtins.property
    def placement_strategies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ecs.PlacementStrategy]]:
        """Placement strategies.

        :default: - None
        """
        result = self._values.get("placement_strategies")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsEc2LaunchTargetOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EcsFargateLaunchTargetOptions",
    jsii_struct_bases=[],
    name_mapping={"platform_version": "platformVersion"},
)
class EcsFargateLaunchTargetOptions:
    def __init__(
        self,
        *,
        platform_version: aws_cdk.aws_ecs.FargatePlatformVersion,
    ) -> None:
        """Properties to define an ECS service.

        :param platform_version: Refers to a specific runtime environment for Fargate task infrastructure. Fargate platform version is a combination of the kernel and container runtime versions.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "platform_version": platform_version,
        }

    @builtins.property
    def platform_version(self) -> aws_cdk.aws_ecs.FargatePlatformVersion:
        """Refers to a specific runtime environment for Fargate task infrastructure.

        Fargate platform version is a combination of the kernel and container runtime versions.

        :see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html
        """
        result = self._values.get("platform_version")
        assert result is not None, "Required property 'platform_version' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsFargateLaunchTargetOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EcsLaunchTargetConfig",
    jsii_struct_bases=[],
    name_mapping={"parameters": "parameters"},
)
class EcsLaunchTargetConfig:
    def __init__(
        self,
        *,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        """Configuration options for the ECS launch type.

        :param parameters: Additional parameters to pass to the base task. Default: - No additional parameters passed
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        """Additional parameters to pass to the base task.

        :default: - No additional parameters passed
        """
        result = self._values.get("parameters")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsLaunchTargetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_ec2.IConnectable)
class EcsRunTask(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EcsRunTask",
):
    """Run a Task on ECS or Fargate."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster: aws_cdk.aws_ecs.ICluster,
        launch_target: "IEcsLaunchTarget",
        task_definition: aws_cdk.aws_ecs.TaskDefinition,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        container_overrides: typing.Optional[typing.List[ContainerOverride]] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster: The ECS cluster to run the task on.
        :param launch_target: An Amazon ECS launch type determines the type of infrastructure on which your tasks and services are hosted.
        :param task_definition: [disable-awslint:ref-via-interface] Task Definition used for running tasks in the service. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions
        :param assign_public_ip: Assign public IP addresses to each task. Default: false
        :param container_overrides: Container setting overrides. Specify the container to use and the overrides to apply. Default: - No overrides
        :param security_groups: Existing security groups to use for the tasks. Default: - A new security group is created
        :param subnets: Subnets to place the task's ENIs. Default: - Public subnets if assignPublicIp is set. Private subnets otherwise.
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        """
        props = EcsRunTaskProps(
            cluster=cluster,
            launch_target=launch_target,
            task_definition=task_definition,
            assign_public_ip=assign_public_ip,
            container_overrides=container_overrides,
            security_groups=security_groups,
            subnets=subnets,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(EcsRunTask, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Manage allowed network traffic for this service."""
        return jsii.get(self, "connections")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        return jsii.get(self, "taskPolicies")


@jsii.implements(aws_cdk.aws_ec2.IConnectable, aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class EcsRunTaskBase(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EcsRunTaskBase",
):
    """A StepFunctions Task to run a Task on ECS or Fargate."""

    def __init__(
        self,
        *,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        cluster: aws_cdk.aws_ecs.ICluster,
        task_definition: aws_cdk.aws_ecs.TaskDefinition,
        container_overrides: typing.Optional[typing.List[ContainerOverride]] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern] = None,
    ) -> None:
        """
        :param parameters: Additional parameters to pass to the base task. Default: - No additional parameters passed
        :param cluster: The topic to run the task on.
        :param task_definition: Task Definition used for running tasks in the service. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions
        :param container_overrides: Container setting overrides. Key is the name of the container to override, value is the values you want to override. Default: - No overrides
        :param integration_pattern: The service integration pattern indicates different ways to call RunTask in ECS. The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET
        """
        props = EcsRunTaskBaseProps(
            parameters=parameters,
            cluster=cluster,
            task_definition=task_definition,
            container_overrides=container_overrides,
            integration_pattern=integration_pattern,
        )

        jsii.create(EcsRunTaskBase, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        task: aws_cdk.aws_stepfunctions.Task,
    ) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """Called when the task object is used in a workflow.

        :param task: -
        """
        return jsii.invoke(self, "bind", [task])

    @jsii.member(jsii_name="configureAwsVpcNetworking")
    def _configure_aws_vpc_networking(
        self,
        vpc: aws_cdk.aws_ec2.IVpc,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
    ) -> None:
        """
        :param vpc: -
        :param assign_public_ip: -
        :param subnet_selection: -
        :param security_group: -
        """
        return jsii.invoke(self, "configureAwsVpcNetworking", [vpc, assign_public_ip, subnet_selection, security_group])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Manage allowed network traffic for this service."""
        return jsii.get(self, "connections")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EcsRunTaskBaseProps",
    jsii_struct_bases=[CommonEcsRunTaskProps],
    name_mapping={
        "cluster": "cluster",
        "task_definition": "taskDefinition",
        "container_overrides": "containerOverrides",
        "integration_pattern": "integrationPattern",
        "parameters": "parameters",
    },
)
class EcsRunTaskBaseProps(CommonEcsRunTaskProps):
    def __init__(
        self,
        *,
        cluster: aws_cdk.aws_ecs.ICluster,
        task_definition: aws_cdk.aws_ecs.TaskDefinition,
        container_overrides: typing.Optional[typing.List[ContainerOverride]] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        """Construction properties for the BaseRunTaskProps.

        :param cluster: The topic to run the task on.
        :param task_definition: Task Definition used for running tasks in the service. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions
        :param container_overrides: Container setting overrides. Key is the name of the container to override, value is the values you want to override. Default: - No overrides
        :param integration_pattern: The service integration pattern indicates different ways to call RunTask in ECS. The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET
        :param parameters: Additional parameters to pass to the base task. Default: - No additional parameters passed
        """
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
            "task_definition": task_definition,
        }
        if container_overrides is not None:
            self._values["container_overrides"] = container_overrides
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """The topic to run the task on."""
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return result

    @builtins.property
    def task_definition(self) -> aws_cdk.aws_ecs.TaskDefinition:
        """Task Definition used for running tasks in the service.

        Note: this must be TaskDefinition, and not ITaskDefinition,
        as it requires properties that are not known for imported task definitions
        """
        result = self._values.get("task_definition")
        assert result is not None, "Required property 'task_definition' is missing"
        return result

    @builtins.property
    def container_overrides(self) -> typing.Optional[typing.List[ContainerOverride]]:
        """Container setting overrides.

        Key is the name of the container to override, value is the
        values you want to override.

        :default: - No overrides
        """
        result = self._values.get("container_overrides")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """The service integration pattern indicates different ways to call RunTask in ECS.

        The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN.

        :default: FIRE_AND_FORGET
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        """Additional parameters to pass to the base task.

        :default: - No additional parameters passed
        """
        result = self._values.get("parameters")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsRunTaskBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EcsRunTaskProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "cluster": "cluster",
        "launch_target": "launchTarget",
        "task_definition": "taskDefinition",
        "assign_public_ip": "assignPublicIp",
        "container_overrides": "containerOverrides",
        "security_groups": "securityGroups",
        "subnets": "subnets",
    },
)
class EcsRunTaskProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        cluster: aws_cdk.aws_ecs.ICluster,
        launch_target: "IEcsLaunchTarget",
        task_definition: aws_cdk.aws_ecs.TaskDefinition,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        container_overrides: typing.Optional[typing.List[ContainerOverride]] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """Properties for ECS Tasks.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param cluster: The ECS cluster to run the task on.
        :param launch_target: An Amazon ECS launch type determines the type of infrastructure on which your tasks and services are hosted.
        :param task_definition: [disable-awslint:ref-via-interface] Task Definition used for running tasks in the service. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions
        :param assign_public_ip: Assign public IP addresses to each task. Default: false
        :param container_overrides: Container setting overrides. Specify the container to use and the overrides to apply. Default: - No overrides
        :param security_groups: Existing security groups to use for the tasks. Default: - A new security group is created
        :param subnets: Subnets to place the task's ENIs. Default: - Public subnets if assignPublicIp is set. Private subnets otherwise.
        """
        if isinstance(subnets, dict):
            subnets = aws_cdk.aws_ec2.SubnetSelection(**subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
            "launch_target": launch_target,
            "task_definition": task_definition,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if assign_public_ip is not None:
            self._values["assign_public_ip"] = assign_public_ip
        if container_overrides is not None:
            self._values["container_overrides"] = container_overrides
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnets is not None:
            self._values["subnets"] = subnets

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """The ECS cluster to run the task on."""
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return result

    @builtins.property
    def launch_target(self) -> "IEcsLaunchTarget":
        """An Amazon ECS launch type determines the type of infrastructure on which your tasks and services are hosted.

        :see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/launch_types.html
        """
        result = self._values.get("launch_target")
        assert result is not None, "Required property 'launch_target' is missing"
        return result

    @builtins.property
    def task_definition(self) -> aws_cdk.aws_ecs.TaskDefinition:
        """[disable-awslint:ref-via-interface] Task Definition used for running tasks in the service.

        Note: this must be TaskDefinition, and not ITaskDefinition,
        as it requires properties that are not known for imported task definitions
        """
        result = self._values.get("task_definition")
        assert result is not None, "Required property 'task_definition' is missing"
        return result

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        """Assign public IP addresses to each task.

        :default: false
        """
        result = self._values.get("assign_public_ip")
        return result

    @builtins.property
    def container_overrides(self) -> typing.Optional[typing.List[ContainerOverride]]:
        """Container setting overrides.

        Specify the container to use and the overrides to apply.

        :default: - No overrides
        """
        result = self._values.get("container_overrides")
        return result

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        """Existing security groups to use for the tasks.

        :default: - A new security group is created
        """
        result = self._values.get("security_groups")
        return result

    @builtins.property
    def subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Subnets to place the task's ENIs.

        :default: - Public subnets if assignPublicIp is set. Private subnets otherwise.
        """
        result = self._values.get("subnets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsRunTaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrAddStep(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrAddStep",
):
    """(experimental) A Step Functions Task to add a Step to an EMR Cluster.

    The StepConfiguration is defined as Parameters in the state machine definition.

    OUTPUT: the StepId

    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster_id: builtins.str,
        jar: builtins.str,
        name: builtins.str,
        action_on_failure: typing.Optional[ActionOnFailure] = None,
        args: typing.Optional[typing.List[builtins.str]] = None,
        main_class: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster_id: (experimental) The ClusterId to add the Step to.
        :param jar: (experimental) A path to a JAR file run during the step.
        :param name: (experimental) The name of the Step.
        :param action_on_failure: (experimental) The action to take when the cluster step fails. Default: ActionOnFailure.CONTINUE
        :param args: (experimental) A list of command line arguments passed to the JAR file's main function when executed. Default: - No args
        :param main_class: (experimental) The name of the main class in the specified Java file. If not specified, the JAR file should specify a Main-Class in its manifest file. Default: - No mainClass
        :param properties: (experimental) A list of Java properties that are set when the step runs. You can use these properties to pass key value pairs to your main function. Default: - No properties
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        :stability: experimental
        """
        props = EmrAddStepProps(
            cluster_id=cluster_id,
            jar=jar,
            name=name,
            action_on_failure=action_on_failure,
            args=args,
            main_class=main_class,
            properties=properties,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(EmrAddStep, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrAddStepProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "cluster_id": "clusterId",
        "jar": "jar",
        "name": "name",
        "action_on_failure": "actionOnFailure",
        "args": "args",
        "main_class": "mainClass",
        "properties": "properties",
    },
)
class EmrAddStepProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        cluster_id: builtins.str,
        jar: builtins.str,
        name: builtins.str,
        action_on_failure: typing.Optional[ActionOnFailure] = None,
        args: typing.Optional[typing.List[builtins.str]] = None,
        main_class: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        """(experimental) Properties for EmrAddStep.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param cluster_id: (experimental) The ClusterId to add the Step to.
        :param jar: (experimental) A path to a JAR file run during the step.
        :param name: (experimental) The name of the Step.
        :param action_on_failure: (experimental) The action to take when the cluster step fails. Default: ActionOnFailure.CONTINUE
        :param args: (experimental) A list of command line arguments passed to the JAR file's main function when executed. Default: - No args
        :param main_class: (experimental) The name of the main class in the specified Java file. If not specified, the JAR file should specify a Main-Class in its manifest file. Default: - No mainClass
        :param properties: (experimental) A list of Java properties that are set when the step runs. You can use these properties to pass key value pairs to your main function. Default: - No properties

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "cluster_id": cluster_id,
            "jar": jar,
            "name": name,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if action_on_failure is not None:
            self._values["action_on_failure"] = action_on_failure
        if args is not None:
            self._values["args"] = args
        if main_class is not None:
            self._values["main_class"] = main_class
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def cluster_id(self) -> builtins.str:
        """(experimental) The ClusterId to add the Step to.

        :stability: experimental
        """
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return result

    @builtins.property
    def jar(self) -> builtins.str:
        """(experimental) A path to a JAR file run during the step.

        :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_HadoopJarStepConfig.html
        :stability: experimental
        """
        result = self._values.get("jar")
        assert result is not None, "Required property 'jar' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """(experimental) The name of the Step.

        :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_StepConfig.html
        :stability: experimental
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def action_on_failure(self) -> typing.Optional[ActionOnFailure]:
        """(experimental) The action to take when the cluster step fails.

        :default: ActionOnFailure.CONTINUE

        :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_StepConfig.html
        :stability: experimental
        """
        result = self._values.get("action_on_failure")
        return result

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        """(experimental) A list of command line arguments passed to the JAR file's main function when executed.

        :default: - No args

        :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_HadoopJarStepConfig.html
        :stability: experimental
        """
        result = self._values.get("args")
        return result

    @builtins.property
    def main_class(self) -> typing.Optional[builtins.str]:
        """(experimental) The name of the main class in the specified Java file.

        If not specified, the JAR file should specify a Main-Class in its manifest file.

        :default: - No mainClass

        :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_HadoopJarStepConfig.html
        :stability: experimental
        """
        result = self._values.get("main_class")
        return result

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) A list of Java properties that are set when the step runs.

        You can use these properties to pass key value pairs to your main function.

        :default: - No properties

        :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_HadoopJarStepConfig.html
        :stability: experimental
        """
        result = self._values.get("properties")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrAddStepProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrCancelStep(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCancelStep",
):
    """(experimental) A Step Functions Task to to cancel a Step on an EMR Cluster.

    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster_id: builtins.str,
        step_id: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster_id: (experimental) The ClusterId to update.
        :param step_id: (experimental) The StepId to cancel.
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        :stability: experimental
        """
        props = EmrCancelStepProps(
            cluster_id=cluster_id,
            step_id=step_id,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(EmrCancelStep, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCancelStepProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "cluster_id": "clusterId",
        "step_id": "stepId",
    },
)
class EmrCancelStepProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        cluster_id: builtins.str,
        step_id: builtins.str,
    ) -> None:
        """(experimental) Properties for EmrCancelStep.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param cluster_id: (experimental) The ClusterId to update.
        :param step_id: (experimental) The StepId to cancel.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "cluster_id": cluster_id,
            "step_id": step_id,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def cluster_id(self) -> builtins.str:
        """(experimental) The ClusterId to update.

        :stability: experimental
        """
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return result

    @builtins.property
    def step_id(self) -> builtins.str:
        """(experimental) The StepId to cancel.

        :stability: experimental
        """
        result = self._values.get("step_id")
        assert result is not None, "Required property 'step_id' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrCancelStepProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrCreateCluster(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster",
):
    """(experimental) A Step Functions Task to create an EMR Cluster.

    The ClusterConfiguration is defined as Parameters in the state machine definition.

    OUTPUT: the ClusterId.

    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        instances: "EmrCreateCluster.InstancesConfigProperty",
        name: builtins.str,
        additional_info: typing.Optional[builtins.str] = None,
        applications: typing.Optional[typing.List["EmrCreateCluster.ApplicationConfigProperty"]] = None,
        auto_scaling_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        bootstrap_actions: typing.Optional[typing.List["EmrCreateCluster.BootstrapActionConfigProperty"]] = None,
        cluster_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        configurations: typing.Optional[typing.List["EmrCreateCluster.ConfigurationProperty"]] = None,
        custom_ami_id: typing.Optional[builtins.str] = None,
        ebs_root_volume_size: typing.Optional[aws_cdk.core.Size] = None,
        kerberos_attributes: typing.Optional["EmrCreateCluster.KerberosAttributesProperty"] = None,
        log_uri: typing.Optional[builtins.str] = None,
        release_label: typing.Optional[builtins.str] = None,
        scale_down_behavior: typing.Optional["EmrCreateCluster.EmrClusterScaleDownBehavior"] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        service_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        visible_to_all_users: typing.Optional[builtins.bool] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param instances: (experimental) A specification of the number and type of Amazon EC2 instances.
        :param name: (experimental) The Name of the Cluster.
        :param additional_info: (experimental) A JSON string for selecting additional features. Default: - None
        :param applications: (experimental) A case-insensitive list of applications for Amazon EMR to install and configure when launching the cluster. Default: - EMR selected default
        :param auto_scaling_role: (experimental) An IAM role for automatic scaling policies. Default: - A role will be created.
        :param bootstrap_actions: (experimental) A list of bootstrap actions to run before Hadoop starts on the cluster nodes. Default: - None
        :param cluster_role: (experimental) Also called instance profile and EC2 role. An IAM role for an EMR cluster. The EC2 instances of the cluster assume this role. This attribute has been renamed from jobFlowRole to clusterRole to align with other ERM/StepFunction integration parameters. Default: - - A Role will be created
        :param configurations: (experimental) The list of configurations supplied for the EMR cluster you are creating. Default: - None
        :param custom_ami_id: (experimental) The ID of a custom Amazon EBS-backed Linux AMI. Default: - None
        :param ebs_root_volume_size: (experimental) The size of the EBS root device volume of the Linux AMI that is used for each EC2 instance. Default: - EMR selected default
        :param kerberos_attributes: (experimental) Attributes for Kerberos configuration when Kerberos authentication is enabled using a security configuration. Default: - None
        :param log_uri: (experimental) The location in Amazon S3 to write the log files of the job flow. Default: - None
        :param release_label: (experimental) The Amazon EMR release label, which determines the version of open-source application packages installed on the cluster. Default: - EMR selected default
        :param scale_down_behavior: (experimental) Specifies the way that individual Amazon EC2 instances terminate when an automatic scale-in activity occurs or an instance group is resized. Default: - EMR selected default
        :param security_configuration: (experimental) The name of a security configuration to apply to the cluster. Default: - None
        :param service_role: (experimental) The IAM role that will be assumed by the Amazon EMR service to access AWS resources on your behalf. Default: - A role will be created that Amazon EMR service can assume.
        :param tags: (experimental) A list of tags to associate with a cluster and propagate to Amazon EC2 instances. Default: - None
        :param visible_to_all_users: (experimental) A value of true indicates that all IAM users in the AWS account can perform cluster actions if they have the proper IAM policy permissions. Default: true
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        :stability: experimental
        """
        props = EmrCreateClusterProps(
            instances=instances,
            name=name,
            additional_info=additional_info,
            applications=applications,
            auto_scaling_role=auto_scaling_role,
            bootstrap_actions=bootstrap_actions,
            cluster_role=cluster_role,
            configurations=configurations,
            custom_ami_id=custom_ami_id,
            ebs_root_volume_size=ebs_root_volume_size,
            kerberos_attributes=kerberos_attributes,
            log_uri=log_uri,
            release_label=release_label,
            scale_down_behavior=scale_down_behavior,
            security_configuration=security_configuration,
            service_role=service_role,
            tags=tags,
            visible_to_all_users=visible_to_all_users,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(EmrCreateCluster, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="autoScalingRole")
    def auto_scaling_role(self) -> aws_cdk.aws_iam.IRole:
        """(experimental) The autoscaling role for the EMR Cluster.

        Only available after task has been added to a state machine.

        :stability: experimental
        """
        return jsii.get(self, "autoScalingRole")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterRole")
    def cluster_role(self) -> aws_cdk.aws_iam.IRole:
        """(experimental) The instance role for the EMR Cluster.

        Only available after task has been added to a state machine.

        :stability: experimental
        """
        return jsii.get(self, "clusterRole")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="serviceRole")
    def service_role(self) -> aws_cdk.aws_iam.IRole:
        """(experimental) The service role for the EMR Cluster.

        Only available after task has been added to a state machine.

        :stability: experimental
        """
        return jsii.get(self, "serviceRole")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.ApplicationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "additional_info": "additionalInfo",
            "args": "args",
            "version": "version",
        },
    )
    class ApplicationConfigProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            additional_info: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
            args: typing.Optional[typing.List[builtins.str]] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            """(experimental) Properties for the EMR Cluster Applications.

            Applies to Amazon EMR releases 4.0 and later. A case-insensitive list of applications for Amazon EMR to install and configure when launching
            the cluster.

            See the RunJobFlow API for complete documentation on input parameters

            :param name: (experimental) The name of the application.
            :param additional_info: (experimental) This option is for advanced users only. This is meta information about third-party applications that third-party vendors use for testing purposes. Default: No additionalInfo
            :param args: (experimental) Arguments for Amazon EMR to pass to the application. Default: No args
            :param version: (experimental) The version of the application. Default: No version

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_Application.html
            :stability: experimental
            """
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
            }
            if additional_info is not None:
                self._values["additional_info"] = additional_info
            if args is not None:
                self._values["args"] = args
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def name(self) -> builtins.str:
            """(experimental) The name of the application.

            :stability: experimental
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def additional_info(
            self,
        ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
            """(experimental) This option is for advanced users only.

            This is meta information about third-party applications that third-party vendors use
            for testing purposes.

            :default: No additionalInfo

            :stability: experimental
            """
            result = self._values.get("additional_info")
            return result

        @builtins.property
        def args(self) -> typing.Optional[typing.List[builtins.str]]:
            """(experimental) Arguments for Amazon EMR to pass to the application.

            :default: No args

            :stability: experimental
            """
            result = self._values.get("args")
            return result

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            """(experimental) The version of the application.

            :default: No version

            :stability: experimental
            """
            result = self._values.get("version")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.AutoScalingPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"constraints": "constraints", "rules": "rules"},
    )
    class AutoScalingPolicyProperty:
        def __init__(
            self,
            *,
            constraints: "EmrCreateCluster.ScalingConstraintsProperty",
            rules: typing.List["EmrCreateCluster.ScalingRuleProperty"],
        ) -> None:
            """(experimental) An automatic scaling policy for a core instance group or task instance group in an Amazon EMR cluster.

            :param constraints: (experimental) The upper and lower EC2 instance limits for an automatic scaling policy. Automatic scaling activity will not cause an instance group to grow above or below these limits.
            :param rules: (experimental) The scale-in and scale-out rules that comprise the automatic scaling policy.

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_AutoScalingPolicy.html
            :stability: experimental
            """
            if isinstance(constraints, dict):
                constraints = ScalingConstraintsProperty(**constraints)
            self._values: typing.Dict[str, typing.Any] = {
                "constraints": constraints,
                "rules": rules,
            }

        @builtins.property
        def constraints(self) -> "EmrCreateCluster.ScalingConstraintsProperty":
            """(experimental) The upper and lower EC2 instance limits for an automatic scaling policy.

            Automatic scaling activity will not cause an instance
            group to grow above or below these limits.

            :stability: experimental
            """
            result = self._values.get("constraints")
            assert result is not None, "Required property 'constraints' is missing"
            return result

        @builtins.property
        def rules(self) -> typing.List["EmrCreateCluster.ScalingRuleProperty"]:
            """(experimental) The scale-in and scale-out rules that comprise the automatic scaling policy.

            :stability: experimental
            """
            result = self._values.get("rules")
            assert result is not None, "Required property 'rules' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoScalingPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.BootstrapActionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "script_bootstrap_action": "scriptBootstrapAction",
        },
    )
    class BootstrapActionConfigProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            script_bootstrap_action: "EmrCreateCluster.ScriptBootstrapActionConfigProperty",
        ) -> None:
            """(experimental) Configuration of a bootstrap action.

            See the RunJobFlow API for complete documentation on input parameters

            :param name: (experimental) The name of the bootstrap action.
            :param script_bootstrap_action: (experimental) The script run by the bootstrap action.

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_BootstrapActionConfig.html
            :stability: experimental
            """
            if isinstance(script_bootstrap_action, dict):
                script_bootstrap_action = ScriptBootstrapActionConfigProperty(**script_bootstrap_action)
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "script_bootstrap_action": script_bootstrap_action,
            }

        @builtins.property
        def name(self) -> builtins.str:
            """(experimental) The name of the bootstrap action.

            :stability: experimental
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def script_bootstrap_action(
            self,
        ) -> "EmrCreateCluster.ScriptBootstrapActionConfigProperty":
            """(experimental) The script run by the bootstrap action.

            :stability: experimental
            """
            result = self._values.get("script_bootstrap_action")
            assert result is not None, "Required property 'script_bootstrap_action' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BootstrapActionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.enum(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.CloudWatchAlarmComparisonOperator"
    )
    class CloudWatchAlarmComparisonOperator(enum.Enum):
        """(experimental) CloudWatch Alarm Comparison Operators.

        :stability: experimental
        """

        GREATER_THAN_OR_EQUAL = "GREATER_THAN_OR_EQUAL"
        """(experimental) GREATER_THAN_OR_EQUAL.

        :stability: experimental
        """
        GREATER_THAN = "GREATER_THAN"
        """(experimental) GREATER_THAN.

        :stability: experimental
        """
        LESS_THAN = "LESS_THAN"
        """(experimental) LESS_THAN.

        :stability: experimental
        """
        LESS_THAN_OR_EQUAL = "LESS_THAN_OR_EQUAL"
        """(experimental) LESS_THAN_OR_EQUAL.

        :stability: experimental
        """

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.CloudWatchAlarmDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "comparison_operator": "comparisonOperator",
            "metric_name": "metricName",
            "period": "period",
            "dimensions": "dimensions",
            "evaluation_periods": "evaluationPeriods",
            "namespace": "namespace",
            "statistic": "statistic",
            "threshold": "threshold",
            "unit": "unit",
        },
    )
    class CloudWatchAlarmDefinitionProperty:
        def __init__(
            self,
            *,
            comparison_operator: "EmrCreateCluster.CloudWatchAlarmComparisonOperator",
            metric_name: builtins.str,
            period: aws_cdk.core.Duration,
            dimensions: typing.Optional[typing.List["EmrCreateCluster.MetricDimensionProperty"]] = None,
            evaluation_periods: typing.Optional[jsii.Number] = None,
            namespace: typing.Optional[builtins.str] = None,
            statistic: typing.Optional["EmrCreateCluster.CloudWatchAlarmStatistic"] = None,
            threshold: typing.Optional[jsii.Number] = None,
            unit: typing.Optional["EmrCreateCluster.CloudWatchAlarmUnit"] = None,
        ) -> None:
            """(experimental) The definition of a CloudWatch metric alarm, which determines when an automatic scaling activity is triggered.

            When the defined alarm conditions
            are satisfied, scaling activity begins.

            :param comparison_operator: (experimental) Determines how the metric specified by MetricName is compared to the value specified by Threshold.
            :param metric_name: (experimental) The name of the CloudWatch metric that is watched to determine an alarm condition.
            :param period: (experimental) The period, in seconds, over which the statistic is applied. EMR CloudWatch metrics are emitted every five minutes (300 seconds), so if an EMR CloudWatch metric is specified, specify 300.
            :param dimensions: (experimental) A CloudWatch metric dimension. Default: - No dimensions
            :param evaluation_periods: (experimental) The number of periods, in five-minute increments, during which the alarm condition must exist before the alarm triggers automatic scaling activity. Default: 1
            :param namespace: (experimental) The namespace for the CloudWatch metric. Default: 'AWS/ElasticMapReduce'
            :param statistic: (experimental) The statistic to apply to the metric associated with the alarm. Default: CloudWatchAlarmStatistic.AVERAGE
            :param threshold: (experimental) The value against which the specified statistic is compared. Default: - None
            :param unit: (experimental) The unit of measure associated with the CloudWatch metric being watched. The value specified for Unit must correspond to the units specified in the CloudWatch metric. Default: CloudWatchAlarmUnit.NONE

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_CloudWatchAlarmDefinition.html
            :stability: experimental
            """
            self._values: typing.Dict[str, typing.Any] = {
                "comparison_operator": comparison_operator,
                "metric_name": metric_name,
                "period": period,
            }
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if evaluation_periods is not None:
                self._values["evaluation_periods"] = evaluation_periods
            if namespace is not None:
                self._values["namespace"] = namespace
            if statistic is not None:
                self._values["statistic"] = statistic
            if threshold is not None:
                self._values["threshold"] = threshold
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def comparison_operator(
            self,
        ) -> "EmrCreateCluster.CloudWatchAlarmComparisonOperator":
            """(experimental) Determines how the metric specified by MetricName is compared to the value specified by Threshold.

            :stability: experimental
            """
            result = self._values.get("comparison_operator")
            assert result is not None, "Required property 'comparison_operator' is missing"
            return result

        @builtins.property
        def metric_name(self) -> builtins.str:
            """(experimental) The name of the CloudWatch metric that is watched to determine an alarm condition.

            :stability: experimental
            """
            result = self._values.get("metric_name")
            assert result is not None, "Required property 'metric_name' is missing"
            return result

        @builtins.property
        def period(self) -> aws_cdk.core.Duration:
            """(experimental) The period, in seconds, over which the statistic is applied.

            EMR CloudWatch metrics are emitted every five minutes (300 seconds), so if
            an EMR CloudWatch metric is specified, specify 300.

            :stability: experimental
            """
            result = self._values.get("period")
            assert result is not None, "Required property 'period' is missing"
            return result

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.List["EmrCreateCluster.MetricDimensionProperty"]]:
            """(experimental) A CloudWatch metric dimension.

            :default: - No dimensions

            :stability: experimental
            """
            result = self._values.get("dimensions")
            return result

        @builtins.property
        def evaluation_periods(self) -> typing.Optional[jsii.Number]:
            """(experimental) The number of periods, in five-minute increments, during which the alarm condition must exist before the alarm triggers automatic scaling activity.

            :default: 1

            :stability: experimental
            """
            result = self._values.get("evaluation_periods")
            return result

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            """(experimental) The namespace for the CloudWatch metric.

            :default: 'AWS/ElasticMapReduce'

            :stability: experimental
            """
            result = self._values.get("namespace")
            return result

        @builtins.property
        def statistic(
            self,
        ) -> typing.Optional["EmrCreateCluster.CloudWatchAlarmStatistic"]:
            """(experimental) The statistic to apply to the metric associated with the alarm.

            :default: CloudWatchAlarmStatistic.AVERAGE

            :stability: experimental
            """
            result = self._values.get("statistic")
            return result

        @builtins.property
        def threshold(self) -> typing.Optional[jsii.Number]:
            """(experimental) The value against which the specified statistic is compared.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("threshold")
            return result

        @builtins.property
        def unit(self) -> typing.Optional["EmrCreateCluster.CloudWatchAlarmUnit"]:
            """(experimental) The unit of measure associated with the CloudWatch metric being watched.

            The value specified for Unit must correspond to the units
            specified in the CloudWatch metric.

            :default: CloudWatchAlarmUnit.NONE

            :stability: experimental
            """
            result = self._values.get("unit")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchAlarmDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.enum(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.CloudWatchAlarmStatistic"
    )
    class CloudWatchAlarmStatistic(enum.Enum):
        """(experimental) CloudWatch Alarm Statistics.

        :stability: experimental
        """

        SAMPLE_COUNT = "SAMPLE_COUNT"
        """(experimental) SAMPLE_COUNT.

        :stability: experimental
        """
        AVERAGE = "AVERAGE"
        """(experimental) AVERAGE.

        :stability: experimental
        """
        SUM = "SUM"
        """(experimental) SUM.

        :stability: experimental
        """
        MINIMUM = "MINIMUM"
        """(experimental) MINIMUM.

        :stability: experimental
        """
        MAXIMUM = "MAXIMUM"
        """(experimental) MAXIMUM.

        :stability: experimental
        """

    @jsii.enum(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.CloudWatchAlarmUnit"
    )
    class CloudWatchAlarmUnit(enum.Enum):
        """(experimental) CloudWatch Alarm Units.

        :stability: experimental
        """

        NONE = "NONE"
        """(experimental) NONE.

        :stability: experimental
        """
        SECONDS = "SECONDS"
        """(experimental) SECONDS.

        :stability: experimental
        """
        MICRO_SECONDS = "MICRO_SECONDS"
        """(experimental) MICRO_SECONDS.

        :stability: experimental
        """
        MILLI_SECONDS = "MILLI_SECONDS"
        """(experimental) MILLI_SECONDS.

        :stability: experimental
        """
        BYTES = "BYTES"
        """(experimental) BYTES.

        :stability: experimental
        """
        KILO_BYTES = "KILO_BYTES"
        """(experimental) KILO_BYTES.

        :stability: experimental
        """
        MEGA_BYTES = "MEGA_BYTES"
        """(experimental) MEGA_BYTES.

        :stability: experimental
        """
        GIGA_BYTES = "GIGA_BYTES"
        """(experimental) GIGA_BYTES.

        :stability: experimental
        """
        TERA_BYTES = "TERA_BYTES"
        """(experimental) TERA_BYTES.

        :stability: experimental
        """
        BITS = "BITS"
        """(experimental) BITS.

        :stability: experimental
        """
        KILO_BITS = "KILO_BITS"
        """(experimental) KILO_BITS.

        :stability: experimental
        """
        MEGA_BITS = "MEGA_BITS"
        """(experimental) MEGA_BITS.

        :stability: experimental
        """
        GIGA_BITS = "GIGA_BITS"
        """(experimental) GIGA_BITS.

        :stability: experimental
        """
        TERA_BITS = "TERA_BITS"
        """(experimental) TERA_BITS.

        :stability: experimental
        """
        PERCENT = "PERCENT"
        """(experimental) PERCENT.

        :stability: experimental
        """
        COUNT = "COUNT"
        """(experimental) COUNT.

        :stability: experimental
        """
        BYTES_PER_SECOND = "BYTES_PER_SECOND"
        """(experimental) BYTES_PER_SECOND.

        :stability: experimental
        """
        KILO_BYTES_PER_SECOND = "KILO_BYTES_PER_SECOND"
        """(experimental) KILO_BYTES_PER_SECOND.

        :stability: experimental
        """
        MEGA_BYTES_PER_SECOND = "MEGA_BYTES_PER_SECOND"
        """(experimental) MEGA_BYTES_PER_SECOND.

        :stability: experimental
        """
        GIGA_BYTES_PER_SECOND = "GIGA_BYTES_PER_SECOND"
        """(experimental) GIGA_BYTES_PER_SECOND.

        :stability: experimental
        """
        TERA_BYTES_PER_SECOND = "TERA_BYTES_PER_SECOND"
        """(experimental) TERA_BYTES_PER_SECOND.

        :stability: experimental
        """
        BITS_PER_SECOND = "BITS_PER_SECOND"
        """(experimental) BITS_PER_SECOND.

        :stability: experimental
        """
        KILO_BITS_PER_SECOND = "KILO_BITS_PER_SECOND"
        """(experimental) KILO_BITS_PER_SECOND.

        :stability: experimental
        """
        MEGA_BITS_PER_SECOND = "MEGA_BITS_PER_SECOND"
        """(experimental) MEGA_BITS_PER_SECOND.

        :stability: experimental
        """
        GIGA_BITS_PER_SECOND = "GIGA_BITS_PER_SECOND"
        """(experimental) GIGA_BITS_PER_SECOND.

        :stability: experimental
        """
        TERA_BITS_PER_SECOND = "TERA_BITS_PER_SECOND"
        """(experimental) TERA_BITS_PER_SECOND.

        :stability: experimental
        """
        COUNT_PER_SECOND = "COUNT_PER_SECOND"
        """(experimental) COUNT_PER_SECOND.

        :stability: experimental
        """

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "classification": "classification",
            "configurations": "configurations",
            "properties": "properties",
        },
    )
    class ConfigurationProperty:
        def __init__(
            self,
            *,
            classification: typing.Optional[builtins.str] = None,
            configurations: typing.Optional[typing.List["EmrCreateCluster.ConfigurationProperty"]] = None,
            properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        ) -> None:
            """(experimental) An optional configuration specification to be used when provisioning cluster instances, which can include configurations for applications and software bundled with Amazon EMR.

            See the RunJobFlow API for complete documentation on input parameters

            :param classification: (experimental) The classification within a configuration. Default: No classification
            :param configurations: (experimental) A list of additional configurations to apply within a configuration object. Default: No configurations
            :param properties: (experimental) A set of properties specified within a configuration classification. Default: No properties

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_Configuration.html
            :stability: experimental
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if classification is not None:
                self._values["classification"] = classification
            if configurations is not None:
                self._values["configurations"] = configurations
            if properties is not None:
                self._values["properties"] = properties

        @builtins.property
        def classification(self) -> typing.Optional[builtins.str]:
            """(experimental) The classification within a configuration.

            :default: No classification

            :stability: experimental
            """
            result = self._values.get("classification")
            return result

        @builtins.property
        def configurations(
            self,
        ) -> typing.Optional[typing.List["EmrCreateCluster.ConfigurationProperty"]]:
            """(experimental) A list of additional configurations to apply within a configuration object.

            :default: No configurations

            :stability: experimental
            """
            result = self._values.get("configurations")
            return result

        @builtins.property
        def properties(
            self,
        ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
            """(experimental) A set of properties specified within a configuration classification.

            :default: No properties

            :stability: experimental
            """
            result = self._values.get("properties")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.EbsBlockDeviceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "volume_specification": "volumeSpecification",
            "volumes_per_instance": "volumesPerInstance",
        },
    )
    class EbsBlockDeviceConfigProperty:
        def __init__(
            self,
            *,
            volume_specification: "EmrCreateCluster.VolumeSpecificationProperty",
            volumes_per_instance: typing.Optional[jsii.Number] = None,
        ) -> None:
            """(experimental) Configuration of requested EBS block device associated with the instance group with count of volumes that will be associated to every instance.

            :param volume_specification: (experimental) EBS volume specifications such as volume type, IOPS, and size (GiB) that will be requested for the EBS volume attached to an EC2 instance in the cluster.
            :param volumes_per_instance: (experimental) Number of EBS volumes with a specific volume configuration that will be associated with every instance in the instance group. Default: EMR selected default

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_EbsBlockDeviceConfig.html
            :stability: experimental
            """
            if isinstance(volume_specification, dict):
                volume_specification = VolumeSpecificationProperty(**volume_specification)
            self._values: typing.Dict[str, typing.Any] = {
                "volume_specification": volume_specification,
            }
            if volumes_per_instance is not None:
                self._values["volumes_per_instance"] = volumes_per_instance

        @builtins.property
        def volume_specification(
            self,
        ) -> "EmrCreateCluster.VolumeSpecificationProperty":
            """(experimental) EBS volume specifications such as volume type, IOPS, and size (GiB) that will be requested for the EBS volume attached to an EC2 instance in the cluster.

            :stability: experimental
            """
            result = self._values.get("volume_specification")
            assert result is not None, "Required property 'volume_specification' is missing"
            return result

        @builtins.property
        def volumes_per_instance(self) -> typing.Optional[jsii.Number]:
            """(experimental) Number of EBS volumes with a specific volume configuration that will be associated with every instance in the instance group.

            :default: EMR selected default

            :stability: experimental
            """
            result = self._values.get("volumes_per_instance")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EbsBlockDeviceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.enum(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.EbsBlockDeviceVolumeType"
    )
    class EbsBlockDeviceVolumeType(enum.Enum):
        """(experimental) EBS Volume Types.

        :stability: experimental
        """

        GP2 = "GP2"
        """(experimental) gp2 Volume Type.

        :stability: experimental
        """
        IO1 = "IO1"
        """(experimental) io1 Volume Type.

        :stability: experimental
        """
        STANDARD = "STANDARD"
        """(experimental) Standard Volume Type.

        :stability: experimental
        """

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.EbsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ebs_block_device_configs": "ebsBlockDeviceConfigs",
            "ebs_optimized": "ebsOptimized",
        },
    )
    class EbsConfigurationProperty:
        def __init__(
            self,
            *,
            ebs_block_device_configs: typing.Optional[typing.List["EmrCreateCluster.EbsBlockDeviceConfigProperty"]] = None,
            ebs_optimized: typing.Optional[builtins.bool] = None,
        ) -> None:
            """(experimental) The Amazon EBS configuration of a cluster instance.

            :param ebs_block_device_configs: (experimental) An array of Amazon EBS volume specifications attached to a cluster instance. Default: - None
            :param ebs_optimized: (experimental) Indicates whether an Amazon EBS volume is EBS-optimized. Default: - EMR selected default

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_EbsConfiguration.html
            :stability: experimental
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if ebs_block_device_configs is not None:
                self._values["ebs_block_device_configs"] = ebs_block_device_configs
            if ebs_optimized is not None:
                self._values["ebs_optimized"] = ebs_optimized

        @builtins.property
        def ebs_block_device_configs(
            self,
        ) -> typing.Optional[typing.List["EmrCreateCluster.EbsBlockDeviceConfigProperty"]]:
            """(experimental) An array of Amazon EBS volume specifications attached to a cluster instance.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("ebs_block_device_configs")
            return result

        @builtins.property
        def ebs_optimized(self) -> typing.Optional[builtins.bool]:
            """(experimental) Indicates whether an Amazon EBS volume is EBS-optimized.

            :default: - EMR selected default

            :stability: experimental
            """
            result = self._values.get("ebs_optimized")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EbsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.enum(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.EmrClusterScaleDownBehavior"
    )
    class EmrClusterScaleDownBehavior(enum.Enum):
        """(experimental) Valid valus for the Cluster ScaleDownBehavior.

        :stability: experimental
        """

        TERMINATE_AT_INSTANCE_HOUR = "TERMINATE_AT_INSTANCE_HOUR"
        """(experimental) Indicates that Amazon EMR terminates nodes at the instance-hour boundary, regardless of when the request to terminate the instance was submitted.

        This option is only available with Amazon EMR 5.1.0 and later and is the default for clusters created using that version

        :stability: experimental
        """
        TERMINATE_AT_TASK_COMPLETION = "TERMINATE_AT_TASK_COMPLETION"
        """(experimental) Indicates that Amazon EMR blacklists and drains tasks from nodes before terminating the Amazon EC2 instances, regardless of the instance-hour boundary.

        :stability: experimental
        """

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.InstanceFleetConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instance_fleet_type": "instanceFleetType",
            "instance_type_configs": "instanceTypeConfigs",
            "launch_specifications": "launchSpecifications",
            "name": "name",
            "target_on_demand_capacity": "targetOnDemandCapacity",
            "target_spot_capacity": "targetSpotCapacity",
        },
    )
    class InstanceFleetConfigProperty:
        def __init__(
            self,
            *,
            instance_fleet_type: "EmrCreateCluster.InstanceRoleType",
            instance_type_configs: typing.Optional[typing.List["EmrCreateCluster.InstanceTypeConfigProperty"]] = None,
            launch_specifications: typing.Optional["EmrCreateCluster.InstanceFleetProvisioningSpecificationsProperty"] = None,
            name: typing.Optional[builtins.str] = None,
            target_on_demand_capacity: typing.Optional[jsii.Number] = None,
            target_spot_capacity: typing.Optional[jsii.Number] = None,
        ) -> None:
            """(experimental) The configuration that defines an instance fleet.

            :param instance_fleet_type: (experimental) The node type that the instance fleet hosts. Valid values are MASTER,CORE,and TASK.
            :param instance_type_configs: (experimental) The instance type configurations that define the EC2 instances in the instance fleet. Default: No instanceTpeConfigs
            :param launch_specifications: (experimental) The launch specification for the instance fleet. Default: No launchSpecifications
            :param name: (experimental) The friendly name of the instance fleet. Default: No name
            :param target_on_demand_capacity: (experimental) The target capacity of On-Demand units for the instance fleet, which determines how many On-Demand instances to provision. Default: No targetOnDemandCapacity
            :param target_spot_capacity: (experimental) The target capacity of Spot units for the instance fleet, which determines how many Spot instances to provision. Default: No targetSpotCapacity

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_InstanceFleetConfig.html
            :stability: experimental
            """
            if isinstance(launch_specifications, dict):
                launch_specifications = InstanceFleetProvisioningSpecificationsProperty(**launch_specifications)
            self._values: typing.Dict[str, typing.Any] = {
                "instance_fleet_type": instance_fleet_type,
            }
            if instance_type_configs is not None:
                self._values["instance_type_configs"] = instance_type_configs
            if launch_specifications is not None:
                self._values["launch_specifications"] = launch_specifications
            if name is not None:
                self._values["name"] = name
            if target_on_demand_capacity is not None:
                self._values["target_on_demand_capacity"] = target_on_demand_capacity
            if target_spot_capacity is not None:
                self._values["target_spot_capacity"] = target_spot_capacity

        @builtins.property
        def instance_fleet_type(self) -> "EmrCreateCluster.InstanceRoleType":
            """(experimental) The node type that the instance fleet hosts.

            Valid values are MASTER,CORE,and TASK.

            :stability: experimental
            """
            result = self._values.get("instance_fleet_type")
            assert result is not None, "Required property 'instance_fleet_type' is missing"
            return result

        @builtins.property
        def instance_type_configs(
            self,
        ) -> typing.Optional[typing.List["EmrCreateCluster.InstanceTypeConfigProperty"]]:
            """(experimental) The instance type configurations that define the EC2 instances in the instance fleet.

            :default: No instanceTpeConfigs

            :stability: experimental
            """
            result = self._values.get("instance_type_configs")
            return result

        @builtins.property
        def launch_specifications(
            self,
        ) -> typing.Optional["EmrCreateCluster.InstanceFleetProvisioningSpecificationsProperty"]:
            """(experimental) The launch specification for the instance fleet.

            :default: No launchSpecifications

            :stability: experimental
            """
            result = self._values.get("launch_specifications")
            return result

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            """(experimental) The friendly name of the instance fleet.

            :default: No name

            :stability: experimental
            """
            result = self._values.get("name")
            return result

        @builtins.property
        def target_on_demand_capacity(self) -> typing.Optional[jsii.Number]:
            """(experimental) The target capacity of On-Demand units for the instance fleet, which determines how many On-Demand instances to provision.

            :default: No targetOnDemandCapacity

            :stability: experimental
            """
            result = self._values.get("target_on_demand_capacity")
            return result

        @builtins.property
        def target_spot_capacity(self) -> typing.Optional[jsii.Number]:
            """(experimental) The target capacity of Spot units for the instance fleet, which determines how many Spot instances to provision.

            :default: No targetSpotCapacity

            :stability: experimental
            """
            result = self._values.get("target_spot_capacity")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceFleetConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.InstanceFleetProvisioningSpecificationsProperty",
        jsii_struct_bases=[],
        name_mapping={"spot_specification": "spotSpecification"},
    )
    class InstanceFleetProvisioningSpecificationsProperty:
        def __init__(
            self,
            *,
            spot_specification: "EmrCreateCluster.SpotProvisioningSpecificationProperty",
        ) -> None:
            """(experimental) The launch specification for Spot instances in the fleet, which determines the defined duration and provisioning timeout behavior.

            :param spot_specification: (experimental) The launch specification for Spot instances in the fleet, which determines the defined duration and provisioning timeout behavior.

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_InstanceFleetProvisioningSpecifications.html
            :stability: experimental
            """
            if isinstance(spot_specification, dict):
                spot_specification = SpotProvisioningSpecificationProperty(**spot_specification)
            self._values: typing.Dict[str, typing.Any] = {
                "spot_specification": spot_specification,
            }

        @builtins.property
        def spot_specification(
            self,
        ) -> "EmrCreateCluster.SpotProvisioningSpecificationProperty":
            """(experimental) The launch specification for Spot instances in the fleet, which determines the defined duration and provisioning timeout behavior.

            :stability: experimental
            """
            result = self._values.get("spot_specification")
            assert result is not None, "Required property 'spot_specification' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceFleetProvisioningSpecificationsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.InstanceGroupConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instance_count": "instanceCount",
            "instance_role": "instanceRole",
            "instance_type": "instanceType",
            "auto_scaling_policy": "autoScalingPolicy",
            "bid_price": "bidPrice",
            "configurations": "configurations",
            "ebs_configuration": "ebsConfiguration",
            "market": "market",
            "name": "name",
        },
    )
    class InstanceGroupConfigProperty:
        def __init__(
            self,
            *,
            instance_count: jsii.Number,
            instance_role: "EmrCreateCluster.InstanceRoleType",
            instance_type: builtins.str,
            auto_scaling_policy: typing.Optional["EmrCreateCluster.AutoScalingPolicyProperty"] = None,
            bid_price: typing.Optional[builtins.str] = None,
            configurations: typing.Optional[typing.List["EmrCreateCluster.ConfigurationProperty"]] = None,
            ebs_configuration: typing.Optional["EmrCreateCluster.EbsConfigurationProperty"] = None,
            market: typing.Optional["EmrCreateCluster.InstanceMarket"] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            """(experimental) Configuration defining a new instance group.

            :param instance_count: (experimental) Target number of instances for the instance group.
            :param instance_role: (experimental) The role of the instance group in the cluster.
            :param instance_type: (experimental) The EC2 instance type for all instances in the instance group.
            :param auto_scaling_policy: (experimental) An automatic scaling policy for a core instance group or task instance group in an Amazon EMR cluster. Default: - None
            :param bid_price: (experimental) The bid price for each EC2 Spot instance type as defined by InstanceType. Expressed in USD. Default: - None
            :param configurations: (experimental) The list of configurations supplied for an EMR cluster instance group. Default: - None
            :param ebs_configuration: (experimental) EBS configurations that will be attached to each EC2 instance in the instance group. Default: - None
            :param market: (experimental) Market type of the EC2 instances used to create a cluster node. Default: - EMR selected default
            :param name: (experimental) Friendly name given to the instance group. Default: - None

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_InstanceGroupConfig.html
            :stability: experimental
            """
            if isinstance(auto_scaling_policy, dict):
                auto_scaling_policy = AutoScalingPolicyProperty(**auto_scaling_policy)
            if isinstance(ebs_configuration, dict):
                ebs_configuration = EbsConfigurationProperty(**ebs_configuration)
            self._values: typing.Dict[str, typing.Any] = {
                "instance_count": instance_count,
                "instance_role": instance_role,
                "instance_type": instance_type,
            }
            if auto_scaling_policy is not None:
                self._values["auto_scaling_policy"] = auto_scaling_policy
            if bid_price is not None:
                self._values["bid_price"] = bid_price
            if configurations is not None:
                self._values["configurations"] = configurations
            if ebs_configuration is not None:
                self._values["ebs_configuration"] = ebs_configuration
            if market is not None:
                self._values["market"] = market
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def instance_count(self) -> jsii.Number:
            """(experimental) Target number of instances for the instance group.

            :stability: experimental
            """
            result = self._values.get("instance_count")
            assert result is not None, "Required property 'instance_count' is missing"
            return result

        @builtins.property
        def instance_role(self) -> "EmrCreateCluster.InstanceRoleType":
            """(experimental) The role of the instance group in the cluster.

            :stability: experimental
            """
            result = self._values.get("instance_role")
            assert result is not None, "Required property 'instance_role' is missing"
            return result

        @builtins.property
        def instance_type(self) -> builtins.str:
            """(experimental) The EC2 instance type for all instances in the instance group.

            :stability: experimental
            """
            result = self._values.get("instance_type")
            assert result is not None, "Required property 'instance_type' is missing"
            return result

        @builtins.property
        def auto_scaling_policy(
            self,
        ) -> typing.Optional["EmrCreateCluster.AutoScalingPolicyProperty"]:
            """(experimental) An automatic scaling policy for a core instance group or task instance group in an Amazon EMR cluster.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("auto_scaling_policy")
            return result

        @builtins.property
        def bid_price(self) -> typing.Optional[builtins.str]:
            """(experimental) The bid price for each EC2 Spot instance type as defined by InstanceType.

            Expressed in USD.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("bid_price")
            return result

        @builtins.property
        def configurations(
            self,
        ) -> typing.Optional[typing.List["EmrCreateCluster.ConfigurationProperty"]]:
            """(experimental) The list of configurations supplied for an EMR cluster instance group.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("configurations")
            return result

        @builtins.property
        def ebs_configuration(
            self,
        ) -> typing.Optional["EmrCreateCluster.EbsConfigurationProperty"]:
            """(experimental) EBS configurations that will be attached to each EC2 instance in the instance group.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("ebs_configuration")
            return result

        @builtins.property
        def market(self) -> typing.Optional["EmrCreateCluster.InstanceMarket"]:
            """(experimental) Market type of the EC2 instances used to create a cluster node.

            :default: - EMR selected default

            :stability: experimental
            """
            result = self._values.get("market")
            return result

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            """(experimental) Friendly name given to the instance group.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("name")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceGroupConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.enum(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.InstanceMarket"
    )
    class InstanceMarket(enum.Enum):
        """(experimental) EC2 Instance Market.

        :stability: experimental
        """

        ON_DEMAND = "ON_DEMAND"
        """(experimental) On Demand Instance.

        :stability: experimental
        """
        SPOT = "SPOT"
        """(experimental) Spot Instance.

        :stability: experimental
        """

    @jsii.enum(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.InstanceRoleType"
    )
    class InstanceRoleType(enum.Enum):
        """(experimental) Instance Role Types.

        :stability: experimental
        """

        MASTER = "MASTER"
        """(experimental) Master Node.

        :stability: experimental
        """
        CORE = "CORE"
        """(experimental) Core Node.

        :stability: experimental
        """
        TASK = "TASK"
        """(experimental) Task Node.

        :stability: experimental
        """

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.InstanceTypeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instance_type": "instanceType",
            "bid_price": "bidPrice",
            "bid_price_as_percentage_of_on_demand_price": "bidPriceAsPercentageOfOnDemandPrice",
            "configurations": "configurations",
            "ebs_configuration": "ebsConfiguration",
            "weighted_capacity": "weightedCapacity",
        },
    )
    class InstanceTypeConfigProperty:
        def __init__(
            self,
            *,
            instance_type: builtins.str,
            bid_price: typing.Optional[builtins.str] = None,
            bid_price_as_percentage_of_on_demand_price: typing.Optional[jsii.Number] = None,
            configurations: typing.Optional[typing.List["EmrCreateCluster.ConfigurationProperty"]] = None,
            ebs_configuration: typing.Optional["EmrCreateCluster.EbsConfigurationProperty"] = None,
            weighted_capacity: typing.Optional[jsii.Number] = None,
        ) -> None:
            """(experimental) An instance type configuration for each instance type in an instance fleet, which determines the EC2 instances Amazon EMR attempts to provision to fulfill On-Demand and Spot target capacities.

            :param instance_type: (experimental) An EC2 instance type.
            :param bid_price: (experimental) The bid price for each EC2 Spot instance type as defined by InstanceType. Expressed in USD. Default: - None
            :param bid_price_as_percentage_of_on_demand_price: (experimental) The bid price, as a percentage of On-Demand price. Default: - None
            :param configurations: (experimental) A configuration classification that applies when provisioning cluster instances, which can include configurations for applications and software that run on the cluster. Default: - None
            :param ebs_configuration: (experimental) The configuration of Amazon Elastic Block Storage (EBS) attached to each instance as defined by InstanceType. Default: - None
            :param weighted_capacity: (experimental) The number of units that a provisioned instance of this type provides toward fulfilling the target capacities defined in the InstanceFleetConfig. Default: - None

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_InstanceTypeConfig.html
            :stability: experimental
            """
            if isinstance(ebs_configuration, dict):
                ebs_configuration = EbsConfigurationProperty(**ebs_configuration)
            self._values: typing.Dict[str, typing.Any] = {
                "instance_type": instance_type,
            }
            if bid_price is not None:
                self._values["bid_price"] = bid_price
            if bid_price_as_percentage_of_on_demand_price is not None:
                self._values["bid_price_as_percentage_of_on_demand_price"] = bid_price_as_percentage_of_on_demand_price
            if configurations is not None:
                self._values["configurations"] = configurations
            if ebs_configuration is not None:
                self._values["ebs_configuration"] = ebs_configuration
            if weighted_capacity is not None:
                self._values["weighted_capacity"] = weighted_capacity

        @builtins.property
        def instance_type(self) -> builtins.str:
            """(experimental) An EC2 instance type.

            :stability: experimental
            """
            result = self._values.get("instance_type")
            assert result is not None, "Required property 'instance_type' is missing"
            return result

        @builtins.property
        def bid_price(self) -> typing.Optional[builtins.str]:
            """(experimental) The bid price for each EC2 Spot instance type as defined by InstanceType.

            Expressed in USD.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("bid_price")
            return result

        @builtins.property
        def bid_price_as_percentage_of_on_demand_price(
            self,
        ) -> typing.Optional[jsii.Number]:
            """(experimental) The bid price, as a percentage of On-Demand price.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("bid_price_as_percentage_of_on_demand_price")
            return result

        @builtins.property
        def configurations(
            self,
        ) -> typing.Optional[typing.List["EmrCreateCluster.ConfigurationProperty"]]:
            """(experimental) A configuration classification that applies when provisioning cluster instances, which can include configurations for applications and software that run on the cluster.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("configurations")
            return result

        @builtins.property
        def ebs_configuration(
            self,
        ) -> typing.Optional["EmrCreateCluster.EbsConfigurationProperty"]:
            """(experimental) The configuration of Amazon Elastic Block Storage (EBS) attached to each instance as defined by InstanceType.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("ebs_configuration")
            return result

        @builtins.property
        def weighted_capacity(self) -> typing.Optional[jsii.Number]:
            """(experimental) The number of units that a provisioned instance of this type provides toward fulfilling the target capacities defined in the InstanceFleetConfig.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("weighted_capacity")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceTypeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.InstancesConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "additional_master_security_groups": "additionalMasterSecurityGroups",
            "additional_slave_security_groups": "additionalSlaveSecurityGroups",
            "ec2_key_name": "ec2KeyName",
            "ec2_subnet_id": "ec2SubnetId",
            "ec2_subnet_ids": "ec2SubnetIds",
            "emr_managed_master_security_group": "emrManagedMasterSecurityGroup",
            "emr_managed_slave_security_group": "emrManagedSlaveSecurityGroup",
            "hadoop_version": "hadoopVersion",
            "instance_count": "instanceCount",
            "instance_fleets": "instanceFleets",
            "instance_groups": "instanceGroups",
            "master_instance_type": "masterInstanceType",
            "placement": "placement",
            "service_access_security_group": "serviceAccessSecurityGroup",
            "slave_instance_type": "slaveInstanceType",
            "termination_protected": "terminationProtected",
        },
    )
    class InstancesConfigProperty:
        def __init__(
            self,
            *,
            additional_master_security_groups: typing.Optional[typing.List[builtins.str]] = None,
            additional_slave_security_groups: typing.Optional[typing.List[builtins.str]] = None,
            ec2_key_name: typing.Optional[builtins.str] = None,
            ec2_subnet_id: typing.Optional[builtins.str] = None,
            ec2_subnet_ids: typing.Optional[typing.List[builtins.str]] = None,
            emr_managed_master_security_group: typing.Optional[builtins.str] = None,
            emr_managed_slave_security_group: typing.Optional[builtins.str] = None,
            hadoop_version: typing.Optional[builtins.str] = None,
            instance_count: typing.Optional[jsii.Number] = None,
            instance_fleets: typing.Optional[typing.List["EmrCreateCluster.InstanceFleetConfigProperty"]] = None,
            instance_groups: typing.Optional[typing.List["EmrCreateCluster.InstanceGroupConfigProperty"]] = None,
            master_instance_type: typing.Optional[builtins.str] = None,
            placement: typing.Optional["EmrCreateCluster.PlacementTypeProperty"] = None,
            service_access_security_group: typing.Optional[builtins.str] = None,
            slave_instance_type: typing.Optional[builtins.str] = None,
            termination_protected: typing.Optional[builtins.bool] = None,
        ) -> None:
            """(experimental) A specification of the number and type of Amazon EC2 instances.

            See the RunJobFlow API for complete documentation on input parameters

            :param additional_master_security_groups: (experimental) A list of additional Amazon EC2 security group IDs for the master node. Default: - None
            :param additional_slave_security_groups: (experimental) A list of additional Amazon EC2 security group IDs for the core and task nodes. Default: - None
            :param ec2_key_name: (experimental) The name of the EC2 key pair that can be used to ssh to the master node as the user called "hadoop.". Default: - None
            :param ec2_subnet_id: (experimental) Applies to clusters that use the uniform instance group configuration. To launch the cluster in Amazon Virtual Private Cloud (Amazon VPC), set this parameter to the identifier of the Amazon VPC subnet where you want the cluster to launch. Default: EMR selected default
            :param ec2_subnet_ids: (experimental) Applies to clusters that use the instance fleet configuration. When multiple EC2 subnet IDs are specified, Amazon EMR evaluates them and launches instances in the optimal subnet. Default: EMR selected default
            :param emr_managed_master_security_group: (experimental) The identifier of the Amazon EC2 security group for the master node. Default: - None
            :param emr_managed_slave_security_group: (experimental) The identifier of the Amazon EC2 security group for the core and task nodes. Default: - None
            :param hadoop_version: (experimental) Applies only to Amazon EMR release versions earlier than 4.0. The Hadoop version for the cluster. Default: - 0.18 if the AmiVersion parameter is not set. If AmiVersion is set, the version of Hadoop for that AMI version is used.
            :param instance_count: (experimental) The number of EC2 instances in the cluster. Default: 0
            :param instance_fleets: (experimental) Describes the EC2 instances and instance configurations for clusters that use the instance fleet configuration. The instance fleet configuration is available only in Amazon EMR versions 4.8.0 and later, excluding 5.0.x versions. Default: - None
            :param instance_groups: (experimental) Configuration for the instance groups in a cluster. Default: - None
            :param master_instance_type: (experimental) The EC2 instance type of the master node. Default: - None
            :param placement: (experimental) The Availability Zone in which the cluster runs. Default: - EMR selected default
            :param service_access_security_group: (experimental) The identifier of the Amazon EC2 security group for the Amazon EMR service to access clusters in VPC private subnets. Default: - None
            :param slave_instance_type: (experimental) The EC2 instance type of the core and task nodes. Default: - None
            :param termination_protected: (experimental) Specifies whether to lock the cluster to prevent the Amazon EC2 instances from being terminated by API call, user intervention, or in the event of a job-flow error. Default: false

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_JobFlowInstancesConfig.html
            :stability: experimental
            """
            if isinstance(placement, dict):
                placement = PlacementTypeProperty(**placement)
            self._values: typing.Dict[str, typing.Any] = {}
            if additional_master_security_groups is not None:
                self._values["additional_master_security_groups"] = additional_master_security_groups
            if additional_slave_security_groups is not None:
                self._values["additional_slave_security_groups"] = additional_slave_security_groups
            if ec2_key_name is not None:
                self._values["ec2_key_name"] = ec2_key_name
            if ec2_subnet_id is not None:
                self._values["ec2_subnet_id"] = ec2_subnet_id
            if ec2_subnet_ids is not None:
                self._values["ec2_subnet_ids"] = ec2_subnet_ids
            if emr_managed_master_security_group is not None:
                self._values["emr_managed_master_security_group"] = emr_managed_master_security_group
            if emr_managed_slave_security_group is not None:
                self._values["emr_managed_slave_security_group"] = emr_managed_slave_security_group
            if hadoop_version is not None:
                self._values["hadoop_version"] = hadoop_version
            if instance_count is not None:
                self._values["instance_count"] = instance_count
            if instance_fleets is not None:
                self._values["instance_fleets"] = instance_fleets
            if instance_groups is not None:
                self._values["instance_groups"] = instance_groups
            if master_instance_type is not None:
                self._values["master_instance_type"] = master_instance_type
            if placement is not None:
                self._values["placement"] = placement
            if service_access_security_group is not None:
                self._values["service_access_security_group"] = service_access_security_group
            if slave_instance_type is not None:
                self._values["slave_instance_type"] = slave_instance_type
            if termination_protected is not None:
                self._values["termination_protected"] = termination_protected

        @builtins.property
        def additional_master_security_groups(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            """(experimental) A list of additional Amazon EC2 security group IDs for the master node.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("additional_master_security_groups")
            return result

        @builtins.property
        def additional_slave_security_groups(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            """(experimental) A list of additional Amazon EC2 security group IDs for the core and task nodes.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("additional_slave_security_groups")
            return result

        @builtins.property
        def ec2_key_name(self) -> typing.Optional[builtins.str]:
            """(experimental) The name of the EC2 key pair that can be used to ssh to the master node as the user called "hadoop.".

            :default: - None

            :stability: experimental
            """
            result = self._values.get("ec2_key_name")
            return result

        @builtins.property
        def ec2_subnet_id(self) -> typing.Optional[builtins.str]:
            """(experimental) Applies to clusters that use the uniform instance group configuration.

            To launch the cluster in Amazon Virtual Private Cloud (Amazon VPC),
            set this parameter to the identifier of the Amazon VPC subnet where you want the cluster to launch.

            :default: EMR selected default

            :stability: experimental
            """
            result = self._values.get("ec2_subnet_id")
            return result

        @builtins.property
        def ec2_subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            """(experimental) Applies to clusters that use the instance fleet configuration.

            When multiple EC2 subnet IDs are specified, Amazon EMR evaluates them and
            launches instances in the optimal subnet.

            :default: EMR selected default

            :stability: experimental
            """
            result = self._values.get("ec2_subnet_ids")
            return result

        @builtins.property
        def emr_managed_master_security_group(self) -> typing.Optional[builtins.str]:
            """(experimental) The identifier of the Amazon EC2 security group for the master node.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("emr_managed_master_security_group")
            return result

        @builtins.property
        def emr_managed_slave_security_group(self) -> typing.Optional[builtins.str]:
            """(experimental) The identifier of the Amazon EC2 security group for the core and task nodes.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("emr_managed_slave_security_group")
            return result

        @builtins.property
        def hadoop_version(self) -> typing.Optional[builtins.str]:
            """(experimental) Applies only to Amazon EMR release versions earlier than 4.0. The Hadoop version for the cluster.

            :default: - 0.18 if the AmiVersion parameter is not set. If AmiVersion is set, the version of Hadoop for that AMI version is used.

            :stability: experimental
            """
            result = self._values.get("hadoop_version")
            return result

        @builtins.property
        def instance_count(self) -> typing.Optional[jsii.Number]:
            """(experimental) The number of EC2 instances in the cluster.

            :default: 0

            :stability: experimental
            """
            result = self._values.get("instance_count")
            return result

        @builtins.property
        def instance_fleets(
            self,
        ) -> typing.Optional[typing.List["EmrCreateCluster.InstanceFleetConfigProperty"]]:
            """(experimental) Describes the EC2 instances and instance configurations for clusters that use the instance fleet configuration.

            The instance fleet configuration is available only in Amazon EMR versions 4.8.0 and later, excluding 5.0.x versions.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("instance_fleets")
            return result

        @builtins.property
        def instance_groups(
            self,
        ) -> typing.Optional[typing.List["EmrCreateCluster.InstanceGroupConfigProperty"]]:
            """(experimental) Configuration for the instance groups in a cluster.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("instance_groups")
            return result

        @builtins.property
        def master_instance_type(self) -> typing.Optional[builtins.str]:
            """(experimental) The EC2 instance type of the master node.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("master_instance_type")
            return result

        @builtins.property
        def placement(
            self,
        ) -> typing.Optional["EmrCreateCluster.PlacementTypeProperty"]:
            """(experimental) The Availability Zone in which the cluster runs.

            :default: - EMR selected default

            :stability: experimental
            """
            result = self._values.get("placement")
            return result

        @builtins.property
        def service_access_security_group(self) -> typing.Optional[builtins.str]:
            """(experimental) The identifier of the Amazon EC2 security group for the Amazon EMR service to access clusters in VPC private subnets.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("service_access_security_group")
            return result

        @builtins.property
        def slave_instance_type(self) -> typing.Optional[builtins.str]:
            """(experimental) The EC2 instance type of the core and task nodes.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("slave_instance_type")
            return result

        @builtins.property
        def termination_protected(self) -> typing.Optional[builtins.bool]:
            """(experimental) Specifies whether to lock the cluster to prevent the Amazon EC2 instances from being terminated by API call, user intervention, or in the event of a job-flow error.

            :default: false

            :stability: experimental
            """
            result = self._values.get("termination_protected")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstancesConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.KerberosAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "realm": "realm",
            "ad_domain_join_password": "adDomainJoinPassword",
            "ad_domain_join_user": "adDomainJoinUser",
            "cross_realm_trust_principal_password": "crossRealmTrustPrincipalPassword",
            "kdc_admin_password": "kdcAdminPassword",
        },
    )
    class KerberosAttributesProperty:
        def __init__(
            self,
            *,
            realm: builtins.str,
            ad_domain_join_password: typing.Optional[builtins.str] = None,
            ad_domain_join_user: typing.Optional[builtins.str] = None,
            cross_realm_trust_principal_password: typing.Optional[builtins.str] = None,
            kdc_admin_password: typing.Optional[builtins.str] = None,
        ) -> None:
            """(experimental) Attributes for Kerberos configuration when Kerberos authentication is enabled using a security configuration.

            See the RunJobFlow API for complete documentation on input parameters

            :param realm: (experimental) The name of the Kerberos realm to which all nodes in a cluster belong. For example, EC2.INTERNAL.
            :param ad_domain_join_password: (experimental) The Active Directory password for ADDomainJoinUser. Default: No adDomainJoinPassword
            :param ad_domain_join_user: (experimental) Required only when establishing a cross-realm trust with an Active Directory domain. A user with sufficient privileges to join resources to the domain. Default: No adDomainJoinUser
            :param cross_realm_trust_principal_password: (experimental) Required only when establishing a cross-realm trust with a KDC in a different realm. The cross-realm principal password, which must be identical across realms. Default: No crossRealmTrustPrincipalPassword
            :param kdc_admin_password: (experimental) The password used within the cluster for the kadmin service on the cluster-dedicated KDC, which maintains Kerberos principals, password policies, and keytabs for the cluster. Default: No kdcAdminPassword

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_KerberosAttributes.html
            :stability: experimental
            """
            self._values: typing.Dict[str, typing.Any] = {
                "realm": realm,
            }
            if ad_domain_join_password is not None:
                self._values["ad_domain_join_password"] = ad_domain_join_password
            if ad_domain_join_user is not None:
                self._values["ad_domain_join_user"] = ad_domain_join_user
            if cross_realm_trust_principal_password is not None:
                self._values["cross_realm_trust_principal_password"] = cross_realm_trust_principal_password
            if kdc_admin_password is not None:
                self._values["kdc_admin_password"] = kdc_admin_password

        @builtins.property
        def realm(self) -> builtins.str:
            """(experimental) The name of the Kerberos realm to which all nodes in a cluster belong.

            For example, EC2.INTERNAL.

            :stability: experimental
            """
            result = self._values.get("realm")
            assert result is not None, "Required property 'realm' is missing"
            return result

        @builtins.property
        def ad_domain_join_password(self) -> typing.Optional[builtins.str]:
            """(experimental) The Active Directory password for ADDomainJoinUser.

            :default: No adDomainJoinPassword

            :stability: experimental
            """
            result = self._values.get("ad_domain_join_password")
            return result

        @builtins.property
        def ad_domain_join_user(self) -> typing.Optional[builtins.str]:
            """(experimental) Required only when establishing a cross-realm trust with an Active Directory domain.

            A user with sufficient privileges to join
            resources to the domain.

            :default: No adDomainJoinUser

            :stability: experimental
            """
            result = self._values.get("ad_domain_join_user")
            return result

        @builtins.property
        def cross_realm_trust_principal_password(self) -> typing.Optional[builtins.str]:
            """(experimental) Required only when establishing a cross-realm trust with a KDC in a different realm.

            The cross-realm principal password, which
            must be identical across realms.

            :default: No crossRealmTrustPrincipalPassword

            :stability: experimental
            """
            result = self._values.get("cross_realm_trust_principal_password")
            return result

        @builtins.property
        def kdc_admin_password(self) -> typing.Optional[builtins.str]:
            """(experimental) The password used within the cluster for the kadmin service on the cluster-dedicated KDC, which maintains Kerberos principals, password policies, and keytabs for the cluster.

            :default: No kdcAdminPassword

            :stability: experimental
            """
            result = self._values.get("kdc_admin_password")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KerberosAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.MetricDimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class MetricDimensionProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            """(experimental) A CloudWatch dimension, which is specified using a Key (known as a Name in CloudWatch), Value pair.

            By default, Amazon EMR uses
            one dimension whose Key is JobFlowID and Value is a variable representing the cluster ID, which is ${emr.clusterId}. This enables
            the rule to bootstrap when the cluster ID becomes available

            :param key: (experimental) The dimension name.
            :param value: (experimental) The dimension value.

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_MetricDimension.html
            :stability: experimental
            """
            self._values: typing.Dict[str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            """(experimental) The dimension name.

            :stability: experimental
            """
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return result

        @builtins.property
        def value(self) -> builtins.str:
            """(experimental) The dimension value.

            :stability: experimental
            """
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricDimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.PlacementTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "availability_zone": "availabilityZone",
            "availability_zones": "availabilityZones",
        },
    )
    class PlacementTypeProperty:
        def __init__(
            self,
            *,
            availability_zone: typing.Optional[builtins.str] = None,
            availability_zones: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """(experimental) The Amazon EC2 Availability Zone configuration of the cluster (job flow).

            :param availability_zone: (experimental) The Amazon EC2 Availability Zone for the cluster. AvailabilityZone is used for uniform instance groups, while AvailabilityZones (plural) is used for instance fleets. Default: - EMR selected default
            :param availability_zones: (experimental) When multiple Availability Zones are specified, Amazon EMR evaluates them and launches instances in the optimal Availability Zone. AvailabilityZones is used for instance fleets, while AvailabilityZone (singular) is used for uniform instance groups. Default: - EMR selected default

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_PlacementType.html
            :stability: experimental
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if availability_zone is not None:
                self._values["availability_zone"] = availability_zone
            if availability_zones is not None:
                self._values["availability_zones"] = availability_zones

        @builtins.property
        def availability_zone(self) -> typing.Optional[builtins.str]:
            """(experimental) The Amazon EC2 Availability Zone for the cluster.

            AvailabilityZone is used for uniform instance groups, while AvailabilityZones
            (plural) is used for instance fleets.

            :default: - EMR selected default

            :stability: experimental
            """
            result = self._values.get("availability_zone")
            return result

        @builtins.property
        def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
            """(experimental) When multiple Availability Zones are specified, Amazon EMR evaluates them and launches instances in the optimal Availability Zone.

            AvailabilityZones is used for instance fleets, while AvailabilityZone (singular) is used for uniform instance groups.

            :default: - EMR selected default

            :stability: experimental
            """
            result = self._values.get("availability_zones")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PlacementTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.ScalingActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "simple_scaling_policy_configuration": "simpleScalingPolicyConfiguration",
            "market": "market",
        },
    )
    class ScalingActionProperty:
        def __init__(
            self,
            *,
            simple_scaling_policy_configuration: "EmrCreateCluster.SimpleScalingPolicyConfigurationProperty",
            market: typing.Optional["EmrCreateCluster.InstanceMarket"] = None,
        ) -> None:
            """(experimental) The type of adjustment the automatic scaling activity makes when triggered, and the periodicity of the adjustment.

            And an automatic scaling configuration, which describes how the policy adds or removes instances, the cooldown period,
            and the number of EC2 instances that will be added each time the CloudWatch metric alarm condition is satisfied.

            :param simple_scaling_policy_configuration: (experimental) The type of adjustment the automatic scaling activity makes when triggered, and the periodicity of the adjustment.
            :param market: (experimental) Not available for instance groups. Instance groups use the market type specified for the group. Default: - EMR selected default

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_ScalingAction.html
            :stability: experimental
            """
            if isinstance(simple_scaling_policy_configuration, dict):
                simple_scaling_policy_configuration = SimpleScalingPolicyConfigurationProperty(**simple_scaling_policy_configuration)
            self._values: typing.Dict[str, typing.Any] = {
                "simple_scaling_policy_configuration": simple_scaling_policy_configuration,
            }
            if market is not None:
                self._values["market"] = market

        @builtins.property
        def simple_scaling_policy_configuration(
            self,
        ) -> "EmrCreateCluster.SimpleScalingPolicyConfigurationProperty":
            """(experimental) The type of adjustment the automatic scaling activity makes when triggered, and the periodicity of the adjustment.

            :stability: experimental
            """
            result = self._values.get("simple_scaling_policy_configuration")
            assert result is not None, "Required property 'simple_scaling_policy_configuration' is missing"
            return result

        @builtins.property
        def market(self) -> typing.Optional["EmrCreateCluster.InstanceMarket"]:
            """(experimental) Not available for instance groups.

            Instance groups use the market type specified for the group.

            :default: - EMR selected default

            :stability: experimental
            """
            result = self._values.get("market")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.enum(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.ScalingAdjustmentType"
    )
    class ScalingAdjustmentType(enum.Enum):
        """(experimental) AutoScaling Adjustment Type.

        :stability: experimental
        """

        CHANGE_IN_CAPACITY = "CHANGE_IN_CAPACITY"
        """(experimental) CHANGE_IN_CAPACITY.

        :stability: experimental
        """
        PERCENT_CHANGE_IN_CAPACITY = "PERCENT_CHANGE_IN_CAPACITY"
        """(experimental) PERCENT_CHANGE_IN_CAPACITY.

        :stability: experimental
        """
        EXACT_CAPACITY = "EXACT_CAPACITY"
        """(experimental) EXACT_CAPACITY.

        :stability: experimental
        """

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.ScalingConstraintsProperty",
        jsii_struct_bases=[],
        name_mapping={"max_capacity": "maxCapacity", "min_capacity": "minCapacity"},
    )
    class ScalingConstraintsProperty:
        def __init__(
            self,
            *,
            max_capacity: jsii.Number,
            min_capacity: jsii.Number,
        ) -> None:
            """(experimental) The upper and lower EC2 instance limits for an automatic scaling policy.

            Automatic scaling activities triggered by automatic scaling
            rules will not cause an instance group to grow above or below these limits.

            :param max_capacity: (experimental) The upper boundary of EC2 instances in an instance group beyond which scaling activities are not allowed to grow. Scale-out activities will not add instances beyond this boundary.
            :param min_capacity: (experimental) The lower boundary of EC2 instances in an instance group below which scaling activities are not allowed to shrink. Scale-in activities will not terminate instances below this boundary.

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_ScalingConstraints.html
            :stability: experimental
            """
            self._values: typing.Dict[str, typing.Any] = {
                "max_capacity": max_capacity,
                "min_capacity": min_capacity,
            }

        @builtins.property
        def max_capacity(self) -> jsii.Number:
            """(experimental) The upper boundary of EC2 instances in an instance group beyond which scaling activities are not allowed to grow.

            Scale-out
            activities will not add instances beyond this boundary.

            :stability: experimental
            """
            result = self._values.get("max_capacity")
            assert result is not None, "Required property 'max_capacity' is missing"
            return result

        @builtins.property
        def min_capacity(self) -> jsii.Number:
            """(experimental) The lower boundary of EC2 instances in an instance group below which scaling activities are not allowed to shrink.

            Scale-in
            activities will not terminate instances below this boundary.

            :stability: experimental
            """
            result = self._values.get("min_capacity")
            assert result is not None, "Required property 'min_capacity' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingConstraintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.ScalingRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "name": "name",
            "trigger": "trigger",
            "description": "description",
        },
    )
    class ScalingRuleProperty:
        def __init__(
            self,
            *,
            action: "EmrCreateCluster.ScalingActionProperty",
            name: builtins.str,
            trigger: "EmrCreateCluster.ScalingTriggerProperty",
            description: typing.Optional[builtins.str] = None,
        ) -> None:
            """(experimental) A scale-in or scale-out rule that defines scaling activity, including the CloudWatch metric alarm that triggers activity, how EC2 instances are added or removed, and the periodicity of adjustments.

            :param action: (experimental) The conditions that trigger an automatic scaling activity.
            :param name: (experimental) The name used to identify an automatic scaling rule. Rule names must be unique within a scaling policy.
            :param trigger: (experimental) The CloudWatch alarm definition that determines when automatic scaling activity is triggered.
            :param description: (experimental) A friendly, more verbose description of the automatic scaling rule. Default: - None

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_ScalingRule.html
            :stability: experimental
            """
            if isinstance(action, dict):
                action = ScalingActionProperty(**action)
            if isinstance(trigger, dict):
                trigger = ScalingTriggerProperty(**trigger)
            self._values: typing.Dict[str, typing.Any] = {
                "action": action,
                "name": name,
                "trigger": trigger,
            }
            if description is not None:
                self._values["description"] = description

        @builtins.property
        def action(self) -> "EmrCreateCluster.ScalingActionProperty":
            """(experimental) The conditions that trigger an automatic scaling activity.

            :stability: experimental
            """
            result = self._values.get("action")
            assert result is not None, "Required property 'action' is missing"
            return result

        @builtins.property
        def name(self) -> builtins.str:
            """(experimental) The name used to identify an automatic scaling rule.

            Rule names must be unique within a scaling policy.

            :stability: experimental
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def trigger(self) -> "EmrCreateCluster.ScalingTriggerProperty":
            """(experimental) The CloudWatch alarm definition that determines when automatic scaling activity is triggered.

            :stability: experimental
            """
            result = self._values.get("trigger")
            assert result is not None, "Required property 'trigger' is missing"
            return result

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            """(experimental) A friendly, more verbose description of the automatic scaling rule.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("description")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.ScalingTriggerProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_watch_alarm_definition": "cloudWatchAlarmDefinition"},
    )
    class ScalingTriggerProperty:
        def __init__(
            self,
            *,
            cloud_watch_alarm_definition: "EmrCreateCluster.CloudWatchAlarmDefinitionProperty",
        ) -> None:
            """(experimental) The conditions that trigger an automatic scaling activity and the definition of a CloudWatch metric alarm.

            When the defined alarm conditions are met along with other trigger parameters, scaling activity begins.

            :param cloud_watch_alarm_definition: (experimental) The definition of a CloudWatch metric alarm. When the defined alarm conditions are met along with other trigger parameters, scaling activity begins.

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_ScalingTrigger.html
            :stability: experimental
            """
            if isinstance(cloud_watch_alarm_definition, dict):
                cloud_watch_alarm_definition = CloudWatchAlarmDefinitionProperty(**cloud_watch_alarm_definition)
            self._values: typing.Dict[str, typing.Any] = {
                "cloud_watch_alarm_definition": cloud_watch_alarm_definition,
            }

        @builtins.property
        def cloud_watch_alarm_definition(
            self,
        ) -> "EmrCreateCluster.CloudWatchAlarmDefinitionProperty":
            """(experimental) The definition of a CloudWatch metric alarm.

            When the defined alarm conditions are met along with other trigger parameters,
            scaling activity begins.

            :stability: experimental
            """
            result = self._values.get("cloud_watch_alarm_definition")
            assert result is not None, "Required property 'cloud_watch_alarm_definition' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingTriggerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.ScriptBootstrapActionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"path": "path", "args": "args"},
    )
    class ScriptBootstrapActionConfigProperty:
        def __init__(
            self,
            *,
            path: builtins.str,
            args: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """(experimental) Configuration of the script to run during a bootstrap action.

            :param path: (experimental) Location of the script to run during a bootstrap action. Can be either a location in Amazon S3 or on a local file system.
            :param args: (experimental) A list of command line arguments to pass to the bootstrap action script. Default: No args

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_ScriptBootstrapActionConfig.html
            :stability: experimental
            """
            self._values: typing.Dict[str, typing.Any] = {
                "path": path,
            }
            if args is not None:
                self._values["args"] = args

        @builtins.property
        def path(self) -> builtins.str:
            """(experimental) Location of the script to run during a bootstrap action.

            Can be either a location in Amazon S3 or on a local file system.

            :stability: experimental
            """
            result = self._values.get("path")
            assert result is not None, "Required property 'path' is missing"
            return result

        @builtins.property
        def args(self) -> typing.Optional[typing.List[builtins.str]]:
            """(experimental) A list of command line arguments to pass to the bootstrap action script.

            :default: No args

            :stability: experimental
            """
            result = self._values.get("args")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScriptBootstrapActionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.SimpleScalingPolicyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "scaling_adjustment": "scalingAdjustment",
            "adjustment_type": "adjustmentType",
            "cool_down": "coolDown",
        },
    )
    class SimpleScalingPolicyConfigurationProperty:
        def __init__(
            self,
            *,
            scaling_adjustment: jsii.Number,
            adjustment_type: typing.Optional["EmrCreateCluster.ScalingAdjustmentType"] = None,
            cool_down: typing.Optional[jsii.Number] = None,
        ) -> None:
            """(experimental) An automatic scaling configuration, which describes how the policy adds or removes instances, the cooldown period, and the number of EC2 instances that will be added each time the CloudWatch metric alarm condition is satisfied.

            :param scaling_adjustment: (experimental) The amount by which to scale in or scale out, based on the specified AdjustmentType. A positive value adds to the instance group's EC2 instance count while a negative number removes instances. If AdjustmentType is set to EXACT_CAPACITY, the number should only be a positive integer.
            :param adjustment_type: (experimental) The way in which EC2 instances are added (if ScalingAdjustment is a positive number) or terminated (if ScalingAdjustment is a negative number) each time the scaling activity is triggered. Default: - None
            :param cool_down: (experimental) The amount of time, in seconds, after a scaling activity completes before any further trigger-related scaling activities can start. Default: 0

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_SimpleScalingPolicyConfiguration.html
            :stability: experimental
            """
            self._values: typing.Dict[str, typing.Any] = {
                "scaling_adjustment": scaling_adjustment,
            }
            if adjustment_type is not None:
                self._values["adjustment_type"] = adjustment_type
            if cool_down is not None:
                self._values["cool_down"] = cool_down

        @builtins.property
        def scaling_adjustment(self) -> jsii.Number:
            """(experimental) The amount by which to scale in or scale out, based on the specified AdjustmentType.

            A positive value adds to the instance group's
            EC2 instance count while a negative number removes instances. If AdjustmentType is set to EXACT_CAPACITY, the number should only be
            a positive integer.

            :stability: experimental
            """
            result = self._values.get("scaling_adjustment")
            assert result is not None, "Required property 'scaling_adjustment' is missing"
            return result

        @builtins.property
        def adjustment_type(
            self,
        ) -> typing.Optional["EmrCreateCluster.ScalingAdjustmentType"]:
            """(experimental) The way in which EC2 instances are added (if ScalingAdjustment is a positive number) or terminated (if ScalingAdjustment is a negative number) each time the scaling activity is triggered.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("adjustment_type")
            return result

        @builtins.property
        def cool_down(self) -> typing.Optional[jsii.Number]:
            """(experimental) The amount of time, in seconds, after a scaling activity completes before any further trigger-related scaling activities can start.

            :default: 0

            :stability: experimental
            """
            result = self._values.get("cool_down")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SimpleScalingPolicyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.SpotProvisioningSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "timeout_action": "timeoutAction",
            "timeout_duration_minutes": "timeoutDurationMinutes",
            "block_duration_minutes": "blockDurationMinutes",
        },
    )
    class SpotProvisioningSpecificationProperty:
        def __init__(
            self,
            *,
            timeout_action: "EmrCreateCluster.SpotTimeoutAction",
            timeout_duration_minutes: jsii.Number,
            block_duration_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            """(experimental) The launch specification for Spot instances in the instance fleet, which determines the defined duration and provisioning timeout behavior.

            :param timeout_action: (experimental) The action to take when TargetSpotCapacity has not been fulfilled when the TimeoutDurationMinutes has expired.
            :param timeout_duration_minutes: (experimental) The spot provisioning timeout period in minutes.
            :param block_duration_minutes: (experimental) The defined duration for Spot instances (also known as Spot blocks) in minutes. Default: No blockDurationMinutes

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_SpotProvisioningSpecification.html
            :stability: experimental
            """
            self._values: typing.Dict[str, typing.Any] = {
                "timeout_action": timeout_action,
                "timeout_duration_minutes": timeout_duration_minutes,
            }
            if block_duration_minutes is not None:
                self._values["block_duration_minutes"] = block_duration_minutes

        @builtins.property
        def timeout_action(self) -> "EmrCreateCluster.SpotTimeoutAction":
            """(experimental) The action to take when TargetSpotCapacity has not been fulfilled when the TimeoutDurationMinutes has expired.

            :stability: experimental
            """
            result = self._values.get("timeout_action")
            assert result is not None, "Required property 'timeout_action' is missing"
            return result

        @builtins.property
        def timeout_duration_minutes(self) -> jsii.Number:
            """(experimental) The spot provisioning timeout period in minutes.

            :stability: experimental
            """
            result = self._values.get("timeout_duration_minutes")
            assert result is not None, "Required property 'timeout_duration_minutes' is missing"
            return result

        @builtins.property
        def block_duration_minutes(self) -> typing.Optional[jsii.Number]:
            """(experimental) The defined duration for Spot instances (also known as Spot blocks) in minutes.

            :default: No blockDurationMinutes

            :stability: experimental
            """
            result = self._values.get("block_duration_minutes")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SpotProvisioningSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.enum(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.SpotTimeoutAction"
    )
    class SpotTimeoutAction(enum.Enum):
        """(experimental) Spot Timeout Actions.

        :stability: experimental
        """

        SWITCH_TO_ON_DEMAND = "SWITCH_TO_ON_DEMAND"
        """(experimental) \\ SWITCH_TO_ON_DEMAND.

        :stability: experimental
        """
        TERMINATE_CLUSTER = "TERMINATE_CLUSTER"
        """(experimental) TERMINATE_CLUSTER.

        :stability: experimental
        """

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateCluster.VolumeSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "volume_size": "volumeSize",
            "volume_type": "volumeType",
            "iops": "iops",
        },
    )
    class VolumeSpecificationProperty:
        def __init__(
            self,
            *,
            volume_size: aws_cdk.core.Size,
            volume_type: "EmrCreateCluster.EbsBlockDeviceVolumeType",
            iops: typing.Optional[jsii.Number] = None,
        ) -> None:
            """(experimental) EBS volume specifications such as volume type, IOPS, and size (GiB) that will be requested for the EBS volume attached to an EC2 instance in the cluster.

            :param volume_size: (experimental) The volume size. If the volume type is EBS-optimized, the minimum value is 10GiB. Maximum size is 1TiB
            :param volume_type: (experimental) The volume type. Volume types supported are gp2, io1, standard.
            :param iops: (experimental) The number of I/O operations per second (IOPS) that the volume supports. Default: - EMR selected default

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_VolumeSpecification.html
            :stability: experimental
            """
            self._values: typing.Dict[str, typing.Any] = {
                "volume_size": volume_size,
                "volume_type": volume_type,
            }
            if iops is not None:
                self._values["iops"] = iops

        @builtins.property
        def volume_size(self) -> aws_cdk.core.Size:
            """(experimental) The volume size.

            If the volume type is EBS-optimized, the minimum value is 10GiB.
            Maximum size is 1TiB

            :stability: experimental
            """
            result = self._values.get("volume_size")
            assert result is not None, "Required property 'volume_size' is missing"
            return result

        @builtins.property
        def volume_type(self) -> "EmrCreateCluster.EbsBlockDeviceVolumeType":
            """(experimental) The volume type.

            Volume types supported are gp2, io1, standard.

            :stability: experimental
            """
            result = self._values.get("volume_type")
            assert result is not None, "Required property 'volume_type' is missing"
            return result

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            """(experimental) The number of I/O operations per second (IOPS) that the volume supports.

            :default: - EMR selected default

            :stability: experimental
            """
            result = self._values.get("iops")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VolumeSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrCreateClusterProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "instances": "instances",
        "name": "name",
        "additional_info": "additionalInfo",
        "applications": "applications",
        "auto_scaling_role": "autoScalingRole",
        "bootstrap_actions": "bootstrapActions",
        "cluster_role": "clusterRole",
        "configurations": "configurations",
        "custom_ami_id": "customAmiId",
        "ebs_root_volume_size": "ebsRootVolumeSize",
        "kerberos_attributes": "kerberosAttributes",
        "log_uri": "logUri",
        "release_label": "releaseLabel",
        "scale_down_behavior": "scaleDownBehavior",
        "security_configuration": "securityConfiguration",
        "service_role": "serviceRole",
        "tags": "tags",
        "visible_to_all_users": "visibleToAllUsers",
    },
)
class EmrCreateClusterProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        instances: EmrCreateCluster.InstancesConfigProperty,
        name: builtins.str,
        additional_info: typing.Optional[builtins.str] = None,
        applications: typing.Optional[typing.List[EmrCreateCluster.ApplicationConfigProperty]] = None,
        auto_scaling_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        bootstrap_actions: typing.Optional[typing.List[EmrCreateCluster.BootstrapActionConfigProperty]] = None,
        cluster_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        configurations: typing.Optional[typing.List[EmrCreateCluster.ConfigurationProperty]] = None,
        custom_ami_id: typing.Optional[builtins.str] = None,
        ebs_root_volume_size: typing.Optional[aws_cdk.core.Size] = None,
        kerberos_attributes: typing.Optional[EmrCreateCluster.KerberosAttributesProperty] = None,
        log_uri: typing.Optional[builtins.str] = None,
        release_label: typing.Optional[builtins.str] = None,
        scale_down_behavior: typing.Optional[EmrCreateCluster.EmrClusterScaleDownBehavior] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        service_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        visible_to_all_users: typing.Optional[builtins.bool] = None,
    ) -> None:
        """(experimental) Properties for EmrCreateCluster.

        See the RunJobFlow API for complete documentation on input parameters

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param instances: (experimental) A specification of the number and type of Amazon EC2 instances.
        :param name: (experimental) The Name of the Cluster.
        :param additional_info: (experimental) A JSON string for selecting additional features. Default: - None
        :param applications: (experimental) A case-insensitive list of applications for Amazon EMR to install and configure when launching the cluster. Default: - EMR selected default
        :param auto_scaling_role: (experimental) An IAM role for automatic scaling policies. Default: - A role will be created.
        :param bootstrap_actions: (experimental) A list of bootstrap actions to run before Hadoop starts on the cluster nodes. Default: - None
        :param cluster_role: (experimental) Also called instance profile and EC2 role. An IAM role for an EMR cluster. The EC2 instances of the cluster assume this role. This attribute has been renamed from jobFlowRole to clusterRole to align with other ERM/StepFunction integration parameters. Default: - - A Role will be created
        :param configurations: (experimental) The list of configurations supplied for the EMR cluster you are creating. Default: - None
        :param custom_ami_id: (experimental) The ID of a custom Amazon EBS-backed Linux AMI. Default: - None
        :param ebs_root_volume_size: (experimental) The size of the EBS root device volume of the Linux AMI that is used for each EC2 instance. Default: - EMR selected default
        :param kerberos_attributes: (experimental) Attributes for Kerberos configuration when Kerberos authentication is enabled using a security configuration. Default: - None
        :param log_uri: (experimental) The location in Amazon S3 to write the log files of the job flow. Default: - None
        :param release_label: (experimental) The Amazon EMR release label, which determines the version of open-source application packages installed on the cluster. Default: - EMR selected default
        :param scale_down_behavior: (experimental) Specifies the way that individual Amazon EC2 instances terminate when an automatic scale-in activity occurs or an instance group is resized. Default: - EMR selected default
        :param security_configuration: (experimental) The name of a security configuration to apply to the cluster. Default: - None
        :param service_role: (experimental) The IAM role that will be assumed by the Amazon EMR service to access AWS resources on your behalf. Default: - A role will be created that Amazon EMR service can assume.
        :param tags: (experimental) A list of tags to associate with a cluster and propagate to Amazon EC2 instances. Default: - None
        :param visible_to_all_users: (experimental) A value of true indicates that all IAM users in the AWS account can perform cluster actions if they have the proper IAM policy permissions. Default: true

        :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_RunJobFlow.html
        :stability: experimental
        """
        if isinstance(instances, dict):
            instances = EmrCreateCluster.InstancesConfigProperty(**instances)
        if isinstance(kerberos_attributes, dict):
            kerberos_attributes = EmrCreateCluster.KerberosAttributesProperty(**kerberos_attributes)
        self._values: typing.Dict[str, typing.Any] = {
            "instances": instances,
            "name": name,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if additional_info is not None:
            self._values["additional_info"] = additional_info
        if applications is not None:
            self._values["applications"] = applications
        if auto_scaling_role is not None:
            self._values["auto_scaling_role"] = auto_scaling_role
        if bootstrap_actions is not None:
            self._values["bootstrap_actions"] = bootstrap_actions
        if cluster_role is not None:
            self._values["cluster_role"] = cluster_role
        if configurations is not None:
            self._values["configurations"] = configurations
        if custom_ami_id is not None:
            self._values["custom_ami_id"] = custom_ami_id
        if ebs_root_volume_size is not None:
            self._values["ebs_root_volume_size"] = ebs_root_volume_size
        if kerberos_attributes is not None:
            self._values["kerberos_attributes"] = kerberos_attributes
        if log_uri is not None:
            self._values["log_uri"] = log_uri
        if release_label is not None:
            self._values["release_label"] = release_label
        if scale_down_behavior is not None:
            self._values["scale_down_behavior"] = scale_down_behavior
        if security_configuration is not None:
            self._values["security_configuration"] = security_configuration
        if service_role is not None:
            self._values["service_role"] = service_role
        if tags is not None:
            self._values["tags"] = tags
        if visible_to_all_users is not None:
            self._values["visible_to_all_users"] = visible_to_all_users

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def instances(self) -> EmrCreateCluster.InstancesConfigProperty:
        """(experimental) A specification of the number and type of Amazon EC2 instances.

        :stability: experimental
        """
        result = self._values.get("instances")
        assert result is not None, "Required property 'instances' is missing"
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """(experimental) The Name of the Cluster.

        :stability: experimental
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def additional_info(self) -> typing.Optional[builtins.str]:
        """(experimental) A JSON string for selecting additional features.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("additional_info")
        return result

    @builtins.property
    def applications(
        self,
    ) -> typing.Optional[typing.List[EmrCreateCluster.ApplicationConfigProperty]]:
        """(experimental) A case-insensitive list of applications for Amazon EMR to install and configure when launching the cluster.

        :default: - EMR selected default

        :stability: experimental
        """
        result = self._values.get("applications")
        return result

    @builtins.property
    def auto_scaling_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """(experimental) An IAM role for automatic scaling policies.

        :default: - A role will be created.

        :stability: experimental
        """
        result = self._values.get("auto_scaling_role")
        return result

    @builtins.property
    def bootstrap_actions(
        self,
    ) -> typing.Optional[typing.List[EmrCreateCluster.BootstrapActionConfigProperty]]:
        """(experimental) A list of bootstrap actions to run before Hadoop starts on the cluster nodes.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("bootstrap_actions")
        return result

    @builtins.property
    def cluster_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """(experimental) Also called instance profile and EC2 role.

        An IAM role for an EMR cluster. The EC2 instances of the cluster assume this role.

        This attribute has been renamed from jobFlowRole to clusterRole to align with other ERM/StepFunction integration parameters.

        :default:

        -
        - A Role will be created

        :stability: experimental
        """
        result = self._values.get("cluster_role")
        return result

    @builtins.property
    def configurations(
        self,
    ) -> typing.Optional[typing.List[EmrCreateCluster.ConfigurationProperty]]:
        """(experimental) The list of configurations supplied for the EMR cluster you are creating.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("configurations")
        return result

    @builtins.property
    def custom_ami_id(self) -> typing.Optional[builtins.str]:
        """(experimental) The ID of a custom Amazon EBS-backed Linux AMI.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("custom_ami_id")
        return result

    @builtins.property
    def ebs_root_volume_size(self) -> typing.Optional[aws_cdk.core.Size]:
        """(experimental) The size of the EBS root device volume of the Linux AMI that is used for each EC2 instance.

        :default: - EMR selected default

        :stability: experimental
        """
        result = self._values.get("ebs_root_volume_size")
        return result

    @builtins.property
    def kerberos_attributes(
        self,
    ) -> typing.Optional[EmrCreateCluster.KerberosAttributesProperty]:
        """(experimental) Attributes for Kerberos configuration when Kerberos authentication is enabled using a security configuration.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("kerberos_attributes")
        return result

    @builtins.property
    def log_uri(self) -> typing.Optional[builtins.str]:
        """(experimental) The location in Amazon S3 to write the log files of the job flow.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("log_uri")
        return result

    @builtins.property
    def release_label(self) -> typing.Optional[builtins.str]:
        """(experimental) The Amazon EMR release label, which determines the version of open-source application packages installed on the cluster.

        :default: - EMR selected default

        :stability: experimental
        """
        result = self._values.get("release_label")
        return result

    @builtins.property
    def scale_down_behavior(
        self,
    ) -> typing.Optional[EmrCreateCluster.EmrClusterScaleDownBehavior]:
        """(experimental) Specifies the way that individual Amazon EC2 instances terminate when an automatic scale-in activity occurs or an instance group is resized.

        :default: - EMR selected default

        :stability: experimental
        """
        result = self._values.get("scale_down_behavior")
        return result

    @builtins.property
    def security_configuration(self) -> typing.Optional[builtins.str]:
        """(experimental) The name of a security configuration to apply to the cluster.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("security_configuration")
        return result

    @builtins.property
    def service_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """(experimental) The IAM role that will be assumed by the Amazon EMR service to access AWS resources on your behalf.

        :default: - A role will be created that Amazon EMR service can assume.

        :stability: experimental
        """
        result = self._values.get("service_role")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) A list of tags to associate with a cluster and propagate to Amazon EC2 instances.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def visible_to_all_users(self) -> typing.Optional[builtins.bool]:
        """(experimental) A value of true indicates that all IAM users in the AWS account can perform cluster actions if they have the proper IAM policy permissions.

        :default: true

        :stability: experimental
        """
        result = self._values.get("visible_to_all_users")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrCreateClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrModifyInstanceFleetByName(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrModifyInstanceFleetByName",
):
    """(experimental) A Step Functions Task to to modify an InstanceFleet on an EMR Cluster.

    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster_id: builtins.str,
        instance_fleet_name: builtins.str,
        target_on_demand_capacity: jsii.Number,
        target_spot_capacity: jsii.Number,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster_id: (experimental) The ClusterId to update.
        :param instance_fleet_name: (experimental) The InstanceFleetName to update.
        :param target_on_demand_capacity: (experimental) The target capacity of On-Demand units for the instance fleet. Default: - None
        :param target_spot_capacity: (experimental) The target capacity of Spot units for the instance fleet. Default: - None
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        :stability: experimental
        """
        props = EmrModifyInstanceFleetByNameProps(
            cluster_id=cluster_id,
            instance_fleet_name=instance_fleet_name,
            target_on_demand_capacity=target_on_demand_capacity,
            target_spot_capacity=target_spot_capacity,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(EmrModifyInstanceFleetByName, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrModifyInstanceFleetByNameProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "cluster_id": "clusterId",
        "instance_fleet_name": "instanceFleetName",
        "target_on_demand_capacity": "targetOnDemandCapacity",
        "target_spot_capacity": "targetSpotCapacity",
    },
)
class EmrModifyInstanceFleetByNameProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        cluster_id: builtins.str,
        instance_fleet_name: builtins.str,
        target_on_demand_capacity: jsii.Number,
        target_spot_capacity: jsii.Number,
    ) -> None:
        """(experimental) Properties for EmrModifyInstanceFleetByName.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param cluster_id: (experimental) The ClusterId to update.
        :param instance_fleet_name: (experimental) The InstanceFleetName to update.
        :param target_on_demand_capacity: (experimental) The target capacity of On-Demand units for the instance fleet. Default: - None
        :param target_spot_capacity: (experimental) The target capacity of Spot units for the instance fleet. Default: - None

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "cluster_id": cluster_id,
            "instance_fleet_name": instance_fleet_name,
            "target_on_demand_capacity": target_on_demand_capacity,
            "target_spot_capacity": target_spot_capacity,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def cluster_id(self) -> builtins.str:
        """(experimental) The ClusterId to update.

        :stability: experimental
        """
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return result

    @builtins.property
    def instance_fleet_name(self) -> builtins.str:
        """(experimental) The InstanceFleetName to update.

        :stability: experimental
        """
        result = self._values.get("instance_fleet_name")
        assert result is not None, "Required property 'instance_fleet_name' is missing"
        return result

    @builtins.property
    def target_on_demand_capacity(self) -> jsii.Number:
        """(experimental) The target capacity of On-Demand units for the instance fleet.

        :default: - None

        :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_InstanceFleetModifyConfig.html
        :stability: experimental
        """
        result = self._values.get("target_on_demand_capacity")
        assert result is not None, "Required property 'target_on_demand_capacity' is missing"
        return result

    @builtins.property
    def target_spot_capacity(self) -> jsii.Number:
        """(experimental) The target capacity of Spot units for the instance fleet.

        :default: - None

        :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_InstanceFleetModifyConfig.html
        :stability: experimental
        """
        result = self._values.get("target_spot_capacity")
        assert result is not None, "Required property 'target_spot_capacity' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrModifyInstanceFleetByNameProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrModifyInstanceGroupByName(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrModifyInstanceGroupByName",
):
    """(experimental) A Step Functions Task to to modify an InstanceGroup on an EMR Cluster.

    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster_id: builtins.str,
        instance_group: "EmrModifyInstanceGroupByName.InstanceGroupModifyConfigProperty",
        instance_group_name: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster_id: (experimental) The ClusterId to update.
        :param instance_group: (experimental) The JSON that you want to provide to your ModifyInstanceGroup call as input. This uses the same syntax as the ModifyInstanceGroups API.
        :param instance_group_name: (experimental) The InstanceGroupName to update.
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        :stability: experimental
        """
        props = EmrModifyInstanceGroupByNameProps(
            cluster_id=cluster_id,
            instance_group=instance_group,
            instance_group_name=instance_group_name,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(EmrModifyInstanceGroupByName, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrModifyInstanceGroupByName.InstanceGroupModifyConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configurations": "configurations",
            "e_c2_instance_ids_to_terminate": "eC2InstanceIdsToTerminate",
            "instance_count": "instanceCount",
            "shrink_policy": "shrinkPolicy",
        },
    )
    class InstanceGroupModifyConfigProperty:
        def __init__(
            self,
            *,
            configurations: typing.Optional[typing.List[EmrCreateCluster.ConfigurationProperty]] = None,
            e_c2_instance_ids_to_terminate: typing.Optional[typing.List[builtins.str]] = None,
            instance_count: typing.Optional[jsii.Number] = None,
            shrink_policy: typing.Optional["EmrModifyInstanceGroupByName.ShrinkPolicyProperty"] = None,
        ) -> None:
            """(experimental) Modify the size or configurations of an instance group.

            :param configurations: (experimental) A list of new or modified configurations to apply for an instance group. Default: - None
            :param e_c2_instance_ids_to_terminate: (experimental) The EC2 InstanceIds to terminate. After you terminate the instances, the instance group will not return to its original requested size. Default: - None
            :param instance_count: (experimental) Target size for the instance group. Default: - None
            :param shrink_policy: (experimental) Policy for customizing shrink operations. Default: - None

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_InstanceGroupModifyConfig.html
            :stability: experimental
            """
            if isinstance(shrink_policy, dict):
                shrink_policy = ShrinkPolicyProperty(**shrink_policy)
            self._values: typing.Dict[str, typing.Any] = {}
            if configurations is not None:
                self._values["configurations"] = configurations
            if e_c2_instance_ids_to_terminate is not None:
                self._values["e_c2_instance_ids_to_terminate"] = e_c2_instance_ids_to_terminate
            if instance_count is not None:
                self._values["instance_count"] = instance_count
            if shrink_policy is not None:
                self._values["shrink_policy"] = shrink_policy

        @builtins.property
        def configurations(
            self,
        ) -> typing.Optional[typing.List[EmrCreateCluster.ConfigurationProperty]]:
            """(experimental) A list of new or modified configurations to apply for an instance group.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("configurations")
            return result

        @builtins.property
        def e_c2_instance_ids_to_terminate(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            """(experimental) The EC2 InstanceIds to terminate.

            After you terminate the instances, the instance group will not return to its original requested size.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("e_c2_instance_ids_to_terminate")
            return result

        @builtins.property
        def instance_count(self) -> typing.Optional[jsii.Number]:
            """(experimental) Target size for the instance group.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("instance_count")
            return result

        @builtins.property
        def shrink_policy(
            self,
        ) -> typing.Optional["EmrModifyInstanceGroupByName.ShrinkPolicyProperty"]:
            """(experimental) Policy for customizing shrink operations.

            :default: - None

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_ShrinkPolicy.html
            :stability: experimental
            """
            result = self._values.get("shrink_policy")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceGroupModifyConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrModifyInstanceGroupByName.InstanceResizePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instances_to_protect": "instancesToProtect",
            "instances_to_terminate": "instancesToTerminate",
            "instance_termination_timeout": "instanceTerminationTimeout",
        },
    )
    class InstanceResizePolicyProperty:
        def __init__(
            self,
            *,
            instances_to_protect: typing.Optional[typing.List[builtins.str]] = None,
            instances_to_terminate: typing.Optional[typing.List[builtins.str]] = None,
            instance_termination_timeout: typing.Optional[aws_cdk.core.Duration] = None,
        ) -> None:
            """(experimental) Custom policy for requesting termination protection or termination of specific instances when shrinking an instance group.

            :param instances_to_protect: (experimental) Specific list of instances to be protected when shrinking an instance group. Default: - No instances will be protected when shrinking an instance group
            :param instances_to_terminate: (experimental) Specific list of instances to be terminated when shrinking an instance group. Default: - No instances will be terminated when shrinking an instance group.
            :param instance_termination_timeout: (experimental) Decommissioning timeout override for the specific list of instances to be terminated. Default: cdk.Duration.seconds

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_InstanceResizePolicy.html
            :stability: experimental
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if instances_to_protect is not None:
                self._values["instances_to_protect"] = instances_to_protect
            if instances_to_terminate is not None:
                self._values["instances_to_terminate"] = instances_to_terminate
            if instance_termination_timeout is not None:
                self._values["instance_termination_timeout"] = instance_termination_timeout

        @builtins.property
        def instances_to_protect(self) -> typing.Optional[typing.List[builtins.str]]:
            """(experimental) Specific list of instances to be protected when shrinking an instance group.

            :default: - No instances will be protected when shrinking an instance group

            :stability: experimental
            """
            result = self._values.get("instances_to_protect")
            return result

        @builtins.property
        def instances_to_terminate(self) -> typing.Optional[typing.List[builtins.str]]:
            """(experimental) Specific list of instances to be terminated when shrinking an instance group.

            :default: - No instances will be terminated when shrinking an instance group.

            :stability: experimental
            """
            result = self._values.get("instances_to_terminate")
            return result

        @builtins.property
        def instance_termination_timeout(
            self,
        ) -> typing.Optional[aws_cdk.core.Duration]:
            """(experimental) Decommissioning timeout override for the specific list of instances to be terminated.

            :default: cdk.Duration.seconds

            :stability: experimental
            """
            result = self._values.get("instance_termination_timeout")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceResizePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrModifyInstanceGroupByName.ShrinkPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "decommission_timeout": "decommissionTimeout",
            "instance_resize_policy": "instanceResizePolicy",
        },
    )
    class ShrinkPolicyProperty:
        def __init__(
            self,
            *,
            decommission_timeout: typing.Optional[aws_cdk.core.Duration] = None,
            instance_resize_policy: typing.Optional["EmrModifyInstanceGroupByName.InstanceResizePolicyProperty"] = None,
        ) -> None:
            """(experimental) Policy for customizing shrink operations.

            Allows configuration of decommissioning timeout and targeted instance shrinking.

            :param decommission_timeout: (experimental) The desired timeout for decommissioning an instance. Overrides the default YARN decommissioning timeout. Default: - EMR selected default
            :param instance_resize_policy: (experimental) Custom policy for requesting termination protection or termination of specific instances when shrinking an instance group. Default: - None

            :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_ShrinkPolicy.html
            :stability: experimental
            """
            if isinstance(instance_resize_policy, dict):
                instance_resize_policy = InstanceResizePolicyProperty(**instance_resize_policy)
            self._values: typing.Dict[str, typing.Any] = {}
            if decommission_timeout is not None:
                self._values["decommission_timeout"] = decommission_timeout
            if instance_resize_policy is not None:
                self._values["instance_resize_policy"] = instance_resize_policy

        @builtins.property
        def decommission_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
            """(experimental) The desired timeout for decommissioning an instance.

            Overrides the default YARN decommissioning timeout.

            :default: - EMR selected default

            :stability: experimental
            """
            result = self._values.get("decommission_timeout")
            return result

        @builtins.property
        def instance_resize_policy(
            self,
        ) -> typing.Optional["EmrModifyInstanceGroupByName.InstanceResizePolicyProperty"]:
            """(experimental) Custom policy for requesting termination protection or termination of specific instances when shrinking an instance group.

            :default: - None

            :stability: experimental
            """
            result = self._values.get("instance_resize_policy")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ShrinkPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrModifyInstanceGroupByNameProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "cluster_id": "clusterId",
        "instance_group": "instanceGroup",
        "instance_group_name": "instanceGroupName",
    },
)
class EmrModifyInstanceGroupByNameProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        cluster_id: builtins.str,
        instance_group: EmrModifyInstanceGroupByName.InstanceGroupModifyConfigProperty,
        instance_group_name: builtins.str,
    ) -> None:
        """(experimental) Properties for EmrModifyInstanceGroupByName.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param cluster_id: (experimental) The ClusterId to update.
        :param instance_group: (experimental) The JSON that you want to provide to your ModifyInstanceGroup call as input. This uses the same syntax as the ModifyInstanceGroups API.
        :param instance_group_name: (experimental) The InstanceGroupName to update.

        :stability: experimental
        """
        if isinstance(instance_group, dict):
            instance_group = EmrModifyInstanceGroupByName.InstanceGroupModifyConfigProperty(**instance_group)
        self._values: typing.Dict[str, typing.Any] = {
            "cluster_id": cluster_id,
            "instance_group": instance_group,
            "instance_group_name": instance_group_name,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def cluster_id(self) -> builtins.str:
        """(experimental) The ClusterId to update.

        :stability: experimental
        """
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return result

    @builtins.property
    def instance_group(
        self,
    ) -> EmrModifyInstanceGroupByName.InstanceGroupModifyConfigProperty:
        """(experimental) The JSON that you want to provide to your ModifyInstanceGroup call as input.

        This uses the same syntax as the ModifyInstanceGroups API.

        :see: https://docs.aws.amazon.com/emr/latest/APIReference/API_ModifyInstanceGroups.html
        :stability: experimental
        """
        result = self._values.get("instance_group")
        assert result is not None, "Required property 'instance_group' is missing"
        return result

    @builtins.property
    def instance_group_name(self) -> builtins.str:
        """(experimental) The InstanceGroupName to update.

        :stability: experimental
        """
        result = self._values.get("instance_group_name")
        assert result is not None, "Required property 'instance_group_name' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrModifyInstanceGroupByNameProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrSetClusterTerminationProtection(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrSetClusterTerminationProtection",
):
    """(experimental) A Step Functions Task to to set Termination Protection on an EMR Cluster.

    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster_id: builtins.str,
        termination_protected: builtins.bool,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster_id: (experimental) The ClusterId to update.
        :param termination_protected: (experimental) Termination protection indicator.
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        :stability: experimental
        """
        props = EmrSetClusterTerminationProtectionProps(
            cluster_id=cluster_id,
            termination_protected=termination_protected,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(EmrSetClusterTerminationProtection, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrSetClusterTerminationProtectionProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "cluster_id": "clusterId",
        "termination_protected": "terminationProtected",
    },
)
class EmrSetClusterTerminationProtectionProps(
    aws_cdk.aws_stepfunctions.TaskStateBaseProps,
):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        cluster_id: builtins.str,
        termination_protected: builtins.bool,
    ) -> None:
        """(experimental) Properties for EmrSetClusterTerminationProtection.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param cluster_id: (experimental) The ClusterId to update.
        :param termination_protected: (experimental) Termination protection indicator.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "cluster_id": cluster_id,
            "termination_protected": termination_protected,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def cluster_id(self) -> builtins.str:
        """(experimental) The ClusterId to update.

        :stability: experimental
        """
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return result

    @builtins.property
    def termination_protected(self) -> builtins.bool:
        """(experimental) Termination protection indicator.

        :stability: experimental
        """
        result = self._values.get("termination_protected")
        assert result is not None, "Required property 'termination_protected' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrSetClusterTerminationProtectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmrTerminateCluster(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrTerminateCluster",
):
    """(experimental) A Step Functions Task to terminate an EMR Cluster.

    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster_id: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster_id: (experimental) The ClusterId to terminate.
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        :stability: experimental
        """
        props = EmrTerminateClusterProps(
            cluster_id=cluster_id,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(EmrTerminateCluster, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EmrTerminateClusterProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "cluster_id": "clusterId",
    },
)
class EmrTerminateClusterProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        cluster_id: builtins.str,
    ) -> None:
        """(experimental) Properties for EmrTerminateCluster.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param cluster_id: (experimental) The ClusterId to terminate.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "cluster_id": cluster_id,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def cluster_id(self) -> builtins.str:
        """(experimental) The ClusterId to terminate.

        :stability: experimental
        """
        result = self._values.get("cluster_id")
        assert result is not None, "Required property 'cluster_id' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmrTerminateClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_option": "encryptionOption",
        "encryption_key": "encryptionKey",
    },
)
class EncryptionConfiguration:
    def __init__(
        self,
        *,
        encryption_option: "EncryptionOption",
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
    ) -> None:
        """(experimental) Encryption Configuration of the S3 bucket.

        :param encryption_option: (experimental) Type of S3 server-side encryption enabled. Default: EncryptionOption.S3_MANAGED
        :param encryption_key: (experimental) KMS key ARN or ID. Default: - No KMS key for Encryption Option SSE_S3 and default master key for Encryption Option SSE_KMS and CSE_KMS

        :see: https://docs.aws.amazon.com/athena/latest/APIReference/API_EncryptionConfiguration.html
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "encryption_option": encryption_option,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key

    @builtins.property
    def encryption_option(self) -> "EncryptionOption":
        """(experimental) Type of S3 server-side encryption enabled.

        :default: EncryptionOption.S3_MANAGED

        :stability: experimental
        """
        result = self._values.get("encryption_option")
        assert result is not None, "Required property 'encryption_option' is missing"
        return result

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """(experimental) KMS key ARN or ID.

        :default: - No KMS key for Encryption Option SSE_S3 and default master key for Encryption Option SSE_KMS and CSE_KMS

        :stability: experimental
        """
        result = self._values.get("encryption_key")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.EncryptionOption")
class EncryptionOption(enum.Enum):
    """(experimental) Encryption Options of the S3 bucket.

    :see: https://docs.aws.amazon.com/athena/latest/APIReference/API_EncryptionConfiguration.html#athena-Type-EncryptionConfiguration-EncryptionOption
    :stability: experimental
    """

    S3_MANAGED = "S3_MANAGED"
    """(experimental) Server side encryption (SSE) with an Amazon S3-managed key.

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingServerSideEncryption.html
    :stability: experimental
    """
    KMS = "KMS"
    """(experimental) Server-side encryption (SSE) with an AWS KMS key managed by the account owner.

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingKMSEncryption.html
    :stability: experimental
    """
    CLIENT_SIDE_KMS = "CLIENT_SIDE_KMS"
    """(experimental) Client-side encryption (CSE) with an AWS KMS key managed by the account owner.

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingClientSideEncryption.html
    :stability: experimental
    """


class EvaluateExpression(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EvaluateExpression",
):
    """(experimental) A Step Functions Task to evaluate an expression.

    OUTPUT: the output of this task is the evaluated expression.

    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        expression: builtins.str,
        runtime: typing.Optional[aws_cdk.aws_lambda.Runtime] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param expression: (experimental) The expression to evaluate. The expression may contain state paths.
        :param runtime: (experimental) The runtime language to use to evaluate the expression. Default: lambda.Runtime.NODEJS_10_X
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        :stability: experimental
        """
        props = EvaluateExpressionProps(
            expression=expression,
            runtime=runtime,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(EvaluateExpression, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EvaluateExpressionProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "expression": "expression",
        "runtime": "runtime",
    },
)
class EvaluateExpressionProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        expression: builtins.str,
        runtime: typing.Optional[aws_cdk.aws_lambda.Runtime] = None,
    ) -> None:
        """(experimental) Properties for EvaluateExpression.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param expression: (experimental) The expression to evaluate. The expression may contain state paths.
        :param runtime: (experimental) The runtime language to use to evaluate the expression. Default: lambda.Runtime.NODEJS_10_X

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "expression": expression,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if runtime is not None:
            self._values["runtime"] = runtime

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def expression(self) -> builtins.str:
        """(experimental) The expression to evaluate.

        The expression may contain state paths.

        :stability: experimental

        Example::

            # Example automatically generated. See https://github.com/aws/jsii/issues/826
            "$.a + $.b"
        """
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return result

    @builtins.property
    def runtime(self) -> typing.Optional[aws_cdk.aws_lambda.Runtime]:
        """(experimental) The runtime language to use to evaluate the expression.

        :default: lambda.Runtime.NODEJS_10_X

        :stability: experimental
        """
        result = self._values.get("runtime")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EvaluateExpressionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueDataBrewStartJobRun(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.GlueDataBrewStartJobRun",
):
    """(experimental) Start a Job run as a Task.

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-databrew.html
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param name: (experimental) Glue DataBrew Job to run.
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        :stability: experimental
        """
        props = GlueDataBrewStartJobRunProps(
            name=name,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(GlueDataBrewStartJobRun, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.GlueDataBrewStartJobRunProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "name": "name",
    },
)
class GlueDataBrewStartJobRunProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        name: builtins.str,
    ) -> None:
        """(experimental) Properties for starting a job run with StartJobRun.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param name: (experimental) Glue DataBrew Job to run.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """(experimental) Glue DataBrew Job to run.

        :stability: experimental
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueDataBrewStartJobRunProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GlueStartJobRun(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.GlueStartJobRun",
):
    """Starts an AWS Glue job in a Task state.

    OUTPUT: the output of this task is a JobRun structure, for details consult
    https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-jobs-runs.html#aws-glue-api-jobs-runs-JobRun

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-glue.html
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        glue_job_name: builtins.str,
        arguments: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
        notify_delay_after: typing.Optional[aws_cdk.core.Duration] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param glue_job_name: Glue job name.
        :param arguments: The job arguments specifically for this run. For this job run, they replace the default arguments set in the job definition itself. Default: - Default arguments set in the job definition
        :param notify_delay_after: After a job run starts, the number of minutes to wait before sending a job run delay notification. Must be at least 1 minute. Default: - Default delay set in the job definition
        :param security_configuration: The name of the SecurityConfiguration structure to be used with this job run. This must match the Glue API Default: - Default configuration set in the job definition
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        """
        props = GlueStartJobRunProps(
            glue_job_name=glue_job_name,
            arguments=arguments,
            notify_delay_after=notify_delay_after,
            security_configuration=security_configuration,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(GlueStartJobRun, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.GlueStartJobRunProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "glue_job_name": "glueJobName",
        "arguments": "arguments",
        "notify_delay_after": "notifyDelayAfter",
        "security_configuration": "securityConfiguration",
    },
)
class GlueStartJobRunProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        glue_job_name: builtins.str,
        arguments: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
        notify_delay_after: typing.Optional[aws_cdk.core.Duration] = None,
        security_configuration: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for starting an AWS Glue job as a task.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param glue_job_name: Glue job name.
        :param arguments: The job arguments specifically for this run. For this job run, they replace the default arguments set in the job definition itself. Default: - Default arguments set in the job definition
        :param notify_delay_after: After a job run starts, the number of minutes to wait before sending a job run delay notification. Must be at least 1 minute. Default: - Default delay set in the job definition
        :param security_configuration: The name of the SecurityConfiguration structure to be used with this job run. This must match the Glue API Default: - Default configuration set in the job definition
        """
        self._values: typing.Dict[str, typing.Any] = {
            "glue_job_name": glue_job_name,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if arguments is not None:
            self._values["arguments"] = arguments
        if notify_delay_after is not None:
            self._values["notify_delay_after"] = notify_delay_after
        if security_configuration is not None:
            self._values["security_configuration"] = security_configuration

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def glue_job_name(self) -> builtins.str:
        """Glue job name."""
        result = self._values.get("glue_job_name")
        assert result is not None, "Required property 'glue_job_name' is missing"
        return result

    @builtins.property
    def arguments(self) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskInput]:
        """The job arguments specifically for this run.

        For this job run, they replace the default arguments set in the job
        definition itself.

        :default: - Default arguments set in the job definition
        """
        result = self._values.get("arguments")
        return result

    @builtins.property
    def notify_delay_after(self) -> typing.Optional[aws_cdk.core.Duration]:
        """After a job run starts, the number of minutes to wait before sending a job run delay notification.

        Must be at least 1 minute.

        :default: - Default delay set in the job definition
        """
        result = self._values.get("notify_delay_after")
        return result

    @builtins.property
    def security_configuration(self) -> typing.Optional[builtins.str]:
        """The name of the SecurityConfiguration structure to be used with this job run.

        This must match the Glue API

        :default: - Default configuration set in the job definition

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-common.html#aws-glue-api-regex-oneLine
        """
        result = self._values.get("security_configuration")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GlueStartJobRunProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-stepfunctions-tasks.IContainerDefinition")
class IContainerDefinition(typing_extensions.Protocol):
    """(experimental) Configuration of the container used to host the model.

    :see: https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_ContainerDefinition.html
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IContainerDefinitionProxy

    @jsii.member(jsii_name="bind")
    def bind(self, task: "ISageMakerTask") -> ContainerDefinitionConfig:
        """(experimental) Called when the ContainerDefinition is used by a SageMaker task.

        :param task: -

        :stability: experimental
        """
        ...


class _IContainerDefinitionProxy:
    """(experimental) Configuration of the container used to host the model.

    :see: https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_ContainerDefinition.html
    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-stepfunctions-tasks.IContainerDefinition"

    @jsii.member(jsii_name="bind")
    def bind(self, task: "ISageMakerTask") -> ContainerDefinitionConfig:
        """(experimental) Called when the ContainerDefinition is used by a SageMaker task.

        :param task: -

        :stability: experimental
        """
        return jsii.invoke(self, "bind", [task])


@jsii.interface(jsii_type="@aws-cdk/aws-stepfunctions-tasks.IEcsLaunchTarget")
class IEcsLaunchTarget(typing_extensions.Protocol):
    """An Amazon ECS launch type determines the type of infrastructure on which your tasks and services are hosted.

    :see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/launch_types.html
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IEcsLaunchTargetProxy

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        task: EcsRunTask,
        *,
        task_definition: aws_cdk.aws_ecs.ITaskDefinition,
        cluster: typing.Optional[aws_cdk.aws_ecs.ICluster] = None,
    ) -> EcsLaunchTargetConfig:
        """called when the ECS launch target is configured on RunTask.

        :param task: -
        :param task_definition: Task definition to run Docker containers in Amazon ECS.
        :param cluster: A regional grouping of one or more container instances on which you can run tasks and services. Default: - No cluster
        """
        ...


class _IEcsLaunchTargetProxy:
    """An Amazon ECS launch type determines the type of infrastructure on which your tasks and services are hosted.

    :see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/launch_types.html
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-stepfunctions-tasks.IEcsLaunchTarget"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        task: EcsRunTask,
        *,
        task_definition: aws_cdk.aws_ecs.ITaskDefinition,
        cluster: typing.Optional[aws_cdk.aws_ecs.ICluster] = None,
    ) -> EcsLaunchTargetConfig:
        """called when the ECS launch target is configured on RunTask.

        :param task: -
        :param task_definition: Task definition to run Docker containers in Amazon ECS.
        :param cluster: A regional grouping of one or more container instances on which you can run tasks and services. Default: - No cluster
        """
        launch_target_options = LaunchTargetBindOptions(
            task_definition=task_definition, cluster=cluster
        )

        return jsii.invoke(self, "bind", [task, launch_target_options])


@jsii.interface(jsii_type="@aws-cdk/aws-stepfunctions-tasks.ISageMakerTask")
class ISageMakerTask(aws_cdk.aws_iam.IGrantable, typing_extensions.Protocol):
    """(experimental) Task to train a machine learning model using Amazon SageMaker.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISageMakerTaskProxy


class _ISageMakerTaskProxy(
    jsii.proxy_for(aws_cdk.aws_iam.IGrantable) # type: ignore
):
    """(experimental) Task to train a machine learning model using Amazon SageMaker.

    :stability: experimental
    """

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-stepfunctions-tasks.ISageMakerTask"
    pass


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.InputMode")
class InputMode(enum.Enum):
    """(experimental) Input mode that the algorithm supports.

    :stability: experimental
    """

    PIPE = "PIPE"
    """(experimental) Pipe mode.

    :stability: experimental
    """
    FILE = "FILE"
    """(experimental) File mode.

    :stability: experimental
    """


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.InvocationType")
class InvocationType(enum.Enum):
    """Invocation type of a Lambda."""

    REQUEST_RESPONSE = "REQUEST_RESPONSE"
    """Invoke synchronously.

    The API response includes the function response and additional data.
    """
    EVENT = "EVENT"
    """Invoke asynchronously.

    Send events that fail multiple times to the function's dead-letter queue (if it's configured).
    The API response only includes a status code.
    """
    DRY_RUN = "DRY_RUN"
    """TValidate parameter values and verify that the user or role has permission to invoke the function."""


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class InvokeActivity(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.InvokeActivity",
):
    """(deprecated) A Step Functions Task to invoke an Activity worker.

    An Activity can be used directly as a Resource.

    :deprecated: - use ``StepFunctionsInvokeActivity``

    :stability: deprecated
    """

    def __init__(
        self,
        activity: aws_cdk.aws_stepfunctions.IActivity,
        *,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param activity: -
        :param heartbeat: Maximum time between heart beats. If the time between heart beats takes longer than this, a 'Timeout' error is raised. Default: No heart beat timeout

        :stability: deprecated
        """
        props = InvokeActivityProps(heartbeat=heartbeat)

        jsii.create(InvokeActivity, self, [activity, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _task: aws_cdk.aws_stepfunctions.Task,
    ) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """(deprecated) Called when the task object is used in a workflow.

        :param _task: -

        :stability: deprecated
        """
        return jsii.invoke(self, "bind", [_task])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.InvokeActivityProps",
    jsii_struct_bases=[],
    name_mapping={"heartbeat": "heartbeat"},
)
class InvokeActivityProps:
    def __init__(
        self,
        *,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """Properties for FunctionTask.

        :param heartbeat: Maximum time between heart beats. If the time between heart beats takes longer than this, a 'Timeout' error is raised. Default: No heart beat timeout
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Maximum time between heart beats.

        If the time between heart beats takes longer than this, a 'Timeout' error is raised.

        :default: No heart beat timeout
        """
        result = self._values.get("heartbeat")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InvokeActivityProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class InvokeFunction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.InvokeFunction",
):
    """(deprecated) A Step Functions Task to invoke a Lambda function.

    The Lambda function Arn is defined as Resource in the state machine definition.

    OUTPUT: the output of this task is the return value of the Lambda Function.

    :deprecated: Use ``LambdaInvoke``

    :stability: deprecated
    """

    def __init__(
        self,
        lambda_function: aws_cdk.aws_lambda.IFunction,
        *,
        payload: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        """
        :param lambda_function: -
        :param payload: (deprecated) The JSON that you want to provide to your Lambda function as input. This parameter is named as payload to keep consistent with RunLambdaTask class. Default: - The JSON data indicated by the task's InputPath is used as payload

        :stability: deprecated
        """
        props = InvokeFunctionProps(payload=payload)

        jsii.create(InvokeFunction, self, [lambda_function, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _task: aws_cdk.aws_stepfunctions.Task,
    ) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """(deprecated) Called when the task object is used in a workflow.

        :param _task: -

        :stability: deprecated
        """
        return jsii.invoke(self, "bind", [_task])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.InvokeFunctionProps",
    jsii_struct_bases=[],
    name_mapping={"payload": "payload"},
)
class InvokeFunctionProps:
    def __init__(
        self,
        *,
        payload: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        """(deprecated) Properties for InvokeFunction.

        :param payload: (deprecated) The JSON that you want to provide to your Lambda function as input. This parameter is named as payload to keep consistent with RunLambdaTask class. Default: - The JSON data indicated by the task's InputPath is used as payload

        :deprecated: use ``LambdaInvoke``

        :stability: deprecated
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if payload is not None:
            self._values["payload"] = payload

    @builtins.property
    def payload(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        """(deprecated) The JSON that you want to provide to your Lambda function as input.

        This parameter is named as payload to keep consistent with RunLambdaTask class.

        :default: - The JSON data indicated by the task's InputPath is used as payload

        :stability: deprecated
        """
        result = self._values.get("payload")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InvokeFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.JobDependency",
    jsii_struct_bases=[],
    name_mapping={"job_id": "jobId", "type": "type"},
)
class JobDependency:
    def __init__(
        self,
        *,
        job_id: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        """An object representing an AWS Batch job dependency.

        :param job_id: The job ID of the AWS Batch job associated with this dependency. Default: - No jobId
        :param type: The type of the job dependency. Default: - No type
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if job_id is not None:
            self._values["job_id"] = job_id
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def job_id(self) -> typing.Optional[builtins.str]:
        """The job ID of the AWS Batch job associated with this dependency.

        :default: - No jobId
        """
        result = self._values.get("job_id")
        return result

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        """The type of the job dependency.

        :default: - No type
        """
        result = self._values.get("type")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobDependency(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.LambdaInvocationType")
class LambdaInvocationType(enum.Enum):
    """Invocation type of a Lambda."""

    REQUEST_RESPONSE = "REQUEST_RESPONSE"
    """Invoke the function synchronously.

    Keep the connection open until the function returns a response or times out.
    The API response includes the function response and additional data.
    """
    EVENT = "EVENT"
    """Invoke the function asynchronously.

    Send events that fail multiple times to the function's dead-letter queue (if it's configured).
    The API response only includes a status code.
    """
    DRY_RUN = "DRY_RUN"
    """Validate parameter values and verify that the user or role has permission to invoke the function."""


class LambdaInvoke(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.LambdaInvoke",
):
    """Invoke a Lambda function as a Task.

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-lambda.html
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        lambda_function: aws_cdk.aws_lambda.IFunction,
        client_context: typing.Optional[builtins.str] = None,
        invocation_type: typing.Optional[LambdaInvocationType] = None,
        payload: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
        payload_response_only: typing.Optional[builtins.bool] = None,
        qualifier: typing.Optional[builtins.str] = None,
        retry_on_service_exceptions: typing.Optional[builtins.bool] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param lambda_function: Lambda function to invoke.
        :param client_context: Up to 3583 bytes of base64-encoded data about the invoking client to pass to the function. Default: - No context
        :param invocation_type: Invocation type of the Lambda function. Default: InvocationType.REQUEST_RESPONSE
        :param payload: The JSON that will be supplied as input to the Lambda function. Default: - The state input (JSON path '$')
        :param payload_response_only: Invoke the Lambda in a way that only returns the payload response without additional metadata. The ``payloadResponseOnly`` property cannot be used if ``integrationPattern``, ``invocationType``, ``clientContext``, or ``qualifier`` are specified. It always uses the REQUEST_RESPONSE behavior. Default: false
        :param qualifier: Version or alias to invoke a published version of the function. You only need to supply this if you want the version of the Lambda Function to depend on data in the state machine state. If not, you can pass the appropriate Alias or Version object directly as the ``lambdaFunction`` argument. Default: - Version or alias inherent to the ``lambdaFunction`` object.
        :param retry_on_service_exceptions: Whether to retry on Lambda service exceptions. This handles ``Lambda.ServiceException``, ``Lambda.AWSLambdaException`` and ``Lambda.SdkClientException`` with an interval of 2 seconds, a back-off rate of 2 and 6 maximum attempts. Default: true
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        """
        props = LambdaInvokeProps(
            lambda_function=lambda_function,
            client_context=client_context,
            invocation_type=invocation_type,
            payload=payload,
            payload_response_only=payload_response_only,
            qualifier=qualifier,
            retry_on_service_exceptions=retry_on_service_exceptions,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(LambdaInvoke, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.LambdaInvokeProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "lambda_function": "lambdaFunction",
        "client_context": "clientContext",
        "invocation_type": "invocationType",
        "payload": "payload",
        "payload_response_only": "payloadResponseOnly",
        "qualifier": "qualifier",
        "retry_on_service_exceptions": "retryOnServiceExceptions",
    },
)
class LambdaInvokeProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        lambda_function: aws_cdk.aws_lambda.IFunction,
        client_context: typing.Optional[builtins.str] = None,
        invocation_type: typing.Optional[LambdaInvocationType] = None,
        payload: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
        payload_response_only: typing.Optional[builtins.bool] = None,
        qualifier: typing.Optional[builtins.str] = None,
        retry_on_service_exceptions: typing.Optional[builtins.bool] = None,
    ) -> None:
        """Properties for invoking a Lambda function with LambdaInvoke.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param lambda_function: Lambda function to invoke.
        :param client_context: Up to 3583 bytes of base64-encoded data about the invoking client to pass to the function. Default: - No context
        :param invocation_type: Invocation type of the Lambda function. Default: InvocationType.REQUEST_RESPONSE
        :param payload: The JSON that will be supplied as input to the Lambda function. Default: - The state input (JSON path '$')
        :param payload_response_only: Invoke the Lambda in a way that only returns the payload response without additional metadata. The ``payloadResponseOnly`` property cannot be used if ``integrationPattern``, ``invocationType``, ``clientContext``, or ``qualifier`` are specified. It always uses the REQUEST_RESPONSE behavior. Default: false
        :param qualifier: Version or alias to invoke a published version of the function. You only need to supply this if you want the version of the Lambda Function to depend on data in the state machine state. If not, you can pass the appropriate Alias or Version object directly as the ``lambdaFunction`` argument. Default: - Version or alias inherent to the ``lambdaFunction`` object.
        :param retry_on_service_exceptions: Whether to retry on Lambda service exceptions. This handles ``Lambda.ServiceException``, ``Lambda.AWSLambdaException`` and ``Lambda.SdkClientException`` with an interval of 2 seconds, a back-off rate of 2 and 6 maximum attempts. Default: true
        """
        self._values: typing.Dict[str, typing.Any] = {
            "lambda_function": lambda_function,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if client_context is not None:
            self._values["client_context"] = client_context
        if invocation_type is not None:
            self._values["invocation_type"] = invocation_type
        if payload is not None:
            self._values["payload"] = payload
        if payload_response_only is not None:
            self._values["payload_response_only"] = payload_response_only
        if qualifier is not None:
            self._values["qualifier"] = qualifier
        if retry_on_service_exceptions is not None:
            self._values["retry_on_service_exceptions"] = retry_on_service_exceptions

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def lambda_function(self) -> aws_cdk.aws_lambda.IFunction:
        """Lambda function to invoke."""
        result = self._values.get("lambda_function")
        assert result is not None, "Required property 'lambda_function' is missing"
        return result

    @builtins.property
    def client_context(self) -> typing.Optional[builtins.str]:
        """Up to 3583 bytes of base64-encoded data about the invoking client to pass to the function.

        :default: - No context
        """
        result = self._values.get("client_context")
        return result

    @builtins.property
    def invocation_type(self) -> typing.Optional[LambdaInvocationType]:
        """Invocation type of the Lambda function.

        :default: InvocationType.REQUEST_RESPONSE
        """
        result = self._values.get("invocation_type")
        return result

    @builtins.property
    def payload(self) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskInput]:
        """The JSON that will be supplied as input to the Lambda function.

        :default: - The state input (JSON path '$')
        """
        result = self._values.get("payload")
        return result

    @builtins.property
    def payload_response_only(self) -> typing.Optional[builtins.bool]:
        """Invoke the Lambda in a way that only returns the payload response without additional metadata.

        The ``payloadResponseOnly`` property cannot be used if ``integrationPattern``, ``invocationType``,
        ``clientContext``, or ``qualifier`` are specified.
        It always uses the REQUEST_RESPONSE behavior.

        :default: false
        """
        result = self._values.get("payload_response_only")
        return result

    @builtins.property
    def qualifier(self) -> typing.Optional[builtins.str]:
        """Version or alias to invoke a published version of the function.

        You only need to supply this if you want the version of the Lambda Function to depend
        on data in the state machine state. If not, you can pass the appropriate Alias or Version object
        directly as the ``lambdaFunction`` argument.

        :default: - Version or alias inherent to the ``lambdaFunction`` object.
        """
        result = self._values.get("qualifier")
        return result

    @builtins.property
    def retry_on_service_exceptions(self) -> typing.Optional[builtins.bool]:
        """Whether to retry on Lambda service exceptions.

        This handles ``Lambda.ServiceException``, ``Lambda.AWSLambdaException`` and
        ``Lambda.SdkClientException`` with an interval of 2 seconds, a back-off rate
        of 2 and 6 maximum attempts.

        :default: true

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/bp-lambda-serviceexception.html
        """
        result = self._values.get("retry_on_service_exceptions")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaInvokeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.LaunchTargetBindOptions",
    jsii_struct_bases=[],
    name_mapping={"task_definition": "taskDefinition", "cluster": "cluster"},
)
class LaunchTargetBindOptions:
    def __init__(
        self,
        *,
        task_definition: aws_cdk.aws_ecs.ITaskDefinition,
        cluster: typing.Optional[aws_cdk.aws_ecs.ICluster] = None,
    ) -> None:
        """Options for binding a launch target to an ECS run job task.

        :param task_definition: Task definition to run Docker containers in Amazon ECS.
        :param cluster: A regional grouping of one or more container instances on which you can run tasks and services. Default: - No cluster
        """
        self._values: typing.Dict[str, typing.Any] = {
            "task_definition": task_definition,
        }
        if cluster is not None:
            self._values["cluster"] = cluster

    @builtins.property
    def task_definition(self) -> aws_cdk.aws_ecs.ITaskDefinition:
        """Task definition to run Docker containers in Amazon ECS."""
        result = self._values.get("task_definition")
        assert result is not None, "Required property 'task_definition' is missing"
        return result

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        """A regional grouping of one or more container instances on which you can run tasks and services.

        :default: - No cluster
        """
        result = self._values.get("cluster")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LaunchTargetBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.MetricDefinition",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "regex": "regex"},
)
class MetricDefinition:
    def __init__(self, *, name: builtins.str, regex: builtins.str) -> None:
        """(experimental) Specifies the metric name and regular expressions used to parse algorithm logs.

        :param name: (experimental) Name of the metric.
        :param regex: (experimental) Regular expression that searches the output of a training job and gets the value of the metric.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "regex": regex,
        }

    @builtins.property
    def name(self) -> builtins.str:
        """(experimental) Name of the metric.

        :stability: experimental
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def regex(self) -> builtins.str:
        """(experimental) Regular expression that searches the output of a training job and gets the value of the metric.

        :stability: experimental
        """
        result = self._values.get("regex")
        assert result is not None, "Required property 'regex' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricDefinition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.Mode")
class Mode(enum.Enum):
    """(experimental) Specifies how many models the container hosts.

    :stability: experimental
    """

    SINGLE_MODEL = "SINGLE_MODEL"
    """(experimental) Container hosts a single model.

    :stability: experimental
    """
    MULTI_MODEL = "MULTI_MODEL"
    """(experimental) Container hosts multiple models.

    :see: https://docs.aws.amazon.com/sagemaker/latest/dg/multi-model-endpoints.html
    :stability: experimental
    """


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.ModelClientOptions",
    jsii_struct_bases=[],
    name_mapping={
        "invocations_max_retries": "invocationsMaxRetries",
        "invocations_timeout": "invocationsTimeout",
    },
)
class ModelClientOptions:
    def __init__(
        self,
        *,
        invocations_max_retries: typing.Optional[jsii.Number] = None,
        invocations_timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """(experimental) Configures the timeout and maximum number of retries for processing a transform job invocation.

        :param invocations_max_retries: (experimental) The maximum number of retries when invocation requests are failing. Default: 0
        :param invocations_timeout: (experimental) The timeout duration for an invocation request. Default: Duration.minutes(1)

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if invocations_max_retries is not None:
            self._values["invocations_max_retries"] = invocations_max_retries
        if invocations_timeout is not None:
            self._values["invocations_timeout"] = invocations_timeout

    @builtins.property
    def invocations_max_retries(self) -> typing.Optional[jsii.Number]:
        """(experimental) The maximum number of retries when invocation requests are failing.

        :default: 0

        :stability: experimental
        """
        result = self._values.get("invocations_max_retries")
        return result

    @builtins.property
    def invocations_timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(experimental) The timeout duration for an invocation request.

        :default: Duration.minutes(1)

        :stability: experimental
        """
        result = self._values.get("invocations_timeout")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ModelClientOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.OutputDataConfig",
    jsii_struct_bases=[],
    name_mapping={
        "s3_output_location": "s3OutputLocation",
        "encryption_key": "encryptionKey",
    },
)
class OutputDataConfig:
    def __init__(
        self,
        *,
        s3_output_location: "S3Location",
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
    ) -> None:
        """(experimental) Configures the S3 bucket where SageMaker will save the result of model training.

        :param s3_output_location: (experimental) Identifies the S3 path where you want Amazon SageMaker to store the model artifacts.
        :param encryption_key: (experimental) Optional KMS encryption key that Amazon SageMaker uses to encrypt the model artifacts at rest using Amazon S3 server-side encryption. Default: - Amazon SageMaker uses the default KMS key for Amazon S3 for your role's account

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "s3_output_location": s3_output_location,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key

    @builtins.property
    def s3_output_location(self) -> "S3Location":
        """(experimental) Identifies the S3 path where you want Amazon SageMaker to store the model artifacts.

        :stability: experimental
        """
        result = self._values.get("s3_output_location")
        assert result is not None, "Required property 's3_output_location' is missing"
        return result

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """(experimental) Optional KMS encryption key that Amazon SageMaker uses to encrypt the model artifacts at rest using Amazon S3 server-side encryption.

        :default: - Amazon SageMaker uses the default KMS key for Amazon S3 for your role's account

        :stability: experimental
        """
        result = self._values.get("encryption_key")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OutputDataConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.ProductionVariant",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "model_name": "modelName",
        "variant_name": "variantName",
        "accelerator_type": "acceleratorType",
        "initial_instance_count": "initialInstanceCount",
        "initial_variant_weight": "initialVariantWeight",
    },
)
class ProductionVariant:
    def __init__(
        self,
        *,
        instance_type: aws_cdk.aws_ec2.InstanceType,
        model_name: builtins.str,
        variant_name: builtins.str,
        accelerator_type: typing.Optional[AcceleratorType] = None,
        initial_instance_count: typing.Optional[jsii.Number] = None,
        initial_variant_weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        """(experimental) Identifies a model that you want to host and the resources to deploy for hosting it.

        :param instance_type: (experimental) The ML compute instance type.
        :param model_name: (experimental) The name of the model that you want to host. This is the name that you specified when creating the model.
        :param variant_name: (experimental) The name of the production variant.
        :param accelerator_type: (experimental) The size of the Elastic Inference (EI) instance to use for the production variant. Default: - None
        :param initial_instance_count: (experimental) Number of instances to launch initially. Default: - 1
        :param initial_variant_weight: (experimental) Determines initial traffic distribution among all of the models that you specify in the endpoint configuration. Default: - 1.0

        :see: https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_ProductionVariant.html
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "instance_type": instance_type,
            "model_name": model_name,
            "variant_name": variant_name,
        }
        if accelerator_type is not None:
            self._values["accelerator_type"] = accelerator_type
        if initial_instance_count is not None:
            self._values["initial_instance_count"] = initial_instance_count
        if initial_variant_weight is not None:
            self._values["initial_variant_weight"] = initial_variant_weight

    @builtins.property
    def instance_type(self) -> aws_cdk.aws_ec2.InstanceType:
        """(experimental) The ML compute instance type.

        :stability: experimental
        """
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return result

    @builtins.property
    def model_name(self) -> builtins.str:
        """(experimental) The name of the model that you want to host.

        This is the name that you specified when creating the model.

        :stability: experimental
        """
        result = self._values.get("model_name")
        assert result is not None, "Required property 'model_name' is missing"
        return result

    @builtins.property
    def variant_name(self) -> builtins.str:
        """(experimental) The name of the production variant.

        :stability: experimental
        """
        result = self._values.get("variant_name")
        assert result is not None, "Required property 'variant_name' is missing"
        return result

    @builtins.property
    def accelerator_type(self) -> typing.Optional[AcceleratorType]:
        """(experimental) The size of the Elastic Inference (EI) instance to use for the production variant.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("accelerator_type")
        return result

    @builtins.property
    def initial_instance_count(self) -> typing.Optional[jsii.Number]:
        """(experimental) Number of instances to launch initially.

        :default: - 1

        :stability: experimental
        """
        result = self._values.get("initial_instance_count")
        return result

    @builtins.property
    def initial_variant_weight(self) -> typing.Optional[jsii.Number]:
        """(experimental) Determines initial traffic distribution among all of the models that you specify in the endpoint configuration.

        :default: - 1.0

        :stability: experimental
        """
        result = self._values.get("initial_variant_weight")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProductionVariant(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class PublishToTopic(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.PublishToTopic",
):
    """(deprecated) A Step Functions Task to publish messages to SNS topic.

    A Function can be used directly as a Resource, but this class mirrors
    integration with other AWS services via a specific class instance.

    :deprecated: Use ``SnsPublish``

    :stability: deprecated
    """

    def __init__(
        self,
        topic: aws_cdk.aws_sns.ITopic,
        *,
        message: aws_cdk.aws_stepfunctions.TaskInput,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern] = None,
        message_per_subscription_type: typing.Optional[builtins.bool] = None,
        subject: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param topic: -
        :param message: (deprecated) The text message to send to the topic.
        :param integration_pattern: (deprecated) The service integration pattern indicates different ways to call Publish to SNS. The valid value is either FIRE_AND_FORGET or WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET
        :param message_per_subscription_type: (deprecated) If true, send a different message to every subscription type. If this is set to true, message must be a JSON object with a "default" key and a key for every subscription type (such as "sqs", "email", etc.) The values are strings representing the messages being sent to every subscription type. Default: false
        :param subject: (deprecated) Used as the "Subject" line when the message is delivered to email endpoints. Also included, if present, in the standard JSON messages delivered to other endpoints. Default: - No subject

        :stability: deprecated
        """
        props = PublishToTopicProps(
            message=message,
            integration_pattern=integration_pattern,
            message_per_subscription_type=message_per_subscription_type,
            subject=subject,
        )

        jsii.create(PublishToTopic, self, [topic, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _task: aws_cdk.aws_stepfunctions.Task,
    ) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """(deprecated) Called when the task object is used in a workflow.

        :param _task: -

        :stability: deprecated
        """
        return jsii.invoke(self, "bind", [_task])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.PublishToTopicProps",
    jsii_struct_bases=[],
    name_mapping={
        "message": "message",
        "integration_pattern": "integrationPattern",
        "message_per_subscription_type": "messagePerSubscriptionType",
        "subject": "subject",
    },
)
class PublishToTopicProps:
    def __init__(
        self,
        *,
        message: aws_cdk.aws_stepfunctions.TaskInput,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern] = None,
        message_per_subscription_type: typing.Optional[builtins.bool] = None,
        subject: typing.Optional[builtins.str] = None,
    ) -> None:
        """(deprecated) Properties for PublishTask.

        :param message: (deprecated) The text message to send to the topic.
        :param integration_pattern: (deprecated) The service integration pattern indicates different ways to call Publish to SNS. The valid value is either FIRE_AND_FORGET or WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET
        :param message_per_subscription_type: (deprecated) If true, send a different message to every subscription type. If this is set to true, message must be a JSON object with a "default" key and a key for every subscription type (such as "sqs", "email", etc.) The values are strings representing the messages being sent to every subscription type. Default: false
        :param subject: (deprecated) Used as the "Subject" line when the message is delivered to email endpoints. Also included, if present, in the standard JSON messages delivered to other endpoints. Default: - No subject

        :deprecated: Use ``SnsPublish``

        :stability: deprecated
        """
        self._values: typing.Dict[str, typing.Any] = {
            "message": message,
        }
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if message_per_subscription_type is not None:
            self._values["message_per_subscription_type"] = message_per_subscription_type
        if subject is not None:
            self._values["subject"] = subject

    @builtins.property
    def message(self) -> aws_cdk.aws_stepfunctions.TaskInput:
        """(deprecated) The text message to send to the topic.

        :stability: deprecated
        """
        result = self._values.get("message")
        assert result is not None, "Required property 'message' is missing"
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """(deprecated) The service integration pattern indicates different ways to call Publish to SNS.

        The valid value is either FIRE_AND_FORGET or WAIT_FOR_TASK_TOKEN.

        :default: FIRE_AND_FORGET

        :stability: deprecated
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def message_per_subscription_type(self) -> typing.Optional[builtins.bool]:
        """(deprecated) If true, send a different message to every subscription type.

        If this is set to true, message must be a JSON object with a
        "default" key and a key for every subscription type (such as "sqs",
        "email", etc.) The values are strings representing the messages
        being sent to every subscription type.

        :default: false

        :see: https://docs.aws.amazon.com/sns/latest/api/API_Publish.html#API_Publish_RequestParameters
        :stability: deprecated
        """
        result = self._values.get("message_per_subscription_type")
        return result

    @builtins.property
    def subject(self) -> typing.Optional[builtins.str]:
        """(deprecated) Used as the "Subject" line when the message is delivered to email endpoints.

        Also included, if present, in the standard JSON messages delivered to other endpoints.

        :default: - No subject

        :stability: deprecated
        """
        result = self._values.get("subject")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PublishToTopicProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.QueryExecutionContext",
    jsii_struct_bases=[],
    name_mapping={"catalog_name": "catalogName", "database_name": "databaseName"},
)
class QueryExecutionContext:
    def __init__(
        self,
        *,
        catalog_name: typing.Optional[builtins.str] = None,
        database_name: typing.Optional[builtins.str] = None,
    ) -> None:
        """(experimental) Database and data catalog context in which the query execution occurs.

        :param catalog_name: (experimental) Name of catalog used in query execution. Default: - No catalog
        :param database_name: (experimental) Name of database used in query execution. Default: - No database

        :see: https://docs.aws.amazon.com/athena/latest/APIReference/API_QueryExecutionContext.html
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if catalog_name is not None:
            self._values["catalog_name"] = catalog_name
        if database_name is not None:
            self._values["database_name"] = database_name

    @builtins.property
    def catalog_name(self) -> typing.Optional[builtins.str]:
        """(experimental) Name of catalog used in query execution.

        :default: - No catalog

        :stability: experimental
        """
        result = self._values.get("catalog_name")
        return result

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        """(experimental) Name of database used in query execution.

        :default: - No database

        :stability: experimental
        """
        result = self._values.get("database_name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QueryExecutionContext(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.RecordWrapperType")
class RecordWrapperType(enum.Enum):
    """(experimental) Define the format of the input data.

    :stability: experimental
    """

    NONE = "NONE"
    """(experimental) None record wrapper type.

    :stability: experimental
    """
    RECORD_IO = "RECORD_IO"
    """(experimental) RecordIO record wrapper type.

    :stability: experimental
    """


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.ResourceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "instance_count": "instanceCount",
        "instance_type": "instanceType",
        "volume_size": "volumeSize",
        "volume_encryption_key": "volumeEncryptionKey",
    },
)
class ResourceConfig:
    def __init__(
        self,
        *,
        instance_count: jsii.Number,
        instance_type: aws_cdk.aws_ec2.InstanceType,
        volume_size: aws_cdk.core.Size,
        volume_encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
    ) -> None:
        """(experimental) Specifies the resources, ML compute instances, and ML storage volumes to deploy for model training.

        :param instance_count: (experimental) The number of ML compute instances to use. Default: 1 instance.
        :param instance_type: (experimental) ML compute instance type. Default: is the 'm4.xlarge' instance type.
        :param volume_size: (experimental) Size of the ML storage volume that you want to provision. Default: 10 GB EBS volume.
        :param volume_encryption_key: (experimental) KMS key that Amazon SageMaker uses to encrypt data on the storage volume attached to the ML compute instance(s) that run the training job. Default: - Amazon SageMaker uses the default KMS key for Amazon S3 for your role's account

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "instance_count": instance_count,
            "instance_type": instance_type,
            "volume_size": volume_size,
        }
        if volume_encryption_key is not None:
            self._values["volume_encryption_key"] = volume_encryption_key

    @builtins.property
    def instance_count(self) -> jsii.Number:
        """(experimental) The number of ML compute instances to use.

        :default: 1 instance.

        :stability: experimental
        """
        result = self._values.get("instance_count")
        assert result is not None, "Required property 'instance_count' is missing"
        return result

    @builtins.property
    def instance_type(self) -> aws_cdk.aws_ec2.InstanceType:
        """(experimental) ML compute instance type.

        :default: is the 'm4.xlarge' instance type.

        :stability: experimental
        """
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return result

    @builtins.property
    def volume_size(self) -> aws_cdk.core.Size:
        """(experimental) Size of the ML storage volume that you want to provision.

        :default: 10 GB EBS volume.

        :stability: experimental
        """
        result = self._values.get("volume_size")
        assert result is not None, "Required property 'volume_size' is missing"
        return result

    @builtins.property
    def volume_encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """(experimental) KMS key that Amazon SageMaker uses to encrypt data on the storage volume attached to the ML compute instance(s) that run the training job.

        :default: - Amazon SageMaker uses the default KMS key for Amazon S3 for your role's account

        :stability: experimental
        """
        result = self._values.get("volume_encryption_key")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.ResultConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_configuration": "encryptionConfiguration",
        "output_location": "outputLocation",
    },
)
class ResultConfiguration:
    def __init__(
        self,
        *,
        encryption_configuration: typing.Optional[EncryptionConfiguration] = None,
        output_location: typing.Optional[aws_cdk.aws_s3.Location] = None,
    ) -> None:
        """(experimental) Location of query result along with S3 bucket configuration.

        :param encryption_configuration: (experimental) Encryption option used if enabled in S3. Default: - SSE_S3 encrpytion is enabled with default encryption key
        :param output_location: (experimental) S3 path of query results. Default: - Query Result Location set in Athena settings for this workgroup

        :see: https://docs.aws.amazon.com/athena/latest/APIReference/API_ResultConfiguration.html
        :stability: experimental
        """
        if isinstance(encryption_configuration, dict):
            encryption_configuration = EncryptionConfiguration(**encryption_configuration)
        if isinstance(output_location, dict):
            output_location = aws_cdk.aws_s3.Location(**output_location)
        self._values: typing.Dict[str, typing.Any] = {}
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if output_location is not None:
            self._values["output_location"] = output_location

    @builtins.property
    def encryption_configuration(self) -> typing.Optional[EncryptionConfiguration]:
        """(experimental) Encryption option used if enabled in S3.

        :default: - SSE_S3 encrpytion is enabled with default encryption key

        :stability: experimental
        """
        result = self._values.get("encryption_configuration")
        return result

    @builtins.property
    def output_location(self) -> typing.Optional[aws_cdk.aws_s3.Location]:
        """(experimental) S3 path of query results.

        :default: - Query Result Location set in Athena settings for this workgroup

        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            s3:
        """
        result = self._values.get("output_location")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResultConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class RunBatchJob(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.RunBatchJob",
):
    """(deprecated) A Step Functions Task to run AWS Batch.

    :deprecated: use ``BatchSubmitJob``

    :stability: deprecated
    """

    def __init__(
        self,
        *,
        job_definition: aws_cdk.aws_batch.IJobDefinition,
        job_name: builtins.str,
        job_queue: aws_cdk.aws_batch.IJobQueue,
        array_size: typing.Optional[jsii.Number] = None,
        attempts: typing.Optional[jsii.Number] = None,
        container_overrides: typing.Optional[ContainerOverrides] = None,
        depends_on: typing.Optional[typing.List[JobDependency]] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern] = None,
        payload: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param job_definition: (deprecated) The job definition used by this job.
        :param job_name: (deprecated) The name of the job. The first character must be alphanumeric, and up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.
        :param job_queue: (deprecated) The job queue into which the job is submitted.
        :param array_size: (deprecated) The array size can be between 2 and 10,000. If you specify array properties for a job, it becomes an array job. For more information, see Array Jobs in the AWS Batch User Guide. Default: - No array size
        :param attempts: (deprecated) The number of times to move a job to the RUNNABLE status. You may specify between 1 and 10 attempts. If the value of attempts is greater than one, the job is retried on failure the same number of attempts as the value. Default: - 1
        :param container_overrides: (deprecated) A list of container overrides in JSON format that specify the name of a container in the specified job definition and the overrides it should receive. Default: - No container overrides
        :param depends_on: (deprecated) A list of dependencies for the job. A job can depend upon a maximum of 20 jobs. Default: - No dependencies
        :param integration_pattern: (deprecated) The service integration pattern indicates different ways to call TerminateCluster. The valid value is either FIRE_AND_FORGET or SYNC. Default: SYNC
        :param payload: (deprecated) The payload to be passed as parametrs to the batch job. Default: - No parameters are passed
        :param timeout: (deprecated) The timeout configuration for this SubmitJob operation. The minimum value for the timeout is 60 seconds. Default: - No timeout

        :stability: deprecated
        """
        props = RunBatchJobProps(
            job_definition=job_definition,
            job_name=job_name,
            job_queue=job_queue,
            array_size=array_size,
            attempts=attempts,
            container_overrides=container_overrides,
            depends_on=depends_on,
            integration_pattern=integration_pattern,
            payload=payload,
            timeout=timeout,
        )

        jsii.create(RunBatchJob, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _task: aws_cdk.aws_stepfunctions.Task,
    ) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """(deprecated) Called when the task object is used in a workflow.

        :param _task: -

        :stability: deprecated
        """
        return jsii.invoke(self, "bind", [_task])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.RunBatchJobProps",
    jsii_struct_bases=[],
    name_mapping={
        "job_definition": "jobDefinition",
        "job_name": "jobName",
        "job_queue": "jobQueue",
        "array_size": "arraySize",
        "attempts": "attempts",
        "container_overrides": "containerOverrides",
        "depends_on": "dependsOn",
        "integration_pattern": "integrationPattern",
        "payload": "payload",
        "timeout": "timeout",
    },
)
class RunBatchJobProps:
    def __init__(
        self,
        *,
        job_definition: aws_cdk.aws_batch.IJobDefinition,
        job_name: builtins.str,
        job_queue: aws_cdk.aws_batch.IJobQueue,
        array_size: typing.Optional[jsii.Number] = None,
        attempts: typing.Optional[jsii.Number] = None,
        container_overrides: typing.Optional[ContainerOverrides] = None,
        depends_on: typing.Optional[typing.List[JobDependency]] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern] = None,
        payload: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """(deprecated) Properties for RunBatchJob.

        :param job_definition: (deprecated) The job definition used by this job.
        :param job_name: (deprecated) The name of the job. The first character must be alphanumeric, and up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.
        :param job_queue: (deprecated) The job queue into which the job is submitted.
        :param array_size: (deprecated) The array size can be between 2 and 10,000. If you specify array properties for a job, it becomes an array job. For more information, see Array Jobs in the AWS Batch User Guide. Default: - No array size
        :param attempts: (deprecated) The number of times to move a job to the RUNNABLE status. You may specify between 1 and 10 attempts. If the value of attempts is greater than one, the job is retried on failure the same number of attempts as the value. Default: - 1
        :param container_overrides: (deprecated) A list of container overrides in JSON format that specify the name of a container in the specified job definition and the overrides it should receive. Default: - No container overrides
        :param depends_on: (deprecated) A list of dependencies for the job. A job can depend upon a maximum of 20 jobs. Default: - No dependencies
        :param integration_pattern: (deprecated) The service integration pattern indicates different ways to call TerminateCluster. The valid value is either FIRE_AND_FORGET or SYNC. Default: SYNC
        :param payload: (deprecated) The payload to be passed as parametrs to the batch job. Default: - No parameters are passed
        :param timeout: (deprecated) The timeout configuration for this SubmitJob operation. The minimum value for the timeout is 60 seconds. Default: - No timeout

        :deprecated: use ``BatchSubmitJob``

        :stability: deprecated
        """
        if isinstance(container_overrides, dict):
            container_overrides = ContainerOverrides(**container_overrides)
        self._values: typing.Dict[str, typing.Any] = {
            "job_definition": job_definition,
            "job_name": job_name,
            "job_queue": job_queue,
        }
        if array_size is not None:
            self._values["array_size"] = array_size
        if attempts is not None:
            self._values["attempts"] = attempts
        if container_overrides is not None:
            self._values["container_overrides"] = container_overrides
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if payload is not None:
            self._values["payload"] = payload
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def job_definition(self) -> aws_cdk.aws_batch.IJobDefinition:
        """(deprecated) The job definition used by this job.

        :stability: deprecated
        """
        result = self._values.get("job_definition")
        assert result is not None, "Required property 'job_definition' is missing"
        return result

    @builtins.property
    def job_name(self) -> builtins.str:
        """(deprecated) The name of the job.

        The first character must be alphanumeric, and up to 128 letters (uppercase and lowercase),
        numbers, hyphens, and underscores are allowed.

        :stability: deprecated
        """
        result = self._values.get("job_name")
        assert result is not None, "Required property 'job_name' is missing"
        return result

    @builtins.property
    def job_queue(self) -> aws_cdk.aws_batch.IJobQueue:
        """(deprecated) The job queue into which the job is submitted.

        :stability: deprecated
        """
        result = self._values.get("job_queue")
        assert result is not None, "Required property 'job_queue' is missing"
        return result

    @builtins.property
    def array_size(self) -> typing.Optional[jsii.Number]:
        """(deprecated) The array size can be between 2 and 10,000.

        If you specify array properties for a job, it becomes an array job.
        For more information, see Array Jobs in the AWS Batch User Guide.

        :default: - No array size

        :stability: deprecated
        """
        result = self._values.get("array_size")
        return result

    @builtins.property
    def attempts(self) -> typing.Optional[jsii.Number]:
        """(deprecated) The number of times to move a job to the RUNNABLE status.

        You may specify between 1 and 10 attempts.
        If the value of attempts is greater than one,
        the job is retried on failure the same number of attempts as the value.

        :default: - 1

        :stability: deprecated
        """
        result = self._values.get("attempts")
        return result

    @builtins.property
    def container_overrides(self) -> typing.Optional[ContainerOverrides]:
        """(deprecated) A list of container overrides in JSON format that specify the name of a container in the specified job definition and the overrides it should receive.

        :default: - No container overrides

        :see: https://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html#Batch-SubmitJob-request-containerOverrides
        :stability: deprecated
        """
        result = self._values.get("container_overrides")
        return result

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[JobDependency]]:
        """(deprecated) A list of dependencies for the job.

        A job can depend upon a maximum of 20 jobs.

        :default: - No dependencies

        :see: https://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html#Batch-SubmitJob-request-dependsOn
        :stability: deprecated
        """
        result = self._values.get("depends_on")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """(deprecated) The service integration pattern indicates different ways to call TerminateCluster.

        The valid value is either FIRE_AND_FORGET or SYNC.

        :default: SYNC

        :stability: deprecated
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def payload(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        """(deprecated) The payload to be passed as parametrs to the batch job.

        :default: - No parameters are passed

        :stability: deprecated
        """
        result = self._values.get("payload")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(deprecated) The timeout configuration for this SubmitJob operation.

        The minimum value for the timeout is 60 seconds.

        :default: - No timeout

        :see: https://docs.aws.amazon.com/batch/latest/APIReference/API_SubmitJob.html#Batch-SubmitJob-request-timeout
        :stability: deprecated
        """
        result = self._values.get("timeout")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunBatchJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RunEcsEc2Task(
    EcsRunTaskBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.RunEcsEc2Task",
):
    """(deprecated) Run an ECS/EC2 Task in a StepFunctions workflow.

    :deprecated: - replaced by ``EcsRunTask``

    :stability: deprecated
    """

    def __init__(
        self,
        *,
        placement_constraints: typing.Optional[typing.List[aws_cdk.aws_ecs.PlacementConstraint]] = None,
        placement_strategies: typing.Optional[typing.List[aws_cdk.aws_ecs.PlacementStrategy]] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        cluster: aws_cdk.aws_ecs.ICluster,
        task_definition: aws_cdk.aws_ecs.TaskDefinition,
        container_overrides: typing.Optional[typing.List[ContainerOverride]] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern] = None,
    ) -> None:
        """
        :param placement_constraints: Placement constraints. Default: No constraints
        :param placement_strategies: Placement strategies. Default: No strategies
        :param security_group: Existing security group to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param subnets: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        :param cluster: The topic to run the task on.
        :param task_definition: Task Definition used for running tasks in the service. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions
        :param container_overrides: Container setting overrides. Key is the name of the container to override, value is the values you want to override. Default: - No overrides
        :param integration_pattern: The service integration pattern indicates different ways to call RunTask in ECS. The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET

        :stability: deprecated
        """
        props = RunEcsEc2TaskProps(
            placement_constraints=placement_constraints,
            placement_strategies=placement_strategies,
            security_group=security_group,
            subnets=subnets,
            cluster=cluster,
            task_definition=task_definition,
            container_overrides=container_overrides,
            integration_pattern=integration_pattern,
        )

        jsii.create(RunEcsEc2Task, self, [props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.RunEcsEc2TaskProps",
    jsii_struct_bases=[CommonEcsRunTaskProps],
    name_mapping={
        "cluster": "cluster",
        "task_definition": "taskDefinition",
        "container_overrides": "containerOverrides",
        "integration_pattern": "integrationPattern",
        "placement_constraints": "placementConstraints",
        "placement_strategies": "placementStrategies",
        "security_group": "securityGroup",
        "subnets": "subnets",
    },
)
class RunEcsEc2TaskProps(CommonEcsRunTaskProps):
    def __init__(
        self,
        *,
        cluster: aws_cdk.aws_ecs.ICluster,
        task_definition: aws_cdk.aws_ecs.TaskDefinition,
        container_overrides: typing.Optional[typing.List[ContainerOverride]] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern] = None,
        placement_constraints: typing.Optional[typing.List[aws_cdk.aws_ecs.PlacementConstraint]] = None,
        placement_strategies: typing.Optional[typing.List[aws_cdk.aws_ecs.PlacementStrategy]] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """Properties to run an ECS task on EC2 in StepFunctionsan ECS.

        :param cluster: The topic to run the task on.
        :param task_definition: Task Definition used for running tasks in the service. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions
        :param container_overrides: Container setting overrides. Key is the name of the container to override, value is the values you want to override. Default: - No overrides
        :param integration_pattern: The service integration pattern indicates different ways to call RunTask in ECS. The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET
        :param placement_constraints: Placement constraints. Default: No constraints
        :param placement_strategies: Placement strategies. Default: No strategies
        :param security_group: Existing security group to use for the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: A new security group is created
        :param subnets: In what subnets to place the task's ENIs. (Only applicable in case the TaskDefinition is configured for AwsVpc networking) Default: Private subnets
        """
        if isinstance(subnets, dict):
            subnets = aws_cdk.aws_ec2.SubnetSelection(**subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
            "task_definition": task_definition,
        }
        if container_overrides is not None:
            self._values["container_overrides"] = container_overrides
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if placement_constraints is not None:
            self._values["placement_constraints"] = placement_constraints
        if placement_strategies is not None:
            self._values["placement_strategies"] = placement_strategies
        if security_group is not None:
            self._values["security_group"] = security_group
        if subnets is not None:
            self._values["subnets"] = subnets

    @builtins.property
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """The topic to run the task on."""
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return result

    @builtins.property
    def task_definition(self) -> aws_cdk.aws_ecs.TaskDefinition:
        """Task Definition used for running tasks in the service.

        Note: this must be TaskDefinition, and not ITaskDefinition,
        as it requires properties that are not known for imported task definitions
        """
        result = self._values.get("task_definition")
        assert result is not None, "Required property 'task_definition' is missing"
        return result

    @builtins.property
    def container_overrides(self) -> typing.Optional[typing.List[ContainerOverride]]:
        """Container setting overrides.

        Key is the name of the container to override, value is the
        values you want to override.

        :default: - No overrides
        """
        result = self._values.get("container_overrides")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """The service integration pattern indicates different ways to call RunTask in ECS.

        The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN.

        :default: FIRE_AND_FORGET
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def placement_constraints(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ecs.PlacementConstraint]]:
        """Placement constraints.

        :default: No constraints
        """
        result = self._values.get("placement_constraints")
        return result

    @builtins.property
    def placement_strategies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ecs.PlacementStrategy]]:
        """Placement strategies.

        :default: No strategies
        """
        result = self._values.get("placement_strategies")
        return result

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """Existing security group to use for the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        :default: A new security group is created
        """
        result = self._values.get("security_group")
        return result

    @builtins.property
    def subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """In what subnets to place the task's ENIs.

        (Only applicable in case the TaskDefinition is configured for AwsVpc networking)

        :default: Private subnets
        """
        result = self._values.get("subnets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunEcsEc2TaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RunEcsFargateTask(
    EcsRunTaskBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.RunEcsFargateTask",
):
    """(deprecated) Start a service on an ECS cluster.

    :deprecated: - replaced by ``EcsRunTask``

    :stability: deprecated
    """

    def __init__(
        self,
        *,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        platform_version: typing.Optional[aws_cdk.aws_ecs.FargatePlatformVersion] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        cluster: aws_cdk.aws_ecs.ICluster,
        task_definition: aws_cdk.aws_ecs.TaskDefinition,
        container_overrides: typing.Optional[typing.List[ContainerOverride]] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern] = None,
    ) -> None:
        """
        :param assign_public_ip: Assign public IP addresses to each task. Default: false
        :param platform_version: Fargate platform version to run this service on. Unless you have specific compatibility requirements, you don't need to specify this. Default: Latest
        :param security_group: Existing security group to use for the tasks. Default: A new security group is created
        :param subnets: In what subnets to place the task's ENIs. Default: Private subnet if assignPublicIp, public subnets otherwise
        :param cluster: The topic to run the task on.
        :param task_definition: Task Definition used for running tasks in the service. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions
        :param container_overrides: Container setting overrides. Key is the name of the container to override, value is the values you want to override. Default: - No overrides
        :param integration_pattern: The service integration pattern indicates different ways to call RunTask in ECS. The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET

        :stability: deprecated
        """
        props = RunEcsFargateTaskProps(
            assign_public_ip=assign_public_ip,
            platform_version=platform_version,
            security_group=security_group,
            subnets=subnets,
            cluster=cluster,
            task_definition=task_definition,
            container_overrides=container_overrides,
            integration_pattern=integration_pattern,
        )

        jsii.create(RunEcsFargateTask, self, [props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.RunEcsFargateTaskProps",
    jsii_struct_bases=[CommonEcsRunTaskProps],
    name_mapping={
        "cluster": "cluster",
        "task_definition": "taskDefinition",
        "container_overrides": "containerOverrides",
        "integration_pattern": "integrationPattern",
        "assign_public_ip": "assignPublicIp",
        "platform_version": "platformVersion",
        "security_group": "securityGroup",
        "subnets": "subnets",
    },
)
class RunEcsFargateTaskProps(CommonEcsRunTaskProps):
    def __init__(
        self,
        *,
        cluster: aws_cdk.aws_ecs.ICluster,
        task_definition: aws_cdk.aws_ecs.TaskDefinition,
        container_overrides: typing.Optional[typing.List[ContainerOverride]] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern] = None,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        platform_version: typing.Optional[aws_cdk.aws_ecs.FargatePlatformVersion] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """Properties to define an ECS service.

        :param cluster: The topic to run the task on.
        :param task_definition: Task Definition used for running tasks in the service. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions
        :param container_overrides: Container setting overrides. Key is the name of the container to override, value is the values you want to override. Default: - No overrides
        :param integration_pattern: The service integration pattern indicates different ways to call RunTask in ECS. The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET
        :param assign_public_ip: Assign public IP addresses to each task. Default: false
        :param platform_version: Fargate platform version to run this service on. Unless you have specific compatibility requirements, you don't need to specify this. Default: Latest
        :param security_group: Existing security group to use for the tasks. Default: A new security group is created
        :param subnets: In what subnets to place the task's ENIs. Default: Private subnet if assignPublicIp, public subnets otherwise
        """
        if isinstance(subnets, dict):
            subnets = aws_cdk.aws_ec2.SubnetSelection(**subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
            "task_definition": task_definition,
        }
        if container_overrides is not None:
            self._values["container_overrides"] = container_overrides
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if assign_public_ip is not None:
            self._values["assign_public_ip"] = assign_public_ip
        if platform_version is not None:
            self._values["platform_version"] = platform_version
        if security_group is not None:
            self._values["security_group"] = security_group
        if subnets is not None:
            self._values["subnets"] = subnets

    @builtins.property
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """The topic to run the task on."""
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return result

    @builtins.property
    def task_definition(self) -> aws_cdk.aws_ecs.TaskDefinition:
        """Task Definition used for running tasks in the service.

        Note: this must be TaskDefinition, and not ITaskDefinition,
        as it requires properties that are not known for imported task definitions
        """
        result = self._values.get("task_definition")
        assert result is not None, "Required property 'task_definition' is missing"
        return result

    @builtins.property
    def container_overrides(self) -> typing.Optional[typing.List[ContainerOverride]]:
        """Container setting overrides.

        Key is the name of the container to override, value is the
        values you want to override.

        :default: - No overrides
        """
        result = self._values.get("container_overrides")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """The service integration pattern indicates different ways to call RunTask in ECS.

        The valid value for Lambda is FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN.

        :default: FIRE_AND_FORGET
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        """Assign public IP addresses to each task.

        :default: false
        """
        result = self._values.get("assign_public_ip")
        return result

    @builtins.property
    def platform_version(
        self,
    ) -> typing.Optional[aws_cdk.aws_ecs.FargatePlatformVersion]:
        """Fargate platform version to run this service on.

        Unless you have specific compatibility requirements, you don't need to
        specify this.

        :default: Latest
        """
        result = self._values.get("platform_version")
        return result

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """Existing security group to use for the tasks.

        :default: A new security group is created
        """
        result = self._values.get("security_group")
        return result

    @builtins.property
    def subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """In what subnets to place the task's ENIs.

        :default: Private subnet if assignPublicIp, public subnets otherwise
        """
        result = self._values.get("subnets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunEcsFargateTaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class RunGlueJobTask(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.RunGlueJobTask",
):
    """(deprecated) Invoke a Glue job as a Task.

    OUTPUT: the output of this task is a JobRun structure, for details consult
    https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-jobs-runs.html#aws-glue-api-jobs-runs-JobRun

    :deprecated: use ``GlueStartJobRun``

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-glue.html
    :stability: deprecated
    """

    def __init__(
        self,
        glue_job_name: builtins.str,
        *,
        arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern] = None,
        notify_delay_after: typing.Optional[aws_cdk.core.Duration] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param glue_job_name: -
        :param arguments: (deprecated) The job arguments specifically for this run. For this job run, they replace the default arguments set in the job definition itself. Default: - Default arguments set in the job definition
        :param integration_pattern: (deprecated) The service integration pattern indicates different ways to start the Glue job. The valid value for Glue is either FIRE_AND_FORGET or SYNC. Default: FIRE_AND_FORGET
        :param notify_delay_after: (deprecated) After a job run starts, the number of minutes to wait before sending a job run delay notification. Must be at least 1 minute. Default: - Default delay set in the job definition
        :param security_configuration: (deprecated) The name of the SecurityConfiguration structure to be used with this job run. This must match the Glue API `single-line string pattern <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-common.html#aws-glue-api-regex-oneLine>`_. Default: - Default configuration set in the job definition
        :param timeout: (deprecated) The job run timeout. This is the maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. Must be at least 1 minute. Default: - Default timeout set in the job definition

        :stability: deprecated
        """
        props = RunGlueJobTaskProps(
            arguments=arguments,
            integration_pattern=integration_pattern,
            notify_delay_after=notify_delay_after,
            security_configuration=security_configuration,
            timeout=timeout,
        )

        jsii.create(RunGlueJobTask, self, [glue_job_name, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        task: aws_cdk.aws_stepfunctions.Task,
    ) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """(deprecated) Called when the task object is used in a workflow.

        :param task: -

        :stability: deprecated
        """
        return jsii.invoke(self, "bind", [task])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.RunGlueJobTaskProps",
    jsii_struct_bases=[],
    name_mapping={
        "arguments": "arguments",
        "integration_pattern": "integrationPattern",
        "notify_delay_after": "notifyDelayAfter",
        "security_configuration": "securityConfiguration",
        "timeout": "timeout",
    },
)
class RunGlueJobTaskProps:
    def __init__(
        self,
        *,
        arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern] = None,
        notify_delay_after: typing.Optional[aws_cdk.core.Duration] = None,
        security_configuration: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """(deprecated) Properties for RunGlueJobTask.

        :param arguments: (deprecated) The job arguments specifically for this run. For this job run, they replace the default arguments set in the job definition itself. Default: - Default arguments set in the job definition
        :param integration_pattern: (deprecated) The service integration pattern indicates different ways to start the Glue job. The valid value for Glue is either FIRE_AND_FORGET or SYNC. Default: FIRE_AND_FORGET
        :param notify_delay_after: (deprecated) After a job run starts, the number of minutes to wait before sending a job run delay notification. Must be at least 1 minute. Default: - Default delay set in the job definition
        :param security_configuration: (deprecated) The name of the SecurityConfiguration structure to be used with this job run. This must match the Glue API `single-line string pattern <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-common.html#aws-glue-api-regex-oneLine>`_. Default: - Default configuration set in the job definition
        :param timeout: (deprecated) The job run timeout. This is the maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. Must be at least 1 minute. Default: - Default timeout set in the job definition

        :deprecated: use ``GlueStartJobRun``

        :stability: deprecated
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if arguments is not None:
            self._values["arguments"] = arguments
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if notify_delay_after is not None:
            self._values["notify_delay_after"] = notify_delay_after
        if security_configuration is not None:
            self._values["security_configuration"] = security_configuration
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def arguments(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(deprecated) The job arguments specifically for this run.

        For this job run, they replace the default arguments set in the job definition itself.

        :default: - Default arguments set in the job definition

        :stability: deprecated
        """
        result = self._values.get("arguments")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """(deprecated) The service integration pattern indicates different ways to start the Glue job.

        The valid value for Glue is either FIRE_AND_FORGET or SYNC.

        :default: FIRE_AND_FORGET

        :stability: deprecated
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def notify_delay_after(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(deprecated) After a job run starts, the number of minutes to wait before sending a job run delay notification.

        Must be at least 1 minute.

        :default: - Default delay set in the job definition

        :stability: deprecated
        """
        result = self._values.get("notify_delay_after")
        return result

    @builtins.property
    def security_configuration(self) -> typing.Optional[builtins.str]:
        """(deprecated) The name of the SecurityConfiguration structure to be used with this job run.

        This must match the Glue API
        `single-line string pattern <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-common.html#aws-glue-api-regex-oneLine>`_.

        :default: - Default configuration set in the job definition

        :stability: deprecated
        """
        result = self._values.get("security_configuration")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(deprecated) The job run timeout.

        This is the maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status.
        Must be at least 1 minute.

        :default: - Default timeout set in the job definition

        :stability: deprecated
        """
        result = self._values.get("timeout")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunGlueJobTaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class RunLambdaTask(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.RunLambdaTask",
):
    """(deprecated) Invoke a Lambda function as a Task.

    OUTPUT: the output of this task is either the return value of Lambda's
    Invoke call, or whatever the Lambda Function posted back using
    ``SendTaskSuccess/SendTaskFailure`` in ``waitForTaskToken`` mode.

    :deprecated: Use ``LambdaInvoke``

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-lambda.html
    :stability: deprecated
    """

    def __init__(
        self,
        lambda_function: aws_cdk.aws_lambda.IFunction,
        *,
        client_context: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern] = None,
        invocation_type: typing.Optional[InvocationType] = None,
        payload: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
        qualifier: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param lambda_function: -
        :param client_context: (deprecated) Client context to pass to the function. Default: - No context
        :param integration_pattern: (deprecated) The service integration pattern indicates different ways to invoke Lambda function. The valid value for Lambda is either FIRE_AND_FORGET or WAIT_FOR_TASK_TOKEN, it determines whether to pause the workflow until a task token is returned. If this is set to WAIT_FOR_TASK_TOKEN, the JsonPath.taskToken value must be included somewhere in the payload and the Lambda must call ``SendTaskSuccess/SendTaskFailure`` using that token. Default: FIRE_AND_FORGET
        :param invocation_type: (deprecated) Invocation type of the Lambda function. Default: RequestResponse
        :param payload: (deprecated) The JSON that you want to provide to your Lambda function as input. Default: - The state input (JSON path '$')
        :param qualifier: (deprecated) Version or alias of the function to be invoked. Default: - No qualifier

        :stability: deprecated
        """
        props = RunLambdaTaskProps(
            client_context=client_context,
            integration_pattern=integration_pattern,
            invocation_type=invocation_type,
            payload=payload,
            qualifier=qualifier,
        )

        jsii.create(RunLambdaTask, self, [lambda_function, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _task: aws_cdk.aws_stepfunctions.Task,
    ) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """(deprecated) Called when the task object is used in a workflow.

        :param _task: -

        :stability: deprecated
        """
        return jsii.invoke(self, "bind", [_task])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.RunLambdaTaskProps",
    jsii_struct_bases=[],
    name_mapping={
        "client_context": "clientContext",
        "integration_pattern": "integrationPattern",
        "invocation_type": "invocationType",
        "payload": "payload",
        "qualifier": "qualifier",
    },
)
class RunLambdaTaskProps:
    def __init__(
        self,
        *,
        client_context: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern] = None,
        invocation_type: typing.Optional[InvocationType] = None,
        payload: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
        qualifier: typing.Optional[builtins.str] = None,
    ) -> None:
        """(deprecated) Properties for RunLambdaTask.

        :param client_context: (deprecated) Client context to pass to the function. Default: - No context
        :param integration_pattern: (deprecated) The service integration pattern indicates different ways to invoke Lambda function. The valid value for Lambda is either FIRE_AND_FORGET or WAIT_FOR_TASK_TOKEN, it determines whether to pause the workflow until a task token is returned. If this is set to WAIT_FOR_TASK_TOKEN, the JsonPath.taskToken value must be included somewhere in the payload and the Lambda must call ``SendTaskSuccess/SendTaskFailure`` using that token. Default: FIRE_AND_FORGET
        :param invocation_type: (deprecated) Invocation type of the Lambda function. Default: RequestResponse
        :param payload: (deprecated) The JSON that you want to provide to your Lambda function as input. Default: - The state input (JSON path '$')
        :param qualifier: (deprecated) Version or alias of the function to be invoked. Default: - No qualifier

        :deprecated: Use ``LambdaInvoke``

        :stability: deprecated
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if client_context is not None:
            self._values["client_context"] = client_context
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if invocation_type is not None:
            self._values["invocation_type"] = invocation_type
        if payload is not None:
            self._values["payload"] = payload
        if qualifier is not None:
            self._values["qualifier"] = qualifier

    @builtins.property
    def client_context(self) -> typing.Optional[builtins.str]:
        """(deprecated) Client context to pass to the function.

        :default: - No context

        :stability: deprecated
        """
        result = self._values.get("client_context")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """(deprecated) The service integration pattern indicates different ways to invoke Lambda function.

        The valid value for Lambda is either FIRE_AND_FORGET or WAIT_FOR_TASK_TOKEN,
        it determines whether to pause the workflow until a task token is returned.

        If this is set to WAIT_FOR_TASK_TOKEN, the JsonPath.taskToken value must be included
        somewhere in the payload and the Lambda must call
        ``SendTaskSuccess/SendTaskFailure`` using that token.

        :default: FIRE_AND_FORGET

        :stability: deprecated
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def invocation_type(self) -> typing.Optional[InvocationType]:
        """(deprecated) Invocation type of the Lambda function.

        :default: RequestResponse

        :stability: deprecated
        """
        result = self._values.get("invocation_type")
        return result

    @builtins.property
    def payload(self) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskInput]:
        """(deprecated) The JSON that you want to provide to your Lambda function as input.

        :default: - The state input (JSON path '$')

        :stability: deprecated
        """
        result = self._values.get("payload")
        return result

    @builtins.property
    def qualifier(self) -> typing.Optional[builtins.str]:
        """(deprecated) Version or alias of the function to be invoked.

        :default: - No qualifier

        :stability: deprecated
        """
        result = self._values.get("qualifier")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunLambdaTaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.S3DataDistributionType")
class S3DataDistributionType(enum.Enum):
    """(experimental) S3 Data Distribution Type.

    :stability: experimental
    """

    FULLY_REPLICATED = "FULLY_REPLICATED"
    """(experimental) Fully replicated S3 Data Distribution Type.

    :stability: experimental
    """
    SHARDED_BY_S3_KEY = "SHARDED_BY_S3_KEY"
    """(experimental) Sharded By S3 Key Data Distribution Type.

    :stability: experimental
    """


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.S3DataSource",
    jsii_struct_bases=[],
    name_mapping={
        "s3_location": "s3Location",
        "attribute_names": "attributeNames",
        "s3_data_distribution_type": "s3DataDistributionType",
        "s3_data_type": "s3DataType",
    },
)
class S3DataSource:
    def __init__(
        self,
        *,
        s3_location: "S3Location",
        attribute_names: typing.Optional[typing.List[builtins.str]] = None,
        s3_data_distribution_type: typing.Optional[S3DataDistributionType] = None,
        s3_data_type: typing.Optional["S3DataType"] = None,
    ) -> None:
        """(experimental) S3 location of the channel data.

        :param s3_location: (experimental) S3 Uri.
        :param attribute_names: (experimental) List of one or more attribute names to use that are found in a specified augmented manifest file. Default: - No attribute names
        :param s3_data_distribution_type: (experimental) S3 Data Distribution Type. Default: - None
        :param s3_data_type: (experimental) S3 Data Type. Default: S3_PREFIX

        :see: https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_S3DataSource.html
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "s3_location": s3_location,
        }
        if attribute_names is not None:
            self._values["attribute_names"] = attribute_names
        if s3_data_distribution_type is not None:
            self._values["s3_data_distribution_type"] = s3_data_distribution_type
        if s3_data_type is not None:
            self._values["s3_data_type"] = s3_data_type

    @builtins.property
    def s3_location(self) -> "S3Location":
        """(experimental) S3 Uri.

        :stability: experimental
        """
        result = self._values.get("s3_location")
        assert result is not None, "Required property 's3_location' is missing"
        return result

    @builtins.property
    def attribute_names(self) -> typing.Optional[typing.List[builtins.str]]:
        """(experimental) List of one or more attribute names to use that are found in a specified augmented manifest file.

        :default: - No attribute names

        :stability: experimental
        """
        result = self._values.get("attribute_names")
        return result

    @builtins.property
    def s3_data_distribution_type(self) -> typing.Optional[S3DataDistributionType]:
        """(experimental) S3 Data Distribution Type.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("s3_data_distribution_type")
        return result

    @builtins.property
    def s3_data_type(self) -> typing.Optional["S3DataType"]:
        """(experimental) S3 Data Type.

        :default: S3_PREFIX

        :stability: experimental
        """
        result = self._values.get("s3_data_type")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3DataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.S3DataType")
class S3DataType(enum.Enum):
    """(experimental) S3 Data Type.

    :stability: experimental
    """

    MANIFEST_FILE = "MANIFEST_FILE"
    """(experimental) Manifest File Data Type.

    :stability: experimental
    """
    S3_PREFIX = "S3_PREFIX"
    """(experimental) S3 Prefix Data Type.

    :stability: experimental
    """
    AUGMENTED_MANIFEST_FILE = "AUGMENTED_MANIFEST_FILE"
    """(experimental) Augmented Manifest File Data Type.

    :stability: experimental
    """


class S3Location(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.S3Location",
):
    """(experimental) Constructs ``IS3Location`` objects.

    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _S3LocationProxy

    def __init__(self) -> None:
        jsii.create(S3Location, self, [])

    @jsii.member(jsii_name="fromBucket")
    @builtins.classmethod
    def from_bucket(
        cls,
        bucket: aws_cdk.aws_s3.IBucket,
        key_prefix: builtins.str,
    ) -> "S3Location":
        """(experimental) An ``IS3Location`` built with a determined bucket and key prefix.

        :param bucket: is the bucket where the objects are to be stored.
        :param key_prefix: is the key prefix used by the location.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromBucket", [bucket, key_prefix])

    @jsii.member(jsii_name="fromJsonExpression")
    @builtins.classmethod
    def from_json_expression(cls, expression: builtins.str) -> "S3Location":
        """(experimental) An ``IS3Location`` determined fully by a JSON Path from the task input.

        Due to the dynamic nature of those locations, the IAM grants that will be set by ``grantRead`` and ``grantWrite``
        apply to the ``*`` resource.

        :param expression: the JSON expression resolving to an S3 location URI.

        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromJsonExpression", [expression])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(
        self,
        task: ISageMakerTask,
        *,
        for_reading: typing.Optional[builtins.bool] = None,
        for_writing: typing.Optional[builtins.bool] = None,
    ) -> "S3LocationConfig":
        """(experimental) Called when the S3Location is bound to a StepFunctions task.

        :param task: -
        :param for_reading: (experimental) Allow reading from the S3 Location. Default: false
        :param for_writing: (experimental) Allow writing to the S3 Location. Default: false

        :stability: experimental
        """
        ...


class _S3LocationProxy(S3Location):
    @jsii.member(jsii_name="bind")
    def bind(
        self,
        task: ISageMakerTask,
        *,
        for_reading: typing.Optional[builtins.bool] = None,
        for_writing: typing.Optional[builtins.bool] = None,
    ) -> "S3LocationConfig":
        """(experimental) Called when the S3Location is bound to a StepFunctions task.

        :param task: -
        :param for_reading: (experimental) Allow reading from the S3 Location. Default: false
        :param for_writing: (experimental) Allow writing to the S3 Location. Default: false

        :stability: experimental
        """
        opts = S3LocationBindOptions(for_reading=for_reading, for_writing=for_writing)

        return jsii.invoke(self, "bind", [task, opts])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.S3LocationBindOptions",
    jsii_struct_bases=[],
    name_mapping={"for_reading": "forReading", "for_writing": "forWriting"},
)
class S3LocationBindOptions:
    def __init__(
        self,
        *,
        for_reading: typing.Optional[builtins.bool] = None,
        for_writing: typing.Optional[builtins.bool] = None,
    ) -> None:
        """(experimental) Options for binding an S3 Location.

        :param for_reading: (experimental) Allow reading from the S3 Location. Default: false
        :param for_writing: (experimental) Allow writing to the S3 Location. Default: false

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if for_reading is not None:
            self._values["for_reading"] = for_reading
        if for_writing is not None:
            self._values["for_writing"] = for_writing

    @builtins.property
    def for_reading(self) -> typing.Optional[builtins.bool]:
        """(experimental) Allow reading from the S3 Location.

        :default: false

        :stability: experimental
        """
        result = self._values.get("for_reading")
        return result

    @builtins.property
    def for_writing(self) -> typing.Optional[builtins.bool]:
        """(experimental) Allow writing to the S3 Location.

        :default: false

        :stability: experimental
        """
        result = self._values.get("for_writing")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3LocationBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.S3LocationConfig",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class S3LocationConfig:
    def __init__(self, *, uri: builtins.str) -> None:
        """(experimental) Stores information about the location of an object in Amazon S3.

        :param uri: (experimental) Uniquely identifies the resource in Amazon S3.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "uri": uri,
        }

    @builtins.property
    def uri(self) -> builtins.str:
        """(experimental) Uniquely identifies the resource in Amazon S3.

        :stability: experimental
        """
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3LocationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SageMakerCreateEndpoint(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.SageMakerCreateEndpoint",
):
    """(experimental) A Step Functions Task to create a SageMaker endpoint.

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-sagemaker.html
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        endpoint_config_name: builtins.str,
        endpoint_name: builtins.str,
        tags: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param endpoint_config_name: (experimental) The name of an endpoint configuration.
        :param endpoint_name: (experimental) The name of the endpoint. The name must be unique within an AWS Region in your AWS account.
        :param tags: (experimental) Tags to be applied to the endpoint. Default: - No tags
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        :stability: experimental
        """
        props = SageMakerCreateEndpointProps(
            endpoint_config_name=endpoint_config_name,
            endpoint_name=endpoint_name,
            tags=tags,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(SageMakerCreateEndpoint, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")


class SageMakerCreateEndpointConfig(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.SageMakerCreateEndpointConfig",
):
    """(experimental) A Step Functions Task to create a SageMaker endpoint configuration.

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-sagemaker.html
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        endpoint_config_name: builtins.str,
        production_variants: typing.List[ProductionVariant],
        kms_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        tags: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param endpoint_config_name: (experimental) The name of the endpoint configuration.
        :param production_variants: (experimental) An list of ProductionVariant objects, one for each model that you want to host at this endpoint. Identifies a model that you want to host and the resources to deploy for hosting it. If you are deploying multiple models, tell Amazon SageMaker how to distribute traffic among the models by specifying variant weights.
        :param kms_key: (experimental) AWS Key Management Service key that Amazon SageMaker uses to encrypt data on the storage volume attached to the ML compute instance that hosts the endpoint. Default: - None
        :param tags: (experimental) Tags to be applied to the endpoint configuration. Default: - No tags
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        :stability: experimental
        """
        props = SageMakerCreateEndpointConfigProps(
            endpoint_config_name=endpoint_config_name,
            production_variants=production_variants,
            kms_key=kms_key,
            tags=tags,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(SageMakerCreateEndpointConfig, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.SageMakerCreateEndpointConfigProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "endpoint_config_name": "endpointConfigName",
        "production_variants": "productionVariants",
        "kms_key": "kmsKey",
        "tags": "tags",
    },
)
class SageMakerCreateEndpointConfigProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        endpoint_config_name: builtins.str,
        production_variants: typing.List[ProductionVariant],
        kms_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        tags: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
    ) -> None:
        """(experimental) Properties for creating an Amazon SageMaker endpoint configuration.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param endpoint_config_name: (experimental) The name of the endpoint configuration.
        :param production_variants: (experimental) An list of ProductionVariant objects, one for each model that you want to host at this endpoint. Identifies a model that you want to host and the resources to deploy for hosting it. If you are deploying multiple models, tell Amazon SageMaker how to distribute traffic among the models by specifying variant weights.
        :param kms_key: (experimental) AWS Key Management Service key that Amazon SageMaker uses to encrypt data on the storage volume attached to the ML compute instance that hosts the endpoint. Default: - None
        :param tags: (experimental) Tags to be applied to the endpoint configuration. Default: - No tags

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-sagemaker.html
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "endpoint_config_name": endpoint_config_name,
            "production_variants": production_variants,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def endpoint_config_name(self) -> builtins.str:
        """(experimental) The name of the endpoint configuration.

        :stability: experimental
        """
        result = self._values.get("endpoint_config_name")
        assert result is not None, "Required property 'endpoint_config_name' is missing"
        return result

    @builtins.property
    def production_variants(self) -> typing.List[ProductionVariant]:
        """(experimental) An list of ProductionVariant objects, one for each model that you want to host at this endpoint.

        Identifies a model that you want to host and the resources to deploy for hosting it.
        If you are deploying multiple models, tell Amazon SageMaker how to distribute traffic among the models by specifying variant weights.

        :stability: experimental
        """
        result = self._values.get("production_variants")
        assert result is not None, "Required property 'production_variants' is missing"
        return result

    @builtins.property
    def kms_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """(experimental) AWS Key Management Service key that Amazon SageMaker uses to encrypt data on the storage volume attached to the ML compute instance that hosts the endpoint.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("kms_key")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskInput]:
        """(experimental) Tags to be applied to the endpoint configuration.

        :default: - No tags

        :stability: experimental
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SageMakerCreateEndpointConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.SageMakerCreateEndpointProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "endpoint_config_name": "endpointConfigName",
        "endpoint_name": "endpointName",
        "tags": "tags",
    },
)
class SageMakerCreateEndpointProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        endpoint_config_name: builtins.str,
        endpoint_name: builtins.str,
        tags: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
    ) -> None:
        """(experimental) Properties for creating an Amazon SageMaker endpoint.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param endpoint_config_name: (experimental) The name of an endpoint configuration.
        :param endpoint_name: (experimental) The name of the endpoint. The name must be unique within an AWS Region in your AWS account.
        :param tags: (experimental) Tags to be applied to the endpoint. Default: - No tags

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-sagemaker.html
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "endpoint_config_name": endpoint_config_name,
            "endpoint_name": endpoint_name,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def endpoint_config_name(self) -> builtins.str:
        """(experimental) The name of an endpoint configuration.

        :stability: experimental
        """
        result = self._values.get("endpoint_config_name")
        assert result is not None, "Required property 'endpoint_config_name' is missing"
        return result

    @builtins.property
    def endpoint_name(self) -> builtins.str:
        """(experimental) The name of the endpoint.

        The name must be unique within an AWS Region in your AWS account.

        :stability: experimental
        """
        result = self._values.get("endpoint_name")
        assert result is not None, "Required property 'endpoint_name' is missing"
        return result

    @builtins.property
    def tags(self) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskInput]:
        """(experimental) Tags to be applied to the endpoint.

        :default: - No tags

        :stability: experimental
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SageMakerCreateEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_iam.IGrantable, aws_cdk.aws_ec2.IConnectable)
class SageMakerCreateModel(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.SageMakerCreateModel",
):
    """(experimental) A Step Functions Task to create a SageMaker model.

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-sagemaker.html
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        model_name: builtins.str,
        primary_container: IContainerDefinition,
        containers: typing.Optional[typing.List[IContainerDefinition]] = None,
        enable_network_isolation: typing.Optional[builtins.bool] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        tags: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param model_name: (experimental) The name of the new model.
        :param primary_container: (experimental) The definition of the primary docker image containing inference code, associated artifacts, and custom environment map that the inference code uses when the model is deployed for predictions.
        :param containers: (experimental) Specifies the containers in the inference pipeline. Default: - None
        :param enable_network_isolation: (experimental) Isolates the model container. No inbound or outbound network calls can be made to or from the model container. Default: false
        :param role: (experimental) An execution role that you can pass in a CreateModel API request. Default: - a role will be created.
        :param subnet_selection: (experimental) The subnets of the VPC to which the hosted model is connected (Note this parameter is only used when VPC is provided). Default: - Private Subnets are selected
        :param tags: (experimental) Tags to be applied to the model. Default: - No tags
        :param vpc: (experimental) The VPC that is accessible by the hosted model. Default: - None
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        :stability: experimental
        """
        props = SageMakerCreateModelProps(
            model_name=model_name,
            primary_container=primary_container,
            containers=containers,
            enable_network_isolation=enable_network_isolation,
            role=role,
            subnet_selection=subnet_selection,
            tags=tags,
            vpc=vpc,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(SageMakerCreateModel, self, [scope, id, props])

    @jsii.member(jsii_name="addSecurityGroup")
    def add_security_group(
        self,
        security_group: aws_cdk.aws_ec2.ISecurityGroup,
    ) -> None:
        """(experimental) Add the security group to all instances via the launch configuration security groups array.

        :param security_group: : The security group to add.

        :stability: experimental
        """
        return jsii.invoke(self, "addSecurityGroup", [security_group])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """(experimental) Allows specify security group connections for instances of this fleet.

        :stability: experimental
        """
        return jsii.get(self, "connections")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        """(experimental) The principal to grant permissions to.

        :stability: experimental
        """
        return jsii.get(self, "grantPrincipal")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """(experimental) The execution role for the Sagemaker Create Model API.

        :stability: experimental
        """
        return jsii.get(self, "role")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.SageMakerCreateModelProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "model_name": "modelName",
        "primary_container": "primaryContainer",
        "containers": "containers",
        "enable_network_isolation": "enableNetworkIsolation",
        "role": "role",
        "subnet_selection": "subnetSelection",
        "tags": "tags",
        "vpc": "vpc",
    },
)
class SageMakerCreateModelProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        model_name: builtins.str,
        primary_container: IContainerDefinition,
        containers: typing.Optional[typing.List[IContainerDefinition]] = None,
        enable_network_isolation: typing.Optional[builtins.bool] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        tags: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """(experimental) Properties for creating an Amazon SageMaker model.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param model_name: (experimental) The name of the new model.
        :param primary_container: (experimental) The definition of the primary docker image containing inference code, associated artifacts, and custom environment map that the inference code uses when the model is deployed for predictions.
        :param containers: (experimental) Specifies the containers in the inference pipeline. Default: - None
        :param enable_network_isolation: (experimental) Isolates the model container. No inbound or outbound network calls can be made to or from the model container. Default: false
        :param role: (experimental) An execution role that you can pass in a CreateModel API request. Default: - a role will be created.
        :param subnet_selection: (experimental) The subnets of the VPC to which the hosted model is connected (Note this parameter is only used when VPC is provided). Default: - Private Subnets are selected
        :param tags: (experimental) Tags to be applied to the model. Default: - No tags
        :param vpc: (experimental) The VPC that is accessible by the hosted model. Default: - None

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-sagemaker.html
        :stability: experimental
        """
        if isinstance(subnet_selection, dict):
            subnet_selection = aws_cdk.aws_ec2.SubnetSelection(**subnet_selection)
        self._values: typing.Dict[str, typing.Any] = {
            "model_name": model_name,
            "primary_container": primary_container,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if containers is not None:
            self._values["containers"] = containers
        if enable_network_isolation is not None:
            self._values["enable_network_isolation"] = enable_network_isolation
        if role is not None:
            self._values["role"] = role
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if tags is not None:
            self._values["tags"] = tags
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def model_name(self) -> builtins.str:
        """(experimental) The name of the new model.

        :stability: experimental
        """
        result = self._values.get("model_name")
        assert result is not None, "Required property 'model_name' is missing"
        return result

    @builtins.property
    def primary_container(self) -> IContainerDefinition:
        """(experimental) The definition of the primary docker image containing inference code, associated artifacts, and custom environment map that the inference code uses when the model is deployed for predictions.

        :stability: experimental
        """
        result = self._values.get("primary_container")
        assert result is not None, "Required property 'primary_container' is missing"
        return result

    @builtins.property
    def containers(self) -> typing.Optional[typing.List[IContainerDefinition]]:
        """(experimental) Specifies the containers in the inference pipeline.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("containers")
        return result

    @builtins.property
    def enable_network_isolation(self) -> typing.Optional[builtins.bool]:
        """(experimental) Isolates the model container.

        No inbound or outbound network calls can be made to or from the model container.

        :default: false

        :stability: experimental
        """
        result = self._values.get("enable_network_isolation")
        return result

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """(experimental) An execution role that you can pass in a CreateModel API request.

        :default: - a role will be created.

        :stability: experimental
        """
        result = self._values.get("role")
        return result

    @builtins.property
    def subnet_selection(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """(experimental) The subnets of the VPC to which the hosted model is connected (Note this parameter is only used when VPC is provided).

        :default: - Private Subnets are selected

        :stability: experimental
        """
        result = self._values.get("subnet_selection")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskInput]:
        """(experimental) Tags to be applied to the model.

        :default: - No tags

        :stability: experimental
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """(experimental) The VPC that is accessible by the hosted model.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("vpc")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SageMakerCreateModelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_iam.IGrantable, aws_cdk.aws_ec2.IConnectable)
class SageMakerCreateTrainingJob(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.SageMakerCreateTrainingJob",
):
    """(experimental) Class representing the SageMaker Create Training Job task.

    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        algorithm_specification: AlgorithmSpecification,
        input_data_config: typing.List[Channel],
        output_data_config: OutputDataConfig,
        training_job_name: builtins.str,
        hyperparameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        resource_config: typing.Optional[ResourceConfig] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        stopping_condition: typing.Optional["StoppingCondition"] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc_config: typing.Optional["VpcConfig"] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param algorithm_specification: (experimental) Identifies the training algorithm to use.
        :param input_data_config: (experimental) Describes the various datasets (e.g. train, validation, test) and the Amazon S3 location where stored.
        :param output_data_config: (experimental) Identifies the Amazon S3 location where you want Amazon SageMaker to save the results of model training.
        :param training_job_name: (experimental) Training Job Name.
        :param hyperparameters: (experimental) Algorithm-specific parameters that influence the quality of the model. Set hyperparameters before you start the learning process. For a list of hyperparameters provided by Amazon SageMaker Default: - No hyperparameters
        :param resource_config: (experimental) Specifies the resources, ML compute instances, and ML storage volumes to deploy for model training. Default: - 1 instance of EC2 ``M4.XLarge`` with ``10GB`` volume
        :param role: (experimental) Role for the Training Job. The role must be granted all necessary permissions for the SageMaker training job to be able to operate. See https://docs.aws.amazon.com/fr_fr/sagemaker/latest/dg/sagemaker-roles.html#sagemaker-roles-createtrainingjob-perms Default: - a role will be created.
        :param stopping_condition: (experimental) Sets a time limit for training. Default: - max runtime of 1 hour
        :param tags: (experimental) Tags to be applied to the train job. Default: - No tags
        :param vpc_config: (experimental) Specifies the VPC that you want your training job to connect to. Default: - No VPC
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        :stability: experimental
        """
        props = SageMakerCreateTrainingJobProps(
            algorithm_specification=algorithm_specification,
            input_data_config=input_data_config,
            output_data_config=output_data_config,
            training_job_name=training_job_name,
            hyperparameters=hyperparameters,
            resource_config=resource_config,
            role=role,
            stopping_condition=stopping_condition,
            tags=tags,
            vpc_config=vpc_config,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(SageMakerCreateTrainingJob, self, [scope, id, props])

    @jsii.member(jsii_name="addSecurityGroup")
    def add_security_group(
        self,
        security_group: aws_cdk.aws_ec2.ISecurityGroup,
    ) -> None:
        """(experimental) Add the security group to all instances via the launch configuration security groups array.

        :param security_group: : The security group to add.

        :stability: experimental
        """
        return jsii.invoke(self, "addSecurityGroup", [security_group])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """(experimental) Allows specify security group connections for instances of this fleet.

        :stability: experimental
        """
        return jsii.get(self, "connections")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> aws_cdk.aws_iam.IPrincipal:
        """(experimental) The principal to grant permissions to.

        :stability: experimental
        """
        return jsii.get(self, "grantPrincipal")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """(experimental) The execution role for the Sagemaker training job.

        Only available after task has been added to a state machine.

        :stability: experimental
        """
        return jsii.get(self, "role")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.SageMakerCreateTrainingJobProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "algorithm_specification": "algorithmSpecification",
        "input_data_config": "inputDataConfig",
        "output_data_config": "outputDataConfig",
        "training_job_name": "trainingJobName",
        "hyperparameters": "hyperparameters",
        "resource_config": "resourceConfig",
        "role": "role",
        "stopping_condition": "stoppingCondition",
        "tags": "tags",
        "vpc_config": "vpcConfig",
    },
)
class SageMakerCreateTrainingJobProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        algorithm_specification: AlgorithmSpecification,
        input_data_config: typing.List[Channel],
        output_data_config: OutputDataConfig,
        training_job_name: builtins.str,
        hyperparameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        resource_config: typing.Optional[ResourceConfig] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        stopping_condition: typing.Optional["StoppingCondition"] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc_config: typing.Optional["VpcConfig"] = None,
    ) -> None:
        """(experimental) Properties for creating an Amazon SageMaker training job.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param algorithm_specification: (experimental) Identifies the training algorithm to use.
        :param input_data_config: (experimental) Describes the various datasets (e.g. train, validation, test) and the Amazon S3 location where stored.
        :param output_data_config: (experimental) Identifies the Amazon S3 location where you want Amazon SageMaker to save the results of model training.
        :param training_job_name: (experimental) Training Job Name.
        :param hyperparameters: (experimental) Algorithm-specific parameters that influence the quality of the model. Set hyperparameters before you start the learning process. For a list of hyperparameters provided by Amazon SageMaker Default: - No hyperparameters
        :param resource_config: (experimental) Specifies the resources, ML compute instances, and ML storage volumes to deploy for model training. Default: - 1 instance of EC2 ``M4.XLarge`` with ``10GB`` volume
        :param role: (experimental) Role for the Training Job. The role must be granted all necessary permissions for the SageMaker training job to be able to operate. See https://docs.aws.amazon.com/fr_fr/sagemaker/latest/dg/sagemaker-roles.html#sagemaker-roles-createtrainingjob-perms Default: - a role will be created.
        :param stopping_condition: (experimental) Sets a time limit for training. Default: - max runtime of 1 hour
        :param tags: (experimental) Tags to be applied to the train job. Default: - No tags
        :param vpc_config: (experimental) Specifies the VPC that you want your training job to connect to. Default: - No VPC

        :stability: experimental
        """
        if isinstance(algorithm_specification, dict):
            algorithm_specification = AlgorithmSpecification(**algorithm_specification)
        if isinstance(output_data_config, dict):
            output_data_config = OutputDataConfig(**output_data_config)
        if isinstance(resource_config, dict):
            resource_config = ResourceConfig(**resource_config)
        if isinstance(stopping_condition, dict):
            stopping_condition = StoppingCondition(**stopping_condition)
        if isinstance(vpc_config, dict):
            vpc_config = VpcConfig(**vpc_config)
        self._values: typing.Dict[str, typing.Any] = {
            "algorithm_specification": algorithm_specification,
            "input_data_config": input_data_config,
            "output_data_config": output_data_config,
            "training_job_name": training_job_name,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if hyperparameters is not None:
            self._values["hyperparameters"] = hyperparameters
        if resource_config is not None:
            self._values["resource_config"] = resource_config
        if role is not None:
            self._values["role"] = role
        if stopping_condition is not None:
            self._values["stopping_condition"] = stopping_condition
        if tags is not None:
            self._values["tags"] = tags
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def algorithm_specification(self) -> AlgorithmSpecification:
        """(experimental) Identifies the training algorithm to use.

        :stability: experimental
        """
        result = self._values.get("algorithm_specification")
        assert result is not None, "Required property 'algorithm_specification' is missing"
        return result

    @builtins.property
    def input_data_config(self) -> typing.List[Channel]:
        """(experimental) Describes the various datasets (e.g. train, validation, test) and the Amazon S3 location where stored.

        :stability: experimental
        """
        result = self._values.get("input_data_config")
        assert result is not None, "Required property 'input_data_config' is missing"
        return result

    @builtins.property
    def output_data_config(self) -> OutputDataConfig:
        """(experimental) Identifies the Amazon S3 location where you want Amazon SageMaker to save the results of model training.

        :stability: experimental
        """
        result = self._values.get("output_data_config")
        assert result is not None, "Required property 'output_data_config' is missing"
        return result

    @builtins.property
    def training_job_name(self) -> builtins.str:
        """(experimental) Training Job Name.

        :stability: experimental
        """
        result = self._values.get("training_job_name")
        assert result is not None, "Required property 'training_job_name' is missing"
        return result

    @builtins.property
    def hyperparameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        """(experimental) Algorithm-specific parameters that influence the quality of the model.

        Set hyperparameters before you start the learning process.
        For a list of hyperparameters provided by Amazon SageMaker

        :default: - No hyperparameters

        :see: https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html
        :stability: experimental
        """
        result = self._values.get("hyperparameters")
        return result

    @builtins.property
    def resource_config(self) -> typing.Optional[ResourceConfig]:
        """(experimental) Specifies the resources, ML compute instances, and ML storage volumes to deploy for model training.

        :default: - 1 instance of EC2 ``M4.XLarge`` with ``10GB`` volume

        :stability: experimental
        """
        result = self._values.get("resource_config")
        return result

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """(experimental) Role for the Training Job.

        The role must be granted all necessary permissions for the SageMaker training job to
        be able to operate.

        See https://docs.aws.amazon.com/fr_fr/sagemaker/latest/dg/sagemaker-roles.html#sagemaker-roles-createtrainingjob-perms

        :default: - a role will be created.

        :stability: experimental
        """
        result = self._values.get("role")
        return result

    @builtins.property
    def stopping_condition(self) -> typing.Optional["StoppingCondition"]:
        """(experimental) Sets a time limit for training.

        :default: - max runtime of 1 hour

        :stability: experimental
        """
        result = self._values.get("stopping_condition")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) Tags to be applied to the train job.

        :default: - No tags

        :stability: experimental
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def vpc_config(self) -> typing.Optional["VpcConfig"]:
        """(experimental) Specifies the VPC that you want your training job to connect to.

        :default: - No VPC

        :stability: experimental
        """
        result = self._values.get("vpc_config")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SageMakerCreateTrainingJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SageMakerCreateTransformJob(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.SageMakerCreateTransformJob",
):
    """(experimental) Class representing the SageMaker Create Transform Job task.

    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        model_name: builtins.str,
        transform_input: "TransformInput",
        transform_job_name: builtins.str,
        transform_output: "TransformOutput",
        batch_strategy: typing.Optional[BatchStrategy] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_concurrent_transforms: typing.Optional[jsii.Number] = None,
        max_payload: typing.Optional[aws_cdk.core.Size] = None,
        model_client_options: typing.Optional[ModelClientOptions] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        transform_resources: typing.Optional["TransformResources"] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param model_name: (experimental) Name of the model that you want to use for the transform job.
        :param transform_input: (experimental) Dataset to be transformed and the Amazon S3 location where it is stored.
        :param transform_job_name: (experimental) Transform Job Name.
        :param transform_output: (experimental) S3 location where you want Amazon SageMaker to save the results from the transform job.
        :param batch_strategy: (experimental) Number of records to include in a mini-batch for an HTTP inference request. Default: - No batch strategy
        :param environment: (experimental) Environment variables to set in the Docker container. Default: - No environment variables
        :param max_concurrent_transforms: (experimental) Maximum number of parallel requests that can be sent to each instance in a transform job. Default: - Amazon SageMaker checks the optional execution-parameters to determine the settings for your chosen algorithm. If the execution-parameters endpoint is not enabled, the default value is 1.
        :param max_payload: (experimental) Maximum allowed size of the payload, in MB. Default: 6
        :param model_client_options: (experimental) Configures the timeout and maximum number of retries for processing a transform job invocation. Default: - 0 retries and 60 seconds of timeout
        :param role: (experimental) Role for the Transform Job. Default: - A role is created with ``AmazonSageMakerFullAccess`` managed policy
        :param tags: (experimental) Tags to be applied to the train job. Default: - No tags
        :param transform_resources: (experimental) ML compute instances for the transform job. Default: - 1 instance of type M4.XLarge
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        :stability: experimental
        """
        props = SageMakerCreateTransformJobProps(
            model_name=model_name,
            transform_input=transform_input,
            transform_job_name=transform_job_name,
            transform_output=transform_output,
            batch_strategy=batch_strategy,
            environment=environment,
            max_concurrent_transforms=max_concurrent_transforms,
            max_payload=max_payload,
            model_client_options=model_client_options,
            role=role,
            tags=tags,
            transform_resources=transform_resources,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(SageMakerCreateTransformJob, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """(experimental) The execution role for the Sagemaker transform job.

        Only available after task has been added to a state machine.

        :stability: experimental
        """
        return jsii.get(self, "role")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.SageMakerCreateTransformJobProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "model_name": "modelName",
        "transform_input": "transformInput",
        "transform_job_name": "transformJobName",
        "transform_output": "transformOutput",
        "batch_strategy": "batchStrategy",
        "environment": "environment",
        "max_concurrent_transforms": "maxConcurrentTransforms",
        "max_payload": "maxPayload",
        "model_client_options": "modelClientOptions",
        "role": "role",
        "tags": "tags",
        "transform_resources": "transformResources",
    },
)
class SageMakerCreateTransformJobProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        model_name: builtins.str,
        transform_input: "TransformInput",
        transform_job_name: builtins.str,
        transform_output: "TransformOutput",
        batch_strategy: typing.Optional[BatchStrategy] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_concurrent_transforms: typing.Optional[jsii.Number] = None,
        max_payload: typing.Optional[aws_cdk.core.Size] = None,
        model_client_options: typing.Optional[ModelClientOptions] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        transform_resources: typing.Optional["TransformResources"] = None,
    ) -> None:
        """(experimental) Properties for creating an Amazon SageMaker transform job task.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param model_name: (experimental) Name of the model that you want to use for the transform job.
        :param transform_input: (experimental) Dataset to be transformed and the Amazon S3 location where it is stored.
        :param transform_job_name: (experimental) Transform Job Name.
        :param transform_output: (experimental) S3 location where you want Amazon SageMaker to save the results from the transform job.
        :param batch_strategy: (experimental) Number of records to include in a mini-batch for an HTTP inference request. Default: - No batch strategy
        :param environment: (experimental) Environment variables to set in the Docker container. Default: - No environment variables
        :param max_concurrent_transforms: (experimental) Maximum number of parallel requests that can be sent to each instance in a transform job. Default: - Amazon SageMaker checks the optional execution-parameters to determine the settings for your chosen algorithm. If the execution-parameters endpoint is not enabled, the default value is 1.
        :param max_payload: (experimental) Maximum allowed size of the payload, in MB. Default: 6
        :param model_client_options: (experimental) Configures the timeout and maximum number of retries for processing a transform job invocation. Default: - 0 retries and 60 seconds of timeout
        :param role: (experimental) Role for the Transform Job. Default: - A role is created with ``AmazonSageMakerFullAccess`` managed policy
        :param tags: (experimental) Tags to be applied to the train job. Default: - No tags
        :param transform_resources: (experimental) ML compute instances for the transform job. Default: - 1 instance of type M4.XLarge

        :stability: experimental
        """
        if isinstance(transform_input, dict):
            transform_input = TransformInput(**transform_input)
        if isinstance(transform_output, dict):
            transform_output = TransformOutput(**transform_output)
        if isinstance(model_client_options, dict):
            model_client_options = ModelClientOptions(**model_client_options)
        if isinstance(transform_resources, dict):
            transform_resources = TransformResources(**transform_resources)
        self._values: typing.Dict[str, typing.Any] = {
            "model_name": model_name,
            "transform_input": transform_input,
            "transform_job_name": transform_job_name,
            "transform_output": transform_output,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if batch_strategy is not None:
            self._values["batch_strategy"] = batch_strategy
        if environment is not None:
            self._values["environment"] = environment
        if max_concurrent_transforms is not None:
            self._values["max_concurrent_transforms"] = max_concurrent_transforms
        if max_payload is not None:
            self._values["max_payload"] = max_payload
        if model_client_options is not None:
            self._values["model_client_options"] = model_client_options
        if role is not None:
            self._values["role"] = role
        if tags is not None:
            self._values["tags"] = tags
        if transform_resources is not None:
            self._values["transform_resources"] = transform_resources

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def model_name(self) -> builtins.str:
        """(experimental) Name of the model that you want to use for the transform job.

        :stability: experimental
        """
        result = self._values.get("model_name")
        assert result is not None, "Required property 'model_name' is missing"
        return result

    @builtins.property
    def transform_input(self) -> "TransformInput":
        """(experimental) Dataset to be transformed and the Amazon S3 location where it is stored.

        :stability: experimental
        """
        result = self._values.get("transform_input")
        assert result is not None, "Required property 'transform_input' is missing"
        return result

    @builtins.property
    def transform_job_name(self) -> builtins.str:
        """(experimental) Transform Job Name.

        :stability: experimental
        """
        result = self._values.get("transform_job_name")
        assert result is not None, "Required property 'transform_job_name' is missing"
        return result

    @builtins.property
    def transform_output(self) -> "TransformOutput":
        """(experimental) S3 location where you want Amazon SageMaker to save the results from the transform job.

        :stability: experimental
        """
        result = self._values.get("transform_output")
        assert result is not None, "Required property 'transform_output' is missing"
        return result

    @builtins.property
    def batch_strategy(self) -> typing.Optional[BatchStrategy]:
        """(experimental) Number of records to include in a mini-batch for an HTTP inference request.

        :default: - No batch strategy

        :stability: experimental
        """
        result = self._values.get("batch_strategy")
        return result

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) Environment variables to set in the Docker container.

        :default: - No environment variables

        :stability: experimental
        """
        result = self._values.get("environment")
        return result

    @builtins.property
    def max_concurrent_transforms(self) -> typing.Optional[jsii.Number]:
        """(experimental) Maximum number of parallel requests that can be sent to each instance in a transform job.

        :default:

        - Amazon SageMaker checks the optional execution-parameters to determine the settings for your chosen algorithm.
        If the execution-parameters endpoint is not enabled, the default value is 1.

        :stability: experimental
        """
        result = self._values.get("max_concurrent_transforms")
        return result

    @builtins.property
    def max_payload(self) -> typing.Optional[aws_cdk.core.Size]:
        """(experimental) Maximum allowed size of the payload, in MB.

        :default: 6

        :stability: experimental
        """
        result = self._values.get("max_payload")
        return result

    @builtins.property
    def model_client_options(self) -> typing.Optional[ModelClientOptions]:
        """(experimental) Configures the timeout and maximum number of retries for processing a transform job invocation.

        :default: - 0 retries and 60 seconds of timeout

        :stability: experimental
        """
        result = self._values.get("model_client_options")
        return result

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """(experimental) Role for the Transform Job.

        :default: - A role is created with ``AmazonSageMakerFullAccess`` managed policy

        :stability: experimental
        """
        result = self._values.get("role")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """(experimental) Tags to be applied to the train job.

        :default: - No tags

        :stability: experimental
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def transform_resources(self) -> typing.Optional["TransformResources"]:
        """(experimental) ML compute instances for the transform job.

        :default: - 1 instance of type M4.XLarge

        :stability: experimental
        """
        result = self._values.get("transform_resources")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SageMakerCreateTransformJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SageMakerUpdateEndpoint(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.SageMakerUpdateEndpoint",
):
    """(experimental) A Step Functions Task to update a SageMaker endpoint.

    :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-sagemaker.html
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        endpoint_config_name: builtins.str,
        endpoint_name: builtins.str,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param endpoint_config_name: (experimental) The name of the new endpoint configuration.
        :param endpoint_name: (experimental) The name of the endpoint whose configuration you want to update.
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None

        :stability: experimental
        """
        props = SageMakerUpdateEndpointProps(
            endpoint_config_name=endpoint_config_name,
            endpoint_name=endpoint_name,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(SageMakerUpdateEndpoint, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """
        :stability: experimental
        """
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.SageMakerUpdateEndpointProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "endpoint_config_name": "endpointConfigName",
        "endpoint_name": "endpointName",
    },
)
class SageMakerUpdateEndpointProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        endpoint_config_name: builtins.str,
        endpoint_name: builtins.str,
    ) -> None:
        """(experimental) Properties for updating Amazon SageMaker endpoint.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param endpoint_config_name: (experimental) The name of the new endpoint configuration.
        :param endpoint_name: (experimental) The name of the endpoint whose configuration you want to update.

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-sagemaker.html
        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "endpoint_config_name": endpoint_config_name,
            "endpoint_name": endpoint_name,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def endpoint_config_name(self) -> builtins.str:
        """(experimental) The name of the new endpoint configuration.

        :stability: experimental
        """
        result = self._values.get("endpoint_config_name")
        assert result is not None, "Required property 'endpoint_config_name' is missing"
        return result

    @builtins.property
    def endpoint_name(self) -> builtins.str:
        """(experimental) The name of the endpoint whose configuration you want to update.

        :stability: experimental
        """
        result = self._values.get("endpoint_name")
        assert result is not None, "Required property 'endpoint_name' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SageMakerUpdateEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class SendToQueue(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.SendToQueue",
):
    """(deprecated) A StepFunctions Task to send messages to SQS queue.

    A Function can be used directly as a Resource, but this class mirrors
    integration with other AWS services via a specific class instance.

    :deprecated: Use ``SqsSendMessage``

    :stability: deprecated
    """

    def __init__(
        self,
        queue: aws_cdk.aws_sqs.IQueue,
        *,
        message_body: aws_cdk.aws_stepfunctions.TaskInput,
        delay: typing.Optional[aws_cdk.core.Duration] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern] = None,
        message_deduplication_id: typing.Optional[builtins.str] = None,
        message_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param queue: -
        :param message_body: (deprecated) The text message to send to the queue.
        :param delay: (deprecated) The length of time, in seconds, for which to delay a specific message. Valid values are 0-900 seconds. Default: Default value of the queue is used
        :param integration_pattern: (deprecated) The service integration pattern indicates different ways to call SendMessage to SQS. The valid value is either FIRE_AND_FORGET or WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET
        :param message_deduplication_id: (deprecated) The token used for deduplication of sent messages. Default: Use content-based deduplication
        :param message_group_id: (deprecated) The tag that specifies that a message belongs to a specific message group. Required for FIFO queues. FIFO ordering applies to messages in the same message group. Default: No group ID

        :stability: deprecated
        """
        props = SendToQueueProps(
            message_body=message_body,
            delay=delay,
            integration_pattern=integration_pattern,
            message_deduplication_id=message_deduplication_id,
            message_group_id=message_group_id,
        )

        jsii.create(SendToQueue, self, [queue, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _task: aws_cdk.aws_stepfunctions.Task,
    ) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """(deprecated) Called when the task object is used in a workflow.

        :param _task: -

        :stability: deprecated
        """
        return jsii.invoke(self, "bind", [_task])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.SendToQueueProps",
    jsii_struct_bases=[],
    name_mapping={
        "message_body": "messageBody",
        "delay": "delay",
        "integration_pattern": "integrationPattern",
        "message_deduplication_id": "messageDeduplicationId",
        "message_group_id": "messageGroupId",
    },
)
class SendToQueueProps:
    def __init__(
        self,
        *,
        message_body: aws_cdk.aws_stepfunctions.TaskInput,
        delay: typing.Optional[aws_cdk.core.Duration] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern] = None,
        message_deduplication_id: typing.Optional[builtins.str] = None,
        message_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """(deprecated) Properties for SendMessageTask.

        :param message_body: (deprecated) The text message to send to the queue.
        :param delay: (deprecated) The length of time, in seconds, for which to delay a specific message. Valid values are 0-900 seconds. Default: Default value of the queue is used
        :param integration_pattern: (deprecated) The service integration pattern indicates different ways to call SendMessage to SQS. The valid value is either FIRE_AND_FORGET or WAIT_FOR_TASK_TOKEN. Default: FIRE_AND_FORGET
        :param message_deduplication_id: (deprecated) The token used for deduplication of sent messages. Default: Use content-based deduplication
        :param message_group_id: (deprecated) The tag that specifies that a message belongs to a specific message group. Required for FIFO queues. FIFO ordering applies to messages in the same message group. Default: No group ID

        :deprecated: Use ``SqsSendMessage``

        :stability: deprecated
        """
        self._values: typing.Dict[str, typing.Any] = {
            "message_body": message_body,
        }
        if delay is not None:
            self._values["delay"] = delay
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if message_deduplication_id is not None:
            self._values["message_deduplication_id"] = message_deduplication_id
        if message_group_id is not None:
            self._values["message_group_id"] = message_group_id

    @builtins.property
    def message_body(self) -> aws_cdk.aws_stepfunctions.TaskInput:
        """(deprecated) The text message to send to the queue.

        :stability: deprecated
        """
        result = self._values.get("message_body")
        assert result is not None, "Required property 'message_body' is missing"
        return result

    @builtins.property
    def delay(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(deprecated) The length of time, in seconds, for which to delay a specific message.

        Valid values are 0-900 seconds.

        :default: Default value of the queue is used

        :stability: deprecated
        """
        result = self._values.get("delay")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """(deprecated) The service integration pattern indicates different ways to call SendMessage to SQS.

        The valid value is either FIRE_AND_FORGET or WAIT_FOR_TASK_TOKEN.

        :default: FIRE_AND_FORGET

        :stability: deprecated
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def message_deduplication_id(self) -> typing.Optional[builtins.str]:
        """(deprecated) The token used for deduplication of sent messages.

        :default: Use content-based deduplication

        :stability: deprecated
        """
        result = self._values.get("message_deduplication_id")
        return result

    @builtins.property
    def message_group_id(self) -> typing.Optional[builtins.str]:
        """(deprecated) The tag that specifies that a message belongs to a specific message group.

        Required for FIFO queues. FIFO ordering applies to messages in the same message
        group.

        :default: No group ID

        :stability: deprecated
        """
        result = self._values.get("message_group_id")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SendToQueueProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.ShuffleConfig",
    jsii_struct_bases=[],
    name_mapping={"seed": "seed"},
)
class ShuffleConfig:
    def __init__(self, *, seed: jsii.Number) -> None:
        """(experimental) Configuration for a shuffle option for input data in a channel.

        :param seed: (experimental) Determines the shuffling order.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "seed": seed,
        }

    @builtins.property
    def seed(self) -> jsii.Number:
        """(experimental) Determines the shuffling order.

        :stability: experimental
        """
        result = self._values.get("seed")
        assert result is not None, "Required property 'seed' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ShuffleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SnsPublish(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.SnsPublish",
):
    """A Step Functions Task to publish messages to SNS topic."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        message: aws_cdk.aws_stepfunctions.TaskInput,
        topic: aws_cdk.aws_sns.ITopic,
        message_per_subscription_type: typing.Optional[builtins.bool] = None,
        subject: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param message: The message you want to send. With the exception of SMS, messages must be UTF-8 encoded strings and at most 256 KB in size. For SMS, each message can contain up to 140 characters.
        :param topic: The SNS topic that the task will publish to.
        :param message_per_subscription_type: Send different messages for each transport protocol. For example, you might want to send a shorter message to SMS subscribers and a more verbose message to email and SQS subscribers. Your message must be a JSON object with a top-level JSON key of "default" with a value that is a string You can define other top-level keys that define the message you want to send to a specific transport protocol (i.e. "sqs", "email", "http", etc) Default: false
        :param subject: Used as the "Subject" line when the message is delivered to email endpoints. This field will also be included, if present, in the standard JSON messages delivered to other endpoints. Default: - No subject
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        """
        props = SnsPublishProps(
            message=message,
            topic=topic,
            message_per_subscription_type=message_per_subscription_type,
            subject=subject,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(SnsPublish, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.SnsPublishProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "message": "message",
        "topic": "topic",
        "message_per_subscription_type": "messagePerSubscriptionType",
        "subject": "subject",
    },
)
class SnsPublishProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        message: aws_cdk.aws_stepfunctions.TaskInput,
        topic: aws_cdk.aws_sns.ITopic,
        message_per_subscription_type: typing.Optional[builtins.bool] = None,
        subject: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for publishing a message to an SNS topic.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param message: The message you want to send. With the exception of SMS, messages must be UTF-8 encoded strings and at most 256 KB in size. For SMS, each message can contain up to 140 characters.
        :param topic: The SNS topic that the task will publish to.
        :param message_per_subscription_type: Send different messages for each transport protocol. For example, you might want to send a shorter message to SMS subscribers and a more verbose message to email and SQS subscribers. Your message must be a JSON object with a top-level JSON key of "default" with a value that is a string You can define other top-level keys that define the message you want to send to a specific transport protocol (i.e. "sqs", "email", "http", etc) Default: false
        :param subject: Used as the "Subject" line when the message is delivered to email endpoints. This field will also be included, if present, in the standard JSON messages delivered to other endpoints. Default: - No subject
        """
        self._values: typing.Dict[str, typing.Any] = {
            "message": message,
            "topic": topic,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if message_per_subscription_type is not None:
            self._values["message_per_subscription_type"] = message_per_subscription_type
        if subject is not None:
            self._values["subject"] = subject

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def message(self) -> aws_cdk.aws_stepfunctions.TaskInput:
        """The message you want to send.

        With the exception of SMS, messages must be UTF-8 encoded strings and
        at most 256 KB in size.
        For SMS, each message can contain up to 140 characters.
        """
        result = self._values.get("message")
        assert result is not None, "Required property 'message' is missing"
        return result

    @builtins.property
    def topic(self) -> aws_cdk.aws_sns.ITopic:
        """The SNS topic that the task will publish to."""
        result = self._values.get("topic")
        assert result is not None, "Required property 'topic' is missing"
        return result

    @builtins.property
    def message_per_subscription_type(self) -> typing.Optional[builtins.bool]:
        """Send different messages for each transport protocol.

        For example, you might want to send a shorter message to SMS subscribers
        and a more verbose message to email and SQS subscribers.

        Your message must be a JSON object with a top-level JSON key of
        "default" with a value that is a string
        You can define other top-level keys that define the message you want to
        send to a specific transport protocol (i.e. "sqs", "email", "http", etc)

        :default: false

        :see: https://docs.aws.amazon.com/sns/latest/api/API_Publish.html#API_Publish_RequestParameters
        """
        result = self._values.get("message_per_subscription_type")
        return result

    @builtins.property
    def subject(self) -> typing.Optional[builtins.str]:
        """Used as the "Subject" line when the message is delivered to email endpoints.

        This field will also be included, if present, in the standard JSON messages
        delivered to other endpoints.

        :default: - No subject
        """
        result = self._values.get("subject")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsPublishProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-stepfunctions-tasks.SplitType")
class SplitType(enum.Enum):
    """(experimental) Method to use to split the transform job's data files into smaller batches.

    :stability: experimental
    """

    NONE = "NONE"
    """(experimental) Input data files are not split,.

    :stability: experimental
    """
    LINE = "LINE"
    """(experimental) Split records on a newline character boundary.

    :stability: experimental
    """
    RECORD_IO = "RECORD_IO"
    """(experimental) Split using MXNet RecordIO format.

    :stability: experimental
    """
    TF_RECORD = "TF_RECORD"
    """(experimental) Split using TensorFlow TFRecord format.

    :stability: experimental
    """


class SqsSendMessage(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.SqsSendMessage",
):
    """A StepFunctions Task to send messages to SQS queue."""

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        message_body: aws_cdk.aws_stepfunctions.TaskInput,
        queue: aws_cdk.aws_sqs.IQueue,
        delay: typing.Optional[aws_cdk.core.Duration] = None,
        message_deduplication_id: typing.Optional[builtins.str] = None,
        message_group_id: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param message_body: The text message to send to the queue.
        :param queue: The SQS queue that messages will be sent to.
        :param delay: The length of time, for which to delay a message. Messages that you send to the queue remain invisible to consumers for the duration of the delay period. The maximum allowed delay is 15 minutes. Default: - delay set on the queue. If a delay is not set on the queue, messages are sent immediately (0 seconds).
        :param message_deduplication_id: The token used for deduplication of sent messages. Any messages sent with the same deduplication ID are accepted successfully, but aren't delivered during the 5-minute deduplication interval. Default: - None
        :param message_group_id: The tag that specifies that a message belongs to a specific message group. Messages that belong to the same message group are processed in a FIFO manner. Messages in different message groups might be processed out of order. Default: - None
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        """
        props = SqsSendMessageProps(
            message_body=message_body,
            queue=queue,
            delay=delay,
            message_deduplication_id=message_deduplication_id,
            message_group_id=message_group_id,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(SqsSendMessage, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.SqsSendMessageProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "message_body": "messageBody",
        "queue": "queue",
        "delay": "delay",
        "message_deduplication_id": "messageDeduplicationId",
        "message_group_id": "messageGroupId",
    },
)
class SqsSendMessageProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        message_body: aws_cdk.aws_stepfunctions.TaskInput,
        queue: aws_cdk.aws_sqs.IQueue,
        delay: typing.Optional[aws_cdk.core.Duration] = None,
        message_deduplication_id: typing.Optional[builtins.str] = None,
        message_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for sending a message to an SQS queue.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param message_body: The text message to send to the queue.
        :param queue: The SQS queue that messages will be sent to.
        :param delay: The length of time, for which to delay a message. Messages that you send to the queue remain invisible to consumers for the duration of the delay period. The maximum allowed delay is 15 minutes. Default: - delay set on the queue. If a delay is not set on the queue, messages are sent immediately (0 seconds).
        :param message_deduplication_id: The token used for deduplication of sent messages. Any messages sent with the same deduplication ID are accepted successfully, but aren't delivered during the 5-minute deduplication interval. Default: - None
        :param message_group_id: The tag that specifies that a message belongs to a specific message group. Messages that belong to the same message group are processed in a FIFO manner. Messages in different message groups might be processed out of order. Default: - None
        """
        self._values: typing.Dict[str, typing.Any] = {
            "message_body": message_body,
            "queue": queue,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if delay is not None:
            self._values["delay"] = delay
        if message_deduplication_id is not None:
            self._values["message_deduplication_id"] = message_deduplication_id
        if message_group_id is not None:
            self._values["message_group_id"] = message_group_id

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def message_body(self) -> aws_cdk.aws_stepfunctions.TaskInput:
        """The text message to send to the queue."""
        result = self._values.get("message_body")
        assert result is not None, "Required property 'message_body' is missing"
        return result

    @builtins.property
    def queue(self) -> aws_cdk.aws_sqs.IQueue:
        """The SQS queue that messages will be sent to."""
        result = self._values.get("queue")
        assert result is not None, "Required property 'queue' is missing"
        return result

    @builtins.property
    def delay(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The length of time, for which to delay a message.

        Messages that you send to the queue remain invisible to consumers for the duration
        of the delay period. The maximum allowed delay is 15 minutes.

        :default:

        - delay set on the queue. If a delay is not set on the queue,
        messages are sent immediately (0 seconds).
        """
        result = self._values.get("delay")
        return result

    @builtins.property
    def message_deduplication_id(self) -> typing.Optional[builtins.str]:
        """The token used for deduplication of sent messages.

        Any messages sent with the same deduplication ID are accepted successfully,
        but aren't delivered during the 5-minute deduplication interval.

        :default: - None
        """
        result = self._values.get("message_deduplication_id")
        return result

    @builtins.property
    def message_group_id(self) -> typing.Optional[builtins.str]:
        """The tag that specifies that a message belongs to a specific message group.

        Messages that belong to the same message group are processed in a FIFO manner.
        Messages in different message groups might be processed out of order.

        :default: - None
        """
        result = self._values.get("message_group_id")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsSendMessageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_stepfunctions.IStepFunctionsTask)
class StartExecution(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.StartExecution",
):
    """(deprecated) A Step Functions Task to call StartExecution on another state machine.

    It supports three service integration patterns: FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN.

    :deprecated: - use 'StepFunctionsStartExecution'

    :stability: deprecated
    """

    def __init__(
        self,
        state_machine: aws_cdk.aws_stepfunctions.IStateMachine,
        *,
        input: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param state_machine: -
        :param input: (deprecated) The JSON input for the execution, same as that of StartExecution. Default: - No input
        :param integration_pattern: (deprecated) The service integration pattern indicates different ways to call StartExecution to Step Functions. Default: FIRE_AND_FORGET
        :param name: (deprecated) The name of the execution, same as that of StartExecution. Default: - None

        :stability: deprecated
        """
        props = StartExecutionProps(
            input=input, integration_pattern=integration_pattern, name=name
        )

        jsii.create(StartExecution, self, [state_machine, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        task: aws_cdk.aws_stepfunctions.Task,
    ) -> aws_cdk.aws_stepfunctions.StepFunctionsTaskConfig:
        """(deprecated) Called when the task object is used in a workflow.

        :param task: -

        :stability: deprecated
        """
        return jsii.invoke(self, "bind", [task])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.StartExecutionProps",
    jsii_struct_bases=[],
    name_mapping={
        "input": "input",
        "integration_pattern": "integrationPattern",
        "name": "name",
    },
)
class StartExecutionProps:
    def __init__(
        self,
        *,
        input: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        """(deprecated) Properties for StartExecution.

        :param input: (deprecated) The JSON input for the execution, same as that of StartExecution. Default: - No input
        :param integration_pattern: (deprecated) The service integration pattern indicates different ways to call StartExecution to Step Functions. Default: FIRE_AND_FORGET
        :param name: (deprecated) The name of the execution, same as that of StartExecution. Default: - None

        :deprecated: - use 'StepFunctionsStartExecution'

        :stability: deprecated
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if input is not None:
            self._values["input"] = input
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def input(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        """(deprecated) The JSON input for the execution, same as that of StartExecution.

        :default: - No input

        :see: https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartExecution.html
        :stability: deprecated
        """
        result = self._values.get("input")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.ServiceIntegrationPattern]:
        """(deprecated) The service integration pattern indicates different ways to call StartExecution to Step Functions.

        :default: FIRE_AND_FORGET

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html
        :stability: deprecated
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """(deprecated) The name of the execution, same as that of StartExecution.

        :default: - None

        :see: https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartExecution.html
        :stability: deprecated
        """
        result = self._values.get("name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StartExecutionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StepFunctionsInvokeActivity(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.StepFunctionsInvokeActivity",
):
    """A Step Functions Task to invoke an Activity worker.

    An Activity can be used directly as a Resource.
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        activity: aws_cdk.aws_stepfunctions.IActivity,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param activity: Step Functions Activity to invoke.
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        """
        props = StepFunctionsInvokeActivityProps(
            activity=activity,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(StepFunctionsInvokeActivity, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.StepFunctionsInvokeActivityProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "activity": "activity",
    },
)
class StepFunctionsInvokeActivityProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        activity: aws_cdk.aws_stepfunctions.IActivity,
    ) -> None:
        """Properties for invoking an Activity worker.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param activity: Step Functions Activity to invoke.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "activity": activity,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def activity(self) -> aws_cdk.aws_stepfunctions.IActivity:
        """Step Functions Activity to invoke."""
        result = self._values.get("activity")
        assert result is not None, "Required property 'activity' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StepFunctionsInvokeActivityProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StepFunctionsStartExecution(
    aws_cdk.aws_stepfunctions.TaskStateBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.StepFunctionsStartExecution",
):
    """A Step Functions Task to call StartExecution on another state machine.

    It supports three service integration patterns: FIRE_AND_FORGET, SYNC and WAIT_FOR_TASK_TOKEN.
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        state_machine: aws_cdk.aws_stepfunctions.IStateMachine,
        input: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
        name: typing.Optional[builtins.str] = None,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param state_machine: The Step Functions state machine to start the execution on.
        :param input: The JSON input for the execution, same as that of StartExecution. Default: - The state input (JSON path '$')
        :param name: The name of the execution, same as that of StartExecution. Default: - None
        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        """
        props = StepFunctionsStartExecutionProps(
            state_machine=state_machine,
            input=input,
            name=name,
            comment=comment,
            heartbeat=heartbeat,
            input_path=input_path,
            integration_pattern=integration_pattern,
            output_path=output_path,
            result_path=result_path,
            timeout=timeout,
        )

        jsii.create(StepFunctionsStartExecution, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskMetrics")
    def _task_metrics(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskMetricsConfig]:
        return jsii.get(self, "taskMetrics")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="taskPolicies")
    def _task_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        return jsii.get(self, "taskPolicies")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.StepFunctionsStartExecutionProps",
    jsii_struct_bases=[aws_cdk.aws_stepfunctions.TaskStateBaseProps],
    name_mapping={
        "comment": "comment",
        "heartbeat": "heartbeat",
        "input_path": "inputPath",
        "integration_pattern": "integrationPattern",
        "output_path": "outputPath",
        "result_path": "resultPath",
        "timeout": "timeout",
        "state_machine": "stateMachine",
        "input": "input",
        "name": "name",
    },
)
class StepFunctionsStartExecutionProps(aws_cdk.aws_stepfunctions.TaskStateBaseProps):
    def __init__(
        self,
        *,
        comment: typing.Optional[builtins.str] = None,
        heartbeat: typing.Optional[aws_cdk.core.Duration] = None,
        input_path: typing.Optional[builtins.str] = None,
        integration_pattern: typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern] = None,
        output_path: typing.Optional[builtins.str] = None,
        result_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        state_machine: aws_cdk.aws_stepfunctions.IStateMachine,
        input: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for StartExecution.

        :param comment: An optional description for this state. Default: - No comment
        :param heartbeat: Timeout for the heartbeat. Default: - None
        :param input_path: JSONPath expression to select part of the state to be the input to this state. May also be the special value JsonPath.DISCARD, which will cause the effective input to be the empty object {}. Default: - The entire task input (JSON path '$')
        :param integration_pattern: AWS Step Functions integrates with services directly in the Amazon States Language. You can control these AWS services using service integration patterns Default: IntegrationPattern.REQUEST_RESPONSE
        :param output_path: JSONPath expression to select select a portion of the state output to pass to the next state. May also be the special value JsonPath.DISCARD, which will cause the effective output to be the empty object {}. Default: - The entire JSON node determined by the state input, the task result, and resultPath is passed to the next state (JSON path '$')
        :param result_path: JSONPath expression to indicate where to inject the state's output. May also be the special value JsonPath.DISCARD, which will cause the state's input to become its output. Default: - Replaces the entire input with the result (JSON path '$')
        :param timeout: Timeout for the state machine. Default: - None
        :param state_machine: The Step Functions state machine to start the execution on.
        :param input: The JSON input for the execution, same as that of StartExecution. Default: - The state input (JSON path '$')
        :param name: The name of the execution, same as that of StartExecution. Default: - None
        """
        self._values: typing.Dict[str, typing.Any] = {
            "state_machine": state_machine,
        }
        if comment is not None:
            self._values["comment"] = comment
        if heartbeat is not None:
            self._values["heartbeat"] = heartbeat
        if input_path is not None:
            self._values["input_path"] = input_path
        if integration_pattern is not None:
            self._values["integration_pattern"] = integration_pattern
        if output_path is not None:
            self._values["output_path"] = output_path
        if result_path is not None:
            self._values["result_path"] = result_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if input is not None:
            self._values["input"] = input
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        """An optional description for this state.

        :default: - No comment
        """
        result = self._values.get("comment")
        return result

    @builtins.property
    def heartbeat(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the heartbeat.

        :default: - None
        """
        result = self._values.get("heartbeat")
        return result

    @builtins.property
    def input_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select part of the state to be the input to this state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        input to be the empty object {}.

        :default: - The entire task input (JSON path '$')
        """
        result = self._values.get("input_path")
        return result

    @builtins.property
    def integration_pattern(
        self,
    ) -> typing.Optional[aws_cdk.aws_stepfunctions.IntegrationPattern]:
        """AWS Step Functions integrates with services directly in the Amazon States Language.

        You can control these AWS services using service integration patterns

        :default: IntegrationPattern.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token
        """
        result = self._values.get("integration_pattern")
        return result

    @builtins.property
    def output_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to select select a portion of the state output to pass to the next state.

        May also be the special value JsonPath.DISCARD, which will cause the effective
        output to be the empty object {}.

        :default:

        - The entire JSON node determined by the state input, the task result,
        and resultPath is passed to the next state (JSON path '$')
        """
        result = self._values.get("output_path")
        return result

    @builtins.property
    def result_path(self) -> typing.Optional[builtins.str]:
        """JSONPath expression to indicate where to inject the state's output.

        May also be the special value JsonPath.DISCARD, which will cause the state's
        input to become its output.

        :default: - Replaces the entire input with the result (JSON path '$')
        """
        result = self._values.get("result_path")
        return result

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """Timeout for the state machine.

        :default: - None
        """
        result = self._values.get("timeout")
        return result

    @builtins.property
    def state_machine(self) -> aws_cdk.aws_stepfunctions.IStateMachine:
        """The Step Functions state machine to start the execution on."""
        result = self._values.get("state_machine")
        assert result is not None, "Required property 'state_machine' is missing"
        return result

    @builtins.property
    def input(self) -> typing.Optional[aws_cdk.aws_stepfunctions.TaskInput]:
        """The JSON input for the execution, same as that of StartExecution.

        :default: - The state input (JSON path '$')

        :see: https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartExecution.html
        """
        result = self._values.get("input")
        return result

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        """The name of the execution, same as that of StartExecution.

        :default: - None

        :see: https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartExecution.html
        """
        result = self._values.get("name")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StepFunctionsStartExecutionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.StoppingCondition",
    jsii_struct_bases=[],
    name_mapping={"max_runtime": "maxRuntime"},
)
class StoppingCondition:
    def __init__(
        self,
        *,
        max_runtime: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """(experimental) Specifies a limit to how long a model training job can run.

        When the job reaches the time limit, Amazon SageMaker ends the training job.

        :param max_runtime: (experimental) The maximum length of time, in seconds, that the training or compilation job can run. Default: - 1 hour

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if max_runtime is not None:
            self._values["max_runtime"] = max_runtime

    @builtins.property
    def max_runtime(self) -> typing.Optional[aws_cdk.core.Duration]:
        """(experimental) The maximum length of time, in seconds, that the training or compilation job can run.

        :default: - 1 hour

        :stability: experimental
        """
        result = self._values.get("max_runtime")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StoppingCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.TaskEnvironmentVariable",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class TaskEnvironmentVariable:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        """An environment variable to be set in the container run as a task.

        :param name: Name for the environment variable. Exactly one of ``name`` and ``namePath`` must be specified.
        :param value: Value of the environment variable. Exactly one of ``value`` and ``valuePath`` must be specified.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        """Name for the environment variable.

        Exactly one of ``name`` and ``namePath`` must be specified.
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def value(self) -> builtins.str:
        """Value of the environment variable.

        Exactly one of ``value`` and ``valuePath`` must be specified.
        """
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskEnvironmentVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.TransformDataSource",
    jsii_struct_bases=[],
    name_mapping={"s3_data_source": "s3DataSource"},
)
class TransformDataSource:
    def __init__(self, *, s3_data_source: "TransformS3DataSource") -> None:
        """(experimental) S3 location of the input data that the model can consume.

        :param s3_data_source: (experimental) S3 location of the input data.

        :stability: experimental
        """
        if isinstance(s3_data_source, dict):
            s3_data_source = TransformS3DataSource(**s3_data_source)
        self._values: typing.Dict[str, typing.Any] = {
            "s3_data_source": s3_data_source,
        }

    @builtins.property
    def s3_data_source(self) -> "TransformS3DataSource":
        """(experimental) S3 location of the input data.

        :stability: experimental
        """
        result = self._values.get("s3_data_source")
        assert result is not None, "Required property 's3_data_source' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransformDataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.TransformInput",
    jsii_struct_bases=[],
    name_mapping={
        "transform_data_source": "transformDataSource",
        "compression_type": "compressionType",
        "content_type": "contentType",
        "split_type": "splitType",
    },
)
class TransformInput:
    def __init__(
        self,
        *,
        transform_data_source: TransformDataSource,
        compression_type: typing.Optional[CompressionType] = None,
        content_type: typing.Optional[builtins.str] = None,
        split_type: typing.Optional[SplitType] = None,
    ) -> None:
        """(experimental) Dataset to be transformed and the Amazon S3 location where it is stored.

        :param transform_data_source: (experimental) S3 location of the channel data.
        :param compression_type: (experimental) The compression type of the transform data. Default: NONE
        :param content_type: (experimental) Multipurpose internet mail extension (MIME) type of the data. Default: - None
        :param split_type: (experimental) Method to use to split the transform job's data files into smaller batches. Default: NONE

        :stability: experimental
        """
        if isinstance(transform_data_source, dict):
            transform_data_source = TransformDataSource(**transform_data_source)
        self._values: typing.Dict[str, typing.Any] = {
            "transform_data_source": transform_data_source,
        }
        if compression_type is not None:
            self._values["compression_type"] = compression_type
        if content_type is not None:
            self._values["content_type"] = content_type
        if split_type is not None:
            self._values["split_type"] = split_type

    @builtins.property
    def transform_data_source(self) -> TransformDataSource:
        """(experimental) S3 location of the channel data.

        :stability: experimental
        """
        result = self._values.get("transform_data_source")
        assert result is not None, "Required property 'transform_data_source' is missing"
        return result

    @builtins.property
    def compression_type(self) -> typing.Optional[CompressionType]:
        """(experimental) The compression type of the transform data.

        :default: NONE

        :stability: experimental
        """
        result = self._values.get("compression_type")
        return result

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        """(experimental) Multipurpose internet mail extension (MIME) type of the data.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("content_type")
        return result

    @builtins.property
    def split_type(self) -> typing.Optional[SplitType]:
        """(experimental) Method to use to split the transform job's data files into smaller batches.

        :default: NONE

        :stability: experimental
        """
        result = self._values.get("split_type")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransformInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.TransformOutput",
    jsii_struct_bases=[],
    name_mapping={
        "s3_output_path": "s3OutputPath",
        "accept": "accept",
        "assemble_with": "assembleWith",
        "encryption_key": "encryptionKey",
    },
)
class TransformOutput:
    def __init__(
        self,
        *,
        s3_output_path: builtins.str,
        accept: typing.Optional[builtins.str] = None,
        assemble_with: typing.Optional[AssembleWith] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
    ) -> None:
        """(experimental) S3 location where you want Amazon SageMaker to save the results from the transform job.

        :param s3_output_path: (experimental) S3 path where you want Amazon SageMaker to store the results of the transform job.
        :param accept: (experimental) MIME type used to specify the output data. Default: - None
        :param assemble_with: (experimental) Defines how to assemble the results of the transform job as a single S3 object. Default: - None
        :param encryption_key: (experimental) AWS KMS key that Amazon SageMaker uses to encrypt the model artifacts at rest using Amazon S3 server-side encryption. Default: - default KMS key for Amazon S3 for your role's account.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "s3_output_path": s3_output_path,
        }
        if accept is not None:
            self._values["accept"] = accept
        if assemble_with is not None:
            self._values["assemble_with"] = assemble_with
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key

    @builtins.property
    def s3_output_path(self) -> builtins.str:
        """(experimental) S3 path where you want Amazon SageMaker to store the results of the transform job.

        :stability: experimental
        """
        result = self._values.get("s3_output_path")
        assert result is not None, "Required property 's3_output_path' is missing"
        return result

    @builtins.property
    def accept(self) -> typing.Optional[builtins.str]:
        """(experimental) MIME type used to specify the output data.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("accept")
        return result

    @builtins.property
    def assemble_with(self) -> typing.Optional[AssembleWith]:
        """(experimental) Defines how to assemble the results of the transform job as a single S3 object.

        :default: - None

        :stability: experimental
        """
        result = self._values.get("assemble_with")
        return result

    @builtins.property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """(experimental) AWS KMS key that Amazon SageMaker uses to encrypt the model artifacts at rest using Amazon S3 server-side encryption.

        :default: - default KMS key for Amazon S3 for your role's account.

        :stability: experimental
        """
        result = self._values.get("encryption_key")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransformOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.TransformResources",
    jsii_struct_bases=[],
    name_mapping={
        "instance_count": "instanceCount",
        "instance_type": "instanceType",
        "volume_encryption_key": "volumeEncryptionKey",
    },
)
class TransformResources:
    def __init__(
        self,
        *,
        instance_count: jsii.Number,
        instance_type: aws_cdk.aws_ec2.InstanceType,
        volume_encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
    ) -> None:
        """(experimental) ML compute instances for the transform job.

        :param instance_count: (experimental) Number of ML compute instances to use in the transform job.
        :param instance_type: (experimental) ML compute instance type for the transform job.
        :param volume_encryption_key: (experimental) AWS KMS key that Amazon SageMaker uses to encrypt data on the storage volume attached to the ML compute instance(s). Default: - None

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "instance_count": instance_count,
            "instance_type": instance_type,
        }
        if volume_encryption_key is not None:
            self._values["volume_encryption_key"] = volume_encryption_key

    @builtins.property
    def instance_count(self) -> jsii.Number:
        """(experimental) Number of ML compute instances to use in the transform job.

        :stability: experimental
        """
        result = self._values.get("instance_count")
        assert result is not None, "Required property 'instance_count' is missing"
        return result

    @builtins.property
    def instance_type(self) -> aws_cdk.aws_ec2.InstanceType:
        """(experimental) ML compute instance type for the transform job.

        :stability: experimental
        """
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return result

    @builtins.property
    def volume_encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """(experimental) AWS KMS key that Amazon SageMaker uses to encrypt data on the storage volume attached to the ML compute instance(s).

        :default: - None

        :stability: experimental
        """
        result = self._values.get("volume_encryption_key")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransformResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.TransformS3DataSource",
    jsii_struct_bases=[],
    name_mapping={"s3_uri": "s3Uri", "s3_data_type": "s3DataType"},
)
class TransformS3DataSource:
    def __init__(
        self,
        *,
        s3_uri: builtins.str,
        s3_data_type: typing.Optional[S3DataType] = None,
    ) -> None:
        """(experimental) Location of the channel data.

        :param s3_uri: (experimental) Identifies either a key name prefix or a manifest.
        :param s3_data_type: (experimental) S3 Data Type. Default: 'S3Prefix'

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "s3_uri": s3_uri,
        }
        if s3_data_type is not None:
            self._values["s3_data_type"] = s3_data_type

    @builtins.property
    def s3_uri(self) -> builtins.str:
        """(experimental) Identifies either a key name prefix or a manifest.

        :stability: experimental
        """
        result = self._values.get("s3_uri")
        assert result is not None, "Required property 's3_uri' is missing"
        return result

    @builtins.property
    def s3_data_type(self) -> typing.Optional[S3DataType]:
        """(experimental) S3 Data Type.

        :default: 'S3Prefix'

        :stability: experimental
        """
        result = self._values.get("s3_data_type")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransformS3DataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.VpcConfig",
    jsii_struct_bases=[],
    name_mapping={"vpc": "vpc", "subnets": "subnets"},
)
class VpcConfig:
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        """(experimental) Specifies the VPC that you want your Amazon SageMaker training job to connect to.

        :param vpc: (experimental) VPC.
        :param subnets: (experimental) VPC subnets. Default: - Private Subnets are selected

        :stability: experimental
        """
        if isinstance(subnets, dict):
            subnets = aws_cdk.aws_ec2.SubnetSelection(**subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }
        if subnets is not None:
            self._values["subnets"] = subnets

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """(experimental) VPC.

        :stability: experimental
        """
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """(experimental) VPC subnets.

        :default: - Private Subnets are selected

        :stability: experimental
        """
        result = self._values.get("subnets")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IContainerDefinition)
class ContainerDefinition(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.ContainerDefinition",
):
    """(experimental) Describes the container, as part of model definition.

    :see: https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_ContainerDefinition.html
    :stability: experimental
    """

    def __init__(
        self,
        *,
        container_host_name: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[aws_cdk.aws_stepfunctions.TaskInput] = None,
        image: typing.Optional[DockerImage] = None,
        mode: typing.Optional[Mode] = None,
        model_package_name: typing.Optional[builtins.str] = None,
        model_s3_location: typing.Optional[S3Location] = None,
    ) -> None:
        """
        :param container_host_name: (experimental) This parameter is ignored for models that contain only a PrimaryContainer. When a ContainerDefinition is part of an inference pipeline, the value of the parameter uniquely identifies the container for the purposes of logging and metrics. Default: - None
        :param environment_variables: (experimental) The environment variables to set in the Docker container. Default: - No variables
        :param image: (experimental) The Amazon EC2 Container Registry (Amazon ECR) path where inference code is stored. Default: - None
        :param mode: (experimental) Defines how many models the container hosts. Default: - Mode.SINGLE_MODEL
        :param model_package_name: (experimental) The name or Amazon Resource Name (ARN) of the model package to use to create the model. Default: - None
        :param model_s3_location: (experimental) The S3 path where the model artifacts, which result from model training, are stored. This path must point to a single gzip compressed tar archive (.tar.gz suffix). The S3 path is required for Amazon SageMaker built-in algorithms, but not if you use your own algorithms. Default: - None

        :stability: experimental
        """
        options = ContainerDefinitionOptions(
            container_host_name=container_host_name,
            environment_variables=environment_variables,
            image=image,
            mode=mode,
            model_package_name=model_package_name,
            model_s3_location=model_s3_location,
        )

        jsii.create(ContainerDefinition, self, [options])

    @jsii.member(jsii_name="bind")
    def bind(self, task: ISageMakerTask) -> ContainerDefinitionConfig:
        """(experimental) Called when the ContainerDefinition type configured on Sagemaker Task.

        :param task: -

        :stability: experimental
        """
        return jsii.invoke(self, "bind", [task])


@jsii.implements(IEcsLaunchTarget)
class EcsEc2LaunchTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EcsEc2LaunchTarget",
):
    """Configuration for running an ECS task on EC2.

    :see: https://docs.aws.amazon.com/AmazonECS/latest/userguide/launch_types.html#launch-type-ec2
    """

    def __init__(
        self,
        *,
        placement_constraints: typing.Optional[typing.List[aws_cdk.aws_ecs.PlacementConstraint]] = None,
        placement_strategies: typing.Optional[typing.List[aws_cdk.aws_ecs.PlacementStrategy]] = None,
    ) -> None:
        """
        :param placement_constraints: Placement constraints. Default: - None
        :param placement_strategies: Placement strategies. Default: - None
        """
        options = EcsEc2LaunchTargetOptions(
            placement_constraints=placement_constraints,
            placement_strategies=placement_strategies,
        )

        jsii.create(EcsEc2LaunchTarget, self, [options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _task: EcsRunTask,
        *,
        task_definition: aws_cdk.aws_ecs.ITaskDefinition,
        cluster: typing.Optional[aws_cdk.aws_ecs.ICluster] = None,
    ) -> EcsLaunchTargetConfig:
        """Called when the EC2 launch type is configured on RunTask.

        :param _task: -
        :param task_definition: Task definition to run Docker containers in Amazon ECS.
        :param cluster: A regional grouping of one or more container instances on which you can run tasks and services. Default: - No cluster
        """
        launch_target_options = LaunchTargetBindOptions(
            task_definition=task_definition, cluster=cluster
        )

        return jsii.invoke(self, "bind", [_task, launch_target_options])


@jsii.implements(IEcsLaunchTarget)
class EcsFargateLaunchTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-stepfunctions-tasks.EcsFargateLaunchTarget",
):
    """Configuration for running an ECS task on Fargate.

    :see: https://docs.aws.amazon.com/AmazonECS/latest/userguide/launch_types.html#launch-type-fargate
    """

    def __init__(
        self,
        *,
        platform_version: aws_cdk.aws_ecs.FargatePlatformVersion,
    ) -> None:
        """
        :param platform_version: Refers to a specific runtime environment for Fargate task infrastructure. Fargate platform version is a combination of the kernel and container runtime versions.
        """
        options = EcsFargateLaunchTargetOptions(platform_version=platform_version)

        jsii.create(EcsFargateLaunchTarget, self, [options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _task: EcsRunTask,
        *,
        task_definition: aws_cdk.aws_ecs.ITaskDefinition,
        cluster: typing.Optional[aws_cdk.aws_ecs.ICluster] = None,
    ) -> EcsLaunchTargetConfig:
        """Called when the Fargate launch type configured on RunTask.

        :param _task: -
        :param task_definition: Task definition to run Docker containers in Amazon ECS.
        :param cluster: A regional grouping of one or more container instances on which you can run tasks and services. Default: - No cluster
        """
        launch_target_options = LaunchTargetBindOptions(
            task_definition=task_definition, cluster=cluster
        )

        return jsii.invoke(self, "bind", [_task, launch_target_options])


__all__ = [
    "AcceleratorClass",
    "AcceleratorType",
    "ActionOnFailure",
    "AlgorithmSpecification",
    "AssembleWith",
    "AthenaGetQueryExecution",
    "AthenaGetQueryExecutionProps",
    "AthenaGetQueryResults",
    "AthenaGetQueryResultsProps",
    "AthenaStartQueryExecution",
    "AthenaStartQueryExecutionProps",
    "AthenaStopQueryExecution",
    "AthenaStopQueryExecutionProps",
    "BatchContainerOverrides",
    "BatchJobDependency",
    "BatchStrategy",
    "BatchSubmitJob",
    "BatchSubmitJobProps",
    "Channel",
    "CodeBuildStartBuild",
    "CodeBuildStartBuildProps",
    "CommonEcsRunTaskProps",
    "CompressionType",
    "ContainerDefinition",
    "ContainerDefinitionConfig",
    "ContainerDefinitionOptions",
    "ContainerOverride",
    "ContainerOverrides",
    "DataSource",
    "DockerImage",
    "DockerImageConfig",
    "DynamoAttributeValue",
    "DynamoConsumedCapacity",
    "DynamoDeleteItem",
    "DynamoDeleteItemProps",
    "DynamoGetItem",
    "DynamoGetItemProps",
    "DynamoItemCollectionMetrics",
    "DynamoProjectionExpression",
    "DynamoPutItem",
    "DynamoPutItemProps",
    "DynamoReturnValues",
    "DynamoUpdateItem",
    "DynamoUpdateItemProps",
    "EcsEc2LaunchTarget",
    "EcsEc2LaunchTargetOptions",
    "EcsFargateLaunchTarget",
    "EcsFargateLaunchTargetOptions",
    "EcsLaunchTargetConfig",
    "EcsRunTask",
    "EcsRunTaskBase",
    "EcsRunTaskBaseProps",
    "EcsRunTaskProps",
    "EmrAddStep",
    "EmrAddStepProps",
    "EmrCancelStep",
    "EmrCancelStepProps",
    "EmrCreateCluster",
    "EmrCreateClusterProps",
    "EmrModifyInstanceFleetByName",
    "EmrModifyInstanceFleetByNameProps",
    "EmrModifyInstanceGroupByName",
    "EmrModifyInstanceGroupByNameProps",
    "EmrSetClusterTerminationProtection",
    "EmrSetClusterTerminationProtectionProps",
    "EmrTerminateCluster",
    "EmrTerminateClusterProps",
    "EncryptionConfiguration",
    "EncryptionOption",
    "EvaluateExpression",
    "EvaluateExpressionProps",
    "GlueDataBrewStartJobRun",
    "GlueDataBrewStartJobRunProps",
    "GlueStartJobRun",
    "GlueStartJobRunProps",
    "IContainerDefinition",
    "IEcsLaunchTarget",
    "ISageMakerTask",
    "InputMode",
    "InvocationType",
    "InvokeActivity",
    "InvokeActivityProps",
    "InvokeFunction",
    "InvokeFunctionProps",
    "JobDependency",
    "LambdaInvocationType",
    "LambdaInvoke",
    "LambdaInvokeProps",
    "LaunchTargetBindOptions",
    "MetricDefinition",
    "Mode",
    "ModelClientOptions",
    "OutputDataConfig",
    "ProductionVariant",
    "PublishToTopic",
    "PublishToTopicProps",
    "QueryExecutionContext",
    "RecordWrapperType",
    "ResourceConfig",
    "ResultConfiguration",
    "RunBatchJob",
    "RunBatchJobProps",
    "RunEcsEc2Task",
    "RunEcsEc2TaskProps",
    "RunEcsFargateTask",
    "RunEcsFargateTaskProps",
    "RunGlueJobTask",
    "RunGlueJobTaskProps",
    "RunLambdaTask",
    "RunLambdaTaskProps",
    "S3DataDistributionType",
    "S3DataSource",
    "S3DataType",
    "S3Location",
    "S3LocationBindOptions",
    "S3LocationConfig",
    "SageMakerCreateEndpoint",
    "SageMakerCreateEndpointConfig",
    "SageMakerCreateEndpointConfigProps",
    "SageMakerCreateEndpointProps",
    "SageMakerCreateModel",
    "SageMakerCreateModelProps",
    "SageMakerCreateTrainingJob",
    "SageMakerCreateTrainingJobProps",
    "SageMakerCreateTransformJob",
    "SageMakerCreateTransformJobProps",
    "SageMakerUpdateEndpoint",
    "SageMakerUpdateEndpointProps",
    "SendToQueue",
    "SendToQueueProps",
    "ShuffleConfig",
    "SnsPublish",
    "SnsPublishProps",
    "SplitType",
    "SqsSendMessage",
    "SqsSendMessageProps",
    "StartExecution",
    "StartExecutionProps",
    "StepFunctionsInvokeActivity",
    "StepFunctionsInvokeActivityProps",
    "StepFunctionsStartExecution",
    "StepFunctionsStartExecutionProps",
    "StoppingCondition",
    "TaskEnvironmentVariable",
    "TransformDataSource",
    "TransformInput",
    "TransformOutput",
    "TransformResources",
    "TransformS3DataSource",
    "VpcConfig",
]

publication.publish()
