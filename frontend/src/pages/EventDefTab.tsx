import React, { useEffect, useState, useCallback } from 'react';
import { Grid, GridColumn, GridToolbar } from '@progress/kendo-react-grid';
import { Button } from '@progress/kendo-react-buttons';
import { Configuration, EventsApiFactory, EventDef } from "../services/api";
import EventDefDialog from "../components/dialog/EventDefDialog";
import "../assets/pages/EventDefTab.scss";

const apiConfig = new Configuration({
    basePath: 'http://192.168.30.36:8080',
});

const eventsApi = EventsApiFactory(apiConfig);

const EventDefTab = () => {
    const [eventDefs, setEventDefs] = useState<EventDef[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [isEventDefDialogOpen, setIsEventDefDialogOpen] = useState<boolean>(false);
    const [eventDefFormData, setEventDefFormData] = useState<EventDef | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const eventDefsResponse = await eventsApi.listEventDefs();
                setEventDefs(eventDefsResponse.data);
            } catch (err) {
                console.error('Error fetching event definitions:', err);
                setError((err as Error).message);
            }
        };

        fetchData();
    }, []);

    const handleEventDefSubmit = useCallback(async (data: EventDef) => {
        try {
            if (eventDefFormData && eventDefFormData.ID) {
                await eventsApi.updateEventDef(eventDefFormData.ID, data);
            } else {
                await eventsApi.createEventDef(data);
            }
            setIsEventDefDialogOpen(false);
            setEventDefFormData(null);
            const eventDefsResponse = await eventsApi.listEventDefs();
            setEventDefs(eventDefsResponse.data);
        } catch (err) {
            console.error('Error submitting event definition:', err);
            setError((err as Error).message);
        }
    }, [eventDefFormData]);

    const handleDeleteEventDef = useCallback(async (eventDefId: string) => {
        try {
            await eventsApi.deleteEventDefById(eventDefId);
            const eventDefsResponse = await eventsApi.listEventDefs();
            setEventDefs(eventDefsResponse.data);
        } catch (err) {
            console.error('Error deleting event definition:', err);
            setError((err as Error).message);
        }
    }, []);

    const openEventDefDialog = useCallback((data?: EventDef) => {
        setEventDefFormData(data || { ID: '', Verbosity: '', Caption: '', Silent: false, Visible: false, Enabled: false });
        setIsEventDefDialogOpen(true);
    }, []);

    return (
        <div>
            <h2>Event Definitions</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}

            <GridToolbar>
                <Button onClick={() => openEventDefDialog()}>Add Event Definition</Button>
            </GridToolbar>

            <Grid data={eventDefs}>
                <GridColumn field="ID" title="ID" />
                <GridColumn field="Caption" title="Caption" />
                <GridColumn field="Verbosity" title="Verbosity" />
                <GridColumn
                    field="Actions"
                    title="Actions"
                    cell={(props) => (
                        <td>
                            <Button onClick={() => openEventDefDialog(props.dataItem)}>Edit</Button>
                            <Button onClick={() => handleDeleteEventDef(props.dataItem.ID)}>Delete</Button>
                        </td>
                    )}
                />
            </Grid>

            {isEventDefDialogOpen && eventDefFormData && (
                <EventDefDialog
                    onClose={() => setIsEventDefDialogOpen(false)}
                    onSubmit={handleEventDefSubmit}
                    initialValues={eventDefFormData}
                />
            )}
        </div>
    );
};

export default EventDefTab;
