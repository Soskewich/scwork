import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";
import {NioktrAPI} from "../api";

export const fetchNioktr = createAsyncThunk(
    "nioktr/fetchNioktr", async (id, {rejectWithValue}) => {
        try {
            const res = await NioktrAPI.getNioktr(id);
            return res.data;
        } catch (err) {
            return rejectWithValue([], err);
        }
    });

const initialState = {
    id: null,
    title: null,
    contract_number: null,
    registration_number: null,
    nioktr_date: null,
    work_supervisor: {},
    keyword_nioktrs: [],
    rosrid_id: null,
    abstract: null,
    document_date: null,
    work_start_date: null,
    work_end_date: null,
    organization_supervisor: {},
    organization_executor: {},
    customer: {},
    nioktr_subject: [],
    nioktr_budget: [],
    types_nioktrs: [],
    organization_coexecutor: [],

    // nioktr_organization: [{
    //     organization: {},
    //     customer: {},
    //     coexecutors: [{}]
    // }],
    // nioktr_authors: [{
    //     work_supervisor: {},
    //     work_supervisor_position: null,
    //     organization_supervisor: {},
    //     organization_supervisor_position: null
    // }],
    accepted: false,
    isFetching: false
};

const nioktrSlice = createSlice({
    name: 'nioktr',
    initialState,
    extraReducers: (builder) => {
        builder
            .addCase(fetchNioktr.pending, (state) => {
                state.isFetching = true;
            })
            .addCase(fetchNioktr.fulfilled, (state, action) => {
                state.isFetching = false;
                const {
                    id, title, contract_number, registration_number, nioktr_date,
                    work_supervisor, keyword_nioktrs,
                    rosrid_id, abstract,
                    document_date, work_start_date,
                    work_end_date, organization_supervisor,
                    organization_executor,
                    customer, nioktr_subject,
                    nioktr_budget, types_nioktrs,
                    organization_coexecutor
                } = action.payload.nioktr;
                state.id = id;
                state.title = title;
                state.contract_number = contract_number;
                state.registration_number = registration_number;
                state.nioktr_date = nioktr_date;
                state.work_supervisor = work_supervisor;
                state.keyword_nioktrs = keyword_nioktrs;
                state.rosrid_id = rosrid_id;
                state.abstract = abstract;
                state.document_date = document_date;
                state.work_start_date = work_start_date;
                state.work_end_date = work_end_date;
                state.organization_supervisor = organization_supervisor;
                state.organization_executor = organization_executor;
                state.customer = customer;
                state.nioktr_subject = nioktr_subject;
                state.nioktr_budget = nioktr_budget;
                state.types_nioktrs = types_nioktrs;
                state.organization_coexecutor = organization_coexecutor;


            })
            .addCase(initialState, (state) => {
                state.isFetching = false;
            })
    },

});

export default nioktrSlice.reducer;
