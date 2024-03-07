import React from "react";
import {useParams} from "react-router-dom";
import {useDispatch, useSelector} from "react-redux";
import {fetchNioktr} from "../../../store/slices/NioktrSlice";
import style from "./Nioktr.module.css"
import {NavLink} from "react-router-dom";

import Preloader from "../../Helpers/Preloader/Preloader";

const Nioktr = () => {
    const params = useParams();
    const dispatch = useDispatch();
    const nioktr = useSelector(state => state.nioktr);
    const keywords = [];

    React.useEffect(() => {
        dispatch(fetchNioktr(params.id))
    }, [])

    return (<div className={style.theme}>
            {nioktr.isFetching === true ? <Preloader/> :
                <div>
                    
                    <div className={style.block}>
                        <div>{nioktr.title}</div>
                        <div>Дата: {nioktr.nioktr_date}</div>
                        <div>Докумет: {nioktr.document_date}</div>
                        <div>Старт: {nioktr.work_start_date}</div>
                        <div>Конец: {nioktr.work_end_date}</div>
                    </div>

                    <div className={style.block}>
                        <div>Руководитель организации: {nioktr.organization_supervisor.name} {nioktr.organization_supervisor.surname} {nioktr.organization_supervisor.patronymic}</div>
                        <div>Руководитель работы: {nioktr.work_supervisor.name} {nioktr.work_supervisor.surname} {nioktr.work_supervisor.patronymic}</div>
                    </div>

                    <div className={style.block}>
                        <div>Исполнитель: <br/>{nioktr.organization_executor.name}</div>
                            <div>
                                <div className={style.line}>Город: {nioktr.organization_executor.city}</div>
                                <div className={style.line}>ОГРН: {nioktr.organization_executor.ogrn}</div>
                                <div className={style.line}>ИНН: {nioktr.organization_executor.inn}</div>
                            </div>

                    </div>

                    <div className={style.block}>
                        {/*Добавить city*/}
                        <div>Заказчик: <br/>{nioktr.customer.name}<br/>
                            <div >
                                <div className={style.line} >Город: {nioktr.customer.city}</div>
                                <div className={style.line} >ОГРН: {nioktr.customer.ogrn}</div>
                                <div className={style.line} >ИНН: {nioktr.customer.inn}</div>
                            </div>
                        </div>
                    </div>

                    <div className={style.block}>
                        Аннотация: <div>{nioktr.abstract}</div>
                    </div>


                    <div className={style.block}>
                        Ключевые слова:
                        {nioktr.keyword_nioktrs.map(word => {
                                keywords.push(word.keyword.keyword)
                            }
                        )}
                        <div>{keywords.join(", ")}</div>
                    </div>


                        <table className={style.block}>
                            Дополнительная информация
                            <tbody>
                            {nioktr.nioktr_subject.map((subject, index) =>

                                <tr key={index} >
                                    <td>{subject.subject.subj_code === null ? '-' : subject.subject.subj_code} </td>
                                    &nbsp;<td>{subject.subject.name}</td>
                                </tr>

                            )}
                            </tbody>
                        </table>



                    <div className={style.block}>
                        Тип
                        {nioktr.types_nioktrs.map(type =>
                            <div>
                                {type.name}
                            </div>
                        )}

                    </div>

                    <div className={style.block}>
                        Бюджет
                        {nioktr.nioktr_budget.map(budget =>
                            <div>
                                <div>{budget.budget_type.name}</div>
                                <div>Задействовано: {budget.funds} тысяч</div>
                                <div>Код бюджетной классификации: {budget.kbk}</div>
                            </div>
                        )}

                    </div>


                </div>
            }
        </div>
    )
};

export default Nioktr;
