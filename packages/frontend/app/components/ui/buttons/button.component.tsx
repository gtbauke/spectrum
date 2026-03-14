import { Loader2 } from "lucide-react";
import type { PropsWithChildren } from "react";
import { cn } from "~/utils/classname.util";

export type ButtonProps = PropsWithChildren<{
	className?: string;
	type: "button" | "submit" | "reset";
	isLoading: boolean;
}> &
	React.InputHTMLAttributes<HTMLButtonElement>;

export function Button({
	className,
	children,
	type,
	isLoading,
	disabled,
	...props
}: ButtonProps) {
	const isDisabled = disabled || isLoading;

	return (
		<button
			{...props}
			type={type}
			disabled={isDisabled}
			className={cn(
				// Base styles
				"relative w-full font-bold py-3 rounded-lg transition-all flex items-center justify-center gap-2",
				"bg-primary-600 text-white shadow-lg shadow-primary-500/10",

				// Active/Hover states
				"hover:bg-primary-700 active:scale-[0.98] cursor-pointer",

				// Disabled styles
				"disabled:opacity-50 disabled:bg-gray-800 disabled:text-gray-500 disabled:cursor-not-allowed disabled:shadow-none disabled:active:scale-100",
				className,
			)}
		>
			{isLoading && (
				<Loader2 size={18} className="animate-spin text-gray-400" />
			)}

			<span className={cn(isLoading ? "opacity-70" : "opacity-100")}>
				{children}
			</span>
		</button>
	);
}
