import React, {useEffect, useState, useCallback} from 'react';
import {Grid, GridColumn, GridToolbar} from '@progress/kendo-react-grid';
import {Button} from '@progress/kendo-react-buttons';
import {EventsApiFactory, EventDef} from "../services/api";
import EventDefDialog from "../components/dialog/EventDefDialog";
import "../assets/pages/EventDefTab.scss";
import apiConfig from "../services/apiConfig";

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
        setEventDefFormData(data || {
            ID: '',
            Verbosity: '',
            Caption: '',
            Silent: false,
            Visible: false,
            Enabled: false
        });
        setIsEventDefDialogOpen(true);
    }, []);

    return (
        <div className="event-def-tab">
            <h2 className="event-def-title">Event Definitions</h2>
            {error && <p style={{color: 'red'}}>{error}</p>}

            <div className="event-def-dashboard">
                <GridToolbar>
                    <Button className="custom-button" onClick={() => openEventDefDialog()}>Add Event Definition</Button>
                </GridToolbar>

                <Grid data={eventDefs} className="grid-toolbar">
                    <GridColumn field="ID" title="ID"/>
                    <GridColumn field="Caption" title="Caption"/>
                    <GridColumn field="Verbosity" title="Verbosity"/>
                    <GridColumn
                        field="Actions"
                        title="Actions"
                        cell={(props) => (
                            <td>
                                <Button className="edit-button" onClick={() => openEventDefDialog(props.dataItem)}>Edit</Button>
                                <Button className="delete-button" onClick={() => handleDeleteEventDef(props.dataItem.ID)}>Delete</Button>
                            </td>
                        )}
                    />
                </Grid>
            </div>

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
