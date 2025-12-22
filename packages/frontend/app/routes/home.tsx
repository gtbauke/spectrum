import { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { AiOutlineCloudUpload, AiOutlineFileExcel } from "react-icons/ai";
import { cn } from "~/utils/classname.util";
import type { Route } from "./+types/home";

export function meta(_: Route.MetaArgs) {
    return [
        { title: "Spectrum" },
        {
            name: "description",
            content: "The web platform for Symbolic Regression",
        },
    ];
}

export default function Home() {
    const onDrop = useCallback((acceptedFiles: File[]) => {
        console.log(acceptedFiles);
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            "text/csv": [".csv"],
        },
        maxFiles: 1,
    });

    return (
        <main className="container mx-auto pt-16 p-4 w-full">
            <div className="text-center">
                <h1 className="text-4xl font-bold">Welcome to Spectrum</h1>
                <p className="mt-2 text-gray-300">
                    The web platform for Symbolic Regression
                </p>
            </div>

            <div
                {...getRootProps()}
                className={cn(
                    "group border-2 border-dashed border-white rounded-lg p-4 mt-8 max-w-lg mx-auto hover:border-blue-400 cursor-pointer transition-colors",
                    isDragActive && "border-blue-400",
                )}
            >
                <input {...getInputProps()} />
                <div className="flex flex-col items-center justify-center h-48">
                    {isDragActive ? (
                        <AiOutlineFileExcel
                            className={cn(
                                "mx-auto text-6xl text-gray-400 group-hover:text-blue-400 transition-colors",
                                isDragActive && "text-blue-400",
                            )}
                        />
                    ) : (
                        <AiOutlineCloudUpload
                            className={cn(
                                "mx-auto text-6xl text-gray-400 group-hover:text-blue-400 transition-colors",
                                isDragActive && "text-blue-400",
                            )}
                        />
                    )}
                    <p
                        className={cn(
                            "mt-4 text-center text-gray-400 group-hover:text-blue-400 transition-colors",
                            isDragActive && "text-blue-400",
                        )}
                    >
                        {isDragActive
                            ? "Drop your dataset here to get started!"
                            : "Upload your dataset or drop the file here to get started!"}
                    </p>
                </div>
            </div>
        </main>
    );
}
