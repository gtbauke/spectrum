import { FaPencilAlt, FaPlay, FaTrash } from "react-icons/fa";
import { useNavigate } from "react-router";

type DatasetCardHeaderProps = {
	id: string;
	name: string;
	status: string;
};

export function DatasetCardHeader({
	name,
	status,
	id,
}: DatasetCardHeaderProps) {
	const navigate = useNavigate();

	const handlePlayClick = () => {
		navigate(`/datasets/${id}/jobs`);
	};

	return (
		<header>
			<div className="flex items-center justify-between">
				<h2 className="text-lg font-semibold">{name}</h2>

				{/* TODO: Add onClick handler */}
				<div className="flex space-x-2">
					<button
						type="button"
						className="text-red-500 hover:text-red-700 active:text-red-800 cursor-pointer"
					>
						<FaTrash size={12} />
					</button>

					<button
						type="button"
						className="text-blue-500 hover:text-blue-700 active:text-blue-800 cursor-pointer"
					>
						<FaPencilAlt size={12} />
					</button>

					<button
						type="button"
						className="text-green-500 hover:text-green-700 active:text-green-800 cursor-pointer"
						onClick={handlePlayClick}
					>
						<FaPlay size={12} />
					</button>
				</div>
			</div>

			<p className="text-sm text-gray-600">Status: {status}</p>
		</header>
	);
}
