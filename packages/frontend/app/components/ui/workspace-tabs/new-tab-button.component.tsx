import { Plus } from "lucide-react";
import { useProfileTabs } from "~/contexts/profile-tabs.context";

export function NewTabButton() {
	const { openTab } = useProfileTabs();

	// TODO: handle the creation of new profiles
	const handleOpenTab = () => {
		const profileId = crypto.randomUUID();

		openTab({
			type: "profile",
			id: profileId,
			name: "New Tab",
			isDirty: true,
			profileId,
			profileVersion: {
				profile_id: profileId,
				is_latest: true,
				version: 1,
				id: crypto.randomUUID(),
				name: "New Tab",
				timestamp: new Date().toISOString(),
				visibility: "public",
				status: "active",
				datasets: [],
				blocks: [],
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
