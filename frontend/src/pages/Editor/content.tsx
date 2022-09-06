import React from 'react';
import { shallowEqual, useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../app/store';
import { Dispatch } from '@reduxjs/toolkit';


import { NodeToolbox } from './Components/Node/Toolbox';
import { PipelineEditorWorkspace } from './Components/Workspace';
import NewNodeForm from './NewNodeForm';
import EditorAreaSettings from './EditorAreaSettings';
import { NodePropertyEditor } from './Components/nodePropertyEditor';
import { EditorState } from './type';




export const EditorContent: React.FC = () => { 
  const dispatch :Dispatch = useDispatch();
    
  const reducer: EditorState = useSelector(
    (state: RootState) => state.editor,
    shallowEqual
  )    


  var sidepanelClasses='sidepanel';


  //if ((activeNode) && ((activeNode as INode).NodeID > 0) && (DRAG_NODE.localeCompare( action.type)!=0)){
  //  sidepanelClasses = sidepanelClasses + ' open';
  //}

  const handleSubmitAreaEditor  = (e: any ) => {
    //e.preventDefault();
   // const form = e.currentTarget;
   //e.preventDefault();
  
    //console.log(document.forms[0]);
    console.log(e);
    //dispatch(reset('EditorAreaSettings'));  // requires form name
    //dispatch(cancelNodeAction());
  
  }
  

  
const handleSubmitNewNode  = (e: any ) => {
  console.log(e);
/*
  var node : INode = {NodeID : -1,
    type : form.elements.Type.value,
    Name : form.elements.Name.value,
    positionX:0,
    positionY:0,
    TrendDef : { } 
  }
*/
  //dispatch(createNode(node));

  //dispatch(reset('EditorAreaSettings'));  // requires form name
  //dispatch(cancelNodeAction());
}


             
  return (
    <>
      <React.Fragment>
          <div id='editor-body' className="table">
            <div className="table-row">
              <NodeToolbox editorState={reducer} ></NodeToolbox>
            </div>
            <PipelineEditorWorkspace editorState={reducer} ></PipelineEditorWorkspace>
          
          </div>
          <NewNodeForm onSubmit={handleSubmitNewNode} ></NewNodeForm>
          <EditorAreaSettings onSubmit={handleSubmitAreaEditor} ></EditorAreaSettings>
          <div id="mySidepanel" className={sidepanelClasses}>
          <NodePropertyEditor  ></NodePropertyEditor>
        </div>
      </React.Fragment>
    </>
  )
}