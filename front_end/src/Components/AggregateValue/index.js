import React, {Fragment} from 'react'
import { useSelector } from 'react-redux'
import {
    formatValue
} from '../../Util'

const AggregateValue = ({rowIndex, actualsOnly}) => {
    const cells = useSelector(state => state.allCells.cells[rowIndex]);

    let total = 0

    for (let i = 1; i < 13; i++) {
        if (!cells[i] || (actualsOnly && cells[i].isEditable))
            continue

        total += cells[i].amount
    }

    return (
        <Fragment>{formatValue(total / 100)}</Fragment>
    );
}

export default AggregateValue
