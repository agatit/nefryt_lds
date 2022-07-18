import * as React from "react";
import { useSelector, shallowEqual, useDispatch } from "react-redux"
import { Dispatch } from "redux"
import { RootState } from "../..";
import { useEffect } from "react";
import { EditorState, IEditorAction, INode } from "./type";
import {Layout} from '../../components/template/Layout'
import { cancelNodeAction, setActiveNode, setNodeList, setPipelineList } from "../../actions/editor/actions";
import NewNodeForm from "./NewNodeForm";
import { NodePropertyEditor } from "./Components/nodePropertyEditor";
import { NodeToolbox } from "./Components/Node/Toolbox";
import { PipelineEditorWorkspace } from "./Components/Workspace";
import { DRAG_NODE, NEW_NODE } from "../../actions/editor/actionType";

import "../../index.css"
import "./Components/Node/nodestyle.css"
import 'bootstrap/dist/css/bootstrap.min.css';
import "./style.css";
import { listNodes, listPipelines } from "../../apis";
import { ForceRequestsCallback, useRequest } from "redux-query-react";
import reducer, { getEntities, getQueries } from "../../store";
import EditorAreaSettings from "./EditorAreaSettings";
import {reset} from 'redux-form';
import {updateEntities} from "redux-query"

const drawerWidth = 240;
var refreshNodes : ForceRequestsCallback;

const EditorPage: React.FC = () => {
  const dispatch: Dispatch= useDispatch();

  const queries = useSelector(getQueries) || [];
  const entities = useSelector(getEntities) || [];
  

  var queryPipelineList;
  var queryNodeList;
  var queryLinkList;

  queryPipelineList = listPipelines(
    {
     //queryKey:'pipeline_list',
     transform: (body:any, text:any) => {
    //  console.log(body);
       return {
         
         pipeline_list: body,
       }
     },
     update:{
      pipeline_list: (oldValue: any, newValue: any) => {
         
         return (newValue);
       },
     },
   });

   

   const [PipelineListState] = useRequest(queryPipelineList);


   

   queryNodeList = listNodes(
    {
     transform: (body:any, text:any) => {
       return {

         node_list: body,
       }
     },
     update:{
      node_list: (oldValue: any, newValue: any) => {
         
         return (newValue);
       },
     },
   });


   const [NodeListState, refreshNodes] = useRequest(queryNodeList);

   
   /*queryLinkList = listLinks(
    {
     transform: (body:any, text:any) => {
       return {

         node_list: body,
       }
     },
     update:{
      node_list: (oldValue: any, newValue: any) => {
         
         return (newValue);
       },
     },
   });


   const [LinkListState] = useRequest(queryLinkList);

   */

  const state: EditorState = useSelector(
    (state: RootState) => state.pipelineEditorReducer,
    shallowEqual
  )
  const activeEditor: string = useSelector(
    (state: RootState) => state.pipelineEditorReducer.activeEditor,
    shallowEqual
  )
  const activeNode: INode | {} = useSelector(
    (state: RootState) => state.pipelineEditorReducer.activeNode,
    shallowEqual
  )
  const action: IEditorAction = useSelector(
    (state: RootState) => state.pipelineEditorReducer.action,
    shallowEqual
  )

  if (state.forceRefresh){
    refreshNodes();
  }

 
  const closePropertyEditor = (e: React.MouseEvent<HTMLElement>) => {
    dispatch(setActiveNode({}));
  }

  if ((PipelineListState.isFinished) && (!state.loaded.pipeline)) {
    //console.log(entities.pipeline_list);
    dispatch(setPipelineList(entities.pipeline_list));
  }

  //console.log(state.Nodes);
  
  if ((NodeListState.isFinished) && (!state.loaded.nodes) && (!state.forceRefresh)) {
    //console.log(entities.node_list);
    dispatch(setNodeList(entities.node_list));
  }


  //console.log(state.pipelines);
  
  const modal: boolean = useSelector(
       (state: RootState) => state.pipelineEditorReducer.action.type == NEW_NODE,
      shallowEqual
   )

  
  var width : number=0;
  var height : number=0;
  
  if (state.area){
    width = (state.area.Width % state.area.ScaleWidth) == 0 ?  Math.floor(state.area.Width / state.area.ScaleWidth) : Math.floor(state.area.Width / state.area.ScaleWidth) + 1;
    height = (state.area.Height % state.area.ScaleHeight) == 0 ?  Math.floor(state.area.Height / state.area.ScaleHeight) : Math.floor(state.area.Height / state.area.ScaleHeight) + 1;
  }
 

  useEffect(() => {
    const handleEsc = (event: { keyCode: number; }) => {
       if (event.keyCode === 27) {
        dispatch(cancelNodeAction());
      }
    };
    window.addEventListener('keydown', handleEsc);
    
  }, []);

  var sidepanelClasses='sidepanel';


  if ((activeNode) && ((activeNode as INode).NodeID > 0) && (DRAG_NODE.localeCompare( action.type)!=0)){
    sidepanelClasses = sidepanelClasses + ' open';
  }

  
const handleSubmitAreaEditor  = (e: any ) => {
  //e.preventDefault();
 // const form = e.currentTarget;
 //e.preventDefault();

  //console.log(document.forms[0]);
  console.log(e);
  dispatch(reset('EditorAreaSettings'));  // requires form name
  dispatch(cancelNodeAction());

}
  
  return (
    <div className={'root'}>
      <Layout onmouseup={undefined}  rPanel={{open:false, visible:false, 
              content:
              <></> 
              }} content={
        <React.Fragment>
          <div id='editor-body' className="table">
            <div className="table-row">
              <NodeToolbox editorState={state} action={action} activeEditor={activeEditor} ></NodeToolbox>
            </div>
            <PipelineEditorWorkspace editorState={state} action={action} acctiveNode={activeNode} ></PipelineEditorWorkspace>
          
          </div>
          <NewNodeForm ></NewNodeForm>
          <EditorAreaSettings onSubmit={handleSubmitAreaEditor} ></EditorAreaSettings>
          <div id="mySidepanel" className={sidepanelClasses}>
          <NodePropertyEditor  ></NodePropertyEditor>
        </div>
      </React.Fragment>
      } />  
      
    </div>
  )
}

export {EditorPage}