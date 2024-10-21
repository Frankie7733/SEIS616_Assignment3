from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_rds as rds
)

from constructs import Construct

class CdkLabServerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Security group for web servers
        web_server_sg = ec2.SecurityGroup(self, "WebServerSG", vpc=vpc, allow_all_outbound=True)
        web_server_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP traffic")

        # Security group for RDS
        rds_sg = ec2.SecurityGroup(self, "RDSSG", vpc=vpc, allow_all_outbound=True)
        rds_sg.add_ingress_rule(web_server_sg, ec2.Port.tcp(3306), "Allow MySQL traffic from web servers")

        # Launch web servers in public subnets
        for i in range(2):
            ec2.Instance(self, f"WebServer{i+1}",
                vpc=vpc,
                instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
                machine_image=ec2.MachineImage.latest_amazon_linux(),
                security_group=web_server_sg,
                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
            )

        # Create RDS instance in private subnets
        rds.DatabaseInstance(self, "RDSInstance",
            engine=rds.DatabaseInstanceEngine.mysql(version=rds.MysqlEngineVersion.VER_8_0_26),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
            vpc=vpc,
            security_groups=[rds_sg],
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT)
        )
