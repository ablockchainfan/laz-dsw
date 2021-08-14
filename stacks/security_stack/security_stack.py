from aws_cdk import core
import aws_cdk.aws_kms as kms


class SecurityStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> kms.Key:
        super().__init__(scope, id, **kwargs)

    # Create Security Groups