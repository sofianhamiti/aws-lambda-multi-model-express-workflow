from aws_cdk import (
    aws_iam as iam,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    core
)


class StateMachineStack(core.NestedStack):
    def __init__(self, scope, id, name=None, lambdas=None) -> None:
        super().__init__(scope, id)
        # ==================================================
        # ================= IAM ROLE =======================
        # ==================================================
        state_machine_role = iam.Role(
            scope=self,
            id='state_machine_role',
            assumed_by=iam.ServicePrincipal(service='states.amazonaws.com'),
        )
        state_machine_role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=['lambda:InvokeFunction'],
            resources=['*']
        ))

        # ==================================================
        # ================= STATE MACHINE ==================
        # ==================================================
        invoke_lambda_rf = tasks.LambdaInvoke(
            scope=self,
            id='Random Forest',
            lambda_function=lambdas['lambda_rf'],
            payload_response_only=True
        )
        invoke_lambda_svr = tasks.LambdaInvoke(
            scope=self,
            id='Support Vector',
            lambda_function=lambdas['lambda_svr'],
            payload_response_only=True
        )
        invoke_lambda_lr = tasks.LambdaInvoke(
            scope=self,
            id='Linear Regressor',
            lambda_function=lambdas['lambda_lr'],
            payload_response_only=True
        )

        definition = sfn.Parallel(
            scope=self,
            id='Invoke Predictions'
        ).branch(
            invoke_lambda_rf
        ).branch(
            invoke_lambda_svr
        ).branch(
            invoke_lambda_lr
        )

        self.state_machine = sfn.StateMachine(
            scope=self,
            id='state_machine',
            state_machine_name=name,
            definition=definition,
            role=state_machine_role,
            state_machine_type=sfn.StateMachineType.EXPRESS
        )
