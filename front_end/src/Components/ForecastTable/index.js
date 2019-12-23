import React, {Fragment, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import Table from '../../Components/Table/index'
import { SET_EDITING_CELL } from '../../Reducers/Edit'
import { store } from '../../Store';
import { 
    TOGGLE_NAC,
    TOGGLE_PROG, 
    TOGGLE_AN1,
    TOGGLE_AN2,
    TOGGLE_PROJ_CODE,

} from '../../Reducers/ShowHideCols'
import { SET_ERROR } from '../../Reducers/Error'
import { SET_CELLS } from '../../Reducers/Cells'

import {
    getCellId,
    postData,
    processForecastData
} from '../../Util'


function ForecastTable() {
    const dispatch = useDispatch();

    const nac = useSelector(state => state.showHideCols.nac);
    const programme = useSelector(state => state.showHideCols.programme);
    const analysis1 = useSelector(state => state.showHideCols.analysis1);
    const analysis2 = useSelector(state => state.showHideCols.analysis2);
    const projectCode = useSelector(state => state.showHideCols.projectCode);

    const errorMessage = useSelector(state => state.error.errorMessage)
    const selectedRow = useSelector(state => state.selected.selectedRow)
    const allSelected = useSelector(state => state.selected.all)

    const cells = useSelector(state => state.allCells.cells);

    useEffect(() => {
        const timer = () => {
                setTimeout(() => {
                if (window.table_data) {
                    let rows = processForecastData(window.table_data)

                    console.log(rows)
                      dispatch({
                        type: SET_CELLS,
                        cells: rows
                      })

                } else {
                    timer()
                }
            }, 100);
        }

        timer()
    }, [dispatch]);

    useEffect(() => {
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
            let payload = new FormData()
            payload.append("paste_content", clipBoardContent)

            if (allSelected) {
                payload.append("all_selected", allSelected)
            } else {
                if (selectedRow > -1) {
                    payload.append("pasted_at_row", JSON.stringify(cells[selectedRow]))
                }
            }

            postData(
                `/forecast/paste-forecast/${window.cost_centre}/`,
                payload
            ).then((response) => {
                if (response.status === 200) {
                    let rows = processForecastData(response.data)
                      dispatch({
                        type: SET_CELLS,
                        cells: rows
                      })
                } else {
                    dispatch(
                        SET_ERROR({
                            errorMessage: response.data.error
                        })
                    );
                }
            })
        }

        capturePaste();
        //window.addEventListener("mousedown", captureMouseDn);
        //window.addEventListener("mouseup", captureMouseUp);
        document.addEventListener("paste", capturePaste)
        //window.addEventListener("keydown", handleKeyDown);
        // window.addEventListener("copy", setClipBoardContent);

        return () => {
           //window.removeEventListener("onmouseup", captureMouseUp);
            //window.removeEventListener("mousedown", captureMouseDn);
            document.removeEventListener("paste", capturePaste)
            // window.removeEventListener("keydown", handleKeyDown);
            // window.removeEventListener("copy", setClipBoardContent);
        };
    }, [dispatch, cells, selectedRow, allSelected]);

    useEffect(() => {
        const handleKeyDown = (event) => {
            if (event.key === "Tab") {
                const state = store.getState();

                if (!state.edit.cellId)
                    return

                let idParts = state.edit.cellId.split("_")

                let month = parseInt(idParts[1])
                let rowIndex = parseInt(idParts[2])
                let next_id = null

                if (event.shiftKey) {
                    if (month === (4 + window.actuals.length)) {
                        month = 4
                    } else if (month === 1) {
                        month = 13
                    }
                    next_id = getCellId(month - 1, rowIndex)
                } else {
                    if (month === 12) {
                        month = 0
                    } else if (month === 3) {
                        month = 3 + window.actuals.length
                    }

                    next_id = getCellId(month + 1, rowIndex)
                }

                dispatch(
                    SET_EDITING_CELL({
                        "cellId": next_id
                    })
                );

                event.preventDefault()
            }
        }

        window.addEventListener("keydown", handleKeyDown);

        return () => {
            window.removeEventListener("keydown", handleKeyDown);
        };
    }, [dispatch]);

    return (
        <Fragment>
            {errorMessage != null &&
                <div className="govuk-error-summary" aria-labelledby="error-summary-title" role="alert" tabIndex="-1" data-module="govuk-error-summary">
                  <h2 className="govuk-error-summary__title" id="error-summary-title">
                    There is a problem
                  </h2>
                  <div className="govuk-error-summary__body">
                    <ul className="govuk-list govuk-error-summary__list">
                      <li id="paste_error_msg">
                        {errorMessage}
                      </li>
                    </ul>
                  </div>
                </div>
            }
            <div className="toggle-links">
                <button id="show_hide_nac"
                    onClick={(e) => {
                        dispatch(
                            TOGGLE_NAC()
                        );
                        e.preventDefault()
                    }}
                >{nac ? (
                        <Fragment>Hide</Fragment>
                    ) : (
                        <Fragment>Show</Fragment>
                    )} NAC</button>
                <button id="show_hide_prog"
                    onClick={(e) => {
                        dispatch(
                            TOGGLE_PROG()
                        );
                        e.preventDefault()
                    }}
                >{programme ? (
                        <Fragment>Hide</Fragment>
                    ) : (
                        <Fragment>Show</Fragment>
                    )} programme</button>
                <button id="show_hide_a1"
                    onClick={(e) => {
                        dispatch(
                            TOGGLE_AN1()
                        );
                        e.preventDefault()
                    }}
                >{analysis1 ? (
                        <Fragment>Hide</Fragment>
                    ) : (
                        <Fragment>Show</Fragment>
                    )} analysis code sector</button>
                <button id="show_hide_a2"
                    onClick={(e) => {
                        dispatch(
                            TOGGLE_AN2()
                        );
                        e.preventDefault()
                    }}
                >{analysis2 ? (
                        <Fragment>Hide</Fragment>
                    ) : (
                        <Fragment>Show</Fragment>
                    )} analysis code market</button>
                <button id="show_hide_proj"
                    onClick={(e) => {
                        dispatch(
                            TOGGLE_PROJ_CODE()
                        );
                        e.preventDefault()
                    }}
                >{projectCode ? (
                        <Fragment>Hide</Fragment>
                    ) : (
                        <Fragment>Show</Fragment>
                    )} project code</button>
            </div>            
            <Table />
        </Fragment>
    );
}

export default ForecastTable;
