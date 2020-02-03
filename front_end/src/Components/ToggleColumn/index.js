import React, { useMemo } from 'react'
import { useSelector } from 'react-redux'

const ToggleColumn = ({columnName}) => {
    const hiddenCols = useSelector(state => state.hiddenCols.hiddenCols)
    const isHidden = hiddenCols.indexOf(columnName) > -1

    let visibilityType = "block"

    if (isHidden) {
    	visibilityType = "collapse"
    }

    return (
        <col style={{visibility: visibilityType}} />
    );
}

export default ToggleColumn
