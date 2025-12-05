import { existsSync } from "node:fs";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

const PACKAGES_DIR = path.join(import.meta.dirname, "..", "packages");

function generatePackageJson(name: string) {
    const p = {
        name,
        type: "module",
    };

    return JSON.stringify(p, null, 4);
}

async function main(args: string[]) {
    const [name] = args;
    if (!name) throw new Error("`create-package` receives a name.");

    const packageFolder = path.join(PACKAGES_DIR, name);

    console.log(`Creating package \`${name}\`...`);
    console.log(`Checking if ${packageFolder} exists`);

    if (!existsSync(packageFolder)) mkdir(packageFolder);
    const packageJson = generatePackageJson(name);

    const packageJsonPath = path.join(packageFolder, "package.json");
    await writeFile(packageJsonPath, packageJson, { encoding: "utf-8" });
}

main(process.argv.slice(2))
    .then((_) => console.log("`create-package` ran successfully"))
    .catch((e) =>
        console.error(`\`Error while running \`create-package\`:\n${e}`),
    );
