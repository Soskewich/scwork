import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";
import {AnalysisAPI} from "../api";

export const fetchAnalysis = createAsyncThunk(
    "analysis/fetchAnalysis", async (_,{rejectWithValue}) => {
        try {
            const res = await AnalysisAPI.getAnalysisDate()
            return res.data;
        } catch (err) {
            return rejectWithValue([], err);
        }
    });


const initialState = {
    analysis:{
        result:[],
        total:null
    }
};

const analysisSlice = createSlice({
    name: 'analysis',
    initialState,
    extraReducers: (builder) => {
        builder
            .addCase(fetchAnalysis.pending, (state) => {
            state.isFetching = true;
        })
            .addCase(fetchAnalysis.fulfilled, (state, action) => {
                state.isFetching = false;
                state.analysis = action.payload;

            })
            .addCase(initialState, (state) => {
                state.isFetching = false;
            })

    }
});

export default analysisSlice.reducer;