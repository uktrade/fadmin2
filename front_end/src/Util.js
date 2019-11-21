import { store } from './Store';

const state = store.getState();

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


