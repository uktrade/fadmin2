import React, {Fragment} from 'react'
import { useSelector } from 'react-redux'

const CellValue = ({rowIndex, cellKey}) => {
    const cell = useSelector(state => state.allCells.cells[rowIndex][cellKey]);

    console.log("cell", cell, rowIndex, cellKey)

    return (
    	<Fragment>
    		{cell.value}
    	</Fragment>
    );
}

export default CellValue
