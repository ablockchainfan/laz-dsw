from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elb
import aws_cdk.aws_autoscaling as autoscaling
import os 

ec2_type = "t2.medium"
key_name = "id_rsa"  # Setup key_name for EC2 instance login 
linux_ami = ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
                                 edition=ec2.AmazonLinuxEdition.STANDARD,
                                 virtualization=ec2.AmazonLinuxVirt.HVM,
                                 storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                 )  # Indicate your AMI, no need a specific id in the region


script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "user_data/user_data.sh"
abs_file_path = os.path.join(script_dir, rel_path)

with open(abs_file_path) as f:
    user_data = f.read()

# with open(".user_data/user_data.sh") as f:


class AutoEc2(core.NestedStack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Bastion
        # bastion = ec2.BastionHostLinux(self, "myBastion",
        #                                vpc=vpc,
        #                                subnet_selection=ec2.SubnetSelection(
        #                                    subnet_type=ec2.SubnetType.ISOLATED),
        #                                instance_name="myBastionHostLinux",
        #                                instance_type=ec2.InstanceType(instance_type_identifier="t2.micro"))
        
        # print(bastion.instance.instance_private_ip)
        
        # Setup key_name for EC2 instance login if you don't use Session Manager
        # bastion.instance.instance.add_property_override("KeyName", key_name)

        # bastion.connections.allow_from_any_ipv4(
        #     ec2.Port.tcp(22), "Internet access SSH")

        # Create ALB
        print("creating LB")
        self.alb = elb.ApplicationLoadBalancer(self, "myALB",
                                          vpc=vpc,
                                          internet_facing=False,
                                          load_balancer_name="myALB"
                                          )

        
        self.alb.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "Internet access ALB 80")
        listener = self.alb.add_listener("my80",
                                    port=80,
                                    open=True)

        # Create Autoscaling Group with fixed 2*EC2 hosts
        self.asg = autoscaling.AutoScalingGroup(self, "myASG",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.ISOLATED),
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                machine_image=linux_ami,
                                                key_name=key_name,
                                                user_data=ec2.UserData.custom(user_data),
                                                desired_capacity=1,
                                                min_capacity=1,
                                                max_capacity=2,
                                                # block_devices=[
                                                #     autoscaling.BlockDevice(
                                                #         device_name="/dev/xvda",
                                                #         volume=autoscaling.BlockDeviceVolume.ebs(
                                                #             volume_type=autoscaling.EbsDeviceVolumeType.GP2,
                                                #             volume_size=12,
                                                #             delete_on_termination=True
                                                #         )),
                                                #     autoscaling.BlockDevice(
                                                #         device_name="/dev/sdb",
                                                #         volume=autoscaling.BlockDeviceVolume.ebs(
                                                #             volume_size=20)
                                                #         # 20GB, with default volume_type gp2
                                                #     )
                                                # ]
                                                )

        self.asg.connections.allow_from(self.alb, ec2.Port.tcp(80), "ALB access 80 port of EC2 in Autoscaling Group")
        listener.add_targets("addTargetGroup",
                             port=80,
                             targets=[self.asg])

        core.CfnOutput(self, "Output",
                       value=self.alb.load_balancer_dns_name)