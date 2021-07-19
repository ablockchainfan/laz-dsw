from typing import Dict, List

from aws_cdk import (
    core,
    aws_ec2 as ec2
)

class TgwAttach(core.Construct):
    def __init__(self, scope: core.Construct, id: str, tgw_id:str ,vpc:ec2.Vpc ,config: Dict) -> None:
        super().__init__(scope, id)
        self.config = config
        self.attach_vpc(tgw_id, vpc )
        # self.attach_vpc(vpc)

    # tgw-022ff64e286df97ce
        # //attach VPCs to gateway
    def attach_vpc(self, tgw_id, vpc:ec2.Vpc): 
        TransitGatewayAttachment = ec2.CfnTransitGatewayAttachment(self, 'TransitGatewayAttachmentEgress', 
            transit_gateway_id=tgw_id,
            vpc_id= vpc.vpc_id,
            subnet_ids= [vpc.isolated_subnets[0].subnet_id, vpc.isolated_subnets[1].subnet_id],
            tags= [{
                'key': 'Name',
                'value': "TG-Egress-VPC-Private_SubNet-Attachment"
            }],
        )

        for  subnet in vpc.isolated_subnets:
            ec2.CfnRoute(self, 
                subnet.node.unique_id, 
                route_table_id=subnet.route_table.route_table_id,
                destination_cidr_block="0.0.0.0/0",
                transit_gateway_id=tgw_id )
            

        # TransitGatewayAttachmentEgress.addDependsOn(TransitGateway);

        # const TransitGatewayAttachmentPrivate = new ec2.CfnTransitGatewayAttachment(this, 'TransitGatewayAttachmentPrivate', {
        # transitGatewayId: TransitGateway.ref,
        # vpcId: privateVPC.vpcId,
        # subnetIds: [privateVPC.isolatedSubnets[0].subnetId],
        # tags: [{
        #     key: 'Name',
        #     value: "TG-Private-VPC-Private_SubNet-Attachment"
        # }],
        # });
        # TransitGatewayAttachmentEgress.addDependsOn(TransitGateway);



    # import cdk = require('@aws-cdk/core');
    # import ec2 = require('@aws-cdk/aws-ec2');
    # import { SubnetType, CfnRoute} from '@aws-cdk/aws-ec2';
    # import { ManagedPolicy, Role, ServicePrincipal, CfnInstanceProfile, PolicyDocument, PolicyStatement, Effect } from '@aws-cdk/aws-iam';

    # export class EgressVpcTgDemoStack extends cdk.Stack {
    #   constructor(scope: cdk.Construct, id: string, props ? : cdk.StackProps) {
    #     super(scope, id, props);
    #     //set-up egress and private VPCs
    #     const egressVPC = new ec2.Vpc(this, 'Egress VPC', {
    #       cidr: "10.0.1.0/26",
    #       //natGateways: 1, add this to limit numer of deployed NAT gateways
    #       subnetConfiguration: [{
    #           cidrMask: 28,
    #           name: 'Public - EgressVPC SubNet',
    #           subnetType: SubnetType.PUBLIC,
    #         },
    #         {
    #           cidrMask: 28,
    #           name: 'Private - EgressVPC SubNet',
    #           subnetType: SubnetType.PRIVATE,
    #         },
    #       ]
    #     });
    #     const privateVPC = new ec2.Vpc(this, 'Private VPC', {
    #       cidr: "10.0.2.0/26",
    #       maxAzs: 1,
    #       enableDnsHostnames: true,
    #       enableDnsSupport: true,
    #       subnetConfiguration: [{
    #         cidrMask: 28,
    #         name: 'Isolated Subnet - privateVPC',
    #         subnetType: SubnetType.ISOLATED,
    #       }],
    #     });
    #     // Security Group to be used by EC2 instances in isolated subnet and accessed via Systems Manager
    #     const ssmPrivateSG = new ec2.SecurityGroup(this, 'SSMPrivateSecurityGroup', {
    #       vpc: privateVPC,
    #       securityGroupName: 'Demo EC2 Instance Security Group',
    #       description: 'Demo EC2 Instance Security Group',
    #       allowAllOutbound: true,
    #     });

    #     // uncomment below lines to add private link endpoints for Systems Manager
        
    #     // adding interface endpoints for Systems Manger use - only 443 from EC2-SG to Interface Endpoints necessary
    #     // const ssmIE = privateVPC.addInterfaceEndpoint('SSM', {
    #     //   service: ec2.InterfaceVpcEndpointAwsService.SSM,
    #     //   privateDnsEnabled: true,
    #     //   subnets: { subnetType: ec2.SubnetType.ISOLATED, onePerAz: true },
    #     // });
    #     // ssmIE.connections.allowFrom(ssmPrivateSG, ec2.Port.tcp(443), 'Allow from SSM IE Private SG');

    #     // const ssmMessagesIE = privateVPC.addInterfaceEndpoint('SSM-Messages', {
    #     //   service: ec2.InterfaceVpcEndpointAwsService.SSM_MESSAGES,
    #     //   privateDnsEnabled: true,
    #     //   subnets: { subnetType: ec2.SubnetType.ISOLATED, onePerAz: true },
    #     // });
    #     // ssmMessagesIE.connections.allowFrom(ssmPrivateSG, ec2.Port.tcp(443), 'Allow from SSM Messages IE Private SG');

    #     // const ec2IE = privateVPC.addInterfaceEndpoint('EC2', {
    #     //   service: ec2.InterfaceVpcEndpointAwsService.EC2,
    #     //   privateDnsEnabled: true,
    #     //   subnets: { subnetType: ec2.SubnetType.ISOLATED, onePerAz: true },
    #     // });
    #     // ec2IE.connections.allowFrom(ssmPrivateSG, ec2.Port.tcp(443), 'Allow from EC2 IE Private SG');

    #     // const ec2Messages = privateVPC.addInterfaceEndpoint('EC2-messages', {
    #     //   service: ec2.InterfaceVpcEndpointAwsService.EC2_MESSAGES,
    #     //   privateDnsEnabled: true,
    #     //   subnets: { subnetType: ec2.SubnetType.ISOLATED, onePerAz: true },
    #     // });
    #     // ec2Messages.connections.allowFrom(ssmPrivateSG, ec2.Port.tcp(443), 'Allow from EC2 Messages IE Private SG');

    #     // privateVPC.addGatewayEndpoint('S3-SSM', {
    #     //   service: ec2.GatewayVpcEndpointAwsService.S3,
    #     //   subnets: [{ subnetType: ec2.SubnetType.ISOLATED, onePerAz: true }],
    #     // });

    #     //Create TG gateway
    #     const TransitGateway = new ec2.CfnTransitGateway(this, 'Transit_Gateway', {
    #       description: "Transit Gateway",
    #       vpnEcmpSupport: 'enable',
    #       defaultRouteTableAssociation: 'disable',
    #       defaultRouteTablePropagation: 'disable',
    #       tags: [{
    #         key: 'Name',
    #         value: "Transit Gateway"
    #       }],
    #     });
    #     //attach VPCs to gateway
    #     const TransitGatewayAttachmentEgress = new ec2.CfnTransitGatewayAttachment(this, 'TransitGatewayAttachmentEgress', {
    #       transitGatewayId: TransitGateway.ref,
    #       vpcId: egressVPC.vpcId,
    #       subnetIds: [egressVPC.privateSubnets[0].subnetId, egressVPC.privateSubnets[1].subnetId],
    #       tags: [{
    #         key: 'Name',
    #         value: "TG-Egress-VPC-Private_SubNet-Attachment"
    #       }],
    #     });
    #     TransitGatewayAttachmentEgress.addDependsOn(TransitGateway);

    #     const TransitGatewayAttachmentPrivate = new ec2.CfnTransitGatewayAttachment(this, 'TransitGatewayAttachmentPrivate', {
    #       transitGatewayId: TransitGateway.ref,
    #       vpcId: privateVPC.vpcId,
    #       subnetIds: [privateVPC.isolatedSubnets[0].subnetId],
    #       tags: [{
    #         key: 'Name',
    #         value: "TG-Private-VPC-Private_SubNet-Attachment"
    #       }],
    #     });
    #     TransitGatewayAttachmentEgress.addDependsOn(TransitGateway);

    #     //add routes
    #     for (let subnet of egressVPC.publicSubnets) {
    #       new CfnRoute(this, subnet.node.uniqueId, {
    #         routeTableId: subnet.routeTable.routeTableId,
    #         destinationCidrBlock: privateVPC.vpcCidrBlock,
    #         transitGatewayId: TransitGateway.ref,
    #       }).addDependsOn(TransitGatewayAttachmentEgress);
    #     };

    #     for (let subnet of privateVPC.isolatedSubnets) {
    #       new CfnRoute(this, subnet.node.uniqueId, {
    #         routeTableId: subnet.routeTable.routeTableId,
    #         destinationCidrBlock: "0.0.0.0/0",
    #         transitGatewayId: TransitGateway.ref,
    #       }).addDependsOn(TransitGatewayAttachmentPrivate);
    #     };

    #     //add TG Route Domain (fancy name for route table) and internet egress route
    #     const TGRouteTable = new ec2.CfnTransitGatewayRouteTable(this, "TGEgressRouteTable", {
    #       transitGatewayId: TransitGateway.ref,
    #       tags: [{
    #         key: 'Name',
    #         value: "TG Route Domain"
    #       }],
    #     }); 
    #     const TransitGatewayRouteTable = new ec2.CfnTransitGatewayRoute(this, "TransitGatewayToEgressVPCRoute", {
    #       transitGatewayRouteTableId: TGRouteTable.ref,
    #       transitGatewayAttachmentId: TransitGatewayAttachmentEgress.ref,
    #       destinationCidrBlock: "0.0.0.0/0"
    #     });
    #     const TGRouteTableAssociationEgressVPC = new ec2.CfnTransitGatewayRouteTableAssociation(this, 'EgressVPC_TG_Association', {
    #       transitGatewayAttachmentId: TransitGatewayAttachmentEgress.ref,
    #       transitGatewayRouteTableId: TransitGatewayRouteTable.transitGatewayRouteTableId,
    #     });
    #     const TGRouteTablePropagationEgressVPC = new ec2.CfnTransitGatewayRouteTablePropagation(this, 'EgressVPC_TG_Propagation', {
    #       transitGatewayAttachmentId: TransitGatewayAttachmentEgress.ref,
    #       transitGatewayRouteTableId: TransitGatewayRouteTable.transitGatewayRouteTableId,
    #     });
    #     const TGRouteTableAssociationPrivateVPC = new ec2.CfnTransitGatewayRouteTableAssociation(this, 'PrivateVPC_TG_Association', {
    #       transitGatewayAttachmentId: TransitGatewayAttachmentPrivate.ref,
    #       transitGatewayRouteTableId: TransitGatewayRouteTable.transitGatewayRouteTableId,
    #     });
    #     const TGRouteTablePropagationPrivateVPC = new ec2.CfnTransitGatewayRouteTablePropagation(this, 'PrivateVPC_TG_Propagation', {
    #       transitGatewayAttachmentId: TransitGatewayAttachmentPrivate.ref,
    #       transitGatewayRouteTableId: TransitGatewayRouteTable.transitGatewayRouteTableId,
    #     });

    #     // Time to test the routes. 

    #     //Getting latest Amazon Linux AMI
    #     const latestLinuxAMI = new ec2.AmazonLinuxImage({
    #       generation: ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
    #       edition: ec2.AmazonLinuxEdition.STANDARD,
    #       virtualization: ec2.AmazonLinuxVirt.HVM,
    #       storage: ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
    #     });
    #     //ssm agent Role - we don't want to rely on a bastion host
    #     const SSMRole = new Role(this, 'SSMRole', {
    #       assumedBy: new ServicePrincipal('ec2.amazonaws.com'),
    #       managedPolicies: [
    #         ManagedPolicy.fromAwsManagedPolicyName('AmazonSSMManagedInstanceCore'),
    #         ManagedPolicy.fromAwsManagedPolicyName('CloudWatchAgentServerPolicy'),
    #       ],
    #       // optional inline policy for S3 SSM
    #       inlinePolicies: {
    #         ssmS3policy: new PolicyDocument({
    #           statements: [
    #             new PolicyStatement({
    #               effect: Effect.ALLOW,
    #               actions: [
    #                 's3:GetObject'
    #               ],
    #               resources: [
    #                 'arn:aws:s3:::aws-ssm-' + this.region +'/*',
    #                 'arn:aws:s3:::aws-windows-downloads-' + this.region +'/*',
    #                 'arn:aws:s3:::amazon-ssm-' +this.region+'/*',
    #                 'arn:aws:s3:::amazon-ssm-packages-' + this.region +'/*',
    #                 'arn:aws:s3:::' + this.region +'-birdwatcher-prod/*',
    #                 'arn:aws:s3:::patch-baseline-snapshot-' + this.region +'/*'
    #               ]
    #             })
    #           ]
    #         })
    #       }
    #     });

    #     //Launch instance in private VPC subnet 
    #     const demoInstance = new ec2.CfnInstance(this, "Demo Instance", {
    #       subnetId: privateVPC.isolatedSubnets[0].subnetId,
    #       imageId: latestLinuxAMI.getImage(this).imageId,
    #       instanceType: "t2.nano",
    #       iamInstanceProfile: new CfnInstanceProfile(this, "DemoEC2_InstanceProfile", {
    #         roles: [SSMRole.roleName]
    #       }).ref,
    #       tags: [{
    #         key: 'Name',
    #         value: "Demo instance"
    #       }],
    #       securityGroupIds: [ssmPrivateSG.securityGroupId] //The Security Group we created earlier, linked to private interface endpoints
    #     });
    #   }
    # }
