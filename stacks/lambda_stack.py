from aws_cdk import (
    aws_iam as iam,
    aws_lambda,
    core
)


class LambdaStack(core.NestedStack):
    def __init__(self, scope, id, *, name=None, directory=None, bucket=None, key=None) -> None:
        super().__init__(scope, id)
        # ==================================================
        # ================= IAM ROLE =======================
        # ==================================================
        lambda_role = iam.Role(
            scope=self,
            id='lambda_role',
            assumed_by=iam.ServicePrincipal(service='lambda.amazonaws.com'),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name('AWSLambdaExecute')]
        )

        # ==================================================
        # =================== ECR IMAGE ====================
        # ==================================================
        ecr_image = aws_lambda.DockerImageCode.from_image_asset(
            repository_name=name,
            directory=directory
        )

        # ==================================================
        # ================ LAMBDA FUNCTION =================
        # ==================================================
        self.lambda_function = aws_lambda.DockerImageFunction(
            scope=self,
            id='lambda',
            function_name=name,
            code=ecr_image,
            memory_size=1024,
            role=lambda_role,
            environment={
                'BUCKET': bucket,
                'KEY': key
            },
            timeout=core.Duration.seconds(60)
        )
