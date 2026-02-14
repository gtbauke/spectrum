import type { z } from "zod";

export const API_BASE_URL = "http://localhost:8000/api/v1";

export async function apiRequest<
	TSchema extends z.ZodType,
	TBody extends Record<string, unknown> | FormData = Record<string, unknown>,
>(
	url: string,
	method: "GET" | "POST" | "PUT" | "DELETE",
	responseSchema?: TSchema,
	body?: TBody,
): Promise<z.infer<TSchema>> {
	const response = await fetch(`${API_BASE_URL}${url}`, {
		method,
		body: body
			? body instanceof FormData
				? body
				: JSON.stringify(body)
			: undefined,
	});

	const responseData = await response.json();
	console.log("API Response:", responseData);

	if (!response.ok) {
		throw new Error(responseData.message || "API request failed");
	}

	if (responseSchema) {
		const parsedData = responseSchema.safeParse(responseData);

		if (!parsedData.success) {
			console.error("Response validation errors:", parsedData.error.issues);
			throw new Error("Response validation failed");
		}

		return parsedData.data;
	}

	return responseData;
}
