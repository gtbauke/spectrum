import { useEffect } from "react";

export function useKeyboardShortcut(key: string, callback: () => void) {
	useEffect(() => {
		const handleKeyDown = (event: KeyboardEvent) => {
			const isModifier = event.metaKey || event.ctrlKey;

			if (isModifier && event.key.toLowerCase() === key.toLowerCase()) {
				event.preventDefault();
				callback();
			}
		};

		window.addEventListener("keydown", handleKeyDown);

		return () => {
			window.removeEventListener("keydown", handleKeyDown);
		};
	}, [key, callback]);
}
