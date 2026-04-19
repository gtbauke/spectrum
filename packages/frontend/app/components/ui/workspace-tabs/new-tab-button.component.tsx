import { Plus } from "lucide-react";
import { useNewProfile } from "~/hooks/use-new-profile.hook";

export function NewTabButton() {
	const { openNewProfile } = useNewProfile();

	return (
		<button
			type="button"
			className="px-3 h-full text-gray-400 hover:text-white hover:bg-white/5 transition cursor-pointer"
			onClick={openNewProfile}
		>
			<Plus size={20} />
		</button>
	);
}
