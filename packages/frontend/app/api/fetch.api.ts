const BASE_URL = "http://localhost:8000/api/v1"; // TODO: pull from environment variables

export async function apiRequest<T>(
	endpoint: string,
	options: RequestInit = {},
): Promise<T> {
	const token = localStorage.getItem("token");

	const response = await fetch(`${BASE_URL}${endpoint}`, {
		...options,
		headers: {
			"Content-Type": "application/json",
			...(token ? { Authorization: `Bearer ${token}` } : {}),
			...options.headers,
		},
	});

	if (!response.ok) {
		const errorData = await response.json();
		console.error(errorData);

		throw new Error(errorData.message || "API request failed");
	}

	return response.json();
}
