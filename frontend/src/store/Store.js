import {configureStore} from '@reduxjs/toolkit'
import allAuthorsReducer from "./slices/AuthorsSlice";
import authorReducer from "./slices/AuthorSlice";
import publicationsSlice from "./slices/PublicationsSlice";
import publicationSlice from "./slices/PublicationSlice";
import SourceSlice from "./slices/SourceSlice";
import SourcesSlice from "./slices/SourcesSlice";
import signInSlice from "./slices/SignInSlice";
import feedbackSlice from "./slices/FeedbackSlice";
import authorsConfirmedFalseSlice from "./slices/AuthorsConfirmedFalseSlice";
import analysisSlice from "./slices/AnalysisSlice";
import analysisSourceRatingSlice from "./slices/AnalysisSourceRatingSlice";
import analysisOrganizationSlice from "./slices/AnalysisOrganizationSlice";
import filterSlices from "./slices/FilterSlices";
import nioktrsSlice from "./slices/NioktrsSlice";
import nioktrSlice from "./slices/NioktrSlice";
import ridsSlice from "./slices/RidsSlice";


const store = configureStore({
    reducer: {
        authors: allAuthorsReducer,
        author: authorReducer,
        publications: publicationsSlice,
        publication: publicationSlice,
        source: SourceSlice,
        sources: SourcesSlice,
        signIn: signInSlice,
        feedbacks: feedbackSlice,
        authorsConfirmedFalse: authorsConfirmedFalseSlice,
        analysis: analysisSlice,
        analysisSourceRating: analysisSourceRatingSlice,
        analysisOrganization: analysisOrganizationSlice,
        filter: filterSlices,
        nioktrs: nioktrsSlice,
        nioktr: nioktrSlice,
        rids: ridsSlice,
    }
})
export default store;

