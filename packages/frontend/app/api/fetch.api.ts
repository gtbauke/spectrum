import { z } from "zod";

const BASE_URL =
	import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

let isRefreshing = false;
let failedQueue: Array<{
	resolve: (token: string) => void;
	reject: (err: unknown) => void;
}> = [];

const processQueue = (error: Error | null, token: string | null = null) => {
	failedQueue.forEach((prom) => {
		if (error) prom.reject(error);
		else prom.resolve(token as string);
	});
	failedQueue = [];
};

export async function safeApiRequest<T extends z.ZodType>(
	endpoint: string,
	responseSchema: T,
	options: RequestInit = {},
	_isRetry = false,
): Promise<z.infer<T>> {
	const response = await apiRequest(endpoint, options, _isRetry);

	const validationResponse = responseSchema.safeParse(response);
	if (!validationResponse.success) {
		const issues = z.treeifyError(validationResponse.error);
		console.error("API response validation failed", issues);

		throw new Error("API response validation failed");
	}

	return validationResponse.data;
}

export async function apiRequest<T>(
	endpoint: string,
	options: RequestInit = {},
	_isRetry = false,
): Promise<T> {
	const headers = new Headers(options.headers);

	if (options.body instanceof FormData) {
		headers.delete("Content-Type");
	} else {
		if (!headers.has("Content-Type")) {
			headers.set("Content-Type", "application/json");
		}
	}

	const response = await fetch(`${BASE_URL}${endpoint}`, {
		...options,
		credentials: "include",
		headers,
	});

	if (response.status === 401 && !_isRetry) {
		if (isRefreshing) {
			return new Promise<void>((resolve, reject) => {
				failedQueue.push({ resolve: () => resolve(), reject });
			})
				.then(() => {
					return apiRequest<T>(endpoint, options, true);
				})
				.catch((err) => {
					return Promise.reject(err);
				});
		}

		isRefreshing = true;

		try {
			const refreshRes = await fetch(`${BASE_URL}/auth/refresh`, {
				method: "POST",
				credentials: "include",
			});

			if (!refreshRes.ok) {
				throw new Error("Refresh failed");
			}

			isRefreshing = false;
			processQueue(null);

			return apiRequest<T>(endpoint, options, true);
		} catch (e) {
			isRefreshing = false;
			processQueue(e as Error, null);

			if (window.location.pathname !== "/login") {
				window.location.href = "/login";
			}
			throw new Error("Session expired. Please log in again.");
		}
	}

	if (!response.ok) {
		const errorData = await response.json().catch(() => ({}));

		if (Array.isArray(errorData.detail)) {
			const messages = errorData.detail.map(
				(e: any) => `${e.loc.join(".")}: ${e.msg}`,
			);
			throw new Error(messages.join(", "));
		}

		throw new Error(
			errorData.detail || errorData.message || "API request failed",
		);
	}

	return response.json();
}
