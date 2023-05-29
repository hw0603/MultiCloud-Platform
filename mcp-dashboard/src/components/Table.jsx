import React from "react";
import { useTable } from "react-table";

const Table = ({ columns, data }) => {
    const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = useTable({ columns, data });

    return (
        <>
            <div className="flex flex-col overflow-x-auto">
                <div className="border-2 rounded-2xl overflow-hidden">
                    <table {...getTableProps()} className="min-w-full">
                        <thead className="bg-gray-200">
                            {headerGroups.map((headerGroup) => (
                                <tr {...headerGroup.getHeaderGroupProps()}>
                                    {headerGroup.headers.map((column) => (
                                        <th 
                                        {...column.getHeaderProps()} 
                                        className="p-3"
                                        >
                                            {column.render("Header")}</th>
                                    ))}
                                </tr>
                            ))}
                        </thead>

                        <tbody {...getTableBodyProps()}>
                            {rows.map((row) => {
                                prepareRow(row);
                                return (
                                    <tr {...row.getRowProps()} className="text-center odd:bg-white even:bg-gray-100 text-sm">
                                        {row.cells.map((cell) => (
                                            <td 
                                            {...cell.getCellProps()}
                                            className="px-6 py-4"
                                            >{cell.render("Cell")}</td>
                                        ))}
                                    </tr>
                                )
                            })}
                        </tbody>
                    </table>

                </div>
            </div>
        </>
    )
}

export default Table;