import { PropTypes } from "@material-ui/core"
import { ClassNameMap } from "@material-ui/core/styles/withStyles"
import { ComponentType } from "react"
import { InjectedFormProps } from "redux-form"


  interface ITrendDefType{
    TrendDefTypeID : number
    Name : sstring
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

  interface ITrendDef{
    TrendDefID : int
    Name : string
    TimeExponent : number
    Format : string
    SIUnit : ISIUnit
    TrendDefType : ITrendDefType
    TrendDefGroup : ITrendDefGroup
  }


  interface INode{
    NodeID : number
    type : string
    Name : string
    positionX:number
    positionY:number
    TrendDef : ITrendDef | {}
  }


  interface IPipeline{
    PipelineID : number
    Name : string
    Width : number
    ScaleWidth : number
    Height : number
    ScaleHeight : number
    SIUnit : ISIUnit
    Nodes : INode[] = []
    Links : ILink[] = []
  }



  interface ISize{
    width:number
    height:number
  }

  interface IMoveNode{
    node : INode
    active : boolean
  }


   export type EditorState = {
    pipeline : IPipeline
    action : IEditorAction
    activeEditor: string 
    activeNode : INode | {}
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
    nodes: INode[]
  }

  export interface ILink {
    BeginNodeID : number
    EndNodeID : number
    beginPointX : number
    beginPointY : number
    endPointX : number
    endPointY : number
  }


 

