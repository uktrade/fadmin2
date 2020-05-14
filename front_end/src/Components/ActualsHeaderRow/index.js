import React, { useEffect, useState } from 'react'

const ActualsHeaderRow = () => {
    const [numActuals, setNumActuals] = useState(0)

    useEffect(() => {
        const timer = () => {
                setTimeout(() => {
                if (window.actuals) {
                    console.log("window.actuals loaded", window.actuals)
                    if (window.actuals.length > 0) {
                        console.log("window.actuals length", window.actuals.length)
                        setNumActuals(window.actuals.length)
                    }
                } else {
                    timer()
                }
            }, 100);
        }
        timer()
    }, [])

    return (
        <tr>
            <th className="govuk-table__head meta-col" colspan="9"></th>
            {numActuals > 0 &&
                <th id="actuals_header" className="govuk-table__head meta-col" colspan={ numActuals }>Actuals</th>
            }
            <th className="govuk-table__head meta-col" colspan={ 18 - numActuals }>Forecast</th>
        </tr>
    );
}

export default ActualsHeaderRow
