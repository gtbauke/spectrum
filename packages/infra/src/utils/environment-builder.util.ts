import { writeFile } from "node:fs/promises";

export class EnvironmentBuilder {
    private readonly values: Map<string, unknown> = new Map();

    public set(key: string, value: unknown): EnvironmentBuilder {
        this.values.set(key, value);
        return this;
    }

    public extend(): EnvironmentBuilder {
        const newBuilder = new EnvironmentBuilder();
        for (const [key, value] of this.values) {
            newBuilder.set(key, value);
        }

        return newBuilder;
    }

    public async build(filePath: string): Promise<void> {
        const fileContent = this.buildFile();
        await writeFile(filePath, fileContent, { encoding: "utf-8" });
    }

    public buildFile(): string {
        const lines: string[] = [];

        for (const [key, value] of this.values) {
            let formattedValue: string;

            if (typeof value === "string") {
                formattedValue = `"${value.replace(/"/g, '\\"')}"`;
            } else if (
                typeof value === "number" ||
                typeof value === "boolean"
            ) {
                formattedValue = value.toString();
            } else if (value === null) {
                formattedValue = "null";
            } else if (Array.isArray(value) || typeof value === "object") {
                formattedValue = JSON.stringify(value);
            } else {
                throw new Error(
                    `Unsupported value type for key "${key}": ${typeof value}`,
                );
            }

            lines.push(`${key} = ${formattedValue}`);
        }

        return lines.join("\n");
    }
}
