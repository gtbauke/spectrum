import { Eye, EyeClosed } from "lucide-react";
import type React from "react";
import { cn } from "~/utils/classname.util";

export type PasswordToggleProps = {
	visible: boolean;
	onToggle: () => void;
	className?: string;
};

export const PasswordToggle = ({
	visible,
	onToggle,
	className,
}: PasswordToggleProps) => {
	return (
		<button
			type="button"
			onClick={onToggle}
			className={cn(
				"p-1.5 hover:text-primary-400 transition-colors cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 rounded-md",
				className,
			)}
			tabIndex={-1}
			aria-label={visible ? "Hide password" : "Show password"}
		>
			{visible ? <EyeClosed size={20} /> : <Eye size={20} />}
		</button>
	);
};
