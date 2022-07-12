
import { EditorState, IEditorAction, ILink, INode } from "../pages/Editor/type"
import * as pipelineEditorAction from "../actions/editor/actions"
import { ACTIVE_NODE, BROWSE, CANCEL_NODE_ACTION, CLONE_NODE, DRAG_NODE, DROP_NODE, LINK_NODES, MOVE_NODE, NEW_NODE, REMOVE_NODE, SAVE_NODE, UNLINK_NODES, USE_EDITOR_MONITORING, USE_EDITOR_NODES } from "../actions/editor/actionType"

const initialState: EditorState = {
    pipeline : {
      PipelineID : 1,
      Name : 'Rurociąg 1',
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
      Nodes :  [
                  {Name:'AAA', NodeID : 1, TrendDef:{}, type : 'VALVE', positionX:130,positionY:100},
                  {Name:'BBB', NodeID : 2, TrendDef:{}, type : 'TEMP',  positionX:50,positionY:50},
                  {Name:'CC', NodeID : 3, TrendDef:{}, type : 'TANK', positionX:230,positionY:200},
                  {Name:'DD', NodeID : 4, TrendDef:{}, type : 'PRESS',  positionX:150,positionY:200},
              ],
       Links : [
         {BeginNodeID:1, EndNodeID:2, beginPointX:-1, beginPointY:-1,endPointX:-1,endPointY:-1},
         {BeginNodeID:3, EndNodeID:4,beginPointX:-1, beginPointY:-1,endPointX:-1,endPointY:-1}
       ],
            
    },
    action:{
      type:BROWSE,
      nodes : []
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
           pipeline: state.pipeline, action:{ type : NEW_NODE, nodes : []}
          }
        } 
        case SAVE_NODE:{
          //console.log(action.type);
          if (state.action.type == MOVE_NODE){
            state.pipeline.Nodes.push(action.nodes[0]);
            var aa : EditorState = {pipeline: state.pipeline, action:{type : MOVE_NODE, nodes : []}, activeEditor : state.activeEditor, activeNode:state.activeNode};

          }else{
            var aa : EditorState = {pipeline: state.pipeline, action:{type : MOVE_NODE, nodes : action.nodes}, activeEditor : state.activeEditor, activeNode:state.activeNode};
          }

          return {
            ...state,
            ...aa
          }
        } 
        case CANCEL_NODE_ACTION:{
         // console.log(state.action);
          if ((state.action.nodes) && (state.action.nodes).length >0){
            state.pipeline.Nodes.push(state.action.nodes[0]);
           // console.log(state.pipeline);
          }
          return {
            ...state,
           pipeline: state.pipeline, action:{ type : BROWSE, nodes : []}
          }
        } 
        case MOVE_NODE:{
          if (action.nodes && (action.nodes).length > 0){
           // var node : INode[] = state.pipeline.Nodes.filter(node => node.NodeID!=(action.nodes[0]).NodeID);
           // node[0].positionX = action.nodes[0].positionX;
           // node[0].positionY = action.nodes[0].positionY;
            //state.pipeline.Nodes = state.pipeline.Nodes.filter(node => node.NodeID!=(action.nodes[0]).NodeID);
            
          }
          return {
            ...state,
            pipeline: state.pipeline , action:{ type : BROWSE, nodes : []}, activeNode:{}
          }
        } 
        case CLONE_NODE:{
          var nodes :INode[] = [];
          var nodeChoosen = false;
          if (action.nodes &&(action.nodes).length){
            nodes.push({...action.nodes[0]});
            (nodes[0]).NodeID = -1;
            nodeChoosen = true;
          }
          return {
            ...state,
            pipeline: state.pipeline , action:{ type : nodeChoosen?  MOVE_NODE : CLONE_NODE, nodes : nodes}
          }
        } 
        case REMOVE_NODE:{
          var nodeChoosen = false;
          if (action.nodes && (action.nodes.length > 0) && (action.nodes[0]).NodeID > 0){
            state.pipeline.Nodes = state.pipeline.Nodes.filter(node => node.NodeID!=(action.nodes[0]).NodeID);
            nodeChoosen = true;
          }
          return {
            ...state,
            pipeline: state.pipeline , action:{ type : nodeChoosen?  REMOVE_NODE : REMOVE_NODE, nodes : nodeChoosen ? [] : action.nodes}
          }
        } 
        case LINK_NODES:{
          var nodeChoosen = false;
        //  console.log(state.action.nodes);
          if (action.nodes && (action.nodes.length > 0) && ((action.nodes[0]).NodeID > 0)){
            if ((state.action.nodes) && (state.action.nodes.length==1)){
              var newLink : ILink = {
                BeginNodeID: (state.action.nodes[0]).NodeID, EndNodeID: (action.nodes[0]).NodeID, beginPointX: 0, beginPointY: 0, endPointX : 0, endPointY: 0
              }
                 
              state.pipeline.Links.push(newLink);
              nodeChoosen = true;
            }else{
              state.action.nodes.push(action.nodes[0])
            }
            
          }
          return {
            ...state,
            pipeline: state.pipeline , action:{ type : nodeChoosen?  BROWSE : LINK_NODES, nodes : nodeChoosen? [] : state.action.nodes}
          }
        } 
        case UNLINK_NODES:{
          var nodeChoosen = false;
        //  console.log(state.action.nodes);
          if (action.nodes && (action.nodes.length > 0) && ((action.nodes[0]).NodeID > 0)){
            if ((state.action.nodes) && (state.action.nodes.length==1)){
              
                 
              state.pipeline.Links = state.pipeline.Links.filter(link => ((link.BeginNodeID != state.action.nodes[0].NodeID) && (link.EndNodeID != action.nodes[0].NodeID)) && ((link.EndNodeID != state.action.nodes[0].NodeID) && (link.BeginNodeID != action.nodes[0].NodeID)));
              nodeChoosen = true;
            }else{
              state.action.nodes.push(action.nodes[0])
            }
            
          }
          return {
            ...state,
            pipeline: state.pipeline , action:{ type : nodeChoosen?  BROWSE : UNLINK_NODES, nodes : nodeChoosen? [] : state.action.nodes}
          }
        } 
        case USE_EDITOR_NODES:{
          
          return {
            ...state,
            pipeline: state.pipeline , action:{ type : BROWSE, nodes : []}, activeEditor:USE_EDITOR_NODES
          }
        } 
        case USE_EDITOR_MONITORING:{
          
          return {
            ...state,
            pipeline: state.pipeline , action:{ type : BROWSE, nodes : []}, activeEditor:USE_EDITOR_MONITORING
          }
        } 
        case DRAG_NODE:{
          var nodeChoosen = false;
          if (action.nodes && (action.nodes.length > 0) && (action.nodes[0]).NodeID > 0){
            nodeChoosen = true;
          }
          return {
            ...state,
            pipeline: state.pipeline , action:{ type : DRAG_NODE, nodes : []}, activeEditor:USE_EDITOR_MONITORING, activeNode: nodeChoosen? action.nodes[0] : {}
          }
        } 
        case ACTIVE_NODE:{
          var nodeChoosen = false;
          if (action.nodes && (action.nodes.length > 0) && (action.nodes[0]).NodeID > 0){
            nodeChoosen = true;
          }
          return {
            ...state,
            pipeline: state.pipeline , action:{ type : ACTIVE_NODE, nodes : []}, activeEditor:USE_EDITOR_MONITORING, activeNode: nodeChoosen? action.nodes[0] : {}
          }
        } 
        case DROP_NODE:{
          var nodeChoosen = false;
          if (action.nodes && (action.nodes.length > 0) && (action.nodes[0]).NodeID > 0){
            nodeChoosen = true;
          }
          return {
            ...state,
            pipeline: state.pipeline , action:{ type : BROWSE, nodes : []}, activeEditor:USE_EDITOR_MONITORING, activeNode:  {}
          }
        } 
       
    }
    return state
  }
  
  export default editorReducer