import React, {useState} from 'react';
import {useParams} from "react-router-dom";
import style from './Author.module.css'
import {useDispatch, useSelector} from "react-redux";
import {setAuthor} from "../../../store/slices/AuthorSlice";
import avatar from "../../../assets/img/avatar.svg"
import AuthorsPublications from "./AuthorsPublications";
import {setData} from "../../../store/slices/PublicationsSlice";
import {AuthorAPI} from "../../../store/api";
import Preloader from "../../Helpers/Preloader/Preloader";
import MergeButton from "../../Admin/Merge/MergeButton";
import {useCookies} from "react-cookie";

const Author = () => {

    const params = useParams();
    const dispatch = useDispatch();
    const author = useSelector(state => state.author);
    const {pageSize} = useSelector(state => state.publications);
    const [isFetching, toggleIsFetching] = useState(false);
    const [cookies, ] = useCookies(['isAuth'])

    React.useEffect(() => {
        toggleIsFetching(true);
        try {
            const fetchAuthor = async () => {
                const res = await AuthorAPI.getAuthor(params.id);
                dispatch(setAuthor(res.data));
                toggleIsFetching(false);
            }
            fetchAuthor();
        } catch (e) {
            console.log(e);
        }
    }, [params.id])


    React.useEffect(() => {
        toggleIsFetching(true);
        try {
            const fetchPublications = async () => {
                const res = await AuthorAPI.getAuthorPublication(params.id, 0, pageSize)
                dispatch(setData(res.data));
                toggleIsFetching(false);
            }
            fetchPublications();
        } catch (e) {
            console.log(e);
        }
    }, [pageSize]);

    return (<div className={style.theme}>
            {isFetching === true ? <Preloader/> :
                <div>
                    {author === undefined ? 'Подождите пожалуйста' : <>
                        <div className={style.block}>
                            <img className={style.block__image}
                                 src={avatar}
                                 alt=""/>
                            <div className={style.block__info}>
                                <p className={style.block__text}>{author.surname} {author.name} {author.patronymic}</p>
                                {author.author_identifiers.map((authors, index) => <div key={index}>
                                    {authors.identifier.name}: {authors.identifier_value}
                                </div>)
                                }
                                {author.author_departments.map((authors, index) => <div key = {index}>
                                    <div>{authors.department.name}</div>
                                    <div>{authors.department.faculty.name} ({authors.position})</div>
                                </div>)}
                            </div>
                        </div>
                        {cookies.isAuth?
                        <div>
                            {author.confirmed === false? <MergeButton authorId = {author.id}/>
                            :null}
                        </div>:null}
                        <div className={style.title}>
                        </div>
                        <AuthorsPublications/>
                    </>
                    }
                </div>
            }
        </div>
    );
};

export default Author;
