import { createContext, useContext, useState } from "react";
import type { DatasetFile } from "~/models/dataset.model";

export type DatasetCreationContextType = {
    file: DatasetFile | null;
    setFile: (file: DatasetFile | null) => void;
};

export const DatasetCreationContext =
    createContext<DatasetCreationContextType | null>(null);

export function useDatasetCreationContext() {
    const context = useContext(DatasetCreationContext);

    if (!context) {
        throw new Error(
            "useDatasetCreationContext must be used within a DatasetCreationProvider",
        );
    }

    return context;
}

export function DatasetCreationProvider({ children }: React.PropsWithChildren) {
    const [file, setFile] = useState<DatasetFile | null>(null);

    const contextValue = {
        file,
        setFile,
    };

    return (
        <DatasetCreationContext.Provider value={contextValue}>
            {children}
        </DatasetCreationContext.Provider>
    );
}
