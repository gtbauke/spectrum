import { TextInput } from "~/components/ui/forms/input/text-input.component";
import { TextAreaInput } from "~/components/ui/forms/input/textarea-input.component";
import { type MetadataData, useEditorStore } from "~/stores/editor.store";

export function MetadataBlock({
    id,
    data,
}: {
    id: string;
    data: MetadataData;
}) {
    const updateBlock = useEditorStore((state) => state.updateBlock);

    return (
        <div className="space-y-4">
            <TextInput
                label="Profile Name"
                value={data.name || ""}
                onChange={(e) => updateBlock(id, { name: e.target.value })}
                className="bg-transparent border-none px-0 py-0 text-lg font-medium focus:ring-0"
            />
            <TextAreaInput
                label="Description"
                value={data.description || ""}
                onChange={(e) => updateBlock(id, { description: e.target.value })}
                className="bg-transparent border-none px-0 py-0 text-sm focus:ring-0 min-h-15"
                placeholder="Document the objective..."
            />
        </div>
    );
}
