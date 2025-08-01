import { BrowserRouter, Route, Routes } from "react-router";
import App from "./App";
import { SidebarSplitLayout } from "./pages/layouts/sidebar-split.layout";
import { UploadDatasetPage } from "./pages/upload-dataset.page";

export function Router() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<SidebarSplitLayout />}>
                    <Route index element={<App />} />
                    <Route path="datasets" element={<UploadDatasetPage />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
}
