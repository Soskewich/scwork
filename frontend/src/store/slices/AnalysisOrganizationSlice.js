import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";
import {AnalysisAPI} from "../api";

export const fetchAnalysisOrganization = createAsyncThunk(
    "analysisOrganization/fetchAnalysisOrganization", async (_,{rejectWithValue}) => {
        try {
            const res = await AnalysisAPI.getAnalysisOrganization()
            return res.data;
        } catch (err) {
            return rejectWithValue([], err);
        }
    });


const initialState = {
    analysisOrganization:{
        result:[],
        total:null
    }
};

const analysisOrganizationSlice = createSlice({
    name: 'analysisOrganization',
    initialState,
    extraReducers: (builder) => {
        builder
            .addCase(fetchAnalysisOrganization.pending, (state) => {
            state.isFetching = true;
        })
            .addCase(fetchAnalysisOrganization.fulfilled, (state, action) => {
                state.isFetching = false;

                for(let i = 0; i < action.payload.result.length; i++){
                    const thisDict = {}
                    thisDict.name = action.payload.result[i].organization.name
                    for (let j = 0; j < action.payload.result[i].counts.length; j++){
                        thisDict[action.payload.result[i].counts[j].year] = action.payload.result[i].counts[j].count
                    }
                    state.analysisOrganization.result.push(thisDict)
                }



            })
            .addCase(initialState, (state) => {
                state.isFetching = false;
            })

    }
});

export default analysisOrganizationSlice.reducer;