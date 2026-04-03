import { ChevronDown } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { useFileUpload } from "./file-upload.context";

export function SelectFileDropdown() {
	const [isOpen, setIsOpen] = useState(false);
	const { files, selectedFileName, selectFile } = useFileUpload();

    const dropdownRef = useRef<HTMLDivElement>(null);

	const fileNames = Object.keys(files);
	const nonSelectedNames = fileNames.filter(
		(name) => name !== selectedFileName,
	);

	const toggle = () => setIsOpen((open) => !open);

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        };

        document.addEventListener("mousedown", handleClickOutside);

        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, []);

	return (
		<div className="group relative">
			<button
				type="button"
				className="flex items-center gap-2 cursor-pointer"
				onClick={toggle}
			>
				<span className="font-medium text-white flex items-center gap-2">
					{selectedFileName}
				</span>

				<ChevronDown
					size={16}
					className="opacity-0 group-hover:opacity-100 transition-opacity"
				/>
			</button>
			<span className="text-xs text-gray-500 mt-1">
				{selectedFileName
					? `${(files[selectedFileName].file.size / 1024 / 1024).toFixed(2)} MB • CSV Format`
					: "No file selected"}
			</span>

			{isOpen && (
				<div className="absolute top-1/2 left-0 bg-[#1e2028] border border-white/10 rounded-md shadow-lg z-10" ref={dropdownRef}>
					{nonSelectedNames.length === 0 ? (
						<div className="px-4 py-2 text-sm text-gray-500">
							No other files
						</div>
					) : (
						nonSelectedNames.map((name) => (
							<button
								key={name}
								className="px-4 py-2 w-full text-sm text-gray-200 hover:bg-white/5 cursor-pointer text-left"
								onClick={() => {
									selectFile(name);
									setIsOpen(false);
								}}
								onKeyDown={(e) => {
									if (e.key === "Enter") {
										selectFile(name);
										setIsOpen(false);
									}
								}}
								type="button"
							>
								{name}
							</button>
						))
					)}
				</div>
			)}
		</div>
	);
}
