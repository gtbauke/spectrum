import { useForm } from "react-hook-form";
import { getJob } from "~/api/get-job.api";
import { MainContainer } from "~/components/layout/main.component";
import type { Route } from "./+types/edit-job";

type EditJobFormData = {};

export async function clientLoader({ params }: Route.ClientLoaderArgs) {
	const response = await getJob(params.datasetId, params.jobId);
	return { job: response };
}

export default function EditJobScreen({ loaderData }: Route.ComponentProps) {
	const { register, handleSubmit, reset } = useForm<EditJobFormData>({
		defaultValues: {},
	});

	const onSubmit = (data: EditJobFormData) => {};

	return (
		<MainContainer>
			<div className="space-y-6">
				<header className="space-y-1">
					<h1 className="text-2xl font-bold">Editing Job</h1>
					<p className="text-xs text-gray-600">{loaderData.job.id}</p>
				</header>

				<div className="border p-4 rounded shadow space-y-4 border-gray-800">
					<h2 className="text-lg font-semibold">Job Properties</h2>

					<form onSubmit={handleSubmit(onSubmit)} className="space-y-4"></form>
				</div>
			</div>
		</MainContainer>
	);
}
