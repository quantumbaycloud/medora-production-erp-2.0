const DataTable = ({ columns, rows, rowKey = "id" }) => {
  return (
    <div className="overflow-hidden rounded-2xl border border-outline-variant bg-surface-container-lowest shadow-sm">
      <div className="overflow-x-auto">
        <table className="min-w-full">
          <thead className="bg-surface-container-low">
            <tr className="text-sm text-on-surface-variant">
              {columns.map((column) => (
                <th
                  key={column.key}
                  className={`px-6 py-4 text-left font-semibold ${
                    column.align === "right"
                      ? "text-right"
                      : column.align === "center"
                        ? "text-center"
                        : ""
                  }`}
                >
                  {column.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-outline-variant">
            {rows.map((row, index) => (
              <tr
                key={row[rowKey] ?? index}
                className="transition-colors hover:bg-surface-container-low"
              >
                {columns.map((column) => (
                  <td
                    key={column.key}
                    className={`px-6 py-4 text-sm ${
                      column.align === "right"
                        ? "text-right"
                        : column.align === "center"
                          ? "text-center"
                          : ""
                    }`}
                  >
                    {column.render
                      ? column.render(row)
                      : row[column.key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DataTable;