import Papa from "papaparse";

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

/**
 * Fetches and parses validation results from the storage API.
 * First resolves the download URL, then fetches the file content.
 */
export async function getValidationData<T extends unknown[]>(
	validationPath: string,
): Promise<T> {
	const downloadEndpoint = `${BASE_URL}/storage/download/${validationPath}`;

	const urlResponse = await fetch(downloadEndpoint);
	if (!urlResponse.ok) {
		throw new Error(
			`Failed to resolve download URL: ${urlResponse.statusText}`,
		);
	}

	const { url } = (await urlResponse.json()) as { url: string };

	const fileResponse = await fetch(url);
	if (!fileResponse.ok) {
		throw new Error(
			`Failed to fetch validation data: ${fileResponse.statusText}`,
		);
	}

	const csvText = await fileResponse.text();

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
