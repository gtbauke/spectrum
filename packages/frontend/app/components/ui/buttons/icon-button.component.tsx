import type { LucideIcon } from "lucide-react";
import { cn } from "~/utils/classname.util";

type IconButtonProps = {
	Icon: LucideIcon;
	className?: string;
} & React.InputHTMLAttributes<HTMLButtonElement>;

export function IconButton({ Icon, className, ...props }: IconButtonProps) {
	return (
		<button
			{...props}
			type="button"
			className={cn(
				"min-w-10 min-h-10 flex items-center justify-center cursor-pointer",
				className,
			)}
		>
			<Icon size={16} />
		</button>
	);
}
