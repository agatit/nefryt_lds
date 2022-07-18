
import { EditorState, IEditorAction, ILink, INode } from "../pages/Editor/type"
import * as pipelineEditorAction from "../actions/editor/actions"
import { ACTIVE_NODE, BROWSE, CANCEL_NODE_ACTION, CLONE_NODE, CREATE_NODE, DRAG_NODE, DROP_NODE, EDITOR_AREA_SETTINGS, LINK_NODES, LOAD_NODE_LIST, LOAD_PIPELINE_LIST, MOVE_NODE, NEW_NODE, REFRESH_DATA, REMOVE_NODE, SAVE_NODE, UNLINK_NODES, USE_EDITOR_MONITORING, USE_EDITOR_NODES } from "../actions/editor/actionType"
import {Node} from "../models/Node"

const initialState: EditorState = {
     area:{
      Width : 1000,
      ScaleWidth : 10,
      Height : 400,
      ScaleHeight : 10,
      SIUnit :{ 
          SIUnitTID : 'm',
          SIUnitID : 1,
          Name : 'metry',
          Description : 'metry',
          Enabled : true,
          ValueFactor : 1,
          ValueOffset : 1,
          SIUnitGroup : {} 
        },
     },
     forceRefresh : false,
     Nodes :  [
     // {Name:'AAA', NodeID : 1, TrendDef:{}, type : 'VALVE', positionX:130,positionY:100},
     // {Name:'BBB', NodeID : 2, TrendDef:{}, type : 'TEMP',  positionX:50,positionY:50},
     // {Name:'CC', NodeID : 3, TrendDef:{}, type : 'TANK', positionX:230,positionY:200},
     // {Name:'DD', NodeID : 4, TrendDef:{}, type : 'PRESS',  positionX:150,positionY:200},
    ],
    Links : [
    //{BeginNodeID:1, EndNodeID:2, beginPointX:-1, beginPointY:-1,endPointX:-1,endPointY:-1},
    //{BeginNodeID:3, EndNodeID:4,beginPointX:-1, beginPointY:-1,endPointX:-1,endPointY:-1}
    ],
    pipelines : [],
    //pipeline_loaded:false,
    loaded:{
      pipeline : false,
      nodes : false,
      links  : false
    },
    action:{
      type:BROWSE,
      data : []
    },
    activeEditor: USE_EDITOR_NODES,  
    activeNode: {}
  }

const editorReducer = (
    state: EditorState = initialState,
    action: IEditorAction
  ): EditorState => {
    switch (action.type) {
      
        case NEW_NODE:{
          return {
            ...state,
           forceRefresh:false, loaded:state.loaded, area:state.area, Nodes : state.Nodes, Links:state.Links, pipelines: state.pipelines, action:{ type : NEW_NODE, data : []}
          }
        } 
        case EDITOR_AREA_SETTINGS:{
          return {
            ...state,
            forceRefresh:false,loaded:state.loaded, area:state.area, Nodes : state.Nodes, Links:state.Links, pipelines: state.pipelines, action:{ type : EDITOR_AREA_SETTINGS, data : []}
          }
        } 
        
        case SAVE_NODE:{
          console.log(action.type);
          console.log(action.data);
          if (state.action.type == MOVE_NODE){
            state.Nodes.push(action.data[0]);
            var aa : EditorState = {forceRefresh:false,loaded:state.loaded, area:state.area, Nodes : state.Nodes, Links:state.Links, pipelines: state.pipelines, action:{type : MOVE_NODE, data : action.data}, activeEditor : state.activeEditor, activeNode:state.activeNode};

          }else{
            var aa : EditorState = {forceRefresh:false,loaded:state.loaded, area:state.area, Nodes : state.Nodes, Links:state.Links, pipelines: state.pipelines, action:{type : MOVE_NODE, data : action.data}, activeEditor : state.activeEditor, activeNode:state.activeNode};
          }

          return {
            ...state,
            ...aa
          }
        } 
        case CREATE_NODE:{
          console.log(action.type);
          console.log(action.data);
          if (state.action.type == MOVE_NODE){
           // state.Nodes.push(action.data[0]);
            var aa : EditorState = {forceRefresh:false,loaded:state.loaded, area:state.area, Nodes : state.Nodes, Links:state.Links, pipelines: state.pipelines, action:{type : MOVE_NODE, data : action.data}, activeEditor : state.activeEditor, activeNode:state.activeNode};

          }else{
            var aa : EditorState = {forceRefresh:false,loaded:state.loaded, area:state.area, Nodes : state.Nodes, Links:state.Links, pipelines: state.pipelines, action:{type : MOVE_NODE, data : action.data}, activeEditor : state.activeEditor, activeNode:state.activeNode};
          }

          return {
            ...state,
            ...aa
          }
        } 

        case CANCEL_NODE_ACTION:{
         // console.log(state.action);
          if ((state.action.data) && (state.action.data).length >0){
            state.Nodes.push(state.action.data[0]);
           // console.log(state.pipeline);
          }
          return {
            ...state,
            forceRefresh:false,loaded:state.loaded, area:state.area, Nodes : state.Nodes, Links:state.Links, pipelines: state.pipelines, action:{ type : BROWSE, data : []}
          }
        } 
        case MOVE_NODE:{
          if (action.data && (action.data).length > 0){
           // var node : INode[] = state.pipeline.Nodes.filter(node => node.NodeID!=(action.nodes[0]).NodeID);
           // node[0].positionX = action.nodes[0].positionX;
           // node[0].positionY = action.nodes[0].positionY;
            //state.pipeline.Nodes = state.pipeline.Nodes.filter(node => node.NodeID!=(action.nodes[0]).NodeID);
            
          }
          return {
            ...state,
            forceRefresh:false,loaded:state.loaded, area:state.area, Nodes : state.Nodes, Links:state.Links, pipelines: state.pipelines, action:{ type : BROWSE, data : []}, activeNode:{}
          }
        } 
        case CLONE_NODE:{
          var nodes :INode[] = [];
          var nodeChoosen = false;
          if (action.data &&(action.data).length){
            nodes.push({...action.data[0]});
            (nodes[0]).NodeID = -1;
            nodeChoosen = true;
          }
          return {
            ...state,
            forceRefresh:false,loaded:state.loaded, area:state.area, Nodes : state.Nodes, Links:state.Links, pipelines: state.pipelines, action:{ type : nodeChoosen?  MOVE_NODE : CLONE_NODE, data : nodes}
          }
        } 
        case REMOVE_NODE:{
          var nodeChoosen = false;
          if (action.data && (action.data.length > 0) && (action.data[0]).NodeID > 0){
            state.Nodes = state.Nodes.filter(node => node.NodeID!=(action.data[0]).NodeID);
            nodeChoosen = true;
          }
          return {
            ...state,
            forceRefresh:false,loaded:state.loaded, area:state.area, Nodes : state.Nodes, Links:state.Links, pipelines: state.pipelines, action:{ type : nodeChoosen?  REMOVE_NODE : REMOVE_NODE, data : nodeChoosen ? [] : action.data}
          }
        } 
        case LINK_NODES:{
          var nodeChoosen = false;
        //  console.log(state.action.nodes);
          if (action.data && (action.data.length > 0) && ((action.data[0]).NodeID > 0)){
            if ((state.action.data) && (state.action.data.length==1)){
              var newLink : ILink = {
                BeginNodeID: (state.action.data[0]).NodeID, EndNodeID: (action.data[0]).NodeID, beginPointX: 0, beginPointY: 0, endPointX : 0, endPointY: 0
              }
                 
              state.Links.push(newLink);
              nodeChoosen = true;
            }else{
              state.action.data.push(action.data[0])
            }
            
          }
          return {
            ...state,
            forceRefresh:false,loaded:state.loaded, area:state.area, Nodes : state.Nodes, Links:state.Links, pipelines: state.pipelines, action:{ type : nodeChoosen?  BROWSE : LINK_NODES, data : nodeChoosen? [] : state.action.data}
          }
        } 
        case UNLINK_NODES:{
          var nodeChoosen = false;
        //  console.log(state.action.nodes);
          if (action.data && (action.data.length > 0) && ((action.data[0]).NodeID > 0)){
            if ((state.action.data) && (state.action.data.length==1)){
              
                 
              state.Links = state.Links.filter(link => ((link.BeginNodeID != state.action.data[0].NodeID) && (link.EndNodeID != action.data[0].NodeID)) && ((link.EndNodeID != state.action.data[0].NodeID) && (link.BeginNodeID != action.data[0].NodeID)));
              nodeChoosen = true;
            }else{
              state.action.data.push(action.data[0])
            }
            
          }
          return {
            ...state,
            forceRefresh:false,loaded:state.loaded, area:state.area, Nodes : state.Nodes, Links:state.Links, pipelines: state.pipelines, action:{ type : nodeChoosen?  BROWSE : UNLINK_NODES, data : nodeChoosen? [] : state.action.data}
          }
        } 
        case USE_EDITOR_NODES:{
          
          return {
            ...state,
            forceRefresh:false,loaded:state.loaded, area:state.area, Nodes : state.Nodes, Links:state.Links, pipelines: state.pipelines, action:{ type : BROWSE, data : []}, activeEditor:USE_EDITOR_NODES
          }
        } 
        case USE_EDITOR_MONITORING:{
          
          return {
            ...state,
            forceRefresh:false,loaded:state.loaded, area:state.area, Nodes : state.Nodes, Links:state.Links, pipelines: state.pipelines, action:{ type : BROWSE, data : []}, activeEditor:USE_EDITOR_MONITORING
          }
        } 
        case DRAG_NODE:{
          var nodeChoosen = false;
          if (action.data && (action.data.length > 0) && (action.data[0]).NodeID > 0){
            nodeChoosen = true;
          }
          return {
            ...state,
            forceRefresh:false,loaded:state.loaded, area:state.area, Nodes : state.Nodes, Links:state.Links, pipelines: state.pipelines, action:{ type : DRAG_NODE, data : []}, activeEditor:USE_EDITOR_MONITORING, activeNode: nodeChoosen? action.data[0] : {}
          }
        } 
        case ACTIVE_NODE:{
          var nodeChoosen = false;
          if (action.data && (action.data.length > 0) && (action.data[0]).NodeID > 0){
            nodeChoosen = true;
          }
          return {
            ...state,
            forceRefresh:false,loaded:state.loaded, area:state.area, Nodes : state.Nodes, Links:state.Links, pipelines: state.pipelines, action:{ type : ACTIVE_NODE, data : []}, activeEditor:USE_EDITOR_MONITORING, activeNode: nodeChoosen? action.data[0] : {}
          }
        } 
        case DROP_NODE:{
          var nodeChoosen = false;
          if (action.data && (action.data.length > 0) && (action.data[0]).NodeID > 0){
            nodeChoosen = true;
          }
          return {
            ...state,
            forceRefresh:false,loaded:state.loaded, area:state.area, Nodes : state.Nodes, Links:state.Links, pipelines: state.pipelines, action:{ type : BROWSE, data : []}, activeEditor:USE_EDITOR_MONITORING, activeNode:  {}
          }
        } 
        case LOAD_PIPELINE_LIST:{
          //console.log(action.data);
          return {
            ...state,
            forceRefresh:false,loaded:{pipeline:true, nodes: state.loaded.nodes, links : state.loaded.links}, area:state.area, Nodes : state.Nodes, Links:state.Links, pipelines: action.data, action:{ type : BROWSE, data : []}, activeEditor:USE_EDITOR_MONITORING, activeNode: {}
          }
        } 
         case LOAD_PIPELINE_LIST:{
          //console.log(action.data);
          return {
            ...state,
            forceRefresh:false,loaded:{pipeline:true, nodes: state.loaded.nodes, links : state.loaded.links}, area:state.area, Nodes : state.Nodes, Links:state.Links, pipelines: action.data, action:{ type : BROWSE, data : []}, activeEditor:USE_EDITOR_MONITORING, activeNode: {}
          }
        } 
        case LOAD_NODE_LIST:{
          console.log(action.data);
          var nds : Node[] = action.data;
          var nodeList : INode [] = [];
           
          var idx=0;
          nds.forEach((element: Node) => {
            var nodeElement : INode = {
              NodeID: element.iD,
              type: element.type,
              Name: element.name? element.name : "",
              positionX: element.editorParams? element.editorParams.posX : 100,
              positionY: element.editorParams? element.editorParams.posY : 100,
              TrendDef: {}
            };
            nodeList.push(nodeElement);
            idx++;
          });
  
          return {
            ...state,
            forceRefresh:false,loaded:{pipeline:state.loaded.pipeline, nodes: true, links : state.loaded.links}, area:state.area, Nodes : nodeList, Links:state.Links, pipelines: state.pipelines, action:{ type : BROWSE, data : []}, activeEditor:USE_EDITOR_MONITORING, activeNode: {}
          }
        } 
        case REFRESH_DATA:{
          return {
            ...state,
            forceRefresh:true,loaded:{pipeline:false, nodes: false, links : false}, area:state.area, Nodes : [], Links:[], pipelines: [], action:{ type : BROWSE, data : []}, activeEditor:USE_EDITOR_MONITORING, activeNode: {}
          }
        }
    }
    return state
  }
  
  export default editorReducer