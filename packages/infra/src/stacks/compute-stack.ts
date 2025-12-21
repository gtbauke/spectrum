import { Stack, type StackProps } from "aws-cdk-lib";
import * as ec2 from "aws-cdk-lib/aws-ec2";
import * as iam from "aws-cdk-lib/aws-iam";
import type * as s3 from "aws-cdk-lib/aws-s3";
import type * as sns from "aws-cdk-lib/aws-sns";
import type { Construct } from "constructs";

interface ComputeStackProps extends StackProps {
    bucket: s3.IBucket;
    datasetUploadedTopic: sns.ITopic;
}

export class ComputeStack extends Stack {
    public constructor(scope: Construct, id: string, props: ComputeStackProps) {
        super(scope, id, props);

        const vpc = new ec2.Vpc(this, "Vpc", {
            maxAzs: 2,
        });

        const role = new iam.Role(this, "ServerRole", {
            assumedBy: new iam.ServicePrincipal("ec2.amazonaws.com"),
        });

        props.bucket.grantReadWrite(role);
        props.datasetUploadedTopic.grantPublish(role);

        const instance = new ec2.Instance(this, "ServerInstance", {
            vpc,
            instanceType: ec2.InstanceType.of(
                ec2.InstanceClass.T3,
                ec2.InstanceSize.MICRO,
            ),
            machineImage: ec2.MachineImage.latestAmazonLinux2(),
            role,
        });

        instance.addUserData(
            `#!/bin/bash
            export DATASET_BUCKET=${props.bucket.bucketName}
            export DATASET_UPLOADED_TOPIC_ARN=${props.datasetUploadedTopic.topicArn}
            `,
        );
    }
}
