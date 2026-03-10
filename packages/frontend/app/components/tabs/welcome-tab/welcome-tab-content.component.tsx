import { Plus, Upload } from "lucide-react";
import { ActionCard } from "~/components/ui/cards/action-card.component";
import { ProfileHistory } from "./profile-history.component";

export function WelcomeTabContent() {
    return (
        <div className="min-h-full w-full py-12 px-6 flex flex-col items-center bg-[radial-gradient(#2D3343_0.5px,transparent_0.5px)] bg-size-[24px_24px]">
            <div className="text-center mb-12 animate-in fade-in zoom-in duration-500">
                <div className="w-16 h-16 bg-primary-500/10 border border-primary-500/30 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-2xl shadow-primary-500/20">
                    <span className="text-3xl text-primary-400 font-bold">Σ</span>
                </div>
                <h2 className="text-3xl font-bold tracking-tight text-white">
                    Spectrum Workspace
                </h2>
                <p className="text-gray-500 mt-2 max-w-sm mx-auto">
                    Select a profile from the sidebar or start a new symbolic regression
                    project.
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-2xl">
                <ActionCard
                    icon={<Plus size={20} className="text-primary-500" />}
                    title="New Profile"
                    description="Create a fresh workspace for a new model."
                    onClick={() => console.log("Create new profile")}
                />
                <ActionCard
                    icon={<Upload size={20} className="text-blue-500" />}
                    title="Import Dataset"
                    description="Upload a CSV file to start modeling immediately."
                    onClick={() => console.log("Datasets View")}
                />
            </div>

            <ProfileHistory />
        </div>
    );
}
