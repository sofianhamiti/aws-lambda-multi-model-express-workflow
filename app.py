from aws_cdk import core
from stacks.api_stack import ApiStack
from stacks.lambda_stack import LambdaStack
from stacks.state_machine_stack import StateMachineStack


class InferenceStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        project_name = 'inference'
        # ==================================================
        # =================== LAMBDAS ======================
        # ==================================================
        lambda_rf_stack = LambdaStack(
            scope=self,
            id='lambda_rf',
            name=f'{project_name}-random-forest',
            directory='lambda_images/random_forest',
            bucket='<ADD YOUR S3 BUCKET NAME HERE>',
            key='<ADD THE MODEL S3 KEY HERE>'
        )

        lambda_svr_stack = LambdaStack(
            scope=self,
            id='lambda_svr',
            name=f'{project_name}-support-vector',
            directory='lambda_images/support_vector',
            bucket='<ADD YOUR S3 BUCKET NAME HERE>',
            key='<ADD THE MODEL S3 KEY HERE>'
        )

        lambda_lr_stack = LambdaStack(
            scope=self,
            id='lambda_lr',
            name=f'{project_name}-linear-regressor',
            directory='lambda_images/linear_regressor',
            bucket='<ADD YOUR S3 BUCKET NAME HERE>',
            key='<ADD THE MODEL S3 KEY HERE>'
        )
        # ==================================================
        # ================= STATE MACHINE ==================
        # ==================================================
        state_machine_stack = StateMachineStack(
            scope=self,
            id='state_machine',
            name=f'{project_name}-state-machine',
            lambdas={
                'lambda_rf': lambda_rf_stack.lambda_function,
                'lambda_svr': lambda_svr_stack.lambda_function,
                'lambda_lr': lambda_lr_stack.lambda_function
            }
        )

        # ==================================================
        # ================== API GATEWAY ===================
        # ==================================================
        api_stack = ApiStack(
            scope=self,
            id='api',
            name=f'{project_name}-api',
            state_machine_arn=state_machine_stack.state_machine.state_machine_arn
        )


app = core.App()
InferenceStack(app, "InferenceStack")
app.synth()
