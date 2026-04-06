import { useQuery } from "@tanstack/react-query";
import { getValidationData } from "~/api/profiles/models/get-validation-data.api";

export type UseModelValidationOptions = {
	modelId: string;
	validationPath?: string | null;
};

export function useModelValidation<T extends unknown[]>({
	modelId,
	validationPath,
}: UseModelValidationOptions) {
	return useQuery({
		queryKey: ["model-validation", modelId, validationPath] as const,
		queryFn: () => {
			if (!validationPath) {
				return Promise.resolve([] as unknown as T);
			}

			return getValidationData<T>(validationPath);
		},
		enabled: !!validationPath,
		staleTime: 1000 * 60 * 5,
	});
}
