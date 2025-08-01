import clsx from "clsx";
import { useCallback } from "react";
import { type FileWithPath, useDropzone } from "react-dropzone";
import { IoCloudUpload } from "react-icons/io5";

// TODO: after the upload, redirect to the dataset page
export function UploadDatasetPage() {
    const onDrop = useCallback((acceptedFiles: FileWithPath[]) => {
        console.log("Accepted files:", acceptedFiles);
    }, []);

    const { getRootProps, acceptedFiles, getInputProps, isDragActive } =
        useDropzone({
            onDrop,
            maxFiles: 1,
            accept: {
                "text/csv": [".csv"],
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                    [".xlsx", ".xls"],
            },
        });

    return (
        <div className="flex flex-col h-full gap-4">
            <div className="flex flex-col items-center justify-center gap-1">
                <h1 className="text-white text-4xl font-bold">
                    Upload dataset
                </h1>
                <p className="text-gray-400 text-lg">
                    Upload your dataset and start having insights on your data
                    now!
                </p>
            </div>

            <div
                {...getRootProps()}
                className={clsx(
                    "border border-dashed border-gray-300 border-2 rounded p-6 flex justify-center items-center flex-1 cursor-pointer transition-colors duration-200 ease-in-out",
                    isDragActive && "bg-gray-100",
                )}
            >
                <input {...getInputProps()} />
                <div className="flex flex-col items-center gap-2 text-gray-400">
                    <IoCloudUpload size={64} className="text-gray-300" />
                    <div className="flex flex-col items-center">
                        <p>
                            Click here to open a file or drag and drop it here!
                        </p>
                        <p>Accepted file formats are: .csv, .xlsx, .xls</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
