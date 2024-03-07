import React from "react";
import {fetchAnalysis} from "../../store/slices/AnalysisSlice";
import {useDispatch, useSelector} from "react-redux";
import {ResponsiveBar} from '@nivo/bar'
import {fetchAnalysisSourceRating} from "../../store/slices/AnalysisSourceRatingSlice";
import style from "./AnalysisDate.modole.css"
import {fetchAnalysisOrganization} from "../../store/slices/AnalysisOrganizationSlice";

const AnalysisDate = () => {
    const dispatch = useDispatch();
    const {analysis} = useSelector(state => state.analysis)
    const {analysisSourceRating} = useSelector(state => state.analysisSourceRating)
    const {analysisOrganization} = useSelector(state => state.analysisOrganization)

    React.useEffect(() => {
        try {
            dispatch(fetchAnalysis())
            dispatch(fetchAnalysisSourceRating())
            dispatch(fetchAnalysisOrganization())
        } catch (e) {
            console.log(e);
        }

    }, []);

    const YearData = {
        keys: ["count"],
        data: analysis.result,
        margin: {
            top: 50,
            right: 120,
            bottom: 50,
            left: 80
        },

        colors: "#06c895",


        colorBy: "id",
        indexBy: "year",
        groupMode: "grouped",
        layout: "vertical",
        enableGridX: true,
        enableGridY: true,
        axisLeft: {
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legend: "Количество публикаций",
            legendPosition: "middle",
            legendOffset: -40,
        },
        axisBottom: {
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legend: "Год",
            legendPosition: "middle",
            legendOffset: 36,
        },
        padding: 0.3,
        innerPadding: 0,
        reverse: false,
        borderRadius: 0,
        borderWidth: 0,
        borderColor: {
            from: "color",
            modifiers: [["darker", "1.6"]]
        },
        isInteractive: false,
        enableLabel: true,
        labelSkipWidth: 0,
        labelSkipHeight: 0,
        labelTextColor: {
            from: "color",
            modifiers: [["darker", "1.6"]]
        }
    };


    return <div>
        <div>
            Количество публикаций в университете за год
        </div>
        <div id = 'block' style={{height: 400}}>
            <ResponsiveBar {...YearData} />
        </div>
        <div>
            Количество публикаций университета в рейтингах
        </div>
        <div style={{height: 400}}>
            <ResponsiveBar
                data={analysisSourceRating.result}
                keys={["2018", "2019", "2020", "2021", "2022", "2023"]}
                indexBy="name"
                margin={{top: 50, right: 130, bottom: 50, left: 60}}
                padding={0.3}
                groupMode="grouped"
                valueScale={{type: 'linear'}}
                indexScale={{type: 'band', round: true}}
                colors={{scheme: 'nivo'}}
                legends={[
                    {
                        dataFrom: 'keys',
                        anchor: 'bottom-right',
                        direction: 'column',
                        justify: false,
                        translateX: 120,
                        translateY: 0,
                        itemsSpacing: 2,
                        itemWidth: 100,
                        itemHeight: 20,
                        itemDirection: 'left-to-right',
                        itemOpacity: 0.85,
                        symbolSize: 20,
                        effects: [
                            {
                                on: 'hover',
                                style: {
                                    itemOpacity: 1
                                }
                            }
                        ]
                    }
                ]}

                borderColor={{
                    from: 'color',
                    modifiers: [
                        [
                            'darker',
                            1.6
                        ]
                    ]
                }}

                axisTop={null}
                axisRight={null}
                animate={true}
                motionConfig="default"
                isInteractive={true}

                axisBottom={{
                    tickSize: 5,
                    tickPadding: 5,
                    tickRotation: 0,
                    legend: 'Рейтинг',
                    legendPosition: 'middle',
                    legendOffset: 32
                }}
                axisLeft={{
                    tickSize: 5,
                    tickPadding: 5,
                    tickRotation: 0,
                    legend: 'Публикации',
                    legendPosition: 'middle',
                    legendOffset: -43
                }}
                labelSkipWidth={12}
                labelSkipHeight={12}
                labelTextColor={{
                    from: 'color',
                    modifiers: [
                        [
                            'darker',
                            1.6
                        ]
                    ]
                }}


            />
        </div>
        <div>
            Количество публикаций университетов
        </div>
        <div style={{height: 400}}>
            <ResponsiveBar
                data={analysisOrganization.result}
                keys={["2018", "2019", "2020", "2021", "2022", "2023"]}
                indexBy="name"
                margin={{top: 50, right: 130, bottom: 50, left: 60}}
                padding={0.3}
                groupMode="grouped"

                valueScale={{type: 'linear'}}
                indexScale={{type: 'band', round: true}}
                colors={{scheme: 'nivo'}}
                legends={[
                    {
                        dataFrom: 'keys',
                        anchor: 'bottom-right',
                        direction: 'column',
                        justify: false,
                        translateX: 120,
                        translateY: 0,
                        itemsSpacing: 2,
                        itemWidth: 100,
                        itemHeight: 20,
                        itemDirection: 'left-to-right',
                        itemOpacity: 0.85,
                        symbolSize: 20,
                        effects: [
                            {
                                on: 'hover',
                                style: {
                                    itemOpacity: 1
                                }
                            }
                        ]
                    }
                ]}

                borderColor={{
                    from: 'color',
                    modifiers: [
                        [
                            'darker',
                            1.6
                        ]
                    ]
                }}

                axisTop={null}
                axisRight={null}
                animate={true}
                motionConfig="default"
                axisBottom={null}
                axisLeft={{
                    tickSize: 5,
                    tickPadding: 5,
                    tickRotation: 0,
                    legend: 'Публикации',
                    legendPosition: 'middle',
                    legendOffset: -43
                }}
                labelSkipWidth={12}
                labelSkipHeight={12}
                labelTextColor={{
                    from: 'color',
                    modifiers: [
                        [
                            'darker',
                            1.6
                        ]
                    ]
                }}


            />
        </div>
    </div>
}

export default AnalysisDate;