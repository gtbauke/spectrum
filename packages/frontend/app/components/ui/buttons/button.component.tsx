import { Loader2 } from "lucide-react";
import type { PropsWithChildren } from "react";
import { cn } from "~/utils/classname.util";
import { ButtonGroup } from "./button-group.component";

export type ButtonProps = PropsWithChildren<{
	className?: string;
	type?: "button" | "submit" | "reset";
	isLoading?: boolean;
	variant?: "primary" | "outline" | "ghost";
}> &
	React.InputHTMLAttributes<HTMLButtonElement>;

const variantClasses = {
	primary:
		"bg-primary-600 text-white border border-primary-600 hover:border-primary-700 hover:bg-primary-700 disabled:bg-gray-800 disabled:border-gray-800 disabled:text-gray-500",
	outline:
		"bg-transparent border border-primary-600 text-primary-600 hover:bg-primary-500/10 hover:border-primary-700 hover:text-primary-700 disabled:border-gray-800 disabled:text-gray-500 disabled:hover:bg-transparent",
	ghost:
		"bg-transparent text-gray-700 hover:bg-gray-100 hover:text-gray-900 disabled:text-gray-500 disabled:hover:bg-transparent",
};

export function ButtonInner({
	className,
	children,
	type = "button",
	isLoading = false,
	disabled,
	variant = "primary",
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
				"relative w-full font-bold py-3 px-4 rounded-lg transition-all flex items-center justify-center gap-2",
				// Active/Hover states
				"active:scale-[0.98] cursor-pointer",
				// Disabled styles
				"disabled:opacity-50 disabled:text-gray-500 disabled:cursor-not-allowed disabled:shadow-none disabled:active:scale-100",
				// Variant styles
				variantClasses[variant],
				className,
			)}
		>
			{isLoading && (
				<Loader2 size={18} className="animate-spin text-current opacity-70" />
			)}

			<span
				className={cn(
					isLoading ? "opacity-70" : "opacity-100",
					"flex items-center gap-2",
				)}
			>
				{children}
			</span>
		</button>
	);
}

export const Button = Object.assign(ButtonInner, {
	Group: ButtonGroup,
});
