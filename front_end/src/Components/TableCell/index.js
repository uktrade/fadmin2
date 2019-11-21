import React, {Fragment, useState, useEffect, useRef, memo } from 'react'
import { useSelector, useDispatch } from 'react-redux'

const TableCell = ({cell, isHidden}) => {
    const dispatch = useDispatch();

    const [value, setValue] = useState(cell.value);
    const selectedRow = useSelector(state => state.selected.selectedRow);

    const isSelected = () => {
        return (selectedRow === cell.rowIndex)
    }

    const getClasses = () => {
        let hiddenResult = '';
        let editable = '';

        if (isHidden) {
            hiddenResult = isHidden(cell.key) ? ' hidden' : ''
        }

        if (!cell.editable) {
            editable = ' not-editable';
        }

        return "govuk-table__cell " + (isSelected() ? 'selected' : '') + hiddenResult + editable
    }

    return (
        <Fragment>
            <td
                className={getClasses()}

                onDoubleClick={ () => {
                    console.log("cellId", cell.id)
                }}

                onMouseOver={ () => {
                    console.log(value)

                }}

                onMouseUp={ () => {

                }}
            >
                <Fragment>
                    {value}
                </Fragment>
            </td>
        </Fragment>
    );
}

const comparisonFn = function(prevProps, nextProps) {
    return (
        prevProps.selectedRow === nextProps.selectedRow
    )
};

export default TableCell // memo(TableCell, comparisonFn);
