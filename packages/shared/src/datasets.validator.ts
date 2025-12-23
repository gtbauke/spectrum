import { z } from "zod";

export const datasetValidator = z.object({
    id: z.cuid({
        error: "Id must be a valid CUID",
    }),

    title: z
        .string({
            error: "Title must be a string",
        })
        .min(1, {
            error: "Title is required",
        }),
    description: z.string({
        error: "Description must be a string",
    }),

    fileUrl: z.url({
        error: "File URL must be a valid URL",
    }),

    createdAt: z.date(),
    updatedAt: z.date(),
});

export const createDatasetValidator = datasetValidator.pick({
    title: true,
    description: true,
});

export type CreateDatasetData = z.infer<typeof createDatasetValidator>;
