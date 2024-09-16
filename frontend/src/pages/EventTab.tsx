import React, {useEffect, useState, useCallback} from 'react';
import {Grid, GridColumn} from '@progress/kendo-react-grid';
import '@progress/kendo-theme-default/dist/all.css';
import {Configuration, EventsApiFactory, Event, EventDef} from "../services/api";
import {Button} from '@progress/kendo-react-buttons';
import "../assets/pages/EventTab.scss";

const apiConfig = new Configuration({
    basePath: 'http://192.168.30.36:8080',
});

const eventsApi = EventsApiFactory(apiConfig);

const EventTab = () => {
    const [events, setEvents] = useState<Event[]>([]);
    const [eventDefs, setEventDefs] = useState<EventDef[]>([]);
    const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const eventsResponse = await eventsApi.listEvents();
                setEvents(eventsResponse.data);

                const eventDefsResponse = await eventsApi.listEventDefs();
                setEventDefs(eventDefsResponse.data);
            } catch (err) {
                console.error('Error fetching data:', err);
                setError((err as Error).message);
            }
        };

        fetchData();
    }, []);

    const getEventCaption = (eventDefID: string): string => {
        const eventDef = eventDefs.find((def: any) => def.ID?.trim() === eventDefID.trim());
        return eventDef && eventDef.Caption ? eventDef.Caption : 'Unknown Event';
    };

    const handleRowClick = useCallback(async (e: any) => {
        try {
            const eventDetails = await eventsApi.getEventById(e.dataItem.ID);
            setSelectedEvent(eventDetails.data);
        } catch (err) {
            console.error('Error fetching event details:', err);
            setError((err as Error).message);
        }
    }, []);

    const handleAcknowledge = useCallback(async (eventId: number) => {
        try {
            const eventToUpdate = events.find(event => event.ID === eventId);
            if (eventToUpdate && !eventToUpdate.AckDate) {
                const currentDate = new Date().toISOString();
                await eventsApi.ackEvent(eventId);

                setEvents(events.map(event =>
                    event.ID === eventId ? {...event, AckDate: currentDate} : event
                ));
            }
        } catch (err) {
            console.error('Error acknowledging event:', err);
            setError((err as Error).message);
        }
    }, [events]);

    return (
        <div>
            <h2>Events</h2>
            {error && <p style={{color: 'red'}}>{error}</p>}

            <div className="event-dashboard">
                <Grid data={events} onRowClick={handleRowClick} className="grid-toolbar">
                    <GridColumn
                        field="EventDefID"
                        title="Event Type"
                        cell={(props) => (<td>{getEventCaption(props.dataItem.EventDefID)}</td>)}
                    />
                    <GridColumn field="Verbosity" title="Severity"/>
                    <GridColumn field="Caption" title="Description"/>
                    <GridColumn field="BeginDate" title="Begin Date"/>
                    <GridColumn
                        field="AckDate"
                        title="Acknowledged Date"
                        cell={(props) => (
                            <td>
                                {props.dataItem.AckDate ? (
                                    props.dataItem.AckDate
                                ) : (
                                    <Button onClick={() => handleAcknowledge(props.dataItem.ID)}>Acknowledge</Button>
                                )}
                            </td>
                        )}
                    />
                </Grid>

                {selectedEvent && (
                    <div className="event-details">
                        <h3>Event Details</h3>
                        <p><strong>ID:</strong> {selectedEvent.ID}</p>
                        <p><strong>Method ID:</strong> {selectedEvent.MethodID}</p>
                        <p><strong>Event Definition ID:</strong> {selectedEvent.EventDefID}</p>
                        <p><strong>Verbosity:</strong> {selectedEvent.Verbosity}</p>
                        <p><strong>Caption:</strong> {selectedEvent.Caption}</p>
                        <p><strong>Details:</strong> {selectedEvent.Details || 'None'}</p>
                        <p><strong>Position:</strong> {selectedEvent.Position || 'None'}</p>
                        <p><strong>Silent:</strong> {selectedEvent.Silient ? 'Yes' : 'No'}</p>
                        <p><strong>Begin Date:</strong> {selectedEvent.BeginDate}</p>
                        <p><strong>Acknowledged Date:</strong> {selectedEvent.AckDate || 'None'}</p>
                        <p><strong>End Date:</strong> {selectedEvent.EndDate || 'None'}</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default EventTab;
