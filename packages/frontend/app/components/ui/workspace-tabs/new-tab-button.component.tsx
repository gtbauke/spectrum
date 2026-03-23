import { Plus } from "lucide-react";
import { useEditorStore } from "~/stores/editor.store";

export function NewTabButton() {
	const openTab = useEditorStore((state) => state.openTab);
	const setActiveTab = useEditorStore((state) => state.setActiveTab);

	const handleOpenTab = () => {
		const profileId = crypto.randomUUID();

		setActiveTab(profileId);
		openTab({
			type: "profile",
			id: profileId,
			data: {
				tabId: profileId,
				profileId,
				versionId: profileId,
				blocks: [],
				past: [],
				future: [],
				isDirty: true,
				activeBlockId: null,
				profile: {
					id: profileId,
					name: "Untitled Profile",
					description: "",
					ownerId: "", 
					mode: "draft",
					datasets: [],
					jobs: [],
					models: [],
					blocks: [],
					createdAt: new Date(),
					updatedAt: new Date(),
				}
			},
		});
	};

	return (
		<button
			type="button"
			className="px-3 h-full text-gray-400 hover:text-white hover:bg-white/5 transition cursor-pointer"
			onClick={handleOpenTab}
		>
			<Plus size={20} />
		</button>
	);
}
