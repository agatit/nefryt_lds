import React, {useCallback, useEffect, useState} from 'react';
import {
    Chart,
    ChartCategoryAxis,
    ChartCategoryAxisItem,
    ChartSeries,
    ChartSeriesItem,
    ChartValueAxis,
    ChartValueAxisItem
} from '@progress/kendo-react-charts';
import '@progress/kendo-theme-default/dist/all.css';
import {Configuration, TrendData, TrendsApiFactory, Trend} from "../services/api";
import {Form, Field, FormElement, FormRenderProps, FieldWrapper} from '@progress/kendo-react-form';
import {Input} from '@progress/kendo-react-inputs';
import {DateTimePicker, DateTimePickerChangeEvent} from '@progress/kendo-react-dateinputs';
import {Button} from '@progress/kendo-react-buttons';
import '../assets/pages/TrendChartTab.scss';

const apiConfig = new Configuration({
    basePath: 'http://192.168.30.36:8080',
});

const trendsApi = TrendsApiFactory(apiConfig);

interface FormData {
    startTime: Date | null;
    endTime: Date | null;
    samples: number;
}

const defaultFormData: FormData = {
    startTime: new Date('2022-08-29T14:08:24'),
    endTime: new Date('2022-08-29T14:08:27'),
    samples: 3,
};

const TrendChartTab = () => {
    const [trendData, setTrendData] = useState<TrendData[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [trendDefs, setTrendDefs] = useState<Trend[]>([]);
    const [formData, setFormData] = useState<FormData>(defaultFormData);

    const fetchTrendData = useCallback(async (start: Date | null, end: Date | null, samples: number) => {
        if (!start || !end || samples <= 0) return;

        const startTime = Math.floor(start.getTime() / 1000);
        const endTime = Math.floor(end.getTime() / 1000);

        try {
            const trendsResponse = await trendsApi.listTrends();
            setTrendDefs(trendsResponse.data);

            if (trendsResponse.data.length > 0) {
                const trendIdList = trendsResponse.data.map(trend => trend.ID).join(',');

                const trendDataResponse = await trendsApi.getTrendData(trendIdList, startTime, endTime, samples);
                setTrendData(trendDataResponse.data);
            }
        } catch (err) {
            console.error('Error fetching trend data:', err);
            setError((err as Error).message);
        }
    }, []);

    useEffect(() => {
        fetchTrendData(formData.startTime, formData.endTime, formData.samples);
    }, [fetchTrendData, formData.endTime, formData.samples, formData.startTime]);

    const getSeries = useCallback(() => {
        return trendDefs.map((trend, index) => {
            const seriesData = trendData.map(data => data.Data ? data.Data[index]?.Value : null);
            return {
                name: trend.Name || `Trend ${index + 1}`,
                data: seriesData
            };
        });
    }, [trendData, trendDefs]);

    const filteredCategories = trendData.map((data, index, arr) => {
        const currentTimestamp = new Date(data.Timestamp * 1000);
        const previousTimestamp = index > 0 ? new Date(arr[index - 1].Timestamp * 1000) : null;
        return previousTimestamp && previousTimestamp.getSeconds() === currentTimestamp.getSeconds()
            ? "" : currentTimestamp.toLocaleString();
    });

    const handleFormSubmit = useCallback((dataItem: any) => {
        setFormData(dataItem);
        fetchTrendData(dataItem.startTime, dataItem.endTime, dataItem.samples);
    }, [fetchTrendData]);

    const handleDateChange = useCallback((field: keyof FormData) => (event: DateTimePickerChangeEvent) => {
        setFormData(prev => ({
            ...prev,
            [field]: event.value
        }));
    }, []);

    return (
        <div className="trend-chart-tab">
            <h2>Trend Chart</h2>
            {error && <p style={{color: 'red'}}>{error}</p>}

            <div className="trend-data">
                <Chart>
                    <ChartCategoryAxis>
                        <ChartCategoryAxisItem
                            categories={filteredCategories}
                            labels={{rotation: "auto"}}
                            title={{text: "Time"}}
                        />
                    </ChartCategoryAxis>
                    <ChartValueAxis>
                        <ChartValueAxisItem title={{text: "Value"}}/>
                    </ChartValueAxis>
                    <ChartSeries>
                        {getSeries().map((series, index) => (
                            <ChartSeriesItem
                                key={index}
                                type="line"
                                data={series.data}
                                name={series.name}
                                markers={{visible: false}}
                            />
                        ))}
                    </ChartSeries>
                </Chart>
            </div>

            <Form
                initialValues={formData}
                onSubmit={handleFormSubmit}
                render={(formRenderProps: FormRenderProps) => (
                    <FormElement>
                        <fieldset className="k-form-fieldset">
                            <legend className="k-form-legend">Enter parameters:</legend>

                            <FieldWrapper>
                                <label className="k-form-label">Start Time</label>
                                <DateTimePicker
                                    value={formData.startTime}
                                    onChange={handleDateChange('startTime')}
                                    format="yyyy-MM-dd HH:mm:ss"
                                />
                            </FieldWrapper>

                            <FieldWrapper>
                                <label className="k-form-label">End Time</label>
                                <DateTimePicker
                                    value={formData.endTime}
                                    onChange={handleDateChange('endTime')}
                                    format="yyyy-MM-dd HH:mm:ss"
                                />
                            </FieldWrapper>

                            <FieldWrapper>
                                <Field
                                    name="samples"
                                    component={Input}
                                    label="Samples"
                                    type="number"
                                />
                            </FieldWrapper>
                        </fieldset>

                        <div className="k-form-buttons">
                            <Button
                                type="submit"
                                disabled={!formRenderProps.allowSubmit}
                            >
                                Apply
                            </Button>
                        </div>
                    </FormElement>
                )}
            />
        </div>
    );
};

export default TrendChartTab;
