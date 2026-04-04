export function isSystemBlock(kind: string): boolean {
	return ["metadata", "datasets", "jobs"].includes(kind);
}
