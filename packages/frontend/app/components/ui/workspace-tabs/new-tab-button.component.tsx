import { Plus } from "lucide-react";
import { useEditorStore } from "~/stores/editor.store";

export function NewTabButton() {
	const openTab = useEditorStore((state) => state.openTab);
	const setActiveTab = useEditorStore((state) => state.setActiveTab);

	// TODO: handle the creation of new profiles
	const handleOpenTab = () => {
		const profileId = crypto.randomUUID();

		setActiveTab(profileId);
		openTab({
			type: "profile",
			id: profileId,
			data: {
				name: "Untitled Profile",
				description: null,
				isDirty: true,
				profileId,
				versionId: crypto.randomUUID(),
				blocks: [],
				past: [],
				future: [],
				activeBlockId: null,
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
