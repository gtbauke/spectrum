import { z } from "zod";

export const datasetValidator = z.object({
    id: z.cuid(),

    title: z.string(),
    fileUrl: z.url(),

    createdAt: z.date(),
    updatedAt: z.date(),
});

export const createDatasetValidator = datasetValidator.pick({
    title: true,
    fileUrl: true,
});

export type CreateDatasetData = z.infer<typeof createDatasetValidator>;
