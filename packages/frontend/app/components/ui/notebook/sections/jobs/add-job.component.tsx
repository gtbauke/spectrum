import { useState } from "react";
import { MultiSelectInput } from "~/components/ui/forms/input/multi-select-input.component";
import { availableFunctionSchema } from "~/schemas/domain/enums.schema";
import { capitalize } from "~/utils/capitalize.util";

export function AddJob() {
	const [selectedFunctions, setSelectedFunctions] = useState<string[]>([]);

	return (
		<div className="p-4 border border-border rounded-lg bg-background-surface">
			<h3 className="text-md font-medium mb-2">Add New Job</h3>

			<form className="space-y-4">
				FINISH FORM
				<MultiSelectInput
					label="Available Functions"
					options={availableFunctionSchema.options.map((opt) => ({
						label: capitalize(opt),
						value: opt,
					}))}
					value={selectedFunctions}
					onChange={setSelectedFunctions}
				/>
			</form>
		</div>
	);
}
