import {ChartParams } from "../../components/chart/type"



export type IEventsAction ={
    type: string
    data :  any
}


export type EventsState = {
    table : EventParams
}

export type EventParams = {
    data: any,
    pageInfo: any
  }