import React from "react";
import { useTable, usePagination } from "react-table";
import { MdOutlineKeyboardDoubleArrowLeft, MdOutlineKeyboardArrowLeft, MdOutlineKeyboardArrowRight, MdOutlineKeyboardDoubleArrowRight } from "react-icons/md"

const Table = ({ columns, data }) => {
    const { 
        getTableProps, 
        getTableBodyProps, 
        headerGroups, 
        // rows, 
        page, 
        prepareRow,
        pageOptions,
        pageCount,
        gotoPage,
        nextPage,
        previousPage, state } = useTable({ columns, data }, usePagination);

    return (
        <>
            <div className="mt-4 flex flex-col">
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
                                {page.map((row) => {
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
                <div className="py-3 flex items-center justify-between">
                    <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
                        <div className="flex gap-x-2 items-baseline">
                            <span className="text-sm text-gray-700">
                                <span className="font-medium">{pageOptions.length} 페이지 중 </span><span className="font-medium">{state.pageIndex + 1} 페이지</span>
                            </span>
                        </div>
                        <div>
                            <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                                <button
                                    type="button"
                                    className="relative inline-flex items-center px-2 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                                    onClick={() => gotoPage(0)}
                                >

                                    <MdOutlineKeyboardDoubleArrowLeft className="h-5 w-5 text-gray-400" aria-hidden="true" />
                                </button>

                                <button
                                    type="button"
                                    className="relative inline-flex items-center px-2 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                                    onClick={() => previousPage()}
                                >
                                    <MdOutlineKeyboardArrowLeft className="h-5 w-5 text-gray-400" aria-hidden="true" />
                                </button>

                                <button
                                    type="button"
                                    className="relative inline-flex items-center px-2 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                                    onClick={() => nextPage()}
                                >
                                    <MdOutlineKeyboardArrowRight className="h-5 w-5 text-gray-400" aria-hidden="true" />
                                </button>

                                <button
                                    type="button"
                                    className="relative inline-flex items-center px-2 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                                    onClick={() => gotoPage(pageCount - 1)}
                                >
                                    <MdOutlineKeyboardDoubleArrowRight className="h-5 w-5 text-gray-400" aria-hidden="true" />
                                </button>
                            </nav>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Table;