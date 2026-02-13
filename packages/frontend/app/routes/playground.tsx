import { useEffect, useRef } from "react";
import { useForm } from "react-hook-form";
import { API_BASE_URL } from "~/api/base.api";
import { getModel } from "~/api/get-model.api";
import { MainContainer } from "~/components/layout/main.component";
import { FormTextArea } from "~/components/ui/forms/form-textarea.component";
import type { Route } from "./+types/playground";

type PlaygroundFormData = {
	query: string;
};

export async function loader({ params }: Route.LoaderArgs) {
	const model = await getModel(params.modelId);
	return { model };
}

export default function PlaygroundScreen({
	params,
	loaderData,
}: Route.ComponentProps) {
	const { model } = loaderData;
	const socketRef = useRef<WebSocket | null>(null);

	useEffect(() => {
		const connectionUrl = `${API_BASE_URL}/inference/${params.modelId}/ws`;
		const socket = new WebSocket(connectionUrl);
		socketRef.current = socket;

		socket.onopen = () => {
			console.log("WebSocket connection established");
		};

		socket.onmessage = (event) => {
			console.log("Received message:", event.data);
		};

		socket.onerror = (error) => {
			console.error("WebSocket error:", error);
		};

		socket.onclose = () => {
			console.log("WebSocket connection closed");
		};

		return () => {
			socket.close();
		};
	}, [params.modelId]);

	const { formState, reset, register, handleSubmit } =
		useForm<PlaygroundFormData>({
			defaultValues: {
				query: "",
			},
		});

	const onCancel = () => {
		reset();
	};

	const onSubmit = (data: PlaygroundFormData) => {
		console.log("Query submitted:", data);

		if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
			socketRef.current.send(JSON.stringify(data));
			return;
		}

		console.error("WebSocket is not open. Unable to send query.");
	};

	return (
		<MainContainer>
			<div className="space-y-6">
				<header>
					<h1 className="text-2xl font-bold">Playground</h1>
					<p className="text-sm text-gray-600">Model ID: {params.modelId}</p>
				</header>

				<div className="border p-4 rounded shadow space-y-4 border-gray-800">
					<form
						className="flex flex-col gap-4"
						onSubmit={handleSubmit(onSubmit)}
					>
						{/* TODO: use real rich text editor */}
						<FormTextArea
							label="Query"
							{...register("query")}
							className="min-h-72"
							placeholder="SELECT expressions FROM TOP 10"
						/>

						<div className="flex flex-col gap-2">
							<input
								type="submit"
								value="Continue"
								className="cursor-pointer p-2 bg-green-600 hover:bg-green-700 active:bg-green-800 rounded-sm font-bold disabled:cursor-not-allowed disabled:bg-gray-600 disabled:hover:bg-gray-600 disabled:active:bg-gray-600"
								disabled={
									socketRef.current?.readyState !== WebSocket.OPEN ||
									formState.isSubmitting
								}
							/>

							<input
								type="reset"
								value="Cancel"
								className="cursor-pointer p-2 bg-red-600 hover:bg-red-700 active:bg-red-800 rounded-sm font-bold"
								onClick={onCancel}
							/>
						</div>
					</form>
				</div>

				<div className="border p-4 rounded shadow space-y-4 border-gray-800">
					<h2 className="text-xl font-bold">Query Response</h2>
				</div>
			</div>
		</MainContainer>
	);
}
