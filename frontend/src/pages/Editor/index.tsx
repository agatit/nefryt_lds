import * as React from "react";
import { useSelector, shallowEqual, useDispatch } from "react-redux"
import { Dispatch } from "redux"
import { RootState } from "../..";
import { useEffect } from "react";
import { IEditorAction, INode, IPipeline } from "./type";
import {Layout} from '../../components/template/Layout'
import { cancelNodeAction, setActiveNode } from "../../actions/editor/actions";
import NewNodeForm from "./NewNodeForm";
import { NodePropertyEditor } from "./Components/nodePropertyEditor";
import { NodeToolbox } from "./Components/Node/Toolbox";
import { PipelineEditorWorkspace } from "./Components/Workspace";
import { DRAG_NODE, NEW_NODE } from "../../actions/editor/actionType";

import "../../index.css"
import "./Components/Node/nodestyle.css"
import 'bootstrap/dist/css/bootstrap.min.css';
import "./editor.css";

const drawerWidth = 240;


const EditorPage: React.FC = () => {
  const dispatch: Dispatch= useDispatch();


  const pipeline: IPipeline = useSelector(
    (state: RootState) => state.pipelineEditorReducer.pipeline,
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

 
  const closePropertyEditor = (e: React.MouseEvent<HTMLElement>) => {
    dispatch(setActiveNode({}));
  }

  
  
  const modal: boolean = useSelector(
       (state: RootState) => state.pipelineEditorReducer.action.type == NEW_NODE,
      shallowEqual
   )

  
  var width : number=0;
  var height : number=0;
  
  if (pipeline){
    width = (pipeline.Width % pipeline.ScaleWidth) == 0 ?  Math.floor(pipeline.Width / pipeline.ScaleWidth) : Math.floor(pipeline.Width / pipeline.ScaleWidth) + 1;
    height = (pipeline.Height % pipeline.ScaleHeight) == 0 ?  Math.floor(pipeline.Height / pipeline.ScaleHeight) : Math.floor(pipeline.Height / pipeline.ScaleHeight) + 1;
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

  return (
    <div className={'root'}>
      <Layout onmouseup={undefined}  rPanel={{open:false, visible:false, 
              content:
              <></> 
              }} content={
        <React.Fragment>
          <div id='editor-body' className="table">
            <div className="table-row">
              <NodeToolbox pipeline={pipeline} action={action} activeEditor={activeEditor} ></NodeToolbox>
            </div>
            <PipelineEditorWorkspace pipeline={pipeline} action={action} acctiveNode={activeNode} ></PipelineEditorWorkspace>
          
          </div>
          <NewNodeForm ></NewNodeForm>
          <div id="mySidepanel" className={sidepanelClasses}>
          <NodePropertyEditor  ></NodePropertyEditor>
        </div>
      </React.Fragment>
      } />  
      
    </div>
  )
}

export {EditorPage}