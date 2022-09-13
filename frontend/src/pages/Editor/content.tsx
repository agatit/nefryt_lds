import React from 'react';
import { shallowEqual, useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../app/store';
import { Dispatch } from '@reduxjs/toolkit';


import { NodeToolbox } from './Components/Node/Toolbox';
import { PipelineEditorWorkspace } from './Components/Workspace';
import NewNodeForm from './NewNodeForm';
import EditorAreaSettings from './EditorAreaSettings';
import { NodePropertyEditor } from './Components/nodePropertyEditor';
import { EditorState, INode, SELECTED } from './type';
import { LinkPropertyEditor } from './Components/linkPropertyEditor';




export const EditorContent: React.FC = () => { 
  const dispatch :Dispatch = useDispatch();
    
  const reducer: EditorState = useSelector(
    (state: RootState) => state.editor,
    shallowEqual
  )    


  var sidepanelClasses='sidepanel';


  if (((reducer.activeElement.node) && (((reducer.activeElement.node as INode).NodeID as number) > 0)  || (reducer.activeElement.LinkID > 0)) && (reducer.activeElement.state == SELECTED))  {
    sidepanelClasses = sidepanelClasses + ' open';
  }

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
  //alert('AAA');
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
              <NodeToolbox state={reducer} ></NodeToolbox>
            </div>
            <PipelineEditorWorkspace state={reducer} ></PipelineEditorWorkspace>
          
          </div>
          <NewNodeForm onSubmit={handleSubmitNewNode} ></NewNodeForm>
          <EditorAreaSettings onSubmit={handleSubmitAreaEditor} ></EditorAreaSettings>
          <div id="mySidepanel" className={sidepanelClasses}>
           {reducer.activeElement.node ? <NodePropertyEditor></NodePropertyEditor> : <LinkPropertyEditor  ></LinkPropertyEditor>}
          </div>
      </React.Fragment>
    </>
  )
}