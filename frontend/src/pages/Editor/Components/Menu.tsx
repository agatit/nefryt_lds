import * as React from "react"
import { Dispatch } from "redux"
import { useSelector, shallowEqual, useDispatch } from "react-redux"
import { USE_EDITOR_MONITORING, USE_EDITOR_NODES } from "../../../actions/editor/actionType";
import { Button } from "@material-ui/core";
import { RootState } from "../../..";
import { useMonitoringEditor, useNodesEditor } from "../../../actions/editor/actions";


export const PipelineMenu: React.FC = () => {
  const dispatch: Dispatch= useDispatch();

  const activeEditor: string = useSelector(
    (state: RootState) => state.pipelineEditorReducer.activeEditor,
    shallowEqual
  )
  const nodesEditorClick = (e: React.MouseEvent<HTMLElement>) => {
    dispatch(useNodesEditor());
  }
  const monitoringEditorClick = (e: React.MouseEvent<HTMLElement>) => {
    dispatch(useMonitoringEditor());
  }

  return (
    <React.Fragment>
      <Button style={{width:"100%" ,marginLeft:100,marginRight:100, backgroundColor:activeEditor==USE_EDITOR_NODES? "rgba(176, 224, 230, 1)" : "#e0e0e0" }}
        id="demo-customized-button"
        aria-haspopup="true"
        variant="contained"
        disableElevation
        onClick={nodesEditorClick}
      >
        Edytor węzłów
    </Button>

    <Button  style={{width:"100%", marginLeft:100,marginRight:100,  backgroundColor:activeEditor==USE_EDITOR_MONITORING? "rgba(176, 224, 230, 1)" : "#e0e0e0"   }}
        id="demo-customized-button"
        aria-haspopup="true"
        variant="contained"
        disableElevation
        onClick={monitoringEditorClick}
    >
        Konfigurator monitoringu
    </Button>
  </React.Fragment>
 )
}


