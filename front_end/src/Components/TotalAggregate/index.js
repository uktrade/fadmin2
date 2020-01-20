import React from 'react'
import { useSelector } from 'react-redux'
import {
    formatValue
} from '../../Util'

const TotalAggregate = ({rowIndex, actualsOnly, id}) => {
    const cells = useSelector(state => state.allCells.cells);

    let total = 0

    // eslint-disable-next-line
    for (const cell of cells) {
        for (let i = 1; i < 13; i++) {
            if (actualsOnly && cell[i].isEditable)
                continue

            total += cell[i].amount
        }
    }

    return (
        <td id={id} className="govuk-table__cell forecast-month-cell not-editable">{formatValue(total / 100)}</td>
    );
}

export default TotalAggregate
