import { Clock } from "lucide-react";

export function ProfileHistory() {
    return (
        <div className="mt-8 w-full max-w-2xl bg-background-surface/50 border border-border rounded-xl p-6 backdrop-blur-sm">
            <div className="flex items-center gap-2 mb-4 text-xs font-bold uppercase tracking-widest text-gray-500">
                <Clock size={14} /> Recent Profiles
            </div>
            <div className="space-y-2">
                {["Production_ETL", "Testing_Alpha", "Legacy_Models"].map((item) => (
                    <button
                        type="button"
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
    );
}
