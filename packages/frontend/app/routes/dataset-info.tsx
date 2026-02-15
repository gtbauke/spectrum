import { useNavigate } from "react-router";
import { getDataset } from "~/api/get-dataset.api";
import { MainContainer } from "~/components/layout/main.component";
import { DatasetInfoHeader } from "~/components/sections/datasets-info/dataset-info-header.component";
import { DatasetMetadata } from "~/components/sections/datasets-info/dataset-metadata.component";
import { DatasetModels } from "~/components/sections/datasets-info/dataset-models.component";
import type { Job } from "~/schemas/job.schema";
import type { Route } from "./+types/dataset-info";

export async function clientLoader({
	params: { datasetId },
}: Route.ClientLoaderArgs) {
	const response = await getDataset(datasetId);
	return response;
}

export function HydrateFallback() {
	return (
		<MainContainer>
			<h1>Loading jobs...</h1>
		</MainContainer>
	);
}

// TODO: add preview of dataset data
export default function JobsScreen({ loaderData }: Route.ComponentProps) {
	const navigate = useNavigate();

	const handleEnterPlayground = (job: Job) => {
		const sortedModels = job.models.sort(
			(a, b) => b.created_at.getTime() - a.created_at.getTime(),
		);

		const modelId = sortedModels[0]?.id;
		navigate(`/playground/${modelId}`);
	};

	const handleEditJob = (job: Job) => {
		navigate(`/datasets/${job.dataset_id}/jobs/${job.id}/edit`);
	};

	return (
		<MainContainer>
			<div className="space-y-6">
				<DatasetInfoHeader name={loaderData.name} id={loaderData.id} />
				<DatasetMetadata metadata={loaderData.dataset_metadata} />
				<DatasetModels models={loaderData.models} />

				{/* <Section title="Models">
					<ul className="container mx-auto gap-4">
						{loaderData.jobs.map((job) => (
							<li
								key={job.id}
								className="border p-4 rounded shadow space-y-4 border-gray-800 w-full"
							>
								<header className="flex items-center justify-between">
									<button
										type="button"
										className="text-green-500 hover:text-green-700 active:text-green-800 cursor-pointer flex items-center space-x-1"
										onClick={() => handleEnterPlayground(job)}
									>
										<p>Enter playground</p>
										<FaPlay size={12} />
									</button>

									<div className="flex space-x-4">
										<button
											type="button"
											className="text-red-500 hover:text-red-700 active:text-red-800 cursor-pointer"
										>
											<FaTrash size={12} />
										</button>

										<button
											type="button"
											className="text-blue-500 hover:text-blue-700 active:text-blue-800 cursor-pointer"
											onClick={() => handleEditJob(job)}
										>
											<FaPencilAlt size={12} />
										</button>

										<button
											type="button"
											className="text-green-500 hover:text-green-700 active:text-green-800 cursor-pointer"
										>
											<FaUndo size={12} />
										</button>
									</div>
								</header>

								<div>
									<p>Status: {job.status}</p>
									<p>Created At: {job.created_at.toLocaleDateString()}</p>
								</div>

								<h2 className="text-xs text-gray-500">{job.id}</h2>
							</li>
						))}
					</ul>
				</Section> */}
			</div>
		</MainContainer>
	);
}
