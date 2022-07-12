import * as React from "react"
import { Dispatch } from "redux"
import { useDispatch } from "react-redux"
import {Node} from "./Node/node" 
import { MOVE_NODE } from "../../../actions/editor/actionType";
import { dropNode, removeNode, setActiveNode } from "../../../actions/editor/actions";
import { useEffect } from "react";
import { IEditorAction, INode, IPipeline } from "../type"
import $ from "jquery"

  type Props = {
    pipeline : IPipeline;
    action : IEditorAction;
    acctiveNode:INode | {};
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
      if ((p.acctiveNode) && (p.acctiveNode as INode).NodeID > 0){
        var id :string = (e.target as HTMLElement).id;
          var position : RegExpMatchArray | null = id.match(/\d+/g);
        if ((position as RegExpMatchArray).length==2){
          (p.acctiveNode as INode).positionX = Math.floor((parseInt((position as RegExpMatchArray)[1]))/2)* p.pipeline.ScaleHeight;
          (p.acctiveNode as INode).positionY = Math.floor((parseInt((position as RegExpMatchArray)[0]))/2)* p.pipeline.ScaleWidth;
          dispatch(dropNode())
        }
      }
    }
    const allowDrop = (e: React.MouseEvent<HTMLElement>) => {
      e.preventDefault();
    }

    const editorMouseClick  = (e: React.MouseEvent<HTMLElement>) => {
      var id :string = (e.target as HTMLElement).id;
      var position : RegExpMatchArray | null = id.match(/\d+/g);
      if (position && (position as RegExpMatchArray).length==2){
        dispatch(setActiveNode({}));
      }
    }


    const clearLink = (i: number) => {
      var beginPosX = p.pipeline.Links[i].beginPointX;
      var beginPosY = p.pipeline.Links[i].beginPointY;

      var lengthX  = p.pipeline.Links[i].endPointX - p.pipeline.Links[i].beginPointX;
      var lengthY  = p.pipeline.Links[i].endPointY - p.pipeline.Links[i].beginPointY;

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
      var width : number;
      var height : number;
      var posX : number;
      var posY : number; 
      var strPosX : string;
      var strPosY : string;

      var beginPosX : number = 0;
      var beginPosY : number = 0; 
      var endPosX : number = 0;
      var endPosY : number = 0; 
      var lengthX : number = 0;
      var lengthY : number = 0;
      $('.table-cell').removeClass('link_horizontal');
      $('.table-cell').removeClass('link_vertical');
      for (let i=0; i<p.pipeline.Links.length;i++){  
        var BeginNode : INode = p.pipeline.Nodes.find((x: { NodeID: any }) => x.NodeID === p.pipeline.Links[i].BeginNodeID) as INode;
        var EndNode : INode = p.pipeline.Nodes.find((x: { NodeID: any }) => x.NodeID === p.pipeline.Links[i].EndNodeID) as INode;
        if (BeginNode && EndNode && (BeginNode.positionX) && (BeginNode.positionY)){
          beginPosX  = (BeginNode.positionX % p.pipeline.ScaleWidth) == 0 ?  Math.floor(BeginNode.positionX / p.pipeline.ScaleWidth) : Math.floor(BeginNode.positionX / p.pipeline.ScaleWidth) + 1;
          beginPosY = (BeginNode.positionY % p.pipeline.ScaleHeight) == 0 ?  Math.floor(BeginNode.positionY / p.pipeline.ScaleHeight) : Math.floor(BeginNode.positionY / p.pipeline.ScaleHeight) + 1;
        
          endPosX  = (EndNode.positionX % p.pipeline.ScaleWidth) == 0 ?  Math.floor(EndNode.positionX / p.pipeline.ScaleWidth) : Math.floor(EndNode.positionX / p.pipeline.ScaleWidth) + 1;
          endPosY = (EndNode.positionY % p.pipeline.ScaleHeight) == 0 ?  Math.floor(EndNode.positionY / p.pipeline.ScaleHeight) : Math.floor(EndNode.positionY / p.pipeline.ScaleHeight) + 1;
            
          lengthX  = endPosX - beginPosX;
          lengthY  = endPosY - beginPosY;

          if ((beginPosX !=  p.pipeline.Links[i].beginPointX) || (beginPosY !=  p.pipeline.Links[i].beginPointY)
            ||  (endPosX !=  p.pipeline.Links[i].endPointX) || (endPosY !=  p.pipeline.Links[i].endPointY)){
          
          }
          
          p.pipeline.Links[i].beginPointX = beginPosX;
          p.pipeline.Links[i].beginPointY = beginPosY;

          p.pipeline.Links[i].endPointX = endPosY;
          p.pipeline.Links[i].endPointY = endPosY;
                
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
            cell_.classList.add("link_vertical");
          }
          
          //poziome
          for (let j=0; j< Math.abs(lengthX) *2; j++){
            strPosX = ((beginPosX * 2) + (markX *j)+lenX).toString();
            strPosY = ((beginPosY *2)+(lengthY *2) ).toString(); 

            var cellid_ : string = 'cell_' + strPosY + '_'+ strPosX;
            var cell_ : HTMLElement = document.getElementById(cellid_) as HTMLElement;
            cell_.classList.add("link_horizontal");
        }
      }else{

      }
    }
  });


  if (p.pipeline){
    let nodes = [];
    for (let i=0;i<p.pipeline.Nodes.length;i++){
        var posX :number = (p.pipeline.Nodes[i].positionX % p.pipeline.ScaleWidth) == 0 ?  Math.floor(p.pipeline.Nodes[i].positionX / p.pipeline.ScaleWidth) : Math.floor(p.pipeline.Nodes[i].positionX / p.pipeline.ScaleWidth) + 1;
        var posY : number = (p.pipeline.Nodes[i].positionY % p.pipeline.ScaleHeight) == 0 ?  Math.floor(p.pipeline.Nodes[i].positionY / p.pipeline.ScaleHeight) : Math.floor(p.pipeline.Nodes[i].positionY / p.pipeline.ScaleHeight) + 1;
    
        var strPosX : string = (posX * 2).toString();
        var strPosY : string = (posY *2).toString(); 
        var cellid : string = 'cell_' + strPosY + '_'+ strPosX;

        var selected=(p.acctiveNode) && ((p.acctiveNode as INode).NodeID == p.pipeline.Nodes[i].NodeID);
        nodes.push({cell_id :cellid, node:<Node key={i} node={p.pipeline.Nodes[i]} removeNode={()=>removeNode(p.pipeline.Nodes[i]) } selected={selected} ></Node>})
    }

    width = (p.pipeline.Width % p.pipeline.ScaleWidth) == 0 ?  Math.floor(p.pipeline.Width / p.pipeline.ScaleWidth) : Math.floor(p.pipeline.Width / p.pipeline.ScaleWidth) + 1;
    height = (p.pipeline.Height % p.pipeline.ScaleHeight) == 0 ?  Math.floor(p.pipeline.Height / p.pipeline.ScaleHeight) : Math.floor(p.pipeline.Height / p.pipeline.ScaleHeight) + 1;
    
    for(let iW = 0; iW <= (width *2) + 1 ; iW++)	{
      row.push(<div className="table-cell" key={iW} style={{height:20, width:20, left:20*iW }}  onMouseLeave={editorMouseLeave}  onMouseEnter={editorMouseEntere}></div>);
    }
    
    for(let iW = 0; iW <= width ; iW++)	{
      positionsHorizontal.push(<p key={iW}><span>{iW*p.pipeline.ScaleWidth}<br/>[{p.pipeline.SIUnit.SIUnitTID}]</span></p>);
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
      positionsVertical.push(<p key={i}><span>{i*p.pipeline.ScaleHeight}<br/>[{p.pipeline.SIUnit.SIUnitTID}]</span></p>);
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
            {(p.action.type==MOVE_NODE) && (p.action.nodes &&(p.action.nodes).length>0) && <div id="tmp-Node"><Node node={p.action.nodes[0]} removeNode={() => removeNode(p.action.nodes[0])} selected={false}></Node></div>}
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




