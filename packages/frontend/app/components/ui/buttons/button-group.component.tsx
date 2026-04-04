import type { PropsWithChildren } from "react";
import { cn } from "~/utils/classname.util";

export type ButtonGroupProps = PropsWithChildren<{
	className?: string;
	mode?: "seamless" | "spaced";
}>;

export function ButtonGroup({
	children,
	className,
	mode = "seamless",
}: ButtonGroupProps) {
	return (
		<div
			className={cn(
				"flex items-center",
				mode === "spaced" && "gap-2",
				mode === "seamless" && [
					// Remove inside borders and apply relative overlap on hover
					"[&>*]:rounded-none",
					"[&>*:first-child]:rounded-l-lg",
					"[&>*:last-child]:rounded-r-lg",
					"[&>*:not(:first-child)]:-ml-px",
					"[&>*:hover]:z-10",
					"[&>*:focus-within]:z-10"
				],
				className,
			)}
		>
			{children}
		</div>
	);
}
