import { FileUploadProvider } from "./file-upload.context";
import UploadDatasetTabContent from "./upload-tab.component";

export function UploadTabContainer() {
	return (
		<FileUploadProvider>
			<UploadDatasetTabContent />
		</FileUploadProvider>
	);
}
