import { RemovalPolicy, Stack, type StackProps } from "aws-cdk-lib";
import * as s3 from "aws-cdk-lib/aws-s3";
import type { Construct } from "constructs";

export class StorageStack extends Stack {
    public readonly datasetBucket: s3.Bucket;

    public constructor(scope: Construct, id: string, props?: StackProps) {
        super(scope, id, props);

        this.datasetBucket = new s3.Bucket(this, "DatasetBucket", {
            bucketName: "datasets",
            versioned: true,
            blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
            removalPolicy: RemovalPolicy.RETAIN,
        });
    }
}
