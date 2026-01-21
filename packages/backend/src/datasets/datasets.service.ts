import type { CreateDatasetData } from "@spectrum/shared";
import type { PrismaClient } from "~prisma/client.js";
import type { DatasetWhereInput } from "~prisma/models.js";

type DatasetsServiceDependencies = {
    prisma: PrismaClient;
};

export class DatasetsService {
    public constructor(private readonly _deps: DatasetsServiceDependencies) {}

    public async getAll(where: DatasetWhereInput) {
        return this._deps.prisma.dataset.findMany({ where });
    }

    public async create(data: CreateDatasetData & { fileUrl: string }) {
        return this._deps.prisma.dataset.create({
            data: {
                title: data.title,
                fileUrl: data.fileUrl,
            },
        });
    }
}
