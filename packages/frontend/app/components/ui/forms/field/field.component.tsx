import * as React from "react";
import type { FieldError as ReactHookFormFieldError } from "react-hook-form";
import { RedirectLink } from "~/components/ui/redirects/redirect-link.component";
import { cn } from "~/utils/classname.util";
import { Control, Slot } from "./control.component";
import { FieldContext, useFieldContext } from "./field-context";

export type FieldProps = {
	children: React.ReactNode;
	error?: ReactHookFormFieldError | string;
	required?: boolean;
	disabled?: boolean;
	className?: string;
};

export const Root = ({
	children,
	error,
	required,
	disabled,
	className,
}: FieldProps) => {
	const id = React.useId();

	const value = React.useMemo(
		() => ({ id, error, required, disabled }),
		[id, error, required, disabled],
	);

	return (
		<FieldContext.Provider value={value}>
			<div className={cn("w-full space-y-2", className)}>{children}</div>
		</FieldContext.Provider>
	);
};

export const Header = ({
	className,
	children,
}: React.HTMLAttributes<HTMLDivElement>) => (
	<div className={cn("flex justify-between items-center", className)}>
		{children}
	</div>
);

export const Label = ({
	className,
	children,
	required,
	...props
}: React.LabelHTMLAttributes<HTMLLabelElement> & { required?: boolean }) => {
	const { id, required: contextRequired } = useFieldContext();
	const isReq = required ?? contextRequired;

	return (
		<div>
			<label
				htmlFor={id}
				className={cn(
					"text-xs font-medium text-gray-400 uppercase tracking-wider",
					className,
				)}
				{...props}
			>
				{children}
			</label>
			{isReq && <span className="text-red-500 ml-1">*</span>}
		</div>
	);
};

export const Action = ({
	to,
	className,
	children,
}: {
	to: string;
	className?: string;
	children: React.ReactNode;
}) => (
	<RedirectLink to={to} className={cn("text-sm", className)}>
		{children}
	</RedirectLink>
);

export const Description = ({
	className,
	children,
}: {
	className?: string;
	children: React.ReactNode;
}) => <p className={cn("text-xs text-gray-500", className)}>{children}</p>;

export const FieldError = ({ className }: { className?: string }) => {
	const { error } = useFieldContext();

	const hasError = Boolean(error);
	const errorMessage = typeof error === "string" ? error : error?.message;

	if (!hasError) return null;

	return (
		<p
			className={cn(
				"text-xs text-red-500 mt-1 animate-in fade-in slide-in-from-top-1",
				className,
			)}
		>
			{errorMessage}
		</p>
	);
};

export const Field = Object.assign(Root, {
	Header,
	Label,
	Description,
	Action,
	Error: FieldError,
	Control,
	Slot,
});
