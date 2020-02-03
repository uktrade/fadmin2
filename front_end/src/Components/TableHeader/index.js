import React, {useMemo} from 'react'
import { useSelector } from 'react-redux'

const TableHeader = ({children, headerType}) => {
    return (
        <th
            className={"govuk-table__header"}
        >
            {children}
        </th>
    );
}

export default TableHeader
