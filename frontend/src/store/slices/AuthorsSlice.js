import {createSlice, createAsyncThunk} from "@reduxjs/toolkit";
import {AuthorsAPI} from "../api";
export const fetchAuthor = createAsyncThunk(
    "authors/fetchAuthor", async ({page, pageSize}, {rejectWithValue}) => {
        try {
            const res = await AuthorsAPI.getAuthors(page, pageSize);
            return res.data;
        } catch (err) {
            return rejectWithValue([], err);
        }
    });
export const fetchAuthorSearch = createAsyncThunk(
    "authors/fetchAuthorSearch", async ({search, page, pageSize}, {rejectWithValue}) => {
        try {
            const res = await AuthorsAPI.getAuthorsSearch(search, page, pageSize)
            return res.data;
        } catch (err) {
            return rejectWithValue([], err);
        }
    });



const initialState = {
    authors: [],
    pageSize: 30,
    count: null,
    currentPage: 1,
    confirmed: true,
    isFetching: false,
};

const authorsSlice = createSlice({
    name: 'authors',
    initialState,
    reducers: {
        setData(state, action) {
            const {authors, count} = action.payload;
            state.authors = authors;
            state.count = count;
        },
        setSize(state, action) {
            state.pageSize = action.payload;
        }

    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchAuthor.pending, (state) => {
                state.isFetching = true;
            })
            .addCase(fetchAuthorSearch.pending, (state) => {
                state.isFetching = true;
            })
            .addCase(fetchAuthor.fulfilled, (state, action) => {
                state.isFetching = false;
                const {authors, count} = action.payload;
                state.authors = authors;
                state.count = count;
            })
            .addCase(fetchAuthorSearch.fulfilled, (state, action) => {
                state.isFetching = false;
                const {authors, count} = action.payload;
                state.authors = authors;
                state.count = count;
            })
            .addCase(initialState, (state) => {
                state.isFetching = false;
            })
    }
});


export const {setData, setSize} = authorsSlice.actions;

export default authorsSlice.reducer;



