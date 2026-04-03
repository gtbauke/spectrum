import {
	createContext,
	type PropsWithChildren,
	useContext,
	useState,
} from "react";
import type { ArtifactRole } from "../../../schemas/domain/enums.schema";

type UploadedFile = {
	name: string;
	file: File;
	error?: string;
	columns?: string[];
	isParsing: boolean;
	previewData?: unknown[];
	datasetRole?: ArtifactRole;
};

type FileUploadContextType = {
	files: Record<string, UploadedFile>;
	selectedFileName: string | null;

	addFile: (file: File) => void;
	addFiles: (files: File[]) => void;
	removeFile: (fileName: string) => void;

	setErrors: (errors: Record<string, string>) => void;
	setError: (fileName: string, error: string) => void;

	updateFile: (
		fileName: string,
		updates: Partial<Omit<UploadedFile, "file" | "name">>,
	) => void;

	reset: () => void;

	selectFile: (fileName: string) => void;
	deselectFile: () => void;
};

export const FileUploadContext = createContext<FileUploadContextType | null>(
	null,
);

export function FileUploadProvider({ children }: PropsWithChildren) {
	const [files, setFiles] = useState<Record<string, UploadedFile>>({});
	const [selectedFileName, setSelectedFileName] = useState<string | null>(null);

	const addFile = (file: File) => {
		setFiles((prev) => ({
			...prev,
			[file.name]: { name: file.name, file, isParsing: false },
		}));
	};

	const addFiles = (files: File[]) => {
		setFiles((prev) => {
			const newFiles = { ...prev };

			files.forEach((file) => {
				newFiles[file.name] = { name: file.name, file, isParsing: false };
			});

			return newFiles;
		});

		setSelectedFileName(files[0].name);
	};

	const removeFile = (fileName: string) => {
		setFiles((prev) => {
			const newFiles = { ...prev };
			delete newFiles[fileName];

			return newFiles;
		});
	};

	const setErrors = (errors: Record<string, string>) => {
		setFiles((prev) => {
			const newFiles = { ...prev };

			for (const fileName in errors) {
				if (newFiles[fileName]) {
					newFiles[fileName].error = errors[fileName];
				}
			}

			return newFiles;
		});
	};

	const setError = (fileName: string, error: string) => {
		setFiles((prev) => {
			const newFiles = { ...prev };

			if (newFiles[fileName]) {
				newFiles[fileName].error = error;
			}

			return newFiles;
		});
	};

	const updateFile = (
		fileName: string,
		updates: Partial<Omit<UploadedFile, "file" | "name">>,
	) => {
		setFiles((prev) => {
			const newFiles = { ...prev };

			if (newFiles[fileName]) {
				newFiles[fileName] = { ...newFiles[fileName], ...updates };
			}

			return newFiles;
		});
	};

	const reset = () => {
		setFiles({});
	};

	return (
		<FileUploadContext.Provider
			value={{
				files,
				addFile,
				addFiles,
				removeFile,
				setErrors,
				setError,
				updateFile,
				reset,
				selectedFileName,
				selectFile: (fileName: string) => setSelectedFileName(fileName),
				deselectFile: () => setSelectedFileName(null),
			}}
		>
			{children}
		</FileUploadContext.Provider>
	);
}

export function useFileUpload() {
	const context = useContext(FileUploadContext);

	if (!context) {
		throw new Error("useFileUpload must be used within a FileUploadProvider");
	}

	return context;
}
