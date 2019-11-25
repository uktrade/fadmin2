import React, {Fragment, useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import Table from '../../Components/Table/index'
import { TOGGLE_NAC, TOGGLE_PROG } from '../../Reducers/ShowHideCols'
import {
    getCellId,
    months,
    postData,
    processForecastData
} from '../../Util'


function ForecastTable() {
    const dispatch = useDispatch();

    const [rowData, setRowData] = useState([]);
    const selectedRow = useSelector(state => state.selected.selectedRow)

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

    useEffect(() => {
        const capturePaste = (event) => {

            if (!event)
                return

            let clipBoardContent = event.clipboardData.getData('text/plain')
            let form = document.getElementById("id_paste_data_form")

            let payload = new FormData()
            payload.append("paste_content", clipBoardContent)



            if (selectedRow) {
                console.log("rowData[selectedRow]", rowData[selectedRow])
                payload.append("pasted_at_row", JSON.stringify(rowData[selectedRow]))
            }

            setRowData([])

            const response = postData(
                '/forecast/paste-forecast/888812/',
                payload
            ).then((response) => {
                let rows = processForecastData(response)
                setRowData(rows)
            })
            




            // if (response.error) {
            //     console.log(response["error"])
            // } else {
            //     console.log(response)
            //     console.log("Processing response...")

            //     let rows = processForecastData(response)
            //     setRowData(rows)

            //     console.log('Setting rows...')
            // }

            // setRowData([])
        };
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
    }, [setRowData, selectedRow]);

    // async function capturePaste(event) {
    //     let clipBoardContent = event.clipboardData.getData('text/plain')
    //     let form = document.getElementById("id_paste_data_form")

    //     let payload = new FormData()
    //     payload.append("paste_content", clipBoardContent)

    //     const response = await postData(
    //         '/forecast/paste-forecast/888812/',
    //         payload
    //     );

    //     if (response.error) {
    //         console.log(response["error"])
    //     } else {
    //         console.log(response)
    //         console.log("Processing response...")

    //         let rows = processForecastData(response)
    //         setRowData(rows)

    //         console.log(rows)
    //     }
    // }

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
