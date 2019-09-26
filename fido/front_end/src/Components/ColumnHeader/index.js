import React, {Fragment, useState, useEffect, useRef, useContext } from 'react';

import RowContext from '../../Components/RowContext'

function ColumnHeader({children, colKey}) {
    const context = useContext(RowContext)

    return (
        <th className="govuk-table__header"
            onClick={() => {
                context.selectColumn(colKey);
            }
        }>
            {children}
        </th>
    );
}

export default ColumnHeader;
