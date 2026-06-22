import { type PropsWithChildren, useCallback, useEffect, useRef } from "react";
import { createPortal } from "react-dom";

type ModalProps = PropsWithChildren<{
	isActive: boolean;
	onClose: () => void;
}>;

export function Modal({ children, isActive, onClose }: ModalProps) {
	const dialogRef = useRef<HTMLDialogElement>(null);

	const handleBackdropClick = useCallback(
		(event: React.MouseEvent<HTMLDialogElement>) => {
			const dialog = dialogRef.current;

			if (!dialog) {
				return;
			}

			const rect = dialog.getBoundingClientRect();
			const isInDialog =
				event.clientX >= rect.left &&
				event.clientX <= rect.right &&
				event.clientY >= rect.top &&
				event.clientY <= rect.bottom;

			if (!isInDialog) {
				onClose();
			}
		},
		[onClose],
	);

	useEffect(() => {
		const dialog = dialogRef.current;

		if (!dialog) {
			return;
		}

		if (isActive) {
			dialog.showModal();
		} else {
			dialog.close();
		}
	}, [isActive]);

	const handleKeyDown = useCallback(
		(event: React.KeyboardEvent<HTMLDialogElement>) => {
			if (event.key === "Escape") {
				onClose();
			}
		},
		[onClose],
	);

	if (!isActive) {
		return null;
	}

	return createPortal(
		<dialog
			ref={dialogRef}
			className="m-auto rounded border border-neutral-500 p-4 min-w-md backdrop:backdrop-blur-sm backdrop:bg-black/30"
			onClick={handleBackdropClick}
			onKeyDown={handleKeyDown}
		>
			{children}
		</dialog>,
		document.body,
	);
}
