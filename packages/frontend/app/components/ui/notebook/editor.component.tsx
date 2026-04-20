import { useEffect } from "react";
import { useKeyboardShortcut } from "~/hooks/use-keyboard-shortcut.hook";
import { useProfileUpdateMutation } from "~/hooks/use-profile-update-mutation.hook";
import { useProfile } from "~/hooks/use-profiles.hook";
import { useEditorStore } from "~/stores/editor.store";
import { mapEditorBlockToProfileBlock } from "~/utils/blocks/map-editor-to-profile-block.util";
import type { ProfileTabData } from "~/utils/types/editor.types";
import { ProfileDatasetsSection } from "./sections/datasets/datasets-section.component";
import { ProfileJobsSection } from "./sections/jobs/jobs-section.component";
import { ProfileMetadataSection } from "./sections/metadata/metadata-section.component";
import { ProfileModelsSection } from "./sections/models/models-section.component";
import { ProfileWorkspaceSection } from "./sections/workspace/workspace-section.component";

type ProfileEditorProps = {
	tabId: string;
};

export function ProfileEditor({ tabId }: ProfileEditorProps) {
	const tab = useEditorStore((state) => state.tabs[tabId]);
	const initializeProfileBlocks = useEditorStore(
		(state) => state.initializeProfileBlocks,
	);

	const { data: profile } = useProfile(
		tab?.type === "profile" ? tab.data.profileId : null,
	);

	useEffect(() => {
		if (
			profile &&
			tab?.type === "profile" &&
			!(tab.data as ProfileTabData).profile
		) {
			initializeProfileBlocks(tabId, profile);
		}
	}, [profile, tabId, tab, initializeProfileBlocks]);

	const undo = useEditorStore((state) => state.undo);
	const redo = useEditorStore((state) => state.redo);

	const { mutate: updateProfile } = useProfileUpdateMutation();

	const handleSave = () => {
		console.log("Saving profile...");
		if (!profile || tab?.type !== "profile") {
			return;
		}

		const blocks = tab.data.blocks
			.map((block, index) =>
				mapEditorBlockToProfileBlock({
					block,
					profile,
					index,
				}),
			)
			.map((b) => ({
				id: b.id,
				profile_id: b.profileId,
				kind: b.kind,
				order_index: b.orderIndex,
				data: b.data,
				created_at: b.createdAt,
				updated_at: b.updatedAt,
			}));

		updateProfile({
			profileId: profile.id,
			data: {
				name: profile.name,
				description: profile.description,
				mode: profile.mode,
				blocks,
			},
		});
	};

	useKeyboardShortcut("z", undo);
	useKeyboardShortcut("y", redo);
	useKeyboardShortcut("s", handleSave);

	if (!tab || tab.type !== "profile" || !profile) {
		return null;
	}

	return (
		<div className="flex-1 h-full p-12 overflow-y-auto custom-scrollbar bg-background">
			<div className="space-y-4">
				<ProfileMetadataSection profile={profile} />
				<ProfileDatasetsSection datasets={profile.datasets} />
				<ProfileJobsSection
					profileId={profile.id}
					jobs={profile.jobs}
					datasets={profile.datasets}
				/>
				<ProfileModelsSection models={profile.models} jobs={profile.jobs} />
				<ProfileWorkspaceSection models={profile.models} />
			</div>

			<div className="h-64" />
		</div>
	);
}
