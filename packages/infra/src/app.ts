import "dotenv/config";

import { App } from "aws-cdk-lib";
import { ComputeStack } from "./stacks/compute-stack.js";
import { EventsStack } from "./stacks/events-stack.js";
import { StorageStack } from "./stacks/storage-stack.js";

const app = new App();
const env = {
    // @ts-expect-error
    account: process.env.CDK_DEFAULT_ACCOUNT,
    // @ts-expect-error
    region: process.env.CDK_DEFAULT_REGION,
};

const storage = new StorageStack(app, "StorageStack", { env });
const events = new EventsStack(app, "EventsStack", { env });

new ComputeStack(app, "ComputeStack", {
    env,
    bucket: storage.datasetBucket,
    datasetUploadedTopic: events.datasetUploadedTopic,
});
