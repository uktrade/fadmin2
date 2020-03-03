import { createSlice } from 'redux-starter-kit';
// Use of this lib guarentees no state mutatation

const hiddenCols = createSlice({
    slice: 'hidden',
    initialState: {
        hiddenCols: [],
        showAll: true
    },
    reducers: {
        TOGGLE_ITEM: (state, action) => {
            let index = state.hiddenCols.indexOf(action.payload)
            if (index > -1) {
               state.hiddenCols.splice(index, 1);
            } else {
                state.hiddenCols.push(action.payload)
            }
        },
        TOGGLE_SHOW_ALL: (state, action) => {
            if (state.showAll) {
                state.showAll = false
            } else {
                state.showAll = true
            }
        },
    }
});

export const {
    TOGGLE_ITEM,
    TOGGLE_SHOW_ALL
} = hiddenCols.actions;

export default hiddenCols.reducer;
