import {createSlice, createAsyncThunk} from "@reduxjs/toolkit";
import {RidsAPI} from "../api";

export const fetchRids = createAsyncThunk(
    "rids/fetchRids", async ({page, pageSize}, {rejectWithValue}) => {
        try {
            const res = await RidsAPI.getRids(page, pageSize)
            return res.data;
        } catch (err) {
            return rejectWithValue([], err);
        }
    });
export const fetchRidsSearch = createAsyncThunk(
    "rids/fetchRidsSearch", async ({search,author_id, from_date, to_date,
                                             page, pageSize}, {rejectWithValue}) => {
        try {
            const res = await RidsAPI.getRidsSearch(search,author_id, from_date, to_date,
                page, pageSize)
            return res.data;
        } catch (err) {
            return rejectWithValue([], err);
        }
    });


const initialState = {
    rids: [{
        title: null,
        registration_number: null,
        keyword_rids: [],
        rid_date: null,
        work_supervisor: {
            id: 0,
            name: null,
            surname: null,
            patronymic: null,
        }
    }],
    pageSize: 20,
    count: 1,
    currentPage: 1,
    isFetching: false,
    data:[]
};

const ridsSlice = createSlice({
    name: 'rids',
    initialState,
    reducers: {
        setSize(state, action) {
            state.pageSize = action.payload;
        },
        setData(state, action) {
            const {rids, count} = action.payload;
            state.rids = rids;
            state.count = count;
        },
        setFilter(state, action){
            state.data = action.payload;
        }
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchRids.pending, (state) => {
                state.isFetching = true;
            })
            .addCase(fetchRidsSearch.pending, (state) => {
                state.isFetching = true;
            })
            .addCase(fetchRids.fulfilled, (state, action) => {
                state.isFetching = false;
                const {rids, count} = action.payload;
                state.rids = rids;
                state.count = count;
            })
            .addCase(fetchRidsSearch.fulfilled, (state, action) => {
                state.isFetching = false;
                const {rids, count} = action.payload;
                state.rids = rids;
                state.count = count;

            })

            .addCase(initialState, (state) => {
                state.isFetching = false;
            })
    },
});


export const {setData, setSize, setFilter} = ridsSlice.actions;

export default ridsSlice.reducer;



