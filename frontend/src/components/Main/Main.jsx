import React from "react";
import style from './Main.module.css'
import {NavLink} from "react-router-dom";
import {useDispatch, useSelector} from "react-redux";
import {fetchPublications} from "../../store/slices/PublicationsSlice";
import {fetchAuthor} from "../../store/slices/AuthorsSlice";
import {fetchSources} from "../../store/slices/SourcesSlice";

const Main = () => {
    const publication = useSelector(state => state.publications)
    const author = useSelector(state => state.authors);
    const source = useSelector(state => state.sources);

    const dispatch = useDispatch();

    React.useEffect(() => {
        dispatch(fetchPublications({page: 0, pageSize: publication.pageSize}))
        dispatch(fetchAuthor({page: 0, pageSize: author.pageSize}))
        dispatch(fetchSources({page: 0, pageSize: source.pageSize}));
    }, [])

    return <div>
        <div className={style.container}>
            <h2 className={style.title}>Тестовая версия системы учета научной деятельности сотрудников ОмГТУ</h2>
        </div>

        <div className={style.counts}>
            <div className={style.block}>
                <div className={style.countTitle}>Количество публикаций <br></br> за последние 10 лет</div>
                <div className={style.count}>{publication.count}</div>
            </div>
            <div className={style.block}>
                <div className={style.countTitle}>Количество авторов</div>
                <div className={style.count}>{author.count}</div>
            </div>
            <div className={style.block}>
                <div className={style.countTitle}>Количество источников</div>
                <div className={style.count}>{source.count}</div>
            </div>
        </div>
        <div className={style.container}>
            <h2 className={style.title}></h2>
        </div>
    </div>
}

export default Main;	
