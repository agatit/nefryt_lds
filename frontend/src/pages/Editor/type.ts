import { PropTypes } from "@material-ui/core"
import { ClassNameMap } from "@material-ui/core/styles/withStyles"
import { ComponentType } from "react"
import { InjectedFormProps } from "redux-form"
import { Pipeline } from "../../store/pipelineApi"


  interface ITrendDefType{
    TrendDefTypeID : number
    Name : string
  }

  interface ITrendDefGroup{
    TrendDefGroupID : number
    Name : string
    AnalisysOnly : boolean
  }

  interface ISIUnitGroup{
    SIUnitGroupID : number
    SIUnitGroupTID : string
    UnitgroupName : string 
  }

  interface ISIUnit{
    SIUnitTID : string
    SIUnitID : number
    Name : string
    Description : string
    Enabled : boolean
    ValueFactor : number
    ValueOffset : number
    SIUnitGroup : ISIUnitGroup | {}
  }

  export interface ITrendDef{
    TrendDefID : number
    Name : string
    TimeExponent : number
    Format : string
    SIUnit : ISIUnit
    TrendDefType : ITrendDefType
    TrendDefGroup : ITrendDefGroup
  }


 export interface INode{
    NodeID : number
    type : string
    Name : string
    positionX:number
    positionY:number
    TrendDef : ITrendDef | {}
  }

  export interface IPipelinesArea{
    Width : number
    ScaleWidth : number
    Height : number
    ScaleHeight : number
    SIUnit : ISIUnit
  }

  /*interface IPipeline{
    PipelineID : number
    Name : string
  }*/



  interface ISize{
    width:number
    height:number
  }

  interface IMoveNode{
    node : INode
    active : boolean
  }

 export const DRAG_NODE = "DRAG_NODE";

   export type EditorState = {
    pipelines : Pipeline[]
    forceRefresh : boolean,
    Nodes : INode[],
    Links : ILink[],
    area : IPipelinesArea
    //action : IEditorAction
    //activeEditor: string 
    activeNode : {
      node : INode | {},
      state : string
    }
  }

  export type PropertyEditorState = {
      activeTab:number;
  }


  export interface IPropertyEditorAction {
    type: string
    tabIndex : number
  }


   export interface IEditorAction {
    type: string
    data:any
    //nodes: INode[]
  }

  //export interface IEditorAction {
  //  type: string
  //  data: any
  //}

  export interface ILink {
    BeginNodeID : number
    EndNodeID : number
    beginPointX : number
    beginPointY : number
    endPointX : number
    endPointY : number
  }


 

