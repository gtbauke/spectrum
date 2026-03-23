import { z } from "zod";
import { safeApiRequest } from "~/api/fetch.api";
import { jobSchema } from "~/schemas/domain/job.schema";
import type { CreateJobDto } from "~/schemas/dtos/job.dto";

export async function createJobs(profileId: string, jobs: CreateJobDto[]) {
	const response = await safeApiRequest(
		`/profiles/${profileId}/jobs`,
		z.array(jobSchema),
		{
			method: "POST",
			body: JSON.stringify(jobs),
		},
	);

	return z.array(jobSchema).safeParse(response);
}
