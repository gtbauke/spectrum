import type { IconType } from "react-icons";
import {
    type ActivityView,
    useActivity,
} from "~/contexts/activity-view.context";

type ActivityIconProps = {
    Icon: IconType;
    label: string;
    activityView: ActivityView;
};

export function ActivityIcon({
    Icon,
    label,
    activityView,
}: ActivityIconProps) {
    const { setActiveView, activeView } = useActivity();
    const active = activeView === activityView;

    const handleOnClick = () => {
        setActiveView(activityView);
    };

    return (
        <div className="group relative flex items-center justify-center">
            <button
                type="button"
                className={`p-3 cursor-pointer rounded-xl transition-all duration-200 ${active
                    ? "bg-primary/20 text-primary"
                    : "text-gray-500 hover:text-white hover:bg-white/5"
                    }`}
                onClick={handleOnClick}
            >
                <Icon size={24} />
            </button>

            <span className="absolute left-14 scale-0 rounded bg-gray-900 px-2 py-1 text-xs font-medium text-white shadow-xl transition-all group-hover:scale-100 z-50 whitespace-nowrap">
                {label}
            </span>

            {active && (
                <div className="absolute -left-4 w-1 h-8 bg-primary rounded-r-full transition-all duration-200" />
            )}
        </div>
    );
}
