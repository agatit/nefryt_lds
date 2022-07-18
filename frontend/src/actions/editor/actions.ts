import { IEditorAction, INode, IPropertyEditorAction } from "../../pages/Editor/type";
import { ACTIVE_NODE, CANCEL_NODE_ACTION, CHANGE_TAB, CLONE_NODE, CREATE_NODE, DRAG_NODE, DROP_NODE, EDITOR_AREA_SETTINGS, LINK_NODES, LOAD_NODE_LIST, LOAD_PIPELINE_LIST, NEW_NODE, REFRESH_DATA, REMOVE_NODE, SAVE_NODE, UNLINK_NODES, USE_EDITOR_MONITORING, USE_EDITOR_NODES } from "./actionType";


export function setActiveNode(node:INode | {}) {
    var nodes : INode[] = [];
    if (node && (node as INode).NodeID > 0 ){
      nodes.push(node as INode);
    }
  
    const action: IEditorAction = {
      type: ACTIVE_NODE,
      data:nodes,
    }
    return action;
  }
  
  export function dragNode(node:INode | {}) {
    var nodes : INode[] = [];
    if (node && (node as INode).NodeID){
      nodes.push(node as INode);
    }
    const action: IEditorAction = {
      type: DRAG_NODE,
      data:nodes,
    }
   // console.log(action);
    return action;
  }
  
  export function dropNode() {
    
    const action: IEditorAction = {
      type: DROP_NODE,
      data:[],
    }
   // console.log(action);
    return action;
  }

  export function refreshData() {
    
    const action: IEditorAction = {
      type: REFRESH_DATA,
      data:[],
    }
   // console.log(action);
    return action;
  }
  
  
  
  export function setEditorArea() {
    const action: IEditorAction = {
      type: EDITOR_AREA_SETTINGS,
      data:[],
    }
    return action;
  }





  export function newNode() {
    const action: IEditorAction = {
      type: NEW_NODE,
      data:[],
    }
    return action;
  }
  
  export function linkNodes(node:INode | {}) {
    var nodes : INode[] = [];
    if (node && (node as INode).NodeID > 0 ){
      nodes.push(node as INode);
    }
    const action: IEditorAction = {
      type: LINK_NODES,
      data:nodes,
    }
    return action;
  }
  
    
  export function unlinkNodes(node:INode | {}) {
    var nodes : INode[] = [];
    if (node && (node as INode).NodeID > 0 ){
      nodes.push(node as INode);
    }
    const action: IEditorAction = {
      type: UNLINK_NODES,
      data:nodes,
    }
    return action;
  }
  
  export function useNodesEditor() {
    const action: IEditorAction = {
      type: USE_EDITOR_NODES,
      data:[],
    }
    return action;
  }
  
  export function useMonitoringEditor() {
    const action: IEditorAction = {
      type: USE_EDITOR_MONITORING,
      data:[],
    }
    return action;
  }
  
  export function cloneNode(node:INode | {}) {
    var nodes : INode[] = [];
    if (node && (node as INode).NodeID){
      nodes.push(node as INode);
    }
    const action: IEditorAction = {
      type: CLONE_NODE,
      data:nodes,
    }
    return action;
  }
  
  export function cancelNodeAction() {
    const action: IEditorAction = {
      type: CANCEL_NODE_ACTION,
      data:[],
    }
    return action;
  }
    
  export function saveNode(node:INode) {
    var nodes : INode[] = [];
    if (node && (node as INode).NodeID){
      nodes.push(node as INode);
    }
    const action: IEditorAction = {
      type: SAVE_NODE,
      data:nodes,
    }
    return action;
  }

  export function createNode(node:INode) {
    var nodes : INode[] = [];
    if (node && (node as INode).NodeID){
      nodes.push(node as INode);
    }
    const action: IEditorAction = {
      type: CREATE_NODE,
      data:nodes,
    }
    return action;
  }
    
  export function removeNode(node: INode | {}) {
    var nodes : INode[] = [];
    if (node && (node as INode).NodeID > 0){
      nodes.push(node as INode);
    }
    const action: IEditorAction = {
      type: REMOVE_NODE,
      data: nodes,
    }
    return action;
  }
  
  export function changeTab(index:number) {
      
    const action: IPropertyEditorAction = {
      type: CHANGE_TAB,
      tabIndex:index
    }
    return action;
  }



  export function setPipelineList(data:any) {
 
    const action: IEditorAction = {
      type: LOAD_PIPELINE_LIST,
      data : data
    }
    return action;
  }

  
  export function setNodeList(data:any) {
 
    const action: IEditorAction = {
      type: LOAD_NODE_LIST,
      data : data
    }
    return action;
  }