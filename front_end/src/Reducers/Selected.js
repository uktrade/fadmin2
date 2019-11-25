import { createSlice } from 'redux-starter-kit';
// Use of this lib guarentees no state mutatation

const selected = createSlice({
    slice: 'select',
    initialState: {
        selectedRows: [],
        all: false
    },
    reducers: {
        SET_SELECTED_ROW: (state, action) => {
            state.all = false
            state.selectedRows = []
            state.selectedRows.push(action.payload.selectedRow)
        },
        SELECT_ALL: (state, action) => {
            state.all = true
        },
        UNSELECT_ALL: (state, action) => {
            state.selectedRows = []
            state.all = false
        },
    }
});

export const {
    SET_SELECTED_ROW,
    SELECT_ALL,
    UNSELECT_ALL
} = selected.actions;

export default selected.reducer;
