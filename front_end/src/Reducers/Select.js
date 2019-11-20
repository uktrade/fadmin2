import { createSlice } from 'redux-starter-kit';
// Use of this lib guarentees no state mutatation

const select = createSlice({
    slice: 'select',
    initialState: {
        useOffset: true,
        initial: {
            x: 0,
            y: 0,
            width: 0,
            height: 0,
        },
        last: {
            x: 0,
            y: 0,
            width: 0,
            height: 0
        }
    },
    reducers: {
        SET_INITIAL: (state, action) => {
            state.initial = action.payload.initial
        },
        SET_LAST: (state, action) => {
            state.last = action.payload.last
        },
        SET_USE_OFFSET: (state, action) => {
            state.useOffset = action.payload.useOffset
        }
    }
});

export const {
    SET_INITIAL,
    SET_LAST,
    SET_USE_OFFSET,
} = select.actions;

export default select.reducer;
