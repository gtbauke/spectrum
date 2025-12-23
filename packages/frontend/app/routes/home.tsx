import Papa from "papaparse";
import { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { AiOutlineCloudUpload, AiOutlineFileExcel } from "react-icons/ai";
import { useNavigate } from "react-router";
import { useDatasetCreationContext } from "~/contexts/dataset-creation.context";
import type { DatasetFile } from "~/models/dataset.model";
import { cn } from "~/utils/classname.util";
import { MainContainer } from "../components/layout/main.component";
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
    const { setFile } = useDatasetCreationContext();
    const navigate = useNavigate();

    const onDrop = useCallback(
        (acceptedFiles: File[]) => {
            if (acceptedFiles.length > 0) {
                Papa.parse(acceptedFiles[0], {
                    delimiter: ",",
                    header: true,
                    worker: true,
                    chunkSize: 1024 * 1024,
                    skipEmptyLines: true,
                    complete: (res) => {
                        const headers = res.meta.fields || [];

                        if (typeof res.data[0] !== "object") {
                            console.error("Received non object element");
                        }

                        const data = (res.data as Record<string, string>[]).map(
                            (r) =>
                                Object.keys(r).reduce(
                                    (acc, key) => {
                                        acc[key] = Number(r[key]);
                                        return acc;
                                    },
                                    {} as Record<string, number>,
                                ),
                        );

                        const datasetFile: DatasetFile = {
                            header: headers,
                            rows: data,
                        };

                        setFile(datasetFile);
                    },
                    error: (err) => console.error(err),
                });

                navigate("/datasets", { replace: true });
            }
        },
        [setFile, navigate],
    );

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            "text/csv": [".csv"],
        },
        maxFiles: 1,
    });

    return (
        <MainContainer>
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
        </MainContainer>
    );
}
