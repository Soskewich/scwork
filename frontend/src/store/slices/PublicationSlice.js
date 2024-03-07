import {createAsyncThunk, createSlice} from "@reduxjs/toolkit";
import {PublicationAPI} from "../api";

export const fetchPublication = createAsyncThunk(
    "publication/fetchPublication", async (id, {rejectWithValue}) => {
        try {
            const res = await PublicationAPI.getPublication(id);
            return res.data;
        } catch (err) {
            return rejectWithValue([], err);
        }
    });

const initialState = {
    id: null,
    publication_type: [],
    source: [],
    title: null,
    publication_date: null,
    publication_authors: [{
        author: {},
        author_publication_organizations: [],

    }],
    abstract: null,
    accepted: false,
    keyword_publications: [],
    publication_links: [],
    isFetching: false
};

const publicationSlice = createSlice({
    name: 'publication',
    initialState,
    extraReducers: (builder) => {
        builder
            .addCase(fetchPublication.pending, (state) => {
                state.isFetching = true;
            })
            .addCase(fetchPublication.fulfilled, (state, action) => {
                state.isFetching = false;
                const {
                    id, publication_type, source, title, publication_date,
                    publication_authors, abstract, accepted, keyword_publications,
                    publication_links
                } = action.payload.publication;
                state.id = id;
                state.publication_type = publication_type;
                state.source = source;
                state.title = title;
                state.publication_date = publication_date;
                state.publication_authors = publication_authors;
                state.abstract = abstract;
                state.accepted = accepted;
                state.keyword_publications = keyword_publications;
                state.publication_links = publication_links;
            })
            .addCase(initialState, (state) => {
                state.isFetching = false;
            })
    },

});

export default publicationSlice.reducer;
