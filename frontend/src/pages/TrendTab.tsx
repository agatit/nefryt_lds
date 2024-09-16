import React, {useEffect, useState, useCallback} from 'react';
import {Grid, GridColumn, GridToolbar} from '@progress/kendo-react-grid';
import '@progress/kendo-theme-default/dist/all.css';
import {Configuration, TrendsApiFactory, Trend, TrendDef, TrendParam} from "../services/api";
import {Button} from '@progress/kendo-react-buttons';
import '@progress/kendo-theme-default/dist/all.css';
import "../assets/pages/TrendTab.scss";
import TrendDialog from "../components/dialog/TrendDialog";
import TrendParamDialog from "../components/dialog/TrendParamDialog";

const apiConfig = new Configuration({
    basePath: 'http://192.168.30.36:8080',
});

const trendsApi = TrendsApiFactory(apiConfig);

const TrendTab = () => {
    const [trends, setTrends] = useState<Trend[]>([]);
    const [trendDefs, setTrendDefs] = useState<TrendDef[]>([]);
    const [selectedTrendParams, setSelectedTrendParams] = useState<TrendParam[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [isTrendDialogOpen, setIsTrendDialogOpen] = useState<boolean>(false);
    const [isTrendParamDialogOpen, setIsTrendParamDialogOpen] = useState<boolean>(false);
    const [trendFormData, setTrendFormData] = useState<Trend | null>(null);
    const [trendParamFormData, setTrendParamFormData] = useState<TrendParam | null>(null);
    const [selectedTrend, setSelectedTrend] = useState<Trend | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const trendsResponse = await trendsApi.listTrends();
                setTrends(trendsResponse.data);

                const trendDefsResponse = await trendsApi.listTrendDefs();
                setTrendDefs(trendDefsResponse.data);
            } catch (err) {
                console.error('Error fetching data:', err);
                setError((err as Error).message);
            }
        };

        fetchData();
    }, []);

    const fetchTrendParams = useCallback(async (trendId: number) => {
            try {
                const trendParamsResponse = await trendsApi.listTrendParams(trendId);
                setSelectedTrendParams(trendParamsResponse.data);
            } catch (err) {
                console.error('Error fetching trend params:', err);
                setError((err as Error).message);
            }
        }, []
    );

    const getTrendCaption = (trendDefID: string): string => {
        const trendDef = trendDefs.find(def => def.ID.match(trendDefID));
        return trendDef && trendDef.Name ? trendDef.Name : 'Unknown Trend';
    };

    const handleTrendSubmit = useCallback(async (data: Trend) => {
            try {
                console.log("Trend: ", data);
                console.log("TrendDefID", data.TrendDefID);
                if (trendFormData && trendFormData.ID) {
                    await trendsApi.updateTrend(trendFormData.ID, data);
                } else {
                    await trendsApi.createTrend(data);
                }
                setIsTrendDialogOpen(false);
                setTrendFormData(null);
                const trendsResponse = await trendsApi.listTrends();
                setTrends(trendsResponse.data);
            } catch (err) {
                console.error('Error submitting trend:', err);
                setError((err as Error).message);
            }
        }, [trendFormData]
    );

    const handleTrendParamSubmit = useCallback(async (data: TrendParam) => {
            try {
                if (trendParamFormData && trendParamFormData.TrendParamDefID) {
                    console.log("Data:", trendParamFormData.TrendID, " ", trendParamFormData.TrendParamDefID);

                    const body = JSON.stringify(data.Value);

                    await trendsApi.updateTrendParam(trendParamFormData.TrendID, trendParamFormData.TrendParamDefID, body);
                }
                setIsTrendParamDialogOpen(false);
                setTrendParamFormData(null);
                if (trendParamFormData) {
                    const trendParamsResponse = await trendsApi.listTrendParams(trendParamFormData.TrendID);
                    setSelectedTrendParams(trendParamsResponse.data);
                }
            } catch (err) {
                console.error('Error submitting trend param:', err);
                setError((err as Error).message);
            }
        }, [trendParamFormData]
    );

    const handleDeleteTrend = useCallback(async (trendId: number) => {
            try {
                await trendsApi.deleteTrendById(trendId);
                const trendsResponse = await trendsApi.listTrends();
                setTrends(trendsResponse.data);
            } catch (err) {
                console.error('Error deleting trend:', err);
                setError((err as Error).message);
            }
        }, []
    );

    const openTrendDialog = useCallback((data?: Trend) => {
        console.log("SET: ", data);
        setTrendFormData(data || {TrendDefID: '', RawMin: 0, RawMax: 0, ScaledMin: 0, ScaledMax: 0});
        setIsTrendDialogOpen(true);
    }, []);

    const openTrendParamDialog = useCallback((data: TrendParam) => {
        setTrendParamFormData(data);
        setIsTrendParamDialogOpen(true);
    }, []);

    const handleTrendSelection = useCallback(async (trend: Trend) => {
            setSelectedTrend(trend);
            if (trend.ID != null) {
                await fetchTrendParams(trend.ID);
            }
        }, [fetchTrendParams]
    );

    return (
        <div>
            <h2>Trends</h2>
            {error && <p style={{color: 'red'}}>{error}</p>}

            <div className="trend-dashboard">
                <GridToolbar>
                    <Button onClick={() => openTrendDialog()}>Add New Trend</Button>
                </GridToolbar>

                <Grid data={trends} className="grid-toolbar" onRowClick={(e) => handleTrendSelection(e.dataItem)}>
                    <GridColumn
                        field="TrendDefID"
                        title="Trend Definition"
                        cell={(props) => <td>{getTrendCaption(props.dataItem.TrendDefID)}</td>}
                    />
                    <GridColumn field="Name" title="Name"/>
                    <GridColumn field="RawMin" title="Raw Min"/>
                    <GridColumn field="RawMax" title="Raw Max"/>
                    <GridColumn field="ScaledMin" title="Scaled Min"/>
                    <GridColumn field="ScaledMax" title="Scaled Max"/>
                    <GridColumn
                        field="Actions"
                        title="Actions"
                        cell={(props) => (
                            <td>
                                <Button onClick={() => openTrendDialog(props.dataItem)}>Edit</Button>
                                <Button onClick={() => handleDeleteTrend(props.dataItem.ID)}>Delete</Button>
                            </td>
                        )}
                    />
                </Grid>

                {selectedTrendParams.length > 0 && selectedTrend && (
                    <div className="trend-params">
                        <h3>Parameters for {selectedTrend.Name}</h3>

                        <Grid data={selectedTrendParams} className="grid-toolbar">
                            <GridColumn field="TrendParamDefID" title="Parameter ID"/>
                            <GridColumn field="Value" title="Value"/>
                            <GridColumn field="DataType" title="DataType"/>
                            <GridColumn
                                field="Actions"
                                title="Actions"
                                cell={(props) => (
                                    <td>
                                        <Button onClick={() => openTrendParamDialog(props.dataItem)}>Edit</Button>
                                    </td>
                                )}
                            />
                        </Grid>
                    </div>
                )}
            </div>

            {isTrendDialogOpen && trendFormData && (
                <TrendDialog
                    data={trendFormData}
                    onSubmit={handleTrendSubmit}
                    onCancel={() => setIsTrendDialogOpen(false)}
                    trendDefs={trendDefs}/>

            )}

            {isTrendParamDialogOpen && (
                <TrendParamDialog
                    data={trendParamFormData}
                    onSubmit={handleTrendParamSubmit}
                    onCancel={() => setIsTrendParamDialogOpen(false)}
                />
            )}
        </div>
    );
};

export default TrendTab;
