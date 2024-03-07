import {createSlice} from "@reduxjs/toolkit";

const initialState = {
    id: 0,
    name: null,
    source_type: {
        id: null,
        name: null
    },
    source_ratings: [{
        source_rating_type: {
            id: null,
            name: null
        },
        source_rating_subjects:[
            {
                subject: {
                    subj_code: null,
                    name: null
                },
                rating_date: null,
                to_rating_date: null,
                active: null
            }
        ],
        source_rating_dates: [
            {
            active: null,
            rating_date: null,
            to_rating_date: null

        }],
        rating: null
    }],
    source_links: [{
        source_link_type: {
            id: null,
            name: null
        },
        link: null
    }],

};
const SourceSlice = createSlice({
    name: 'source',
    initialState,
    reducers: {
        setSource(state, action) {
            const {id, name, source_type, source_ratings,source_rating_type, source_rating_subjects, subject, source_rating_dates, source_links, rating_date} = action.payload.source;
            state.id = id;
            state.name = name;
            state.source_type = source_type;
            state.source_ratings = source_ratings;
            state.source_rating_type = source_rating_type;
            state.source_rating_subjects = source_rating_subjects;
            state.subject = subject;
            state.source_rating_dates = source_rating_dates;
            state.source_links = source_links;
            state.rating_date = rating_date;
        }
    }
})

export const {setSource} = SourceSlice.actions;
export default SourceSlice.reducer;