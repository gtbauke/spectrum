import { Edit } from "lucide-react";
import { useState } from "react";
import { Button } from "~/components/ui/buttons/button.component";
import { IconButton } from "~/components/ui/buttons/icon-button.component";
import { TextInput } from "~/components/ui/forms/input/text-input.component";
import { TextAreaInput } from "~/components/ui/forms/input/textarea-input.component";
import { useProfileUpdateMutation } from "~/hooks/use-profile-update-mutation.hook";
import type { Profile } from "~/schemas/domain/profile.schema";

type ProfileMetadataSectionProps = {
	profile: Profile;
};

export function ProfileMetadataSection({
	profile,
}: ProfileMetadataSectionProps) {
	const [isEditing, setIsEditing] = useState(false);
	const [tempName, setTempName] = useState(profile.name);
	const [tempDescription, setTempDescription] = useState(profile.description);

	const { mutate: updateProfile } = useProfileUpdateMutation();

	const handleEditClick = () => {
		setIsEditing(true);
	};

	const handleSaveClick = () => {
		updateProfile({
			profileId: profile.id,
			data: {
				name: tempName,
				description: tempDescription,
			},
		});

		setIsEditing(false);
	};

	return (
		<div className="bg-background-surface border border-border rounded-lg p-4 shadow-sm">
			{isEditing ? (
				<div className="space-y-4">
					<div className="flex flex-col gap-4">
						<TextInput
							label="Profile Name"
							value={tempName}
							onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
								setTempName(e.target.value)
							}
						/>

						<TextAreaInput
							label="Description"
							value={tempDescription}
							onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
								setTempDescription(e.target.value)
							}
							placeholder="Document the objective..."
						/>
					</div>

					<Button type="button" className="py-2" onClick={handleSaveClick}>
						Save
					</Button>
				</div>
			) : (
				<>
					<div className="flex items-center gap-2">
						<h2 className="text-lg font-semibold">{tempName}</h2>
						<IconButton
							Icon={Edit}
							aria-label="Edit Profile Metadata"
							className="hover:text-blue-500 hover:bg-blue-500/10 transition-colors"
							variant="xs"
							onClick={handleEditClick}
						/>
					</div>
					<p className="text-gray-500">{tempDescription}</p>
				</>
			)}
		</div>
	);
}
