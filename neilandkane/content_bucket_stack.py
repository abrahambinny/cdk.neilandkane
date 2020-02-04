"""Class to create a Cross Region Replica Bucket

Author: Binny Abraham

"""

from aws_cdk import core, aws_s3
from aws_cdk.core import Environment
from cdk_common import CdkCommonStack
from cdk_config import CFN_VARIABLES

class ContentBucketStack(CdkCommonStack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.account_name = kwargs['env'].account
        self.region_name = kwargs['env'].region
        self.cfn_variables = CFN_VARIABLES
        self.common = self.cfn_variables['common']

        # GENERATE CLOUDFORMATION RESOURCES
        stack_key = self.generate_stack_key(id)
        resource_variables = self.cfn_variables['accounts'][self.account_name]['regions'][self.region_name]['stacks'][stack_key]['cfn_resource_variables']
        self.resources = self.generate_cfn_resources(stack_key, resource_variables)

    def create_content_bucket(self, logical_id, bucket_name, **kwargs):
        """
        Create bucket using aws_s3 Bucket method
        """
        s3_bucket = aws_s3.Bucket(
            self,
            logical_id,
            bucket_name=bucket_name,
            versioned=True,
            removal_policy=core.RemovalPolicy.DESTROY
        )
        s3_bucket.grant_public_access()
        return s3_bucket
