import {createSlice} from "@reduxjs/toolkit";


const initialState = {
    publicationType: [],
    sourceRatingTypes: [],
    departments: [],
    nioktr_organization: [],

};

const filterSlices = createSlice({
    name: 'filter',
    initialState,
    reducers: {
        getPublicationType(state, action) {
            state.publicationType = action.payload;
        },
        getSourceRatingTypes(state, action) {
            state.sourceRatingTypes = action.payload;
        },
        getDepartments(state, action) {
            state.departments = action.payload;
        },
        getNioktrOrganization(state, action) {
            state.nioktr_organization = action.payload;
        }
    }
});


export const {getPublicationType, getSourceRatingTypes, getDepartments, getNioktrOrganization} = filterSlices.actions;

export default filterSlices.reducer;
