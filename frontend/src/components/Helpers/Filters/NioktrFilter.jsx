
import React, {useState} from "react";
import {FilterAPI, NioktrsAPI} from "../../../store/api";
import {useDispatch, useSelector} from "react-redux";
import {getPublicationType, getSourceRatingTypes, getDepartments} from "../../../store/slices/FilterSlices";
import {useForm} from "react-hook-form";
import {fetchAuthorSearch} from "../../../store/slices/AuthorsSlice";
import {useDebounce} from "use-debounce";
import {fetchNioktrsSearch, setFilter} from "../../../store/slices/NioktrsSlice";
import style from './NioktrFilter.module.css'
import {createAsyncThunk} from "@reduxjs/toolkit";

const NioktrFilter = () => {

    const {register, formState: {errors}, handleSubmit} = useForm();
    const dispatch = useDispatch();
    const {publicationType, sourceRatingTypes, departments} = useSelector(state => state.filter)
    const [search, setSearch] = useState('');
    const {authors, count} = useSelector(state => state.authors);
    const debouncedSearch = useDebounce(search, 500);
    const {nioktrs, pageSize} = useSelector(state => state.nioktrs);
    let date = new Date().toLocaleDateString('en-ca')
    const state = {
        button: 1
    };

    const onSearchChange = (e) => {
        const {value} = e.target
        setSearch(value)
    }

    React.useEffect(() => {
        const getOrganization = async () => {
            const res = await FilterAPI.getPublicationType();
            dispatch(getPublicationType(res.data.publication_types))
        }


        getOrganization();

    }, [])

    React.useEffect(() => {
        try {
            dispatch(fetchAuthorSearch({search, page: 0, pageSize: count}))
        } catch (e) {
            console.log(e);
        }
    }, [debouncedSearch[0]])

    const onSubmit = (data) => {
        if (data.publicationType === '') {
            data.publicationType = null
        }
        if (data.authorName === '') {
            data.authorName = null
        }
        if (data.SourceRating === '') {
            data.SourceRating = null
        }
        if (data.department === '') {
            data.department = null
        }
        if (data.beforeTime === '') {
            data.beforeTime = `1960-06-12`
        }
        if (data.afterTime === '') {
            data.afterTime = date
        }
        dispatch(setFilter(data))



        const sendFilters = async () => {
            try {
                dispatch(fetchNioktrsSearch({
                    search: null, author_id: data.authorName,
                    from_date: data.beforeTime,
                    to_date: data.afterTime, page: 0, pageSize
                }));
            } catch (e) {
                console.log(e)
            }
        }
        if (state.button === 1)
            sendFilters();
        if (state.button === 2){
            try {
                let url = '/api/nioktr?';

                if (data.authorName)
                    url += `author_id=${data.authorName}&`
                if (data.beforeTime)
                    url += `from_date=${data.beforeTime}&`
                if (data.afterTime)
                    url += `to_date=${data.afterTime}&`
                url += `limit=1000`
                fetch(url).then(res => {
                    return res.blob();
                })
            }
            catch (e){
                console.log(e)
            }
        }
    }


    return <div className={style.filter}>
        <div>Фильтры</div>
        <div>
            <form onSubmit={handleSubmit(onSubmit)}>
                <div>
                    <label htmlFor="time">Период времени</label>
                    <div>
                        От: <input className={style.date} {...register("beforeTime")} type={"date"}/>
                    </div>
                    <div>
                        До: <input className={style.date} {...register("afterTime")} type={"date"}/>
                    </div>
                </div>



                <div>
                    <label htmlFor="authorName">Автор:</label>
                    <input className={style.dataName} list="authorName" placeholder={"Введите имя автора"} type="search" value={search}
                           onChange={onSearchChange}/>
                    <select className={style.dataName} id="authorName" {...register("authorName")}>
                        <option>{null}</option>
                        {authors.map((author, index) =>
                            <option value={author.id} key={index}>
                                {author.surname} {author.name} {author.patronymic}
                            </option>
                        )}
                    </select>
                </div>
                <div>
                    <input className={style.dataName} type={"submit"} value={"Применить"} onClick={() => (state.button = 1)}/>
                </div>

            </form>
        </div>
    </div>
}

export default NioktrFilter;
