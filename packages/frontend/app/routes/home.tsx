import { WorkspaceLayout } from "~/components/layouts/workspace.layout";
import { useProfileTabs } from "~/contexts/profile-tabs.context";
import type { Route } from "./+types/home";

export function meta(_: Route.MetaArgs) {
    return [
        { title: "Spectrum" },
        {
            name: "description",
            content: "The web platform for Symbolic Regression",
        },
    ];
}

// TODO: fix the layout

import { BookOpen, Clock, Plus, Upload } from "lucide-react";

export function WelcomeScreen() {
    const { openTab } = useProfileTabs(); // From our context

    return (
        <div className="h-full w-full flex flex-col items-center justify-center p-8 bg-[radial-gradient(#2D3343_0.5px,transparent_0.5px)] [background-size:24px_24px]">
            {/* 1. Header Hero */}
            <div className="text-center mb-12 animate-in fade-in zoom-in duration-500">
                <div className="w-16 h-16 bg-violet-500/10 border border-violet-500/30 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-2xl shadow-violet-500/20">
                    <span className="text-3xl text-violet-400 font-bold">Σ</span>
                </div>
                <h2 className="text-3xl font-bold tracking-tight text-white">
                    Spectrum Workspace
                </h2>
                <p className="text-gray-500 mt-2 max-w-sm mx-auto">
                    Select a profile from the sidebar or start a new symbolic regression
                    project.
                </p>
            </div>

            {/* 2. Quick Action Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-2xl">
                <ActionCard
                    icon={<Plus className="text-violet-400" />}
                    title="New Profile"
                    description="Create a fresh workspace for a new model."
                    onClick={() => {
                        /* Trigger Create Modal */
                    }}
                />
                <ActionCard
                    icon={<Upload className="text-blue-400" />}
                    title="Import Dataset"
                    description="Connect S3, SQL, or upload a CSV/JSON file."
                    onClick={() => {
                        /* Switch to Dataset view */
                    }}
                />
            </div>

            {/* 3. Recent History (Bento Style) */}
            <div className="mt-8 w-full max-w-2xl bg-[#161922]/50 border border-border rounded-xl p-6 backdrop-blur-sm">
                <div className="flex items-center gap-2 mb-4 text-xs font-bold uppercase tracking-widest text-gray-500">
                    <Clock size={14} /> Recent Profiles
                </div>
                <div className="space-y-2">
                    {/* Map through your actual history here */}
                    {["Production_ETL", "Testing_Alpha", "Legacy_Models"].map((item) => (
                        <button
                            key={item}
                            className="w-full flex justify-between items-center p-3 rounded-lg hover:bg-white/5 transition group text-sm"
                        >
                            <span className="text-gray-300 group-hover:text-white">
                                📁 {item}
                            </span>
                            <span className="text-xs text-gray-600 italic">2 hours ago</span>
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
}

function ActionCard({
    icon,
    title,
    description,
    onClick,
}: {
    icon: any;
    title: string;
    description: string;
    onClick: () => void;
}) {
    return (
        <button
            onClick={onClick}
            className="flex flex-col items-start p-6 bg-[#161922] border border-border rounded-xl hover:border-violet-500/50 hover:bg-violet-500/5 transition-all group text-left shadow-xl"
        >
            <div className="p-2 bg-background rounded-lg mb-4 group-hover:scale-110 transition-transform">
                {icon}
            </div>
            <h3 className="font-bold text-white mb-1">{title}</h3>
            <p className="text-sm text-gray-500 leading-relaxed">{description}</p>
        </button>
    );
}

export default function Home() {
    const { activeTabId } = useProfileTabs();

    return (
        <WorkspaceLayout>
            {activeTabId === null && <WelcomeScreen />}
        </WorkspaceLayout>
    );
}
