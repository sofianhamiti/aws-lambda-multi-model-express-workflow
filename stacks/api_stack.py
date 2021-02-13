from aws_cdk import (
    aws_iam as iam,
    aws_apigatewayv2 as apigw,
    core
)


class ApiStack(core.NestedStack):
    def __init__(self, scope, id, name=None, state_machine_arn=None) -> None:
        super().__init__(scope, id)
        # ==================================================
        # ================= IAM ROLE =======================
        # ==================================================
        api_role = iam.Role(
            scope=self,
            id='api_role',
            assumed_by=iam.ServicePrincipal(service='apigateway.amazonaws.com'),
        )
        api_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=['states:StartSyncExecution'],
                resources=['*']
            )
        )

        # ==================================================
        # ================== API GATEWAY ===================
        # ==================================================
        api = apigw.HttpApi(
            scope=self,
            id='api',
            api_name=name,
            cors_preflight={
                "allow_headers": ["Authorization"],
                "allow_methods": [apigw.HttpMethod.POST],
                "allow_origins": ["*"],
                "max_age": core.Duration.days(10)
            }
        )

        integration = apigw.CfnIntegration(
            scope=self,
            id='integration',
            api_id=api.http_api_id,
            credentials_arn=api_role.role_arn,
            integration_type='AWS_PROXY',
            integration_subtype='StepFunctions-StartSyncExecution',
            request_parameters={
                'Input': '$request.body',
                'StateMachineArn': f'{state_machine_arn}'
            },
            payload_format_version='1.0'
        )

        apigw.CfnRoute(
            scope=self,
            id='route',
            api_id=api.http_api_id,
            route_key='POST /',
            target=f'integrations/{integration.ref}'
        )
