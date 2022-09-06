import * as React from "react"
import { Dispatch } from "redux"
import { shallowEqual, useDispatch, useSelector } from "react-redux"
import { EditorState, INode, ITrendDef } from "../../type"
import { RootState } from "../../../../app/store"
import { dragNode, setActiveNode } from "../../../../features/editor/editorSlice"


type Props = {
  node: INode | {}
  selected : boolean
  removeNode: (node: INode|{}) => void
}


export const NodeElm: React.FC<Props> = (p) => {
  const dispatch: Dispatch<any> = useDispatch()

  function deleteNode(n : INode | {}){
    p.removeNode(n);
  }

 
  const reducer: EditorState = useSelector(
    (state: RootState) => state.editor,
    shallowEqual
  )


  const onDragStart = (e: React.MouseEvent<HTMLElement>) => {
    var id :string  = (e.currentTarget as HTMLElement).parentElement?  ((e.currentTarget as HTMLElement).parentElement as HTMLElement).id : '';
    var nodeID : RegExpMatchArray | null = id.match(/\d+/g);
    if (nodeID && (nodeID as RegExpMatchArray).length==1){
      var ID : number = parseInt((nodeID as RegExpMatchArray)[0]);
      
      var tmpNode : INode[] = reducer.Nodes.filter(node => node.NodeID==ID);
      
      dispatch(dragNode(tmpNode[0] as INode));
      //dispatch(setActiveNode(tmpNode[0] as INode));
    }
  }



 const nodeClick = (e: React.MouseEvent<HTMLElement>) => {
    var id :string = (e.currentTarget as HTMLElement).id;
    var nodeID : RegExpMatchArray | null = id.match(/\d+/g);
    if (nodeID && (nodeID as RegExpMatchArray).length==1){
      var ID : number = parseInt((nodeID as RegExpMatchArray)[0]);
      var tmpNode : INode[] = reducer.Nodes.filter(node => node.NodeID==ID);
    
      dispatch(setActiveNode(tmpNode[0] as INode));
    }
 }

 var id :number = p.node ? (p.node as INode).NodeID : -1;
 var name : string = p.node ? (p.node as INode).Name : '';
 var nodeType : string = p.node ? (p.node as INode).type : 'unknown_node_type'; 
 var TrendDef : ITrendDef | {}  = p.node ? (p.node as INode).TrendDef : {};

 var classes = "node " + nodeType;
 var idd : string = id ? id.toString() : '-1';
 var id_s : string = 'node_' + idd;  
 if (p.selected){
  classes = classes + " selected"  
 }

  return (
    <div className="node" id={id_s} onClick={nodeClick} >
      <span draggable="true" className={classes} onDragStart={onDragStart} > 
        
      </span>
    </div>
  )
}