export const getCellId = (key, index) => {
    return "id_" + key + "_" + index;
}

export const months = [ 
    "apr", 
    "may", 
    "jun",
    "jul", 
    "aug", 
    "sep", 
    "oct", 
    "nov", 
    "dec",
    "jan", 
    "feb", 
    "mar"
];

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export async function postData(url = '', data = {}) {
    var csrftoken = getCookie('csrftoken');

    /*
    const defaults = {
      'method': 'POST',
      'credentials': 'include',
      'headers': new Headers({
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
      })
    */

    // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            //'Content-Type': 'application/json',
            //'Content-Type': 'multipart/formdata',
            'X-CSRFToken': csrftoken,
            //'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
        },
        redirect: 'follow', // manual, *follow, error
        referrer: 'no-referrer', // no-referrer, *client
        body: data // body data type must match "Content-Type" header
    });

    let jsonData = await response.json()

    return {
        status: response.status,
        data: jsonData // parses JSON response into native JavaScript objects
    }
}

export const processForecastData = (forecastData) => {
    let cellIndex = 0;
    let rows = [];

    let financialCodeCols = [
        "analysis1_code",
        "analysis2_code",
        "cost_centre",
        "natural_account_code",
        "programme",
        "project_code"
    ]

    forecastData.forEach(function (rowData, rowIndex) {
        let cells = {}
        let colIndex = 0

        for (const financialCodeCol of financialCodeCols) {
            cells[financialCodeCol] = {
                id: getCellId(financialCodeCol, rowIndex),
                rowIndex: rowIndex,
                colIndex: colIndex,
                key: financialCodeCol,
                value: rowData[financialCodeCol],
                isEditable: false
            }

            colIndex++
        }

        for (const [key, monthlyFigure] of Object.entries(rowData["monthly_figures"])) {
            cells[monthlyFigure.month] = {
                id: getCellId(monthlyFigure.month, rowIndex),
                rowIndex: rowIndex,
                colIndex: colIndex,
                key: monthlyFigure.month,
                versions: monthlyFigure.monthly_figure_amounts.sort(function(a, b){return a - b}),
                isEditable: !monthlyFigure.actual
            }

            colIndex++
        }

        rows.push(cells)
    });

    return rows;
}
