import {ChartParams } from "../../components/chart/type"



export type IEventsAction ={
    type: string
    data :  any
}


export type EventsState = {
    table : EventParams,
    is_loading:boolean
}

export type EventParams = {
    nodes: any,
    pageInfo: any
  }