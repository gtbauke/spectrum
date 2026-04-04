import { File } from "lucide-react";
import type { Artifact } from "~/schemas/domain/dataset.schema";
import { capitalize } from "~/utils/capitalize.util";
import { cn } from "~/utils/classname.util";
import { formatBytes } from "~/utils/format-bytes.util";

type ArtifactItemProps = {
	artifact: Artifact;
};

export function ArtifactItem({ artifact }: ArtifactItemProps) {
	return (
		<div className="border border-border rounded-md p-2 col-span-1 only:col-span-full">
			<div className="flex items-center space-x-2">
				<File
					size={16}
					className={cn(
						artifact.role === "data"
							? "text-primary-500"
							: "text-secondary-500",
					)}
				/>
				<div className="flex-1 flex items-center justify-between">
					<span
						className={cn(
							"text-sm",
							artifact.role === "data"
								? "text-primary-500"
								: "text-secondary-500",
						)}
					>
						{capitalize(artifact.role)}
					</span>

					<span className="text-xs text-gray-500">
						{formatBytes(artifact.sizeInBytes)}
					</span>
				</div>
			</div>
		</div>
	);
}
