import React, {Fragment, useState, useEffect, useRef, memo } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import TableCell from '../../Components/TableCell/index'
import TableHeader from '../../Components/TableHeader/index'
import { SET_SELECTED_ROW } from '../../Reducers/Selected'

import {
    months,
    postData
} from '../../Util'

function Table({rowData}) {
    const dispatch = useDispatch();

    const [errorMessage, setErrorMessage] = useState(null);
    const [rows, setRows] = useState([]);
    const selectedRow = useSelector(state => state.selected.selectedRow);

    useEffect(() => {
        //window.addEventListener("mousedown", captureMouseDn);
        //window.addEventListener("mouseup", captureMouseUp);
        window.addEventListener("paste", capturePaste);
        // window.addEventListener("keydown", handleKeyDown);
        // window.addEventListener("copy", setClipBoardContent);

        return () => {
           //window.removeEventListener("onmouseup", captureMouseUp);
            //window.removeEventListener("mousedown", captureMouseDn);
            window.removeEventListener("paste", capturePaste);
            // window.removeEventListener("keydown", handleKeyDown);
            // window.removeEventListener("copy", setClipBoardContent);
        };
    }, [selectedRow]);

    async function capturePaste(event) {
        let clipBoardContent = event.clipboardData.getData('text/plain')
        let form = document.getElementById("id_paste_data_form")

        console.log(clipBoardContent)
        console.log("selectedRow", selectedRow)

        let payload = new FormData();
        payload.append("pasted_at_row", selectedRow)
        payload.append("paste_content", clipBoardContent)


        const response = await postData(
            '/forecast/paste-forecast/888812/',
            payload
        );
        //const test = await response.json();
        if (response.error) {
            console.log(response["error"])
        } else {
            console.log(response)
        }
        
    }

    useEffect(() => {
        setRows(rowData)
    }, [rowData]);

    const nac = useSelector(state => state.showHideCols.nac);
    const programme = useSelector(state => state.showHideCols.programme);
    const analysis1 = useSelector(state => state.showHideCols.analysis1);
    const analysis2 = useSelector(state => state.showHideCols.analysis2);
    const projectCode = useSelector(state => state.showHideCols.projectCode);

    const isHidden = (key) => {
        if (!nac && key === "cost_centre__cost_centre_code") {
            return true
        }

        if (!programme && key === "programme__programme_code") {
            return true
        }

        // if (!analysis1 && key === "cost_centre__cost_centre_code") {
        //     return true
        // }

        // if (!analysis2 && key === "cost_centre__cost_centre_code") {
        //     return true
        // }

        if (!projectCode && key === "project_code__project_code") {
            return true
        }

        return false
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
                    <tr index="0">
                        <th></th>
                        <TableHeader isHidden={isHidden} headerType="cost_centre__cost_centre_code">Natural Account Code</TableHeader>
                        <TableHeader isHidden={isHidden} headerType="programme__programme_code">Programme</TableHeader>
                        <TableHeader isHidden={isHidden} headerType="a1">Analysis Code Sector</TableHeader>
                        <TableHeader isHidden={isHidden} headerType="a2">Analysis Code Market</TableHeader>
                        <TableHeader isHidden={isHidden} headerType="project_code__project_code">Project Code</TableHeader>
                        <th className="govuk-table__header">Apr</th>
                        <th className="govuk-table__header">May</th>
                        <th className="govuk-table__header">Jun</th>
                        <th className="govuk-table__header">Jul</th>
                        <th className="govuk-table__header">Aug</th>
                        <th className="govuk-table__header">Sep</th>
                        <th className="govuk-table__header">Oct</th>
                        <th className="govuk-table__header">Nov</th>
                        <th className="govuk-table__header">Dec</th>
                        <th className="govuk-table__header">Jan</th>
                        <th className="govuk-table__header">Feb</th>
                        <th className="govuk-table__header">Mar</th>
                    </tr>
                </thead>
                <tbody className="govuk-table__body">
                    {rows.map((cells, rowIndex) => {
                        return <tr key={rowIndex} index={(rowIndex + 1)}>
                            <td className="handle govuk-table__cell indicate-action"
                                onClick={() => { 
                                    console.log(rowIndex)
                                    dispatch(
                                        SET_SELECTED_ROW({
                                            selectedRow: rowIndex
                                        })
                                    );
                                }
                            }>
                                select
                            </td>
                            <TableCell isHidden={isHidden} cell={cells["cost_centre__cost_centre_code"]} />
                            <TableCell isHidden={isHidden} cell={cells["programme__programme_code"]} />
                            <td className="govuk-table__cell">Analysis 1</td>
                            <td className="govuk-table__cell">Analysis 2</td>
                            <TableCell isHidden={isHidden} cell={cells["project_code__project_code"]} />
                            <TableCell cell={cells["Apr"]} />
                            <TableCell cell={cells["May"]} />
                            <TableCell cell={cells["Jun"]} />
                            <TableCell cell={cells["Jul"]} />
                            <TableCell cell={cells["Aug"]} />
                            <TableCell cell={cells["Sep"]} />
                            <TableCell cell={cells["Oct"]} />
                            <TableCell cell={cells["Nov"]} />
                            <TableCell cell={cells["Dec"]} />
                            <TableCell cell={cells["Jan"]} />
                            <TableCell cell={cells["Feb"]} />
                            <TableCell cell={cells["Mar"]} />
                        </tr>
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
