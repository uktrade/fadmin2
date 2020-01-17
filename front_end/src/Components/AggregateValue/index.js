import React, {Fragment} from 'react'
import { useSelector } from 'react-redux'

const AggregateValue = ({rowIndex, actualsOnly}) => {
    const cells = useSelector(state => state.allCells.cells[rowIndex]);

    let total = 0

    for (let i = 1; i < 13; i++) {
    	if (actualsOnly && cells[i].isEditable)
    		continue

    	total += cells[i].amount
    }

    return (
    	<Fragment>{total / 100}</Fragment>
    );
}

export default AggregateValue
