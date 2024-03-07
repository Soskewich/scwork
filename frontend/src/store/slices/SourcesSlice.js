import {createSlice, createAsyncThunk} from "@reduxjs/toolkit";
import {SourcesAPI} from "../api";

export const fetchSources = createAsyncThunk(
    "sources/fetchSources", async ({page, pageSize}, {rejectWithValue}) => {
        try {
            const res = await SourcesAPI.getSources(page, pageSize);
            return res.data;
        } catch (err) {
            return rejectWithValue([], err);
        }
    });
export const fetchSourcesSearch = createAsyncThunk(
    "sources/fetchSourcesSearch", async ({search, page, pageSize}, {rejectWithValue}) => {
        try {
            const res = await SourcesAPI.getSourcesSearch(search, page, pageSize)
            return res.data;
        } catch (err) {
            return rejectWithValue([], err);
        }
    });

const initialState = {
    sources: [{
        name: null,
        source_type: {
            id: null,
            name: null
        }
    }],
    pageSize: 30,
    count: 1,
    isFetching: false,
};

const SourcesSlice = createSlice({
    name: 'sources',
    initialState,
    reducers: {
        setSize(state, action) {
            state.pageSize = action.payload;
        }
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchSources.pending, (state) => {
                state.isFetching = true;
            })
            .addCase(fetchSourcesSearch.pending, (state) => {
                state.isFetching = true;
            })
            .addCase(fetchSources.fulfilled, (state, action) => {
                state.isFetching = false;
                state.sources = action.payload.sources;
                state.count = action.payload.count;
            })
            .addCase(fetchSourcesSearch.fulfilled, (state, action) => {
                state.isFetching = false;
                state.sources = action.payload.sources;
                state.count = action.payload.count;
            })
            .addCase(initialState, (state) => {
                state.isFetching = false;
            })
    }
})
export const {setSize} = SourcesSlice.actions;
export default SourcesSlice.reducer;