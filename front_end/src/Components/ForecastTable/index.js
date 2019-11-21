import React, {Fragment, useState, useEffect } from 'react';
import Table from '../../Components/Table/index'
import { useDispatch } from 'react-redux';
import { TOGGLE_NAC, TOGGLE_PROG } from '../../Reducers/ShowHideCols'

import {
    getCellId,
    months
} from '../../Util'

function ForecastTable() {
    const dispatch = useDispatch();

    const [rowData, setRowData] = useState([]);

    const timer = () => {
            setTimeout(() => {
            if (window.table_data) {
                loadData()
            } else {
                timer()
            }
        }, 100);
    }

    useEffect(() => {
        timer()
    }, [])

    const loadData = () => {
        let cellCounter = -1
        let cellIndex = 0;
        let rows = [];
        window.table_data.forEach(function (rowdata, rowIndex) {
            let cells = {}
            let colIndex = 0
            for (let key in rowdata) {
                let editable = true;

                for (let i = 0; i < window.actuals_periods.length; i++) {
                    let shortName = window.actuals_periods[i]["fields"]["period_short_name"];

                    if (shortName == key) {
                        editable = false;
                        break;
                    }
                }

                cells[key] = {
                    id: getCellId(key, rowIndex),
                    index: cellIndex,
                    rowIndex: rowIndex,
                    colIndex: colIndex,
                    editable: editable,
                    key: key,
                    value: rowdata[key],
                    programmeCode: `${rowData["programme__programme_description"]} - ${rowData["programme__programme_code"]}`,
                    nac: `${rowData["natural_account_code__natural_account_code_description"]} - ${rowData["natural_account_code__natural_account_code"]}`,
                    analysis1: "analysis 1",
                    analysis2: "analysis 2",
                    projectCode: `${rowData["project_code__project_description"]} - ${rowData["project_code__project_code"]}`
                }

                cellIndex++
                colIndex++
            }
            rows.push(cells)
        });

        console.log(rows)

        setRowData(rows)
    }

    return (
        <Fragment>
            <p>
                <a
                    href="#"
                    onClick={(e) => {
                        dispatch(
                            TOGGLE_NAC()
                        );
                        e.preventDefault()
                    }}
                >Toggle NAC</a>
            </p>
            <p>
                <a
                    href="#"
                    onClick={(e) => {
                        dispatch(
                            TOGGLE_PROG()
                        );
                        e.preventDefault()
                    }}
                >Toggle programme</a>
            </p>
            <Table rowData={rowData} />
        </Fragment>
    );
}

export default ForecastTable;
