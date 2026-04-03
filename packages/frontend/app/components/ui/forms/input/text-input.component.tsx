import { Eye, EyeClosed } from "lucide-react";
import type React from "react";
import { forwardRef, useState } from "react";
import type { FieldError } from "react-hook-form";
import { RedirectLink } from "~/components/ui/redirects/redirect-link.component";
import { cn } from "~/utils/classname.util";

export type TextInputProps = {
	label: string;
	className?: string;
	required?: boolean;
	error?: FieldError | string;
	redirect?: string;
	redirectHref?: string;
	labelClassName?: string;
} & React.InputHTMLAttributes<HTMLInputElement>;

export const TextInput = forwardRef<HTMLInputElement, TextInputProps>(
	(
		{
			label,
			className,
			required,
			error,
			redirect,
			redirectHref,
			labelClassName,
			...props
		},
		ref,
	) => {
		const [showPassword, setShowPassword] = useState(false);
		const isPassword = props.type === "password";
		const inputType = isPassword
			? showPassword
				? "text"
				: "password"
			: props.type;

		const togglePassword = () => setShowPassword((prev) => !prev);

		const hasError = Boolean(error);
		const errorMessage = typeof error === "string" ? error : error?.message;

		return (
			<div className="w-full space-y-2">
				<label>
					<div className="flex justify-between items-center">
						<div>
							<span
								className={cn(
									"text-xs font-medium text-gray-400 uppercase tracking-wider",
									labelClassName,
								)}
							>
								{label}
							</span>
							{required && <span className="text-red-500 ml-1">*</span>}
						</div>

						{redirect && redirectHref && (
							<RedirectLink to={redirectHref} className="text-sm">
								{redirect}
							</RedirectLink>
						)}
					</div>

					<div className="relative group">
						<input
							{...props}
							ref={ref}
							type={inputType}
							className={cn(
								"w-full bg-background border rounded-lg px-4 py-3 outline-none transition-all",
								"placeholder:text-gray-600 text-white",
								isPassword ? "pr-12" : "",
								error
									? "border-red-500 focus:ring-1 focus:ring-red-500"
									: "border-border focus:ring-1 focus:ring-violet-500",
								className,
							)}
							aria-invalid={error ? "true" : "false"}
						/>

						{isPassword && (
							<button
								type="button"
								onClick={togglePassword}
								className="absolute right-3 top-1/2 -translate-y-1/2 p-1.5 text-gray-500 hover:text-primary-400 transition-colors cursor-pointer"
								tabIndex={-1}
							>
								{showPassword ? <EyeClosed size={20} /> : <Eye size={20} />}
							</button>
						)}
					</div>

					{hasError && (
						<p className="text-xs text-red-500 mt-1 animate-in fade-in slide-in-from-top-1">
							{errorMessage}
						</p>
					)}
				</label>
			</div>
		);
	},
);

TextInput.displayName = "TextInput";
