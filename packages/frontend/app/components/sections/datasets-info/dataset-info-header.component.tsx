import { FaPencilAlt, FaTrash } from "react-icons/fa";

type DatasetInfoHeaderProps = {
	name: string;
	id: string;
};

export function DatasetInfoHeader({ name, id }: DatasetInfoHeaderProps) {
	return (
		<header>
			<div className="flex items-center justify-between">
				<h1 className="text-2xl font-bold">{name}</h1>
				<div className="flex space-x-2 mt-2">
					<button
						type="button"
						className="text-red-500 hover:text-red-700 active:text-red-800 cursor-pointer"
					>
						<FaTrash size={16} />
					</button>

					<button
						type="button"
						className="text-blue-500 hover:text-blue-700 active:text-blue-800 cursor-pointer"
					>
						<FaPencilAlt size={16} />
					</button>
				</div>
			</div>
			<p className="text-xs text-gray-600">{id}</p>
		</header>
	);
}
