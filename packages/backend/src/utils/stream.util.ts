import { Readable } from "node:stream";
import type { BodyDataTypes } from "@aws-sdk/lib-storage";
import type { Middleware } from "./middleware.util.js";

export type StreamedFile = {
    stream: BodyDataTypes;
    mimeType: string;
    originalName: string;
    size?: number;
};

type FileContext<T> = {
    files: T;
};

export class MissingRequiredFileError extends Error {
    public constructor(fileField: string) {
        super(`Missing required file: ${fileField}`);
        this.name = "MissingRequiredFileError";
    }
}

export class InvalidMimeTypeError extends Error {
    public constructor(
        fileField: string,
        expectedTypes: string[],
        actualType: string,
    ) {
        super(
            `Invalid MIME type for file ${fileField}: expected one of [${expectedTypes.join(
                ", ",
            )}], but got ${actualType}`,
        );
        this.name = "InvalidMimeTypeError";
    }
}

export function streamFiles<T extends Record<string, StreamedFile>>(
    rules: {
        [K in keyof T]: {
            required?: boolean;
            mimeTypes?: string[];
        };
    },
): Middleware<Record<string, unknown>, { context: FileContext<T> }> {
    return async (_, req) => {
        const multerFiles = req.files as
            | Record<string, Express.Multer.File[]>
            | undefined;

        const files: Partial<Record<keyof T, StreamedFile>> = {};

        for (const field in rules) {
            const rule = rules[field];
            const fileArray = multerFiles?.[field];

            const file = fileArray?.[0];

            if (rule.required && !file) {
                throw new MissingRequiredFileError(field);
            }

            if (!file) {
                continue;
            }

            if (rule.mimeTypes && !rule.mimeTypes.includes(file.mimetype)) {
                throw new InvalidMimeTypeError(
                    field,
                    rule.mimeTypes,
                    file.mimetype,
                );
            }

            files[field] = {
                stream: Readable.from(file.buffer),
                mimeType: file.mimetype,
                originalName: file.originalname,
                size: file.size,
            };
        }

        return { context: { files: files as T } };
    };
}
