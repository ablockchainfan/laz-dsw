import setuptools

with open("README.md") as fp:
    long_description = fp.read()


# def __read_cdk_version() -> str:
#     f = open('cdk.version')
#     return f.read()


# CDK_VERSION = __read_cdk_version()

setuptools.setup(
    name="laz-dsw",
    version="0.0.1",

    description="A sample CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    install_requires=[
     "aws-cdk-lib>=2.0.0rc1",
     "constructs>=10.0.0",
     "python-benedict==0.22.4"
    ],
    # install_requires=[
    #     "aws-cdk.core==" + CDK_VERSION,
    #     "aws-cdk.aws-ec2==" + CDK_VERSION,
    #     "aws-cdk.aws-eks==" + CDK_VERSION,
    #     "aws-cdk.aws-elasticsearch==" + CDK_VERSION,
    #     "aws-cdk.aws-rds==" + CDK_VERSION,
    #     "aws_cdk.pipelines==" + CDK_VERSION,
    #     "python-benedict==0.22.4"
    # ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
