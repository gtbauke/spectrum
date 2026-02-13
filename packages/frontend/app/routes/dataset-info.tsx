import { FaPencilAlt, FaPlay, FaTrash } from "react-icons/fa";
import { getDataset } from "~/api/get-dataset.api";
import { MainContainer } from "~/components/layout/main.component";
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

export default function JobsScreen({
	params,
	loaderData,
}: Route.ComponentProps) {
	return (
		<MainContainer>
			<div className="space-y-6">
				<header>
					<div className="flex items-center justify-between">
						<h1 className="text-2xl font-bold">{loaderData.name}</h1>
						<div className="flex space-x-2 mt-2">
							<button
								type="button"
								className="text-red-500 hover:text-red-700 active:text-red-800 cursor-pointer"
							>
								<FaTrash size={16} />
							</button>

							<button
								type="button"
								className="text-blue-500 hover:text-blue-700 active:text-blue-800 cursor-pointer"
							>
								<FaPencilAlt size={16} />
							</button>
						</div>
					</div>
					<p className="text-xs text-gray-600">{loaderData.id}</p>
				</header>

				<div className="border p-4 rounded shadow space-y-4 border-gray-800">
					<h2 className="text-xl font-bold">Dataset Metadata</h2>
					{loaderData.dataset_metadata ? (
						<div>
							<p>Rows: {loaderData.dataset_metadata.num_rows}</p>
							<p>Features: {loaderData.dataset_metadata.num_features}</p>
							<p>
								Processing Attempts:{" "}
								{loaderData.dataset_metadata.processing_attempts}
							</p>
							{loaderData.dataset_metadata.last_processing_error && (
								<p className="text-red-500">
									Last Error:{" "}
									{loaderData.dataset_metadata.last_processing_error}
								</p>
							)}
						</div>
					) : (
						<p className="text-gray-500">No metadata available.</p>
					)}
				</div>

				<div className="border p-4 rounded shadow space-y-4 border-gray-800">
					<h2 className="text-xl font-bold">Jobs</h2>
					<ul className="container mx-auto gap-4">
						{loaderData.jobs.map((job) => (
							<li
								key={job.id}
								className="border p-4 rounded shadow space-y-4 border-gray-800 w-full"
							>
								<header>
									<button
										type="button"
										className="text-green-500 hover:text-green-700 active:text-green-800 cursor-pointer flex items-center space-x-1"
									>
										<p>Enter playground</p>
										<FaPlay size={12} />
									</button>
								</header>

								<div>
									<p>Status: {job.status}</p>
									<p>Created At: {job.created_at.toLocaleDateString()}</p>
								</div>

								<h2 className="text-xs text-gray-500">{job.id}</h2>
							</li>
						))}
					</ul>
				</div>
			</div>
		</MainContainer>
	);
}
