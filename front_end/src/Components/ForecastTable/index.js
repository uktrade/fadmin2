import React, {Fragment, useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import Table from '../../Components/Table/index'
import { TOGGLE_NAC, TOGGLE_PROG } from '../../Reducers/ShowHideCols'
import { SET_ERROR } from '../../Reducers/Error'
import {
    getCellId,
    months,
    postData,
    processForecastData
} from '../../Util'


function ForecastTable() {
    const dispatch = useDispatch();

    const [rowData, setRowData] = useState([]);
    const errorMessage = useSelector(state => state.error.errorMessage)
    const selectedRow = useSelector(state => state.selected.selectedRow)
    const allSelected = useSelector(state => state.selected.all)

    const timer = () => {
            setTimeout(() => {
            if (window.table_data) {
                let rows = processForecastData(window.table_data)
                setRowData(rows)
            } else {
                timer()
            }
        }, 100);
    }

    useEffect(() => {
        timer()
    }, []);

    const capturePaste = (event) => {
        if (!event)
            return

        if (selectedRow < 0 && !allSelected) {
            return
        }

        dispatch(
            SET_ERROR({
                errorMessage: null
            })
        );

        let clipBoardContent = event.clipboardData.getData('text/plain')
        let form = document.getElementById("id_paste_data_form")

        let payload = new FormData()
        payload.append("paste_content", clipBoardContent)

        if (allSelected) {
            payload.append("all_selected", allSelected)
        } else {

            if (selectedRow > -1) {
                payload.append("pasted_at_row", JSON.stringify(rowData[selectedRow]))
            }
        }

        setRowData([])

        const response = postData(
            '/forecast/paste-forecast/888812/',
            payload
        ).then((response) => {
            if (response.status === 200) {
                let rows = processForecastData(response.data)
                setRowData(rows)
            } else {
                dispatch(
                    SET_ERROR({
                        errorMessage: response.data.error
                    })
                );
                setRowData(window.rowCache)
            }
        })
    };

    useEffect(() => {
        capturePaste();
        //window.addEventListener("mousedown", captureMouseDn);
        //window.addEventListener("mouseup", captureMouseUp);
        document.addEventListener("paste", capturePaste)
        // window.addEventListener("keydown", handleKeyDown);
        // window.addEventListener("copy", setClipBoardContent);

        return () => {
           //window.removeEventListener("onmouseup", captureMouseUp);
            //window.removeEventListener("mousedown", captureMouseDn);
            document.removeEventListener("paste", capturePaste)
            // window.removeEventListener("keydown", handleKeyDown);
            // window.removeEventListener("copy", setClipBoardContent);
        };
    }, [setRowData, selectedRow, allSelected]);

    return (
        <Fragment>
            {errorMessage != null &&
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
