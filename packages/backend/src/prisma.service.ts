import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "~prisma/client.js";
import { ROOT_ENV } from "~utils/root-env.util.js";

const adapter = new PrismaPg({ connectionString: ROOT_ENV.DATABASE_URL });
const prisma = new PrismaClient({ adapter });

export { prisma };
