import { FaPlay } from "react-icons/fa";
import { getAllJobsForDataset } from "~/api/get-all-jobs.api";
import { MainContainer } from "~/components/layout/main.component";
import type { Route } from "./+types/dataset-info";

export async function clientLoader({
	params: { datasetId },
}: Route.ClientLoaderArgs) {
	const response = await getAllJobsForDataset(datasetId);
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
				<h1 className="text-2xl font-bold mb-4">Jobs for {params.datasetId}</h1>

				<ul className="container mx-auto grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
					{loaderData.map((job) => (
						<li key={job.id} className="border p-4 rounded shadow space-y-4">
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
		</MainContainer>
	);
}
