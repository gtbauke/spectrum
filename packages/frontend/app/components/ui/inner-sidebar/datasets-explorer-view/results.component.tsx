import { DatasetItem } from "./dataset-item.component";

export function Results() {
    return (
        <div className="flex-1 overflow-y-auto custom-scrollbar p-2 space-y-6">
            <section>
                <h3 className="px-2 mb-2 text-[9px] font-bold text-gray-600 uppercase">
                    Recent
                </h3>
                <div className="space-y-1">
                    <DatasetItem name="user_behavior_v1" type="CSV" size="1.2GB" />
                    <DatasetItem
                        name="sensor_logs_prod"
                        type="SQL"
                        size="450MB"
                        active
                    />
                </div>
            </section>

            <section>
                <h3 className="px-2 mb-2 text-[9px] font-bold text-gray-600 uppercase">
                    Shared Workspace
                </h3>
                <div className="space-y-1">
                    <DatasetItem name="weather_metrics_2024" type="JSON" size="12MB" />
                    <DatasetItem
                        name="patient_records_anonymized"
                        type="CSV"
                        size="89MB"
                    />
                </div>
            </section>
        </div>
    );
}
