import { IoCopy, IoPencil, IoTrash } from "react-icons/io5";
import { useParams } from "react-router";

type DatasetPageParams = {
    datasetId: string;
};

export function DatasetPage() {
    const { datasetId } = useParams<DatasetPageParams>();

    return (
        <div>
            <h1 className="text-white">Dataset - {datasetId}</h1>

            {/* TODO: move this to a Job component */}
            <div className="flex bg-background-secondary p-2 rounded">
                <div className="flex flex-row items-center justify-between w-full">
                    <p className="text-white">Job ID - Job Name</p>

                    <div className="flex flex-row items-center">
                        <button type="button" className="cursor-pointer p-2">
                            <IoPencil
                                size={20}
                                className="text-white hover:text-gray-300 active:text-blue-300"
                            />
                        </button>

                        <button type="button" className="cursor-pointer p-2">
                            <IoCopy
                                size={20}
                                className="text-white hover:text-gray-300 active:text-green-300"
                            />
                        </button>

                        <button type="button" className="cursor-pointer p-2">
                            <IoTrash
                                size={20}
                                className="text-white hover:text-gray-300 active:text-red-300"
                            />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
