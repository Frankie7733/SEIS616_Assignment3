#!/usr/bin/env python3
import aws_cdk as cdk

from my_cdk_project.network_stack import CdkLabNetworkStack
from my_cdk_project.server_stack import CdkLabServerStack

app = cdk.App()

network_stack = CdkLabNetworkStack(app, "CdkLabNetworkStack")
CdkLabServerStack(app, "CdkLabServerStack", vpc=network_stack.vpc)

app.synth()
