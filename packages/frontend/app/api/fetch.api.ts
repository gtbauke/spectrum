//TODO: pull from env
const BASE_URL = "http://localhost:8000/api/v1";

export async function apiRequest<T>(
	endpoint: string,
	options: RequestInit = {},
	_isRetry = false,
): Promise<T> {
	const token = localStorage.getItem("access_token");

	const response = await fetch(`${BASE_URL}${endpoint}`, {
		...options,
		credentials: "include",
		headers: {
			"Content-Type": "application/json",
			...(token ? { Authorization: `Bearer ${token}` } : {}),
			...options.headers,
		},
	});

	if (response.status === 401 && !_isRetry) {
		try {
			const refreshRes = await fetch(`${BASE_URL}/auth/refresh`, {
				method: "POST",
				credentials: "include",
			});

			if (refreshRes.ok) {
				const { accessToken } = await refreshRes.json();
				localStorage.setItem("access_token", accessToken);

				return apiRequest<T>(endpoint, options, true);
			}
		} catch (e) {
			console.error("Refresh failed", e);
		}

		localStorage.removeItem("access_token");
		window.location.href = "/login";
		throw new Error("Session expired");
	}

	if (!response.ok) {
		const errorData = await response.json().catch(() => ({}));
		throw new Error(errorData.message || "API request failed");
	}

	return response.json();
}
