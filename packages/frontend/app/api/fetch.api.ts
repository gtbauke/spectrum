// TODO: pull from env
const BASE_URL = "http://localhost:8000/api/v1";

let isRefreshing = false;
let failedQueue: Array<{
	resolve: (token: string) => void;
	reject: (err: any) => void;
}> = [];

const processQueue = (error: Error | null, token: string | null = null) => {
	failedQueue.forEach((prom) => {
		if (error) prom.reject(error);
		else prom.resolve(token as string);
	});
	failedQueue = [];
};

export async function apiRequest<T>(
	endpoint: string,
	options: RequestInit = {},
	_isRetry = false,
): Promise<T> {
	const token = localStorage.getItem("access_token");
	const headers = new Headers(options.headers);

	if (token) {
		headers.set("Authorization", `Bearer ${token}`);
	}

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
			return new Promise<string>((resolve, reject) => {
				failedQueue.push({ resolve, reject });
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

			const refreshData = await refreshRes.json();
			const newToken = refreshData.access_token || refreshData.accessToken;

			if (!newToken) {
				throw new Error("No token returned");
			}

			localStorage.setItem("access_token", newToken);

			isRefreshing = false;
			processQueue(null, newToken);

			return apiRequest<T>(endpoint, options, true);
		} catch (e) {
			isRefreshing = false;
			processQueue(e as Error, null);

			localStorage.removeItem("access_token");
			window.location.href = "/login";
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
