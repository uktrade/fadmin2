import React, {Fragment, useState, useEffect, useRef, memo } from 'react'
import { isHidden } from '../../Util';

const TableHeader = ({children, headerType, isHidden}) => {
    return (
            <th
                className={"govuk-table__header " + (isHidden(headerType) ? 'hidden' : '')}
            >
                {children}
            </th>
    );
}

export default TableHeader
