'use strict';

import { createStore, combineReducers } from 'redux';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';
import { mouse } from './Reducers/Mouse';
import allCells from './Reducers/Cells';
import { editCell } from './Reducers/Edit'
import select from './Reducers/Select'

const persistConfig = {
    key: 'root',
    //transforms: [encryptor],
    storage
}

const appReducer = combineReducers({
    mouse,
    allCells,
    editCell,
    select,
});

const persistedReducer = persistReducer(persistConfig, appReducer)

//export const store = createStore(persistedReducer);
export const store = createStore(appReducer);
//export const persistor = persistStore(store);
export const purge = () => {
    //persistor.purge();
    localStorage.clear();
};