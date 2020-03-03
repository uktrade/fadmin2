import React, {Fragment, useRef, useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { 
    TOGGLE_ITEM,
    TOGGLE_SHOW_ALL
} from '../../Reducers/HiddenCols'
import { 
    TOGGLE_FILTER,
} from '../../Reducers/Filter'


const EditActionBar = () => {
    const dispatch = useDispatch()
    const hiddenCols = useSelector(state => state.hiddenCols.hiddenCols)
    const filterOpen = useSelector(state => state.filter.open)
    const containerRef = useRef()

    useEffect(() => {
        let addForecastRow = document.getElementById("add_forecast_row")
        let downloadForecast = document.getElementById("download_forecast")

        containerRef.current.insertBefore(
            downloadForecast,
            containerRef.current.firstChild,
        )
        containerRef.current.insertBefore(
            addForecastRow,
            containerRef.current.firstChild,
        )
    }, [])

    const getClasses = () => {
        let classes = "filter-content-wrapper "

        if (filterOpen)
            classes += "filter-open"

        return classes
    }

    return (
        <div className="filter" ref={containerRef}>
            <div className="filter-by">
                <span className="govuk-body">Filter by </span>                
                <button id="filter-switch"
                    className="link-button govuk-link"
                    onClick={(e) => {
                        dispatch(
                            TOGGLE_FILTER()
                        );
                        e.preventDefault()
                    }}
                >
                    Table filters
                </button>
            </div>
 
            <div className={getClasses()}>
                <div className="filter-content">
                    <h3 className="govuk-heading-m">Table filters</h3>

                    <div class="govuk-checkboxes">
                        <div class="govuk-checkboxes__item">
                            <input
                                type="checkbox"
                                className="govuk-checkboxes__input"
                                checked={hiddenCols.indexOf("natural_account_code") === -1}
                                onChange={(e) => {
                                    dispatch(
                                        TOGGLE_SHOW_ALL()
                                    );
                                }}
                            />
                            <label class="govuk-label govuk-checkboxes__label" for="waste">
                                All columns
                            </label>
                        </div>
                    </div>

                    <div className="filter-cols">
                        <h4 className="govuk-heading-m">Table columns</h4>
                        <div class="govuk-checkboxes">
                            <div class="govuk-checkboxes__item">
                                <input
                                    type="checkbox"
                                    name="natural_account_code"
                                    className="govuk-checkboxes__input"
                                    checked={hiddenCols.indexOf("natural_account_code") === -1}
                                    onChange={(e) => {
                                        dispatch(
                                            TOGGLE_ITEM("natural_account_code")
                                        );
                                    }}
                                />
                                <label class="govuk-label govuk-checkboxes__label" for="natural_account_code">
                                    Natural account code
                                </label>
                            </div>
                            <div class="govuk-checkboxes__item">
                                <input
                                    type="checkbox"
                                    name="programme"
                                    className="govuk-checkboxes__input"
                                    checked={hiddenCols.indexOf("programme") === -1}
                                    onChange={(e) => {
                                        dispatch(
                                            TOGGLE_ITEM("programme")
                                        );
                                    }}
                                />
                                <label class="govuk-label govuk-checkboxes__label" for="programme">
                                    Programme
                                </label>
                            </div>
                            <div class="govuk-checkboxes__item">
                                <input
                                    type="checkbox"
                                    name="analysis1_code"
                                    className="govuk-checkboxes__input"
                                    checked={hiddenCols.indexOf("analysis1_code") === -1}
                                    onChange={(e) => {
                                        dispatch(
                                            TOGGLE_ITEM("analysis1_code")
                                        );
                                    }}
                                />
                                <label class="govuk-label govuk-checkboxes__label" for="analysis1_code">
                                    Analysis 1
                                </label>
                            </div>
                            <div class="govuk-checkboxes__item">
                                <input
                                    type="checkbox"
                                    name="analysis2_code"
                                    className="govuk-checkboxes__input"
                                    checked={hiddenCols.indexOf("analysis2_code") === -1}
                                    onChange={(e) => {
                                        dispatch(
                                            TOGGLE_ITEM("analysis2_code")
                                        );
                                    }}
                                />
                                <label class="govuk-label govuk-checkboxes__label" for="analysis2_code">
                                    Analysis 2
                                </label>
                            </div>
                            <div class="govuk-checkboxes__item">
                                <input
                                    type="checkbox"
                                    name="project_code"
                                    className="govuk-checkboxes__input"
                                    checked={hiddenCols.indexOf("project_code") === -1}
                                    onChange={(e) => {
                                        dispatch(
                                            TOGGLE_ITEM("project_code")
                                        );
                                    }}
                                />
                                <label class="govuk-label govuk-checkboxes__label" for="project_code">
                                    Project Code
                                </label>
                            </div>
                        </div> 
                    </div>
                </div>
            </div>
        </div>
    )
}

export default EditActionBar
