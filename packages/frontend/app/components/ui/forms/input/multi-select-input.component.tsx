import { Check, ChevronDown, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { cn } from "~/utils/classname.util";
import type { SelectOption } from "./select-input.component";

export type MultiSelectInputProps = {
	options: SelectOption[];
	value: string[];
	onChange: (value: string[]) => void;
	className?: string;
	placeholder?: string;
};

export const MultiSelectInput = ({
	options,
	value = [],
	onChange,
	className,
	placeholder = "Select options...",
}: MultiSelectInputProps) => {
	const [isOpen, setIsOpen] = useState(false);
	const containerRef = useRef<HTMLDivElement>(null);

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

	console.log(
		"MultiSelectInput rendered with value:",
		value,
		"selectedOptions:",
		selectedOptions,
		"isOpen:",
		isOpen,
	);

	return (
		<div
			className={cn(
				"relative flex-1 w-full",
				isOpen ? "z-50" : "z-10",
				className,
			)}
			ref={containerRef}
		>
			{/** biome-ignore lint/a11y/noStaticElementInteractions: Cannot have nested interactive elements */}
			<div
				onClick={() => setIsOpen((v) => !v)}
				className={cn(
					"w-full min-h-12 bg-transparent border-none outline-none p-2 cursor-pointer flex flex-wrap gap-2 items-center text-white",
				)}
				onKeyDown={(e) => {
					if (e.key === "Enter" || e.key === " ") {
						e.preventDefault();
						setIsOpen(!isOpen);
					}
				}}
				// biome-ignore lint/a11y/noNoninteractiveTabindex: Needs to be a div
				tabIndex={0}
			>
				{selectedOptions.length === 0 ? (
					<span className="text-gray-600 p-2 select-none flex-1">
						{placeholder}
					</span>
				) : (
					<div className="flex flex-wrap gap-2 flex-1">
						{selectedOptions.map((opt) => (
							<span
								key={opt.value}
								className="flex items-center gap-1 bg-white/10 text-gray-200 py-1 px-2 rounded-md text-sm select-none"
							>
								{opt.label}
								<button
									type="button"
									onClick={(e) => removeOption(e, opt.value)}
									className="hover:text-red-400 transition-colors rounded-full p-0.5 hover:bg-white/10 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary-500"
								>
									<X size={12} />
								</button>
							</span>
						))}
					</div>
				)}

				<div className="shrink-0 text-gray-500 group-hover:text-gray-300 transition-colors absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none">
					<ChevronDown
						size={16}
						className={cn("transition-transform", isOpen && "rotate-180")}
					/>
				</div>
			</div>

			{isOpen && (
				<div className="absolute z-50 w-full mt-2 bg-background-surface border border-white/10 rounded-md shadow-lg max-h-60 overflow-y-auto custom-scrollbar overflow-hidden">
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
	);
};
