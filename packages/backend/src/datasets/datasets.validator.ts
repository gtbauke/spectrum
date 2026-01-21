import { createDatasetValidator } from "@spectrum/shared";
import type { StreamedFile } from "~/utils/stream.util.js";

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
