DB_NAME="spectrum"
DB_USER="postgres"
DB_HOST="localhost"
DB_PORT="5432"
TABLE_NAME="job_runs"

read -p "Are you sure you want to delete ALL entries from table '$TABLE_NAME'? (y/N): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Aborted"
    exit 1
fi

psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "DELETE FROM $TABLE_NAME;"

echo "All rows deleted from '$TABLE_NAME'."
