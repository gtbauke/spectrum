import type { LucideIcon } from "lucide-react";
import { cn } from "~/utils/classname.util";

type IconButtonProps = React.InputHTMLAttributes<HTMLButtonElement> & {
	Icon: LucideIcon;
	className?: string;
	variant?: "xs" | "sm" | "md" | "lg";
};

export function IconButton({
	Icon,
	className,
	variant: size = "md",
	...props
}: IconButtonProps) {
	const sizeClasses = {
		xs: "min-w-6 min-h-6",
		sm: "min-w-8 min-h-8",
		md: "min-w-10 min-h-10",
		lg: "min-w-12 min-h-12",
	};

	return (
		<button
			{...props}
			type="button"
			className={cn(
				"flex items-center rounded justify-center cursor-pointer",
				sizeClasses[size],
				className,
			)}
		>
			<Icon size={16} />
		</button>
	);
}
