import React from 'react';
import {Dispatch } from "redux";
import {shallowEqual, useDispatch, useSelector} from 'react-redux';
import {IconButton} from "@material-ui/core"
import {ChevronLeftOutlined, ChevronRightOutlined} from "@material-ui/icons"
import {RPanelParams } from "./type";




export const RightPanel: React.FC<RPanelParams> = (p) => {
  const dispatch: Dispatch= useDispatch();


  var rightpanelClasses="rightpanel"

  var is_open = p.is_open;
  if (is_open){
    rightpanelClasses = rightpanelClasses + ' open';
  }
  
  //const toggleRightPanel = (e: React.MouseEvent<HTMLElement>) => {
      //dispatch(toggleRPanel());
  //}

  const panelclick = (e: React.MouseEvent<HTMLElement>) => {
    // e.preventDefault();
  }


  return (  
    <div id="mySidepanel" className={rightpanelClasses} onClick={panelclick}>
      <div style={{textAlign:'left'}}>
        <IconButton className={p.styles.sidebarRightButton} onClick={p.handleDrawer}>
          {is_open?  <ChevronRightOutlined /> :  <ChevronLeftOutlined />}
        </IconButton>   
      </div>   
      {is_open? p.content : <div></div>}
    </div>
  )
}