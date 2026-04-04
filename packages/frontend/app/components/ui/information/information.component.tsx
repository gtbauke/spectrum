import * as TooltipPrimitive from "@radix-ui/react-tooltip";
import { motion } from "framer-motion";
import { Info } from "lucide-react";
import * as React from "react";
import { cn } from "~/utils/classname.util";

export const InformationRoot = ({
	children,
	delayDuration = 300,
	...props
}: React.ComponentPropsWithoutRef<typeof TooltipPrimitive.Root> & {
	delayDuration?: number;
}) => (
	<TooltipPrimitive.Provider delayDuration={delayDuration}>
		<TooltipPrimitive.Root {...props}>{children}</TooltipPrimitive.Root>
	</TooltipPrimitive.Provider>
);

export const InformationTrigger = TooltipPrimitive.Trigger;

export const InformationIcon = React.forwardRef<
	React.ComponentRef<typeof TooltipPrimitive.Trigger>,
	React.ComponentPropsWithoutRef<typeof TooltipPrimitive.Trigger> & {
		size?: number;
	}
>(({ className, size = 16, ...props }, ref) => (
	<TooltipPrimitive.Trigger
		ref={ref}
		className={cn(
			"inline-flex items-center justify-center rounded-full text-gray-400 hover:text-white transition-colors cursor-help focus:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 focus-visible:ring-offset-background",
			className,
		)}
		{...props}
	>
		<Info size={size} />
		<span className="sr-only">More information</span>
	</TooltipPrimitive.Trigger>
));
InformationIcon.displayName = "InformationIcon";

export const InformationContent = React.forwardRef<
	React.ComponentRef<typeof TooltipPrimitive.Content>,
	React.ComponentPropsWithoutRef<typeof TooltipPrimitive.Content>
>(({ className, sideOffset = 6, children, side = "top", ...props }, ref) => {
	const initialY = side === "top" ? 4 : side === "bottom" ? -4 : 0;
	const initialX = side === "left" ? 4 : side === "right" ? -4 : 0;

	return (
		<TooltipPrimitive.Content
			ref={ref}
			side={side}
			sideOffset={sideOffset}
			className="z-50"
			asChild
			{...props}
		>
			<motion.div
				initial={{ opacity: 0, scale: 0.96, y: initialY, x: initialX }}
				animate={{ opacity: 1, scale: 1, y: 0, x: 0 }}
				transition={{ duration: 0.15, ease: "easeOut" }}
				className={cn(
					"overflow-hidden rounded-md bg-background-surface border border-border px-3 py-2 text-sm text-gray-200 shadow-lg",
					"max-w-xs wrap-break-word",
					className,
				)}
			>
				{children}
				<TooltipPrimitive.Arrow className="fill-background-surface" />
			</motion.div>
		</TooltipPrimitive.Content>
	);
});

InformationContent.displayName = "InformationContent";

export const Information = Object.assign(InformationRoot, {
	Trigger: InformationTrigger,
	Icon: InformationIcon,
	Content: InformationContent,
});
