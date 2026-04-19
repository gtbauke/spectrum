import type { ReactNode } from "react";

type ActionCardProps = {
	icon: ReactNode;
	title: string;
	description: string;
	onClick: () => void;
};

export function ActionCard({
	icon,
	title,
	description,
	onClick,
}: ActionCardProps) {
	return (
		<button
			type="button"
			onClick={onClick}
			className="flex flex-col items-start p-6 bg-background-surface border border-border rounded-xl hover:border-primary-500/50 hover:bg-primary-500/5 transition-all group text-left shadow-xl cursor-pointer"
		>
			<div className="p-2 bg-background rounded-lg mb-4 group-hover:scale-110 transition-transform">
				{icon}
			</div>
			<h3 className="font-bold text-white mb-1">{title}</h3>
			<p className="text-sm text-gray-500 leading-relaxed">{description}</p>
		</button>
	);
}
