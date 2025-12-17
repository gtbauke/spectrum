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
}
