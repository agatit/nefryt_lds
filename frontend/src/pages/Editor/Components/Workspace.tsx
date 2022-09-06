import * as React from "react"
import { Dispatch } from "redux"
import { useDispatch } from "react-redux"
import {NodeElm} from "./Node/node" 
import { useEffect } from "react";
import { EditorState, IEditorAction, INode } from "../type"
import $ from "jquery"
import { mutateAsync, updateEntities } from "redux-query";
import { CropLandscapeOutlined } from "@material-ui/icons";
import { useMutation } from "redux-query-react";
import { removeNode } from "../../../features/editor/editorSlice";

  type Props = {
    state : EditorState;
   // action : IEditorAction;
   // acctiveNode:INode | {};
  }

  const editorMouseEntere = (e: React.MouseEvent<HTMLElement>) => {
    var sl = $('#editor-draw-area').scrollLeft();
    var st = $('#editor-draw-area').scrollTop();
    if (sl==undefined){
      sl=0;
    }
    if (st==undefined){
      st=0;
    }
    
    var x = e.pageX - 120 - 40 +  sl;
    var y = e.pageY -50 -40 + st;

    if (((Math.floor(x/20)-1) *20) > parseInt($('#editor-vertical-indicator').css('left')) + 20) {
      x= (Math.floor(x/20) + 1)*20;
    }else if (((Math.floor(x/20))*20) < parseInt($('#editor-vertical-indicator').css('left'))){
      x = (Math.floor(x/20)-1)*20;
    }else{
      x =  (Math.floor(x/20)-1)*20;
    }
      
    if (((Math.floor(y/20)-1) *20) > parseInt($('#editor-horizontal-indicator').css('top')) + 20) {
      y= (Math.floor(y/20) + 1)*20;
    }else if (((Math.floor(y/20))*20) < parseInt($('#editor-horizontal-indicator').css('top'))){
      y = (Math.floor(y/20)-1)*20;
    }else{
      y = (Math.floor(y/20)-1)*20;
    }
    
    $('#editor-vertical-indicator').css({'left': x});
    $('#editor-horizontal-indicator').css({'top': y});
    
    $('#editor-horizontal-indicator').show();
    $('#editor-vertical-indicator').show();

    $('#tmp-Node').css({'margin-left': x+'px', 'margin-top': y+'px'});       
  }
    

  const editorMouseLeave  = (e: React.MouseEvent<HTMLElement>) => {  
    $('#editor-horizontal-indicator').hide();
    $('#editor-vertical-indicator').hide();
  }
    
  export const PipelineEditorWorkspace: React.FC<Props> = (p) => {
    const dispatch: Dispatch<any> = useDispatch()

    let content = [];
    let row = [];
    let positionsVertical = [];
    let positionsHorizontal = [];

    let nodes: any[] = [];
    
    var width : number=0;
    var height : number=0;

    const onDrop = (e: React.MouseEvent<HTMLElement>) => {
     {/* if ((p.acctiveNode) && (p.acctiveNode as INode).NodeID > 0){
        var id :string = (e.target as HTMLElement).id;
          var position : RegExpMatchArray | null = id.match(/\d+/g);
        if ((position as RegExpMatchArray).length==2){
          (p.acctiveNode as INode).positionX = Math.floor((parseInt((position as RegExpMatchArray)[1]))/2)* p.editorState.area.ScaleHeight;
          (p.acctiveNode as INode).positionY = Math.floor((parseInt((position as RegExpMatchArray)[0]))/2)* p.editorState.area.ScaleWidth;
           var aa : UpdateNodeRequest = {
             nodeId: 0
           }
           var nodeA : Node = {
             iD: (p.acctiveNode as INode).NodeID,
             editorParams: {
               posX: (p.acctiveNode as INode).positionX,
               posY: (p.acctiveNode as INode).positionY
             },
             type: (p.acctiveNode as INode).type
           }
          var queryUpdateNode = updateNode(
            {
              nodeId: (p.acctiveNode as INode).NodeID,
              node: nodeA
           });
           

           //queryUpdateNode.optimisticUpdate = true;
          //dispatch( mutateAsync (queryUpdateNode));
           

         // dispatch(dropNode());
        }
      }*/}
    }
    const allowDrop = (e: React.MouseEvent<HTMLElement>) => {
      e.preventDefault();
    }

    const link_horizontalClick  = async (e: any) => {
      if (e.target.classList.contains('selected')){
        e.target.classList.remove('selected');
        console.log(e.target.classList);
      }else{
        e.target.classList.add('selected');
        console.log(e.target.classList);
        for (var x=0; x< e.target.classList.length; x++){
          let pattern1 = /Link_/g;
          let result1 = pattern1.test(e.target.classList[x]);
          if (result1){
            const collection = document.getElementsByClassName(e.target.classList[x]);
            for (var y=0; y< collection.length; y++){
              collection[y].classList.add("selected");
            }
            break;
          }
        }
      }
    }

    const editorMouseClick  = async (e: React.MouseEvent<HTMLElement>) => {
      var id :string = (e.target as HTMLElement).id;
      var position : RegExpMatchArray | null = id.match(/\d+/g);
      if (position && (position as RegExpMatchArray).length==2){
        
      {/* if (p.editorState.action.type=='MOVE_NODE'){
          console.log('DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD');
          if ((p.editorState.action.data) && (p.editorState.action.data.length > 0)){
          var nodeA : Node = {
            editorParams: {
              posX: Math.floor((parseInt((position as RegExpMatchArray)[1]))/2)* p.editorState.area.ScaleHeight,
              posY: Math.floor((parseInt((position as RegExpMatchArray)[0]))/2)* p.editorState.area.ScaleHeight
            },
            type: (p.editorState.action.data[0] as INode).type,
            name: (p.editorState.action.data[0] as INode).Name,
            iD: 0
          }
         var queryCreateNode = createNode(
           {
             node: nodeA
          });
console.log(nodeA);
          queryCreateNode.optimisticUpdate = true;
          try{
            var todo = await mutateAsync (queryCreateNode);
            dispatch(todo);
            dispatch(refreshData());

          }catch(error){
            console.log(error);
          }
        }
      
        }
      */}
      }
    }


    const clearLink = (i: number) => {
      var beginPosX = p.state.Links[i].beginPointX;
      var beginPosY = p.state.Links[i].beginPointY;

      var lengthX  = p.state.Links[i].endPointX - p.state.Links[i].beginPointX;
      var lengthY  = p.state.Links[i].endPointY - p.state.Links[i].beginPointY;

      var markY : number=1;
      var lenY : number =1;
      var markX : number=1;
      var lenX : number =1;
      if (lengthY < 0){
        markY=-1;
        lenY=0;
      }
      if (lengthX < 0){
        markX=-1;
        lenX=0;
      }
      
      for (let j=0; j< (Math.abs(lengthY) *2) + lenY; j++){
        strPosX = (beginPosX * 2).toString();
        strPosY = ((beginPosY *2)+(markY*j)).toString(); 
        var cellid_ : string = 'cell_' + strPosY + '_'+ strPosX;
        var cell_ : HTMLElement = document.getElementById(cellid_) as HTMLElement;
      }
      //poziome
      for (let j=0; j< Math.abs(lengthX) *2; j++){
        strPosX = ((beginPosX * 2) + (markX *j)+lenX).toString();
        strPosY = ((beginPosY *2)+(lengthY *2) ).toString(); 
        var cellid_ : string = 'cell_' + strPosY + '_'+ strPosX;
        var cell_ : HTMLElement = document.getElementById(cellid_) as HTMLElement;
        cell_.classList.remove("link_horizontal");
      }
    }


    useEffect(() => {
      var strPosX : string;
      var strPosY : string;

     
      var lengthX : number = 0;
      var lengthY : number = 0;
      $('.table-cell').removeClass('link_horizontal');
      $('.table-cell').removeClass('link_vertical');
      for (let i=0; i<p.state.Links.length;i++){  
        /*var BeginNode : INode = p.state.Nodes.find((x: { NodeID: any }) => x.NodeID === p.state.Links[i].BeginNodeID) as INode;
        var EndNode : INode = p.state.Nodes.find((x: { NodeID: any }) => x.NodeID === p.state.Links[i].EndNodeID) as INode;
        if (BeginNode && EndNode && (BeginNode.positionX) && (BeginNode.positionY)){
          beginPosX  = (BeginNode.positionX % p.state.area.ScaleWidth) == 0 ?  Math.floor(BeginNode.positionX / p.state.area.ScaleWidth) : Math.floor(BeginNode.positionX / p.state.area.ScaleWidth) + 1;
          beginPosY = (BeginNode.positionY % p.state.area.ScaleHeight) == 0 ?  Math.floor(BeginNode.positionY / p.state.area.ScaleHeight) : Math.floor(BeginNode.positionY / p.state.area.ScaleHeight) + 1;
        
          endPosX  = (EndNode.positionX % p.state.area.ScaleWidth) == 0 ?  Math.floor(EndNode.positionX / p.state.area.ScaleWidth) : Math.floor(EndNode.positionX / p.state.area.ScaleWidth) + 1;
          endPosY = (EndNode.positionY % p.state.area.ScaleHeight) == 0 ?  Math.floor(EndNode.positionY / p.state.area.ScaleHeight) : Math.floor(EndNode.positionY / p.state.area.ScaleHeight) + 1;
            
          lengthX  = endPosX - beginPosX;
          lengthY  = endPosY - beginPosY;

          if ((beginPosX !=  p.state.Links[i].beginPointX) || (beginPosY !=  p.state.Links[i].beginPointY)
            ||  (endPosX !=  p.state.Links[i].endPointX) || (endPosY !=  p.state.Links[i].endPointY)){
          
          }
          
          p.state.Links[i].beginPointX = beginPosX;
          p.state.Links[i].beginPointY = beginPosY;

          p.state.Links[i].endPointX = endPosY;
          p.state.Links[i].endPointY = endPosY;
            */
          lengthX = p.state.Links[i].endPointX -  p.state.Links[i].beginPointX;
          lengthY = p.state.Links[i].endPointY - p.state.Links[i].beginPointY;  
          
          var markY : number=1;
          var lenY : number =1;
          var markX : number=1;
          var lenX : number =1;
          if (lengthY < 0){
            markY=-1;
            lenY=0;
          }

          if (lengthX < 0){
            markX=-1;
            lenX=0;
          }
            
          for (let j=0; j< (Math.abs(lengthY) *2) + lenY; j++){
            strPosX = (p.state.Links[i].beginPointX * 2).toString();
            strPosY = ((p.state.Links[i].beginPointY *2)+(markY*j)).toString(); 
            var cellid_ : string = 'cell_' + strPosY + '_'+ strPosX;
            var cell_ : HTMLElement = document.getElementById(cellid_) as HTMLElement;
            cell_.classList.add("link_vertical");
            cell_.classList.add("Link_" + p.state.Links[i].ID);
          }
          
          //poziome
          for (let j=0; j< Math.abs(lengthX) *2; j++){
            strPosX = ((p.state.Links[i].beginPointX * 2) + (markX *j)+lenX).toString();
            strPosY = ((p.state.Links[i].beginPointY *2)+(lengthY *2) ).toString(); 

            var cellid_ : string = 'cell_' + strPosY + '_'+ strPosX;
            var cell_ : HTMLElement = document.getElementById(cellid_) as HTMLElement;
            cell_.classList.add("link_horizontal");
            cell_.classList.add("Link_" + p.state.Links[i].ID);
            cell_.onclick = link_horizontalClick;
        
          }
      //else{

      //}
    }
    
  });


  if (p.state){
    let nodes:any[] = [];
    for (let i=0;i<p.state.Nodes.length;i++){
        var posX :number = (p.state.Nodes[i].positionX % p.state.area.ScaleWidth) == 0 ?  Math.floor(p.state.Nodes[i].positionX / p.state.area.ScaleWidth) : Math.floor(p.state.Nodes[i].positionX / p.state.area.ScaleWidth) + 1;
        var posY : number = (p.state.Nodes[i].positionY % p.state.area.ScaleHeight) == 0 ?  Math.floor(p.state.Nodes[i].positionY / p.state.area.ScaleHeight) : Math.floor(p.state.Nodes[i].positionY / p.state.area.ScaleHeight) + 1;
    
        var strPosX : string = (posX * 2).toString();
        var strPosY : string = (posY *2).toString(); 
        var cellid : string = 'cell_' + strPosY + '_'+ strPosX;

        var selected=(p.state.activeNode) && ((p.state.activeNode.node as INode).NodeID == p.state.Nodes[i].NodeID);
        nodes.push({cell_id :cellid, node:<NodeElm key={i} node={p.state.Nodes[i]} removeNode={()=>removeNode(p.state.Nodes[i]) } selected={selected} ></NodeElm>})
    }

    width = (p.state.area.Width % p.state.area.ScaleWidth) == 0 ?  Math.floor(p.state.area.Width / p.state.area.ScaleWidth) : Math.floor(p.state.area.Width / p.state.area.ScaleWidth) + 1;
    height = (p.state.area.Height % p.state.area.ScaleHeight) == 0 ?  Math.floor(p.state.area.Height / p.state.area.ScaleHeight) : Math.floor(p.state.area.Height / p.state.area.ScaleHeight) + 1;
    
    for(let iW = 0; iW <= (width *2) + 1 ; iW++)	{
      row.push(<div className="table-cell" key={iW} style={{height:20, width:20, left:20*iW }}  onMouseLeave={editorMouseLeave}  onMouseEnter={editorMouseEntere}></div>);
    }
    
    for(let iW = 0; iW <= width ; iW++)	{
      positionsHorizontal.push(<p key={iW}><span>{iW*p.state.area.ScaleWidth}<br/>[{p.state.area.SIUnit.SIUnitTID}]</span></p>);
    }
    for (let i = 0; i <= (height *2)+1; i++) {
      row=[];
      for(let iW = 0; iW <= (width *2) + 1 ; iW++)	{
          let id = 'cell_' + i.toString() + '_' + iW.toString();
          var n :any = nodes.filter(a=>a.cell_id == id);    
          row.push(<div  id={id}  className="table-cell" key={iW} style={{height:20, width:20, left:20*iW }} onClick={editorMouseClick} onDragOver={allowDrop} onDrop={onDrop}  onMouseLeave={editorMouseLeave}  onMouseEnter={editorMouseEntere}>{n.length > 0? n[0].node : ''}</div>);
        } 
        content.push(<div className="table-row" style={{height:20}} key={i}>{row}</div>);
    }
    
    for (let i = 0; i <= height; i++) {
      positionsVertical.push(<p key={i}><span>{i*p.state.area.ScaleHeight}<br/>[{p.state.area.SIUnit.SIUnitTID}]</span></p>);
    }
  }
  return (
    <div id="editor-draw-area" className="editor-body table-cell">
      <div  className="table">
        <div className="table-row">
          <div className="ruler-top table-cell" ><div style={{width:40}}></div></div>
          <div className="ruler-horizontal-item">{positionsHorizontal}</div>
          <div className="ruler-top table-cell" ><div style={{width:40}}></div></div>
        </div>
        <div className="table-row">
          <div className="ruler-left table-cell"><div className="ruler-vertical-item">{positionsVertical}</div></div>
          <div className="editor-content table-cell">
            {//(p.action.type==MOVE_NODE) && (p.action.data &&(p.action.data).length>0) && <div id="tmp-Node"><NodeElm node={p.action.data[0]} removeNode={() => removeNode(p.action.data[0])} selected={false}></NodeElm></div>}
            }
            <p id="editor-horizontal-indicator">&nbsp;</p>
            <p id="editor-vertical-indicator">&nbsp;</p>
            <div style={{width: (width+1)*40, height: (height+1)*40}}><div className="table">{content}</div></div>
          </div>
          <div className="ruler-right table-cell"><div className="ruler-vertical-item">{positionsVertical}</div></div>
        </div>
        <div className="table-row">
          <div className="ruler-bottom table-cell"><div style={{width:40}}></div></div>
          <div className="ruler-bottom table-cell"><div className="ruler-horizontal-item">{positionsHorizontal}</div></div>
          <div className="ruler-bottom table-cell"><div style={{width:40}}></div></div>
        </div>
        
        <div id="tmp-NodeList">{nodes}</div>
      </div>
      
    </div>
  )
  
}




