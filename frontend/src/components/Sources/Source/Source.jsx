import React, {useState} from "react";
import {useParams} from "react-router-dom";
import {useDispatch, useSelector} from "react-redux";
import {setSource} from "../../../store/slices/SourceSlice";
import style from "./Source.module.css"
import SourcePublications from "./SourcesPublication";
import {SourceAPI} from "../../../store/api";
import Preloader from "../../Helpers/Preloader/Preloader";
import {setData} from "../../../store/slices/PublicationsSlice";

const Source = () => {


    const params = useParams();
    const dispatch = useDispatch();
    const source = useSelector(state => state.source)
    const {pageSize} = useSelector(state => state.publications);
    const [isFetching, toggleIsFetching] = useState(false);

    React.useEffect(() => {
        toggleIsFetching(true);
        const fetchSource = async () => {
            const res = await SourceAPI.getSource(params.id);
            dispatch(setSource(res.data));
            toggleIsFetching(false);
        }
        fetchSource();
    }, [params.id])

    React.useEffect(() => {
        toggleIsFetching(true);
        const fetchSource = async () => {
            const res = await SourceAPI.getSourcePageSize(params.id, 0, pageSize);
            dispatch(setData(res.data));
            toggleIsFetching(false);
        }
        fetchSource();
    }, [pageSize]);

    return <div className={style.theme}>
        {isFetching === true ? <Preloader/> :
            <div>
                <div className={style.block}>
                    <div>{source.source_type.name}</div>
                    <div>{source.name}</div>
                </div>
                <div className={style.block}>
                    <div>{source.source_links.map((links, index) => <div key = {index}>
                        {links.source_link_type.name}{links.link === null ? '' : ':'} {links.link}
                    </div>)}</div>
                </div>
                <div>

                    <div >{source.source_ratings.map((ratings, index) =>
                        <Dropdown source_rating={ratings}></Dropdown>
                    )}
                    </div>
                </div>

                <SourcePublications/>
            </div>
        }
    </div>
}

const Dropdown = (source_rating) => {
    const [isOpen, setOpen] = useState(false);

    const handleChangeOpen = () => setOpen(!isOpen);
    return (
            <div ><div className={style.blockRating} onClick={handleChangeOpen}>
                <div>{source_rating.source_rating.source_rating_type.name}</div>

                <div>{source_rating.source_rating.rating === null ? null : source_rating.source_rating.rating}</div>


                <div>{source_rating.source_rating.source_rating_dates.length !== 0 ? source_rating.source_rating.source_rating_dates.map((rating_dates, index) => <div key = {index}>

                    <div>{rating_dates.rating_date === null ? null : ''}</div>
                    {rating_dates.rating_date} {" – "}
                    {rating_dates.active === false ? rating_dates.to_rating_date : 'Active' }
                </div>) : null}
                </div>
            </div>
                {isOpen && (
                    <div>
                            <table className={style.tableRating}>
                                <tbody>
                                {source_rating.source_rating.source_rating_subjects.map((rating_subjects, index) =>
                                    <tr key={index}>
                                    <td>{rating_subjects.subject.subj_code}</td>
                                    <td>{rating_subjects.subject.name}</td>
                                    <td>{rating_subjects.rating_date}</td>
                                    <td>{rating_subjects.active === false ? rating_subjects.to_rating_date : 'Active' }</td>
                                    </tr>
                                )}

                                </tbody>
                            </table>
                    </div>)
                }
            </div>
    );
};

export default Source;
