import { Check, ChevronDown, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import type { FieldError } from "react-hook-form";
import { cn } from "~/utils/classname.util";
import type { SelectOption } from "./select-input.component";

export type MultiSelectInputProps = {
	label: string;
	options: SelectOption[];
	value: string[];
	onChange: (value: string[]) => void;
	className?: string;
	labelClassName?: string;
	required?: boolean;
	error?: FieldError | string;
	placeholder?: string;
};

export const MultiSelectInput = ({
	label,
	options,
	value = [],
	onChange,
	className,
	labelClassName,
	required,
	error,
	placeholder = "Select options...",
}: MultiSelectInputProps) => {
	const [isOpen, setIsOpen] = useState(false);
	const containerRef = useRef<HTMLDivElement>(null);

	const hasError = Boolean(error);
	const errorMessage = typeof error === "string" ? error : error?.message;

	useEffect(() => {
		function handleClickOutside(event: MouseEvent) {
			if (
				containerRef.current &&
				!containerRef.current.contains(event.target as Node)
			) {
				setIsOpen(false);
			}
		}
		document.addEventListener("mousedown", handleClickOutside);
		return () => document.removeEventListener("mousedown", handleClickOutside);
	}, []);

	const toggleOption = (optionValue: string) => {
		const newValue = value.includes(optionValue)
			? value.filter((v) => v !== optionValue)
			: [...value, optionValue];
		onChange(newValue);
	};

	const removeOption = (e: React.MouseEvent, optionValue: string) => {
		e.stopPropagation();
		onChange(value.filter((v) => v !== optionValue));
	};

	const selectedOptions = options.filter((opt) => value.includes(opt.value));

	return (
		<div className="w-full space-y-2" ref={containerRef}>
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
			</div>

			<div className="relative group mt-2">
				{/** biome-ignore lint/a11y/noStaticElementInteractions: Cannot have nested interactive elements */}
				<div
					onClick={() => setIsOpen(!isOpen)}
					className={cn(
						"w-full min-h-12 bg-background border rounded-lg px-3 py-2 outline-none transition-all cursor-pointer flex flex-wrap gap-2 items-center",
						error
							? "border-red-500 ring-1 ring-red-500"
							: "border-border hover:border-white/10",
						isOpen && !error && "ring-2 ring-violet-500 border-white/10",
						className,
					)}
					onKeyDown={(e) => {
						if (e.key === "Enter" || e.key === " ") {
							e.preventDefault();
							setIsOpen(!isOpen);
						}
					}}
					aria-invalid={error ? "true" : "false"}
				>
					{selectedOptions.length === 0 ? (
						<span className="text-gray-600 px-1 select-none">
							{placeholder}
						</span>
					) : (
						selectedOptions.map((opt) => (
							<span
								key={opt.value}
								className="flex items-center gap-1 bg-white/10 text-gray-200 px-2 py-1 rounded-md text-sm select-none"
							>
								{opt.label}
								<button
									type="button"
									onClick={(e) => removeOption(e, opt.value)}
									className="hover:text-red-400 transition-colors rounded-full p-0.5 hover:bg-white/10"
								>
									<X size={12} />
								</button>
							</span>
						))
					)}

					<div className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 group-hover:text-gray-300 transition-colors">
						<ChevronDown
							size={16}
							className={cn("transition-transform", isOpen && "rotate-180")}
						/>
					</div>
				</div>

				{isOpen && (
					<div className="absolute z-50 w-full mt-2 bg-[#1e2028] border border-white/10 rounded-md shadow-lg max-h-60 overflow-y-auto custom-scrollbar overflow-hidden">
						{options.length === 0 ? (
							<div className="px-4 py-3 text-sm text-gray-500 text-center">
								No options available
							</div>
						) : (
							<div className="flex flex-col p-1">
								{options.map((option) => {
									const isSelected = value.includes(option.value);
									return (
										<button
											key={option.value}
											type="button"
											onClick={() => toggleOption(option.value)}
											className={cn(
												"flex items-center justify-between w-full px-3 py-2 text-sm text-left rounded-md transition-colors cursor-pointer",
												isSelected
													? "bg-violet-500/10 text-violet-400 font-medium"
													: "text-gray-200 hover:bg-white/5",
											)}
										>
											{option.label}
											{isSelected && <Check size={16} />}
										</button>
									);
								})}
							</div>
						)}
					</div>
				)}
			</div>

			{hasError && (
				<p className="text-xs text-red-500 mt-1 animate-in fade-in slide-in-from-top-1">
					{errorMessage}
				</p>
			)}
		</div>
	);
};
