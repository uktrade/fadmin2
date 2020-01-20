import React, {Fragment } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import TableCell from '../../Components/TableCell/index'
import InfoCell from '../../Components/InfoCell/index'
import CellValue from '../../Components/CellValue/index'
import AggregateValue from '../../Components/AggregateValue/index'
import TableHeader from '../../Components/TableHeader/index'
import TotalRow from '../../Components/TotalRow/index'
import TotalAggregate from '../../Components/TotalAggregate/index'
import { SET_SELECTED_ROW, SELECT_ALL } from '../../Reducers/Selected'


function Table({rowData, sheetUpdating}) {
    const dispatch = useDispatch();
    const rows = useSelector(state => state.allCells.cells);

    return (
        <Fragment>
            <table
                className="govuk-table" id="forecast-table">
                <caption className="govuk-table__caption govuk-!-font-size-27">Edit forecast</caption>
                <thead className="govuk-table__head">
                    <tr index="0">
                        <td className="handle govuk-table__cell indicate-action">
                            <button className="link-button"
                                id="select_all"                          
                                onMouseDown={() => { 
                                    dispatch(
                                        SELECT_ALL()
                                    );
                                }
                            }>select all</button>
                        </td>
                        <TableHeader id="natural_account_code_header" headerType="natural_account_code">NAC</TableHeader>
                        <TableHeader headerType="programme">Programme</TableHeader>
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
                        <th className="govuk-table__header">Year to date</th>
                        <th className="govuk-table__header">Year total</th>
                    </tr>
                </thead>
                <tbody className="govuk-table__body">
                    {rows.map((cells, rowIndex) => {
                        return <tr key={rowIndex} index={(rowIndex + 1)}>
                            <td id={"select_" + rowIndex} className="handle govuk-table__cell indicate-action">
                                <button
                                    className="select_row_btn link-button"
                                    id={"select_row_" + rowIndex}
                                    onMouseDown={() => { 
                                        dispatch(
                                            SET_SELECTED_ROW({
                                                selectedRow: rowIndex
                                            })
                                        );
                                    }
                                }>select</button>
                            </td>
                            <InfoCell cellKey={"natural_account_code"} rowIndex={rowIndex}>
                                <CellValue rowIndex={rowIndex} cellKey={"natural_account_code"} />
                            </InfoCell>
                            <InfoCell cellKey={"programme"} rowIndex={rowIndex}>
                                <CellValue rowIndex={rowIndex} cellKey={"programme"} />
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
                            <InfoCell cellKey={"budget"} rowIndex={rowIndex}>
                                <CellValue rowIndex={rowIndex} cellKey={"budget"} />
                            </InfoCell>
                            <TableCell sheetUpdating={sheetUpdating} rowIndex={rowIndex} cellKey={1} />
                            <TableCell sheetUpdating={sheetUpdating} rowIndex={rowIndex} cellKey={2} />
                            <TableCell sheetUpdating={sheetUpdating} rowIndex={rowIndex} cellKey={3} />
                            <TableCell sheetUpdating={sheetUpdating} rowIndex={rowIndex} cellKey={4} />
                            <TableCell sheetUpdating={sheetUpdating} rowIndex={rowIndex} cellKey={5} />
                            <TableCell sheetUpdating={sheetUpdating} rowIndex={rowIndex} cellKey={6} />
                            <TableCell sheetUpdating={sheetUpdating} rowIndex={rowIndex} cellKey={7} />
                            <TableCell sheetUpdating={sheetUpdating} rowIndex={rowIndex} cellKey={8} />
                            <TableCell sheetUpdating={sheetUpdating} rowIndex={rowIndex} cellKey={9} />
                            <TableCell sheetUpdating={sheetUpdating} rowIndex={rowIndex} cellKey={10} />
                            <TableCell sheetUpdating={sheetUpdating} rowIndex={rowIndex} cellKey={11} />
                            <TableCell sheetUpdating={sheetUpdating} rowIndex={rowIndex} cellKey={12} />
                            <InfoCell rowIndex={rowIndex}>
                                <AggregateValue rowIndex={rowIndex} actualsOnly={true} />
                            </InfoCell>
                            <InfoCell rowIndex={rowIndex}>
                                <AggregateValue rowIndex={rowIndex} actualsOnly={false} />
                            </InfoCell>
                        </tr>
                    })}
                    <tr>
                        <td className="govuk-table__cell total">Totals</td>
                        <InfoCell cellKey={"natural_account_code"} />
                        <InfoCell cellKey={"programme"} />
                        <InfoCell cellKey={"analysis1_code"} />
                        <InfoCell cellKey={"analysis2_code"} />
                        <InfoCell cellKey={"project_code"} />
                        <InfoCell cellKey={"budget"} />
                        <TotalRow month={1} />
                        <TotalRow month={2} />
                        <TotalRow month={3} />
                        <TotalRow month={4} />
                        <TotalRow month={5} />
                        <TotalRow month={6} />
                        <TotalRow month={7} />
                        <TotalRow month={8} />
                        <TotalRow month={9} />
                        <TotalRow month={10} />
                        <TotalRow month={11} />
                        <TotalRow month={12} />
                        <TotalAggregate actualsOnly={true} id="year-to-date" />
                        <TotalAggregate actualsOnly={false} id="year-total" />
                    </tr>
                </tbody>
            </table>
        </Fragment>
    );
}

export default Table
