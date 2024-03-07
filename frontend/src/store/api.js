import axios from "axios";

const instance = axios.create({
    withCredentials: true,
});




export const postSignIn = (data) => {
    return instance.post("/api/user/token", data, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
}

export const postMergeAuthors = (merge_id, base_id, token) => {
    return instance.post(`/api/author/${merge_id}/merge?base_id=${base_id}`, {merge_id: merge_id, base_id: base_id})
}


export const DataUploadAPI = {
    postAuthors(data) {
        return instance.post("/api/admin/upload/authors", data, {
            headers: {
                "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarylMDxS6LSTp97MKcy",
            }
        })
    },
    postWhiteListUpgraded(data, rating_date) {
        return instance.post(`/api/admin/upload/white_list_upgraded?rating_date=${rating_date}`, data)
    },
    postVakWithRank(data, rating_date) {
        return instance.post(`/api/admin/upload/vak_with_rank?rating_date=${rating_date}`, data)
    },
    postRSCIJournalsRank(data, rating_date) {
        return instance.post(`/api/admin/upload/rsci_journals_rank?rating_date=${rating_date}`, data, {
            headers: {
                "content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryeAGvovuKxSANvAaj",
            }
        })
    },
    postScopus(data) {
        return instance.post("/api/admin/upload/scopus", data, {
            headers: {
                "content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryeAGvovuKxSANvAaj",
            }
        })
    },
    postElibrary(data) {
        return instance.post("/api/admin/upload/elibrary", data)
    },
    postWhiteList(data, rating_date) {
        return instance.post(`/api/admin/upload/white_list?rating_date=${rating_date}`, data)
    },
    postJCR(data, rating_date) {
        return instance.post(`/api/admin/upload/jcr?rating_date=${rating_date}`, data)
    },

}

export const AnalysisAPI= {
    getAnalysisDate(){
        return instance.get('/api/analysis/')
    },
    getAnalysisSourceRating(){
        return instance.get('/api/analysis/source_rating')
    },
    getAnalysisOrganization(){
        return instance.get('/api/analysis/organization')
    },

}

export const FilterAPI = {
    getPublicationType(){
        return instance.get('/api/publication/publication_types')
    },
    getSourceRatingTypes(){
        return instance.get('/api/source/source_rating_types')
    },
    getDepartments(){
        return instance.get('/api/faculty/departments/all?limit=100')
    }
}

export const AuthorAPI = {
    getAuthor(id) {
        return instance.get(`/api/author/${id}`)
    },
    getAuthorPublication(id, page, pageSize) {
        return instance.get(`/api/author/${id}/publications?page=${page}&limit=${pageSize}`)
    }
}
export const AuthorsAPI = {
    getAuthorsSearch(search, page, pageSize) {
        return instance.get(`/api/author?search=${search}&page=${page}&limit=${pageSize}`)
    },
    getAuthors(page, pageSize) {
        return instance.get(`/api/author?page=${page}&limit=${pageSize}`)
    },
    getUnconfirmedOmSTU(page, pageSize) {
        return instance.get(`/api/author/unconfirmed_omstu?page=${page}&limit=${pageSize}`)
    },
    getUnconfirmedOmSTUSearch(search, page, pageSize) {
        return instance.get(`/api/author/unconfirmed_omstu?search=${search}&page=${page}&limit=${pageSize}`)
    }
}

export const FeedbackAPI = {

    getFeedback(page, pageSize) {
        return instance.get(`/api/admin/feedbacks?page=${page}&limit=${pageSize}`)
    }
}

export const PublicationAPI = {
    getPublication(id) {
        return instance.get(`/api/publication/${id}`)
    }
}

export const PublicationsAPI = {
    getPublicationsSearch(search,publication_type_id,author_id,
                          source_rating_type_id, department, from_date, to_date,
                          page, pageSize=20) {
        let url = '/api/publication?';
        if (search)
            url += `search=${search}&`
        if (publication_type_id)
            url += `publication_type_id=${publication_type_id}&`
        if (author_id)
            url += `author_id=${author_id}&`
        if (source_rating_type_id)
            url += `source_rating_type_id=${source_rating_type_id}&`
        if (department)
            url += `department_id=${department}&`
        if (from_date)
            url += `from_date=${from_date}&`
        if (to_date)
            url += `to_date=${to_date}&`

        return instance.get(`${url}page=${page}&limit=${pageSize}`)
    },
    getPublications(page, pageSize) {
        return instance.get(`/api/publication?page=${page}&limit=${pageSize}`)
    },
    getPublicationsExcel(search,publication_type_id,author_id,
                         source_rating_type_id, department, from_date, to_date){
        let url = '/api/publication/excel?';
        if (search)
            url += `search=${search}&`
        if (publication_type_id)
            url += `publication_type_id=${publication_type_id}&`
        if (author_id)
            url += `author_id=${author_id}&`
        if (source_rating_type_id)
            url += `source_rating_type_id=${source_rating_type_id}&`
        if (department)
            url += `department_id=${department}&`
        if (from_date)
            url += `from_date=${from_date}&`
        if (to_date)
            url += `to_date=${to_date}`
        return instance.get(`${url}&limit=1000`)
    }
}

export const NioktrAPI = {
    getNioktr(id) {
        return instance.get(`/api/nioktr/${id}`)
    }
}


export const NioktrsAPI = {
    getNioktrsSearch(search,author_id,
                          from_date, to_date,
                          page, pageSize=20) {
        let url = '/api/nioktr?';
        if (search)
            url += `search=${search}&`
        if (author_id)
            url += `author_id=${author_id}&`
        if (from_date)
            url += `from_date=${from_date}&`
        if (to_date)
            url += `to_date=${to_date}&`

        return instance.get(`${url}page=${page}&limit=${pageSize}`)
    },
    getNioktrs(page, pageSize) {
        return instance.get(`/api/nioktr?page=${page}&limit=${pageSize}`)
    },

}

export const RidAPI = {
    getRid(id) {
        return instance.get(`/api/rid/${id}`)
    }
}

export const RidsAPI = {
    getRidsSearch(search,author_id,
                     from_date, to_date,
                     page, pageSize=20) {
        let url = '/api/rid?';
        if (search)
            url += `search=${search}&`
        if (author_id)
            url += `author_id=${author_id}&`
        if (from_date)
            url += `from_date=${from_date}&`
        if (to_date)
            url += `to_date=${to_date}&`

        return instance.get(`${url}page=${page}&limit=${pageSize}`)
    },
    getRids(page, pageSize) {
        return instance.get(`/api/rid?page=${page}&limit=${pageSize}`)
    },

}



export const SourceAPI = {
    getSource(id) {
        return instance.get(`/api/source/${id}`)
    },
    getSourcePageSize(id, page = 0, pageSize, header) {
        return instance.get(`/api/source/${id}/publications?page=${page}&limit=${pageSize}`)
    }
}

export const SourcesAPI = {
    getSourcesSearch(search, page, pageSize) {
        return instance.get(`/api/source?search=${search}&page=${page}&limit=${pageSize}`)
    },
    getSources(page, pageSize) {
        return instance.get(`/api/source?page=${page}&limit=${pageSize}`)
    }
}
