import { Stack, type StackProps } from "aws-cdk-lib";
import * as sns from "aws-cdk-lib/aws-sns";
import type { Construct } from "constructs";

export class EventsStack extends Stack {
    public readonly datasetUploadedTopic: sns.Topic;

    public constructor(scope: Construct, id: string, props?: StackProps) {
        super(scope, id, props);

        this.datasetUploadedTopic = new sns.Topic(
            this,
            "DatasetUploadedTopic",
            {
                topicName: "DatasetUploadedTopic",
                displayName: "Topic for dataset uploaded events",
            },
        );
    }
}
