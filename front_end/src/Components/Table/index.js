import React, {Fragment, useState, useEffect, useRef, memo } from 'react';
import { useDispatch } from 'react-redux';
import TableRow from '../../Components/TableRow/index'
import TableCell from '../../Components/TableCell/index'
import TableHandle from '../../Components/TableHandle/index'
import ColumnHeader from '../../Components/ColumnHeader/index'
import { SET_INITIAL, SET_LAST } from '../../Reducers/Select'

import {
    months
} from '../../Util'

/* TODO
List of selected cells
Pasting
Copying
Cut down cell loop to relevant cells
*/

function Table({rowData, cellCount}) {
    const dispatch = useDispatch();

    const [errorMessage, setErrorMessage] = useState(null);

    const mouseRef = useRef(false);
    const editCellRef = useRef(null)

    const rects = []

    const [rows, setRows] = useState([]);

    const [initialSelection, setInitialSelection] = useState([])
    const [lastSelection, setlastSelection] = useState([])


    useEffect(() => {
        window.addEventListener("mousedown", captureMouseDn);
        window.addEventListener("mouseup", captureMouseUp);
        // window.addEventListener("paste", capturePaste);
        // window.addEventListener("keydown", handleKeyDown);
        // window.addEventListener("copy", setClipBoardContent);

        return () => {
           window.removeEventListener("onmouseup", captureMouseUp);
            window.removeEventListener("mousedown", captureMouseDn);
            // window.removeEventListener("paste", capturePaste);
            // window.removeEventListener("keydown", handleKeyDown);
            // window.removeEventListener("copy", setClipBoardContent);
        };


    }, []);

    useEffect(() => {
        setRows(rowData)
    }, [rowData]);

    const updateRow = (cellId, row, property, value=true) => {
        let cellIndex = rows[row].findIndex(function(element) {
          return element.id === cellId
        });

        let newRows = [...rows];
        newRows[row][cellIndex][property] = value

        setRows(newRows);
    }

    const removeFromSelected = (arr, cellId) => {
        var index = arr.findIndex(cell => cell.id === cellId);
        if (index > -1) {
            arr.splice(index, 1);
        }

        return index
    }

    const mouseOverCell = (cellId, row, col, lastRect) => {
        if (mouseRef.current) {
                dispatch(
                    SET_LAST({
                        last: lastRect
                    })
                );
           }
    }

    const selectInitialCell = (cellId, row, col, rect) => {

        dispatch(
            SET_INITIAL({
                initial: rect
            })
        );

        dispatch(
            SET_LAST({
                last: rect
            })
        );
    }

    const mouseUpOnCell = (cellId, row, col) => {
        //setlastSelection([cellId, row, col])
    }

    const editCell = (cellId, row) => {
        let newRows = [...rows];

        let cellIndex = getCellIndex(cellId, row)
        newRows[row][cellIndex]["editing"] = true

        editCellRef.current = {
            id: cellId,
            row: row
        }

        //setRows(newRows)
    }

    const captureMouseUp = (e) => {
        mouseRef.current = false
    }

    const captureMouseDn = (e) => {
        mouseRef.current = true
    }

    const setRect = (cellId, row, rect) => {
        //console.log("Setitng rect...", cellCount, rects.length)

        rects.push(rect)

        if (cellCount === rects.length) {
            let newRows = [...rows];
            let rectCounter = 0

            newRows.forEach(function (row, i) {
                row.forEach(function (cellData, j) {
                    if (months.includes(cellData.key.toLowerCase())) {
                        newRows[i][j]["rect"] = rects[rectCounter]
                        rectCounter++
                    }
                })
            })

            setRows(newRows);
        }
    }

    const getCellData = (cellId, row) => {
        let index = getCellIndex(cellId, row)
        return rows[row][index]
    }

    const getCellIndex = (cellId, row) => {
        var cellIndex = rows[row].findIndex(function(element) {
          return element.id === cellId
        });

        return cellIndex
    }

    const [selectionArea, setSelectionArea] = useState({
        x: 0,
        y: 0,
        width: 0,
        height: 0
    });

    const createSelectionArea = () => {
        if (mouseRef.current && initialSelection && lastSelection) {
            let initial = getCellData(initialSelection.id, initialSelection.row)
            let last = getCellData(lastSelection.id, lastSelection.row)
        }
    }

    return (
        <Fragment>
            {errorMessage &&
                <div className="govuk-error-summary" aria-labelledby="error-summary-title" role="alert" tabIndex="-1" data-module="govuk-error-summary">
                    <h2 className="govuk-error-summary__title" id="error-summary-title">
                        There is a problem
                    </h2>
                    <div className="govuk-error-summary__body">
                        <ul className="govuk-list govuk-error-summary__list">
                            <li>
                                <a href="#passport-issued-error">{errorMessage}</a>
                            </li>
                        </ul>
                    </div>
                </div>
            }
            <table
                className="govuk-table" id="forecast-table">
                <caption className="govuk-table__caption">Edit forecast</caption>
                <thead className="govuk-table__head">
                    <TableRow index="0">
                        <th></th>
                        <th className="govuk-table__header ">Natural Account Code</th>
                        <th className="govuk-table__header ">Programme</th>
                        <th className="govuk-table__header ">Analysis Code Sector</th>
                        <th className="govuk-table__header ">Analysis Code Market</th>
                        <th className="govuk-table__header ">Project Code</th>
                        <ColumnHeader colKey="apr">Apr</ColumnHeader>
                        <ColumnHeader colKey="may">May</ColumnHeader>
                        <ColumnHeader colKey="jun">Jun</ColumnHeader>
                        <ColumnHeader colKey="jul">Jul</ColumnHeader>
                        <ColumnHeader colKey="aug">Aug</ColumnHeader>
                        <ColumnHeader colKey="sep">Sep</ColumnHeader>
                        <ColumnHeader colKey="oct">Oct</ColumnHeader>
                        <ColumnHeader colKey="nov">Nov</ColumnHeader>
                        <ColumnHeader colKey="dec">Dec</ColumnHeader>
                        <ColumnHeader colKey="jan">Jan</ColumnHeader>
                        <ColumnHeader colKey="feb">Feb</ColumnHeader>
                        <ColumnHeader colKey="mar">Mar</ColumnHeader>
                    </TableRow>
                </thead>
                <tbody className="govuk-table__body">
                    {rows.map((rowData, rowIndex) => {
                        //console.log("rowData from table...", rowData)
                        return <TableRow key={rowIndex} index={(rowIndex + 1)}>
                            <TableHandle rowIndex={rowIndex}>
                                H
                            </TableHandle>
                            <td>
                                {rowData["nac"]}
                            </td>
                            <td>
                                {rowData["programmeCode"]}
                            </td>

                            <td>
                                {rowData["analysis1"]}
                            </td>
                            <td>
                                {rowData["analysis2"]}
                            </td>
                            <td>
                                {rowData["projectCode"]}
                            </td>
                            {rowData.map((cell, cellIndex) => {
                                //console.log("cell key", cell.key.toLowerCase())

                                if (months.includes(cell.key.toLowerCase())) {
                                    return <TableCell
                                        row={rowIndex}
                                        col={cell.colIndex}
                                        key={cellIndex}
                                        index={cellIndex}
                                        cellId={cell.id}
                                        selected={cell.selected}
                                        selectInitialCell={selectInitialCell}
                                        initialValue={cell.value}
                                        mouseOverCell={mouseOverCell}
                                        mouseUpOnCell={mouseUpOnCell}
                                        setRect={setRect}
                                    />
                                }
                            })}
                        </TableRow>
                    })}
                </tbody>
            </table>
        </Fragment>
    );
}

const comparisonFn = function(prevProps, nextProps) {
    return (
        prevProps.rowData === nextProps.rowData
    )
};

export default memo(Table, comparisonFn);