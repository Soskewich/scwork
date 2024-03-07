import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";
import {AnalysisAPI} from "../api";

export const fetchAnalysisSourceRating = createAsyncThunk(
    "analysisSourceRating/fetchAnalysis", async (_,{rejectWithValue}) => {
        try {
            const res = await AnalysisAPI.getAnalysisSourceRating()
            return res.data;
        } catch (err) {
            return rejectWithValue([], err);
        }
    });


const initialState = {
    analysisSourceRating:{
        result:[],
        total:null
    }
};

const analysisSourceRatingSlice = createSlice({
    name: 'analysisSourceRating',
    initialState,
    extraReducers: (builder) => {
        builder
            .addCase(fetchAnalysisSourceRating.pending, (state) => {
            state.isFetching = true;
        })
            .addCase(fetchAnalysisSourceRating.fulfilled, (state, action) => {
                state.isFetching = false;

                for(let i = 0; i < action.payload.result.length; i++){
                    const thisDict = {}
                    thisDict.name = action.payload.result[i].source_rating.name
                    for (let j = 0; j < action.payload.result[i].counts.length; j++){
                        thisDict[action.payload.result[i].counts[j].year] = action.payload.result[i].counts[j].count
                    }
                    state.analysisSourceRating.result.push(thisDict)
                }


            })
            .addCase(initialState, (state) => {
                state.isFetching = false;
            })

    }
});

export default analysisSourceRatingSlice.reducer;