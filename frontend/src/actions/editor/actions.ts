import { IEditorAction, INode, IPropertyEditorAction } from "../../pages/Editor/type";
import { ACTIVE_NODE, CANCEL_NODE_ACTION, CHANGE_TAB, CLONE_NODE, DRAG_NODE, DROP_NODE, LINK_NODES, NEW_NODE, REMOVE_NODE, SAVE_NODE, UNLINK_NODES, USE_EDITOR_MONITORING, USE_EDITOR_NODES } from "./actionType";


export function setActiveNode(node:INode | {}) {
    var nodes : INode[] = [];
    if (node && (node as INode).NodeID > 0 ){
      nodes.push(node as INode);
    }
  
    const action: IEditorAction = {
      type: ACTIVE_NODE,
      nodes:nodes,
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
      nodes:nodes,
    }
   // console.log(action);
    return action;
  }
  
  export function dropNode() {
    
    const action: IEditorAction = {
      type: DROP_NODE,
      nodes:[],
    }
   // console.log(action);
    return action;
  }
  
  
  
  
  export function newNode() {
    const action: IEditorAction = {
      type: NEW_NODE,
      nodes:[],
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
      nodes:nodes,
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
      nodes:nodes,
    }
    return action;
  }
  
  export function useNodesEditor() {
    const action: IEditorAction = {
      type: USE_EDITOR_NODES,
      nodes:[],
    }
    return action;
  }
  
  export function useMonitoringEditor() {
    const action: IEditorAction = {
      type: USE_EDITOR_MONITORING,
      nodes:[],
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
      nodes:nodes,
    }
    return action;
  }
  
  export function cancelNodeAction() {
    const action: IEditorAction = {
      type: CANCEL_NODE_ACTION,
      nodes:[],
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
      nodes:nodes,
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
      nodes: nodes,
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