import React, {Fragment, useState, useEffect } from 'react';

import Table from '../../Components/Table/index'
import Selection from '../../Components/Selection/index'
import EditCell from '../../Components/EditCell/index'

import { useDispatch } from 'react-redux';
import { SET_CELL_COUNT } from '../../Reducers/CellCount'

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
            let cellDatas = []
            let colIndex = 0
            for (let key in rowdata) {
                let editable = false;

                for (let i = 0; i < window.editable_periods.length; i++) {
                    let shortName = window.editable_periods[i]["fields"]["period_short_name"];
                    if (shortName && shortName.toLowerCase() == key) {
                        editable = true;
                        break;
                    }
                }

                let cell = {
                    rect: null,
                    id: getCellId(key, rowIndex),
                    index: cellIndex,
                    colIndex: colIndex,
                    rowIndex: rowIndex,
                    key: key,
                    value: rowdata[key],
                    editable: editable,
                    selected: false,
                    editing: false,
                    programmeCode: `${rowData["programme__programme_description"]} - ${rowData["programme__programme_code"]}`,
                    nac: `${rowData["programme__programme_description"]} - ${rowData["programme__programme_code"]}`,
                    analysis1: "analysis 1",
                    analysis2: "analysis 2",
                    projectCode: `${rowData["project_code__project_description"]} - ${rowData["project_code__project_code"]}`
                }

                if (months.includes(cell.key.toLowerCase())) {
                    cellCounter++
                }

                cellDatas.push(cell)
                cellIndex++
                colIndex++
            }
            rows.push(cellDatas)
        });

        setRowData(rows)

        dispatch(
            SET_CELL_COUNT({
                "cellCount": cellCounter
            })
        );
    }

    return (
        <Fragment>
            <a href="">Show natural account code</a>
            <a href="">Show natural account code</a>

            <EditCell />
            <Selection />
            <Table rowData={rowData} />
        </Fragment>
    );
}

export default ForecastTable;
