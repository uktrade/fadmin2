import React, {Fragment, memo} from 'react'
import { useSelector } from 'react-redux'

import {
    formatValue
} from '../../Util'

const CellValue = ({rowIndex, cellKey, format}) => {
    const cell = useSelector(state => state.allCells.cells[rowIndex][cellKey]);

    const getValue = (value) => {
    	if (format) {
    		return formatValue(parseInt(value)/100)
    	}

    	return value
    }

    return (
    	<Fragment>
    		{getValue(cell.value)}
    	</Fragment>
    );
}


const comparisonFn = function(prevProps, nextProps) {
    return (
        prevProps.cell === nextProps.cell
    )
};

export default memo(CellValue, comparisonFn);
