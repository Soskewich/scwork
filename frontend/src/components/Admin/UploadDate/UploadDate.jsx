import React, {useState} from "react";
import {useForm} from "react-hook-form";
import {DataUploadAPI} from "../../../store/api";
import Admin from "../Admin";
import s from "./Upload.module.css"
import {useCookies} from "react-cookie";
import Error404 from "../../Helpers/Errors/Erorr404";
import Calendar from "react-calendar";
import CalendarStyle from "./Calendar.css"

const UploadDate = () => {
    const {register, handleSubmit, formState: {errors}} = useForm({
        defaultValues: {
            Authors: FileList,
            WhiteListUpgraded: FileList,
            VakWithRank: FileList,
            RsciJournalsRank: FileList,
            WhiteList: FileList,
            Scopus: FileList,
            Elibrary: FileList,
            JCR: FileList
        }
    });
    const [cookies,] = useCookies(['isAuth'])
    let date = new Date().toLocaleDateString('en-ca')
    const [value, onChangeDate] = useState(new Date());

    const onSubmitAuthors = (data) => {
        let formData = new FormData();
        formData.append("file", data.Authors[0], data.Authors[0].filename)
        const UploadAuthors = async () => {
            try {
                const res = await DataUploadAPI.postAuthors(formData);
            } catch (e) {
                console.log(e)
            }
        }
        UploadAuthors();
    }
    const onSubmitWhiteListUpgraded = (data) => {
        let formData = new FormData();
        formData.append("file", data.WhiteListUpgraded[0], data.WhiteListUpgraded[0].filename)
        const WhiteListUpgraded = async () => {
            try {
                const res = await DataUploadAPI.postWhiteListUpgraded(formData, value.toLocaleDateString('en-ca'));

            } catch (e) {
                console.log(e)
            }
        }
        WhiteListUpgraded();
    }

    const onSubmitVakWithRank = (data) => {
        let formData = new FormData();
        formData.append("file", data.VakWithRank[0], data.VakWithRank[0].filename)

        const VakWithRank = async () => {
            try {
                const res = await DataUploadAPI.postVakWithRank(formData, value.toLocaleDateString('en-ca'));

            } catch (e) {
                console.log(e)
            }
        }
        VakWithRank();
    }

    const onSubmitRsciJournalsRank = (data) => {
        let formData = new FormData();
        formData.append("file", data.RsciJournalsRank[0], data.RsciJournalsRank[0].filename)
        const RsciJournalsRank = async () => {
            try {
                const res = await DataUploadAPI.postRSCIJournalsRank(formData, value.toLocaleDateString('en-ca'));

            } catch (e) {
                console.log(e)
            }
        }
        RsciJournalsRank();
    }

    const onSubmitWhiteList = (data) => {
        let formData = new FormData();
        formData.append("file", data.WhiteList[0], data.WhiteList[0].filename)
        const WhiteList = async () => {
            try {
                const res = await DataUploadAPI.postWhiteList(formData, value.toLocaleDateString('en-ca'));

            } catch (e) {
                console.log(e)
            }
        }
        WhiteList();
    }

    const onSubmitScopus = (data) => {
        let formData = new FormData();
        formData.append("file", data.Scopus[0], data.Scopus[0].filename)
        const Scopus = async () => {
            try {
                const res = await DataUploadAPI.postScopus(formData);

            } catch (e) {
                console.log(e)
            }
        }
        Scopus();
    }

    const onSubmitElibrary = (data) => {
        let formData = new FormData();
        formData.append("file", data.Elibrary[0], data.Elibrary[0].filename)
        const Elibrary = async () => {
            try {
                const res = await DataUploadAPI.postElibrary(formData);

            } catch (e) {
                console.log(e)
            }
        }
        Elibrary();
    }

    const onSubmitJCR = (data) => {
        let formData = new FormData();
        formData.append("file", data.JCR[0], data.JCR[0].filename)

        const JCR = async () => {
            try {
                const res = await DataUploadAPI.postJCR(formData, value.toLocaleDateString('en-ca'));

            } catch (e) {
                console.log(e)
            }
        }
        JCR();
    }

    return <div>
        {cookies.isAuth ? <div>
            <Admin/>
            <div className={s.main_container}>
                <div>
                    <Calendar onChange={date => onChangeDate(date)} value={value} minDate={new Date('2000-01-01')}
                              maxDate={new Date()}/>
                </div>
                <div className={s.container}>
                    <form onSubmit={handleSubmit(onSubmitAuthors)}>
                        Authors:
                        <div>
                            <input  {...register("Authors")} className={s.submit} accept="text/csv" type="file"/>
                        </div>
                        <div>
                            <input className={s.submit} type="submit"/>
                        </div>
                    </form>
                    <form onSubmit={handleSubmit(onSubmitWhiteListUpgraded)}>
                        White List Upgraded:
                        <div>
                            <input  {...register("WhiteListUpgraded")} className={s.submit} accept="text/csv"
                                    type="file"/>
                        </div>

                        <div>
                            <input className={s.submit} type="submit"/>
                        </div>
                    </form>
                    <form onSubmit={handleSubmit(onSubmitVakWithRank)}>
                        Vak with rank:
                        <div>
                            <input  {...register("VakWithRank")} className={s.submit} accept="text/csv" type="file"/>
                        </div>
                        <div>
                            <input className={s.submit} type="submit"/>
                        </div>
                    </form>
                    <form onSubmit={handleSubmit(onSubmitRsciJournalsRank)}>
                        RSCI journals rank:
                        <div>
                            <input  {...register("RsciJournalsRank")} className={s.submit} accept="text/csv"
                                    type="file"/>
                        </div>
                        <div>
                            <input className={s.submit} type="submit"/>
                        </div>
                    </form>
                    <form onSubmit={handleSubmit(onSubmitWhiteList)}>
                        White list:
                        <div>
                            <input className={s.submit}  {...register("WhiteList")} accept="text/csv" type="file"/>
                        </div>
                        <div>
                            <input className={s.submit} type="submit"/>
                        </div>
                    </form>
                    <form onSubmit={handleSubmit(onSubmitScopus)}>
                        Scopus:
                        <div>
                            <input className={s.submit} {...register("Scopus")} accept="text/csv" type="file"/>
                        </div>
                        <div>
                            <input className={s.submit} type="submit"/>
                        </div>
                    </form>
                    <form onSubmit={handleSubmit(onSubmitElibrary)}>
                        Elibrary:
                        <div>
                            <input className={s.submit} {...register("Elibrary")} accept="text/csv" type="file"/>
                        </div>
                        <div>
                            <input className={s.submit} type="submit"/>
                        </div>
                    </form>
                    <form onSubmit={handleSubmit(onSubmitJCR)}>
                        JCR:
                        <div>
                            <input className={s.submit} {...register("JCR")} accept="text/csv" type="file"/>
                        </div>
                        <div>
                            <input className={s.submit} type="submit"/>
                        </div>
                    </form>
                </div>
            </div>
        </div> : <Error404/>}
    </div>
}

export default UploadDate;
