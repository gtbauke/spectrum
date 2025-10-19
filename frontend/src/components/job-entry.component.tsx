import { IoCopy, IoPencil, IoTrash } from "react-icons/io5";

type JobEntryProps = {
    id: string;
    name: string;
};

export function JobEntry({ id, name }: JobEntryProps) {
    return (
        <div className="flex rounded bg-background-secondary p-2">
            <div className="flex w-full flex-row items-center justify-between">
                <p className="text-white">
                    {id} - {name}
                </p>

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
    );
}
