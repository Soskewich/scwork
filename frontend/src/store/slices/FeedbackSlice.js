import {createSlice, createAsyncThunk} from "@reduxjs/toolkit";
import {FeedbackAPI} from "../api";

export const fetchFeedback = createAsyncThunk(
    "feedbacks/fetchSources", async ({page, pageSize}, {rejectWithValue}) => {
        try {
            const res = await FeedbackAPI.getFeedback(page, pageSize)
            return res.data;
        } catch (err) {
            return rejectWithValue([], err);
        }
    });

const initialState = {
    feedbacks: [{
        name: null,
        mail: null,
        message: null,
        date: null,
        solved: false
    }],
    pageSize: 20,
    count: 1,
    currentPage: 1,
    isFetching: false,
};

const feedbackSlice = createSlice({
    name: 'feedbacks',
    initialState,
    reducers: {
        setData(state, action) {
            const {feedbacks, count} = action.payload;
            state.feedbacks = feedbacks;
            state.count = count;
        },
        setSize(state, action) {
            state.pageSize = action.payload;
        }

    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchFeedback.pending, (state) => {
                state.isFetching = true;
            })
            .addCase(fetchFeedback.fulfilled, (state, action) => {
                state.isFetching = false;
                const {feedbacks, count} = action.payload;
                state.feedbacks = feedbacks;
                state.count = count;
            })
            .addCase(initialState, (state) => {
                state.isFetching = false;
            })
    }
});
export default feedbackSlice.reducer;



