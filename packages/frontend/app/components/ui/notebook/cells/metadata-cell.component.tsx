import { useRef } from "react";
import { Field } from "~/components/ui/forms/field/field.component";
import { TextInput } from "~/components/ui/forms/input/text-input.component";
import { TextAreaInput } from "~/components/ui/forms/input/textarea-input.component";
import { useEditorStore } from "~/stores/editor.store";

export function MetadataBlock({ tabId }: { id: string; tabId: string }) {
	const tab = useEditorStore((state) => state.tabs[tabId]);

	const updateTab = useEditorStore((state) => state.updateTab);
	const commit = useEditorStore((state) => state.commit);

	const timerRef = useRef<NodeJS.Timeout | null>(null);

	if (!tab || tab.type !== "profile") return null;
	const profile = tab.data.profile;

	const handleTextChange = (field: "name" | "description", value: string) => {
		if (!profile) return;

		updateTab(tabId, "profile", {
			profile: {
				...profile,
				[field]: value,
			},
		});

		if (timerRef.current) {
			clearTimeout(timerRef.current);
		}

		timerRef.current = setTimeout(() => {
			commit();
		}, 500);
	};

	return (
		<div className="space-y-4">
			<Field>
				<Field.Label className="sr-only">Profile Name</Field.Label>
				<Field.Control className="bg-transparent border-none px-0 py-0 focus-within:ring-0">
					<TextInput
						value={profile?.name || ""}
						onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
							handleTextChange("name", e.target.value)
						}
						className="text-lg font-medium px-0"
						onBlur={() => {
							if (timerRef.current) {
								clearTimeout(timerRef.current);
								commit();
								timerRef.current = null;
							}
						}}
					/>
				</Field.Control>
			</Field>
			<Field>
				<Field.Label className="sr-only">Description</Field.Label>
				<Field.Control className="bg-transparent border-none px-0 py-0 focus-within:ring-0">
					<TextAreaInput
						value={profile?.description || ""}
						onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
							handleTextChange("description", e.target.value)
						}
						className="text-sm min-h-15 px-0"
						placeholder="Document the objective..."
						onBlur={() => {
							if (timerRef.current) {
								clearTimeout(timerRef.current);
								commit();
								timerRef.current = null;
							}
						}}
					/>
				</Field.Control>
			</Field>
		</div>
	);
}
