import { Plus } from "lucide-react";
import { useId, useState } from "react";
import { TextInput } from "~/components/ui/forms/input/text-input.component";
import { TextAreaInput } from "~/components/ui/forms/input/textarea-input.component";
import { NotebookCell } from "~/components/ui/notebook/cell.componenet";
import type { ProfileVersion } from "~/schemas/generated/profile-version.schema";

type ProfileEditorProps = {
    version: ProfileVersion;
};

export function ProfileEditor({ version }: ProfileEditorProps) {
    const [activeCellId, setActiveCellId] = useState<string | null>("metadata");

    return (
        <div className="flex-1 h-full overflow-y-auto custom-scrollbar bg-[#111319] py-8 px-4">
            {/* Header / Breadcrumbs could go here */}
            <div className="max-w-4xl mx-auto mb-8 pl-12">
                <h1 className="text-2xl font-bold text-gray-200">{version.name}</h1>
                <p className="text-xs text-gray-500 mt-1">
                    Version {version.version} • {version.status}
                </p>
            </div>

            {/* Block 1: Profile Metadata */}
            <NotebookCell
                id={useId()}
                type="markdown"
                isActive={activeCellId === "metadata"}
                onClick={() => setActiveCellId("metadata")}
            >
                <div className="space-y-4">
                    <TextInput
                        label="Profile Name"
                        defaultValue={version.name}
                        className="bg-transparent border-none px-0 py-0 text-lg font-medium focus:ring-0"
                    />
                    <TextAreaInput
                        label="Description"
                        defaultValue={version.description || ""}
                        className="bg-transparent border-none px-0 py-0 text-sm focus:ring-0 min-h-[60px]"
                        placeholder="Document the objective of this symbolic regression run..."
                    />
                </div>
            </NotebookCell>

            {/* Block 2: Datasets */}
            <NotebookCell
                id={useId()}
                type="dataset"
                isActive={activeCellId === "datasets"}
                onClick={() => setActiveCellId("datasets")}
            >
                <div className="space-y-2">
                    <span className="text-xs font-medium text-gray-400 uppercase tracking-wider">
                        Attached Datasets
                    </span>
                    <div className="rounded border border-white/5 overflow-hidden">
                        {/* Map over your associations here */}
                        {version.datasets?.map((ds) => (
                            <div
                                key={ds.id}
                                className="flex justify-between items-center p-3 border-b border-white/5 bg-[#111319]/50 hover:bg-white/5 transition-colors text-sm text-gray-300"
                            >
                                <span>Dataset</span>
                                <span className="text-[10px] uppercase bg-primary-500/10 text-primary-400 px-2 py-0.5 rounded">
                                    {ds.role}
                                </span>
                            </div>
                        ))}
                        {version.datasets?.length === 0 && (
                            <div className="p-4 text-center text-xs text-gray-500">
                                No datasets attached.
                            </div>
                        )}
                    </div>
                    <button
                        type="button"
                        className="text-xs text-primary-400 hover:text-primary-300 flex items-center gap-1 mt-2"
                    >
                        <Plus size={12} /> Add Dataset
                    </button>
                </div>
            </NotebookCell>

            {/* Block 3: Algorithm Configuration (Conceptual Example) */}
            <NotebookCell
                id={useId()}
                type="configuration"
                isActive={activeCellId === "config"}
                onClick={() => setActiveCellId("config")}
                onRun={() => console.log("Dispatching job to Worker package...")}
            >
                <div className="space-y-2">
                    <span className="text-xs font-medium text-gray-400 uppercase tracking-wider">
                        Algorithm Hyper-parameters
                    </span>
                    <div className="p-3 bg-[#0d0e12] rounded border border-white/5 font-mono text-xs text-gray-300">
                        {/* You could render a JSON editor or a grid of inputs here */}
                        <pre>
                            <code>
                                {`{
  "population_size": 1000,
  "generations": 50,
  "tournament_size": 5
}`}
                            </code>
                        </pre>
                    </div>
                </div>
            </NotebookCell>

            {/* Add Cell Button */}
            <div className="max-w-4xl mx-auto mt-4 pl-12 opacity-0 hover:opacity-100 transition-opacity">
                <button
                    type="button"
                    className="flex items-center gap-2 text-xs text-gray-500 hover:text-gray-300 px-4 py-2 rounded border border-dashed border-gray-600 hover:border-gray-400 transition-colors w-full justify-center"
                >
                    <Plus size={14} /> Add Block
                </button>
            </div>

            {/* Bottom padding to allow the last cell to scroll up to the middle of the screen */}
            <div className="h-64" />
        </div>
    );
}
