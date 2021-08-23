- Make sure the region for cli is same as the region teh vpc are being created. (in correct error message:  no permission to create TGW)
- Wait for TGW created before creting attachment.
- env should be passed to teh stacks as a paramater (optionals) but not explicit... This eliminate error about same environemnt for stacks...
- SSM access require the multiple VPC end points, includingssm, ec2 and s3
- THere is SSM connector to log in to linux Machines.... thisd can be isntalled on Windows machines and log on to any machine, the access can be easily revoked and all the commands they run can be logged in S3 and Sumo.

S3 bucket lifecycle.
  - https://blog.codecentric.de/en/2019/10/aws-cdk-part-2-s3-bucket/


SSO from Workspaces?
  - https://www.talkncloud.com/aws-temporary-creds-sso-cdk/

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

Pass env to the sub stack, use kwargs['env']
Only Stacks need env, not the constructs...

Pattern...

define a stage, 
in this stage define the components you need in that...
Ec2, RDS and S3 created as a stage

# Recommended AWS CDK project structure for Python applications
https://aws.amazon.com/blogs/developer/recommended-aws-cdk-project-structure-for-python-applications/

# Generate diagram
https://github.com/pistazie/cdk-dia

To up grade cdk, simply install only cdk-lib and constructs libraties, do not worry about teh incompatible versions.
Now update imports, remove core and use COnstructs 