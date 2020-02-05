"""Class to create a HostedZone using AWS CDK HostedZone method

Author: Binny Abraham

"""

from aws_cdk import core, aws_route53, aws_s3
import boto3
from cdk_config import account

class CdkCommonStack(core.Stack):

    # INIT
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


    # COMMON FUNCTIONS
    def generate_cfn_stack_name(self, project_code, environment, region_name, stack_suffix):
        """Generate CFN stack name"""
        return '{}-{}-{}-{}'.format(project_code, environment, region_name, stack_suffix)

    def generate_stack_key(self, stack_id):
        """Generate CFN stack id"""
        return stack_id.split('-')[-1]

    def generate_resource_name(self, project_code, environment, region_name, stack_name, resource_suffix):
        """Generate CFN Resource name"""
        return '{}-{}-{}-{}-{}'.format(project_code, environment, region_name, stack_name, resource_suffix)

    def generate_outputs_from_dependent_stacks(self, project_code, environment, dependent_stacks):
        """
        Generate CFN Outputs from dependent stacks mentioned in config file
        """
        cfn_outputs = []
        for exp_stack in dependent_stacks:
            export_stack_name = self.generate_cfn_stack_name(project_code, environment, exp_stack['region'], exp_stack['suffix'])
            cfn_outputs.extend(self.get_cfn_output_using_sdk(export_stack_name, exp_stack['account'], exp_stack['region']))
        return cfn_outputs


    # PARAMETERS
    def generate_cfn_parameters(self, cfn_params):
        '''
        Generate all Cloudformation parameters here
        '''
        params_dct = {}
        for param_key, param_values in cfn_params.items():
            param_obj = self.create_cfn_parameter(param_key, **param_values)
            params_dct[param_obj.to_string()] = param_obj.value.to_string()
        return params_dct

    def create_cfn_parameter(self, param_key, **param_values):
        '''
        Create individual cloudformation parameter using aws_cdk core.CfnParameter method
        '''
        return core.CfnParameter(
            self,
            param_key,
            **param_values
        )

    def generate_cfn_parameters_from_cfn_outputs(self, cfn_outputs):
        '''
        Create cfn parameters from cfn outputs
        '''
        output_dct = {}
        for output in cfn_outputs:
            print(output)
            output_dct.update({output['OutputKey']:{
                'type': 'String',
                'default': output['OutputValue'],
                'description': ''
            }})
        return output_dct

    def get_value_from_parameters(self, parameter_key, parameters, stack_id):
        '''
        Get value from cfn parameters using parameter key
        '''
        return parameters["{}/{}".format(stack_id, parameter_key)]


    # TAGS
    def generate_cfn_tags(self, cfn_tags):
        '''
        Create individual cloudformation Tags using aws_cdk core.Tag.add method
        '''
        for tag_key, tag_value in cfn_tags.items():
            core.Tag.add(self, key=tag_key, value=tag_value)


    # OUTPUTS
    def create_cfn_output(self, output_id, output_value, **output_variables):
        '''
        Create individual cloudformation output using aws_cdk core.CfnOutput method
        '''
        core.CfnOutput(
            self,
            output_id,
            value=output_value,
            **output_variables
        )

    def get_cfn_output_using_sdk(self, stack_id, dest_account, dest_region):
        '''
        Get cloudformation outputs from stack using stack id and sdk boto3
        '''
        boto3.setup_default_session(profile_name=dest_account, region_name=dest_region)
        cloudformation = boto3.resource('cloudformation')
        stack_resource = cloudformation.Stack(stack_id)
        return stack_resource.outputs

    def get_cfn_output_using_cdk(self, export_name):
        '''
        Get cloudformation outputs from stack using cdk import
        '''
        return core.Fn.import_value(export_name)

    def extract_cfn_output(self, export_name, description):
        return {
            "OutputKey": export_name,
            "OutputValue": self.get_cfn_output_using_cdk(export_name),
            "Description": description
        }


    # CFN RESOURCES CREATION
    # GENERATE CLOUDFORMATION RESOURCES STARTS HERE
    def generate_cfn_resources(self, stack_key, resource_variables):
        '''
        Generate all Cloudformation resources here
        '''
        resource_dct = {}
        for resource_key, resource_value in resource_variables.items():
            resource_name = self.generate_resource_name(self.common['project_code'], self.common['environment'], self.region_name, stack_key, resource_value['suffix'])
            func_name = "self.create_{}('{}{}', '{}', kwargs={})".format(resource_key, stack_key, resource_key, resource_name, resource_value)
            resource_dct[resource_key] = eval(func_name)

            # GENERATE CLOUDFORMATION OUTPUTS
            if 'outputs' in resource_value:
                self.generate_cfn_outputs(resource_key, resource_dct, resource_value['outputs'])
        return resource_dct
    # GENERATE CLOUDFORMATION RESOURCES ENDS HERE


    # GENERATE CLOUDFORMATION OUTPUTS STARTS HERE
    def generate_cfn_outputs(self, resource_key, resource_dct, output_variables):
        '''
        Generate all Cloudformation outputs here
        '''
        for output_key, output_value in output_variables.items():
            export_value = eval("{}.{}".format('resource_dct[resource_key]', output_value['field_name']))
            self.create_cfn_output(output_value['id'], export_value)
     # GENERATE CLOUDFORMATION OUTPUTS ENDS HERE
