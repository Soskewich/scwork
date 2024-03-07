import {createSlice, createAsyncThunk} from "@reduxjs/toolkit";
import {NioktrsAPI} from "../api";

export const fetchNioktrs = createAsyncThunk(
    "nioktrs/fetchNioktrs", async ({page, pageSize}, {rejectWithValue}) => {
        try {
            const res = await NioktrsAPI.getNioktrs(page, pageSize)
            return res.data;
        } catch (err) {
            return rejectWithValue([], err);
        }
    });
export const fetchNioktrsSearch = createAsyncThunk(
    "nioktrs/fetchNioktrsSearch", async ({search,author_id, from_date, to_date,
                                             page, pageSize}, {rejectWithValue}) => {
        try {
            const res = await NioktrsAPI.getNioktrsSearch(search,author_id, from_date, to_date,
                page, pageSize)
            return res.data;
        } catch (err) {
            return rejectWithValue([], err);
        }
    });


const initialState = {
    nioktrs: [{
        title: null,
        registration_number: null,
        keyword_nioktrs: [],
        nioktr_date: null,
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

const nioktrsSlice = createSlice({
    name: 'nioktrs',
    initialState,
    reducers: {
        setSize(state, action) {
            state.pageSize = action.payload;
        },
        setData(state, action) {
            const {nioktrs, count} = action.payload;
            state.nioktrs = nioktrs;
            state.count = count;
        },
        setFilter(state, action){
            state.data = action.payload;
        }
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchNioktrs.pending, (state) => {
                state.isFetching = true;
            })
            .addCase(fetchNioktrsSearch.pending, (state) => {
                state.isFetching = true;
            })
            .addCase(fetchNioktrs.fulfilled, (state, action) => {
                state.isFetching = false;
                const {nioktrs, count} = action.payload;
                state.nioktrs = nioktrs;
                state.count = count;
            })
            .addCase(fetchNioktrsSearch.fulfilled, (state, action) => {
                state.isFetching = false;
                const {nioktrs, count} = action.payload;
                state.nioktrs = nioktrs;
                state.count = count;

            })

            .addCase(initialState, (state) => {
                state.isFetching = false;
            })
    },
});


export const {setData, setSize, setFilter} = nioktrsSlice.actions;

export default nioktrsSlice.reducer;



