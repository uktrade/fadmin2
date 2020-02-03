import React, {Fragment } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import TableCell from '../../Components/TableCell/index'
import InfoCell from '../../Components/InfoCell/index'
import CellValue from '../../Components/CellValue/index'
import AggregateValue from '../../Components/AggregateValue/index'
import TableHeader from '../../Components/TableHeader/index'
import TotalCol from '../../Components/TotalCol/index'
import ToggleColumn from '../../Components/ToggleColumn/index'
import TotalAggregate from '../../Components/TotalAggregate/index'
import TotalBudget from '../../Components/TotalBudget/index'
import OverspendUnderspend from '../../Components/OverspendUnderspend/index'
import TotalOverspendUnderspend from '../../Components/TotalOverspendUnderspend/index'

import { SET_EDITING_CELL } from '../../Reducers/Edit'
import { SET_SELECTED_ROW, SELECT_ALL, UNSELECT_ALL } from '../../Reducers/Selected'


function Table({rowData, sheetUpdating}) {
    const dispatch = useDispatch();
    const rows = useSelector(state => state.allCells.cells);

    const selectedRow = useSelector(state => state.selected.selectedRow);
    const allSelected = useSelector(state => state.selected.all);

    return (
        <Fragment>
            <table
                className="govuk-table finance-table" id="forecast-table">
                <caption className="govuk-table__caption govuk-!-font-size-27">Edit forecast</caption>
                <colgroup>
                    <ToggleColumn columnName="natural_account_code" />
                    <ToggleColumn columnName="natural_account_code" />
                    <ToggleColumn columnName="programme" />
                    <ToggleColumn columnName="programme" />
                    <ToggleColumn columnName="analysis1_code" />
                    <ToggleColumn columnName="analysis2_code" />
                    <ToggleColumn columnName="budget" />
                </colgroup>
                <thead className="govuk-table__head">
                    <tr index="0">
                        <th className="handle govuk-table__cell indicate-action select-all">
                            <button className="link-button govuk-link"
                                id="select_all"                          
                                onMouseDown={() => {
                                    dispatch(
                                        SET_EDITING_CELL({
                                            "cellId": null
                                        })
                                    )
                                    if (allSelected) {
                                        dispatch(
                                            UNSELECT_ALL()
                                        )
                                    } else {
                                        dispatch(
                                            SELECT_ALL()
                                        )
                                    }
                                }
                            }>
                                {allSelected ? (
                                    <Fragment>unselect</Fragment>
                                ) : (
                                    <Fragment>select all</Fragment>
                                )}
                            </button>
                        </th>
                        <TableHeader id="natural_account_code_header" headerType="natural_account_code">NAC code</TableHeader>
                        <TableHeader headerType="natural_account_code">NAC description</TableHeader>
                        <TableHeader headerType="programme">Programme code</TableHeader>
                        <TableHeader headerType="programme">Programme description</TableHeader>
                        <TableHeader headerType="analysis1_code">Analysis Code Sector</TableHeader>
                        <TableHeader headerType="analysis2_code">Analysis Code Market</TableHeader>
                        <TableHeader headerType="project_code">Project Code</TableHeader>
                        <TableHeader headerType="budget">Budget</TableHeader>
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
                        {window.period_display && window.period_display.includes(13) &&
                            <th className="govuk-table__header">Adj 1</th>
                        }
                        {window.period_display && window.period_display.includes(14) &&
                            <th className="govuk-table__header">Adj 2</th>
                        }
                        {window.period_display && window.period_display.includes(15) &&
                            <th className="govuk-table__header">Adj 3</th>
                        }
                        <th className="govuk-table__header">Year to date</th>
                        <th className="govuk-table__header">Year total</th>
                        <th className="govuk-table__header">Underspend (Overspend)</th>
                    </tr>
                </thead>
                <tbody className="govuk-table__body">
                    {rows.map((cells, rowIndex) => {
                        return <tr key={rowIndex} index={(rowIndex + 1)}>
                            <td id={"select_" + rowIndex} className="handle govuk-table__cell indicate-action">
                                <button
                                    className="select_row_btn govuk-link link-button"
                                    id={"select_row_" + rowIndex}
                                    onMouseDown={() => {
                                        dispatch(
                                            SET_EDITING_CELL({
                                                "cellId": null
                                            })
                                        )
                                        if (selectedRow === rowIndex) {
                                            dispatch(
                                                SET_SELECTED_ROW({
                                                    selectedRow: null
                                                })
                                            )
                                        } else {
                                            dispatch(
                                                SET_SELECTED_ROW({
                                                    selectedRow: rowIndex
                                                })
                                            )
                                        }
                                    }
                                }>
                                    {selectedRow === rowIndex ? (
                                        <Fragment>unselect</Fragment>
                                    ) : (
                                        <Fragment>select</Fragment>
                                    )}
                                </button>
                            </td>
                            <InfoCell cellKey={"natural_account_code"} rowIndex={rowIndex}>
                                <CellValue rowIndex={rowIndex} cellKey={"natural_account_code"} />
                            </InfoCell>

                            <InfoCell cellKey={"nac_description"} rowIndex={rowIndex}>
                                <CellValue rowIndex={rowIndex} cellKey={"nac_description"} />
                            </InfoCell>

                            <InfoCell cellKey={"programme"} rowIndex={rowIndex}>
                                <CellValue rowIndex={rowIndex} cellKey={"programme"} />
                            </InfoCell>

                            <InfoCell cellKey={"programme_description"} rowIndex={rowIndex}>
                                <CellValue rowIndex={rowIndex} cellKey={"programme_description"} />
                            </InfoCell>

                            <InfoCell cellKey={"analysis1_code"} rowIndex={rowIndex}>
                                <CellValue rowIndex={rowIndex} cellKey={"analysis1_code"} />
                            </InfoCell>
                            <InfoCell cellKey={"analysis2_code"} rowIndex={rowIndex}>
                                <CellValue rowIndex={rowIndex} cellKey={"analysis2_code"} />
                            </InfoCell>
                            <InfoCell cellKey={"project_code"} rowIndex={rowIndex}>
                                <CellValue rowIndex={rowIndex} cellKey={"project_code"} />
                            </InfoCell>
                            <InfoCell className="figure-cell" cellKey={"budget"} rowIndex={rowIndex}>
                                <CellValue rowIndex={rowIndex} cellKey={"budget"} format={true} />
                            </InfoCell>
                            {window.period_display.map((value, index) => {
                                return <TableCell key={index} sheetUpdating={sheetUpdating} rowIndex={rowIndex} cellKey={value} />
                            })}
                            <InfoCell className="figure-cell" rowIndex={rowIndex}>
                                <AggregateValue rowIndex={rowIndex} actualsOnly={true} />
                            </InfoCell>
                            <InfoCell className="figure-cell" rowIndex={rowIndex}>
                                <AggregateValue rowIndex={rowIndex} actualsOnly={false} />
                            </InfoCell>
                            <InfoCell className="figure-cell" rowIndex={rowIndex}>
                                <OverspendUnderspend rowIndex={rowIndex} />
                            </InfoCell>
                        </tr>
                    })}
                    <tr>
                        <td className="govuk-table__cell total">Totals</td>
                        <InfoCell cellKey={"natural_account_code"} ignoreSelection={true} />
                        <InfoCell cellKey={"nac_description"} ignoreSelection={true} />
                        <InfoCell cellKey={"programme"} ignoreSelection={true} />
                        <InfoCell cellKey={"programme_description"} ignoreSelection={true} />
                        <InfoCell cellKey={"analysis1_code"} ignoreSelection={true} />
                        <InfoCell cellKey={"analysis2_code"} ignoreSelection={true} />
                        <InfoCell cellKey={"project_code"} ignoreSelection={true} />
                        <TotalBudget id="total-budget" cellKey={"budget"} />
                        {window.period_display && window.period_display.map((value, index) => {
                            return <TotalCol key={index} month={value} />
                        })}
                        <TotalAggregate actualsOnly={true} id="year-to-date" />
                        <TotalAggregate actualsOnly={false} id="year-total" />
                        <TotalOverspendUnderspend id="overspend-underspend-total" />
                    </tr>
                </tbody>
            </table>
        </Fragment>
    );
}

export default Table
