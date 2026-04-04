import type * as React from "react";
import { cn } from "~/utils/classname.util";
import { useFieldContext } from "./field-context";

export const Control = ({
	className,
	children,
	...props
}: React.HTMLAttributes<HTMLDivElement>) => {
	const { error } = useFieldContext();
	const hasError = Boolean(error);

	return (
		<div
			className={cn(
				"relative group flex items-center w-full bg-background border rounded-lg transition-all focus-within:ring-1",
				hasError
					? "border-red-500 focus-within:ring-red-500"
					: "border-border focus-within:ring-violet-500 focus-within:border-violet-500 hover:border-white/10",
				className,
			)}
			{...props}
		>
			{children}
		</div>
	);
};

export const Slot = ({
	side,
	className,
	children,
}: {
	side: "left" | "right";
	className?: string;
	children: React.ReactNode;
}) => (
	<div
		className={cn(
			"flex items-center text-gray-500 transition-colors pointer-events-auto shrink-0",
			side === "left" ? "pl-4 pr-2" : "pr-4 pl-2",
			className,
		)}
	>
		{children}
	</div>
);
