import type { StreamedFile } from "~b/utils/stream.util.js";
import { createDatasetValidator } from "~shared/datasets.validator.js";

export const createDatasetRequestValidator = {
    body: createDatasetValidator,
};

export type CreateDatasetRequestValidator =
    typeof createDatasetRequestValidator;

export type CreateDatasetContext = {
    files: {
        dataset: StreamedFile;
    };
};
