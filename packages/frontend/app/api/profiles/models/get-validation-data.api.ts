import Papa from "papaparse";

/**
 * Fetches and parses validation results from the storage API.
 */
export async function getValidationData<T extends unknown[]>(
	validationPath: string,
): Promise<T> {
	const baseUrl =
		import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";
	const url = `${baseUrl}/storage/download/${validationPath}`;

	const response = await fetch(url);
	if (!response.ok) {
		throw new Error(`Failed to fetch validation data: ${response.statusText}`);
	}

	const csvText = await response.text();

	return new Promise((resolve, reject) => {
		Papa.parse(csvText, {
			header: true,
			dynamicTyping: true,
			skipEmptyLines: true,
			complete: (results) => resolve(results.data as T),
			error: (error: unknown) => reject(error),
		});
	});
}
