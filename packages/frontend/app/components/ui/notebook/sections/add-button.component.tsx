import { Check, Plus, X } from "lucide-react";
import { IconButton } from "~/components/ui/buttons/icon-button.component";
import { cn } from "~/utils/classname.util";

type AddButtonProps = {
	isEditing: boolean;
	onEditClick: () => void;
	onSaveClick: () => void;
	onCancelClick?: () => void;
};

export function AddButton({
	isEditing,
	onEditClick,
	onSaveClick,
	onCancelClick,
}: AddButtonProps) {
	return (
		<div className="flex items-center gap-2">
			<IconButton
				Icon={isEditing ? Check : Plus}
				onClick={isEditing ? onSaveClick : onEditClick}
				variant="sm"
				className={cn(
					"transition-colors",
					isEditing
						? "bg-secondary-500/10 text-secondary-500 hover:bg-secondary-500/20"
						: "bg-primary-500/10 text-primary-500 hover:bg-primary-500/20",
				)}
			/>

			{isEditing && (
				<IconButton
					Icon={X}
					onClick={onCancelClick}
					variant="sm"
					className="transition-colors bg-red-500/10 text-red-500 hover:bg-red-500/20"
				/>
			)}
		</div>
	);
}
