import * as React from "react"
import { Dispatch } from "redux"
import { useDispatch } from "react-redux"
import { EditorState, IEditorAction } from "../../type";
import { ExpandMore } from '@material-ui/icons';
import { Accordion, AccordionSummary, AccordionDetails, createTheme, withStyles, makeStyles, FormControl, Select, InputLabel, MenuItem } from '@material-ui/core';
import { Button, TextField } from "@mui/material";



const MuiAccordion = withStyles({
  root: {
    border: '1px solid rgba(0, 0, 0, .125)',
    boxShadow: 'none',
    
    '&:not(:last-child)': {
      borderBottom: 0,
    },
    '&:before': {
      display: 'none',
    },
    '&$expanded': {
      margin: 'auto',
    },
    "&:last-child": {
      borderRadius:0,
    }
  },
  expanded: {},
})(Accordion);

const MuiAccordionSummary = withStyles({
  root: {
    paddingLeft:5,
    paddingRight:0,
    borderBottom: '1px solid #12738E',
    marginBottom: -1,
    color: '#666666',
    fontSize:11,
    width:'125px',
    textTransform: 'uppercase',
    fontWeight: 'bold',
    minHeight: 46,
    '&$expanded': {
      minHeight: 46,
    },
    "&:hover":{
      textDecorationLine: 'underline',
    },
    
  },
  content: {
    width:100,
    '&$expanded': {
      margin: '12px 0',
      float:'left'
    },
  },
  expanded: {},
  expandIcon: {
    marginRight:0,
    float:'right',
    width:'25px',
    padding:0
  }
})(AccordionSummary);


const MuiAccordionDetails = withStyles((theme) => ({
  root: {
    paddingTop:8,
    paddingBottom:0,
    paddingLeft:5,
    paddingRight:5,

  },
}))(AccordionDetails);

const MuiInputLabel = withStyles((theme) =>({
  root: {
    fontSize:12,
    textTransform:"uppercase"

  },
}))(InputLabel);

const MuiFormControl = withStyles((theme) =>({
  root:{
    color:'red',
    
  }, 
}))(FormControl);


const MuiSelect = withStyles((theme) =>({
  root: {
    marginTop:0,
    
  }, 
}))(Select);


type Props = {
  editorState : EditorState;
  //action : IEditorAction;
  //activeEditor : string;
}

const theme = createTheme();

theme.typography.h6 = {
  fontSize: '9px',
  fontWeight:"bold",
  textTransform:"uppercase"
};
  

export const NodeToolbox: React.FC<Props> = (p) => {
  const dispatch: Dispatch= useDispatch();

 var editorHeight = 0;

  const menuItemClick = (e: React.MouseEvent<HTMLElement>) => {
    if (e.currentTarget.classList.contains('node-new')){	
       //dispatch(newNode());
    }else if (e.currentTarget.classList.contains('node-move')){	
     // dispatch(moveNode({}));
    }else if (e.currentTarget.classList.contains('node-clone')){	
      //dispatch(cloneNode({}));
    }else if (e.currentTarget.classList.contains('node-delete')){	
      //dispatch(removeNode({}));
    }
    else if (e.currentTarget.classList.contains('link-new')){	
      //dispatch(linkNodes({}));
    }else if (e.currentTarget.classList.contains('link-delete')){	
      //dispatch(unlinkNodes({}));
    }else if (e.currentTarget.classList.contains('settings')){	
     // dispatch(setEditorArea());
    }else if (e.currentTarget.classList.contains('refresh')){	
      
      //dispatch(refreshData());
      //console.log('RRRRRRRRRRRRRRRRRRRRRRRRRRR');
      //dispatch(setEditorArea());
    }
  }

  if (p.editorState){
    editorHeight = (p.editorState.area.Height % p.editorState.area.ScaleHeight) == 0 ?  Math.floor(p.editorState.area.Height / p.editorState.area.ScaleHeight) : Math.floor(p.editorState.area.Height / p.editorState.area.ScaleHeight) + 1;
  }
  //var activeMoveNode = p.action.type == editorAction.MOVE_NODE ? 'active' : '';
  //var moveNodeClasses = "node node-move " + activeMoveNode;
  //var activeNewNode = p.action.type == editorAction.NEW_NODE ? 'active' : '';
  //var newNodeClasses = "node node-new " + activeNewNode;

  //var activeEditNode = p.action.type == editorAction.EDIT_NODE ? 'active' : '';
  //var editNodeClasses = "node node-edit " + activeEditNode;

  //var activeCloneNode = p.action.type == editorAction.CLONE_NODE ? 'active' : '';
  //var cloneNodeClasses = "node node-clone " + activeCloneNode;

  //var activeDeleteNode = p.action.type == editorAction.REMOVE_NODE ? 'active' : '';
  //var deleteNodeClasses = "node node-delete " + activeDeleteNode;

  //var activeLinkNodes = p.action.type == editorAction.LINK_NODES ? 'active' : '';
  //var linkNodesClasses = "node link-new " + activeLinkNodes;

  //var activeUnlinkNodes = p.action.type == editorAction.UNLINK_NODES ? 'active' : '';
  //var unlinkNodesClasses = "node link-delete " + activeUnlinkNodes;
      
  var settiongsClasses = "node settings ";
  var refreshClasses = "node refresh ";

  const handleChange  = (e: React.ChangeEvent<{}>) => {
    // setSelectedOption(e.target.value)
  }

  let pipeline_id = 1;

  var SelValues : any[] = [];  
  p.editorState.pipelines.forEach((pipeline) => {
    SelValues.push(<MenuItem value={pipeline.iD}>pipeline.name</MenuItem>);
  }) 
    console.log(p.editorState.pipelines);
  return (
    <div style={{maxHeight: '100%', overflowY: 'auto', overflowX:'hidden'}} id="editor-menu" >
       
       <MuiAccordion >
        <MuiAccordionSummary
          expandIcon={<ExpandMore />}
          aria-label="Expand"
          aria-controls="additional-actions1-content"
          id="additional-actions1-header"
        >Edytor
        </MuiAccordionSummary>
        <MuiAccordionDetails>

       <div id="editor-menu-containetr" className="table-cell">
            <p onClick={menuItemClick} className={refreshClasses}><span>&nbsp;</span>Załaduj z DB</p>
            <p onClick={menuItemClick} className={settiongsClasses}><span>&nbsp;</span>Ustawienia Obszaru</p>
           
       </div>     

      
          </MuiAccordionDetails>
      </MuiAccordion>
      <MuiAccordion >
        <MuiAccordionSummary
          expandIcon={<ExpandMore />}
          aria-label="Expand"
          aria-controls="additional-actions1-content"
          id="additional-actions1-header"
        >
          Edycja Węzłów
        </MuiAccordionSummary>
        <MuiAccordionDetails>
          <div id="editor-menu-containetr" className="table-cell">
            {//<p onClick={menuItemClick} className={newNodeClasses}><span>&nbsp;</span>Nowy węzeł</p>
            //<p onClick={menuItemClick} className={editNodeClasses} ><span>&nbsp;</span>Edytuj węzeł</p>
            //<p onClick={menuItemClick} className={moveNodeClasses}><span>&nbsp;</span>Przesuń węzeł</p>
            //<p onClick={menuItemClick} className={cloneNodeClasses}><span>&nbsp;</span>Sklonuj węzeł</p>
            //<p onClick={menuItemClick} className={deleteNodeClasses}><span>&nbsp;</span>Usuń węzeł</p>
            //<p onClick={menuItemClick} className={linkNodesClasses}><span>&nbsp;</span>Połącz węzły</p>
            //<p onClick={menuItemClick} className={unlinkNodesClasses}><span>&nbsp;</span>Rozłącz węzły</p>
            }
          </div>
        </MuiAccordionDetails>
      </MuiAccordion>
      <MuiAccordion>
        <MuiAccordionSummary
          expandIcon={<ExpandMore />}
          aria-label="Expand"
          aria-controls="additional-actions2-content"
          id="additional-actions2-header"
        >
          Edycja odcinków
        </MuiAccordionSummary>
        <MuiAccordionDetails>
          <div id="editor-menu-containetr" className="table-cell">
            {//<p onClick={menuItemClick} className={newNodeClasses}><span>&nbsp;</span>Nowy odcinek</p>  
            }
          </div>
        </MuiAccordionDetails>
        <MuiAccordionDetails>
          <MuiFormControl fullWidth>
            <MuiInputLabel >Wybór odcinka</MuiInputLabel>
              <MuiSelect
                labelId="demo-simple-select-label"
                id="select-pipeline"
               // value={pipeline_id}
                label="Odcinek"
                onChange={handleChange}
              >
                 {p.editorState.pipelines.map((pipeline) => {
                   return <MenuItem key={"pid" + pipeline.iD} value={pipeline.iD}>{pipeline.name}</MenuItem>
                  })
                } 
              {/*  <MenuItem value={1}>Ten</MenuItem>
                <MenuItem value={2}>Twenty</MenuItem>
                <MenuItem value={3}>Thirty</MenuItem>
                <MenuItem value={4}>Ten</MenuItem>
                <MenuItem value={5}>Twenty</MenuItem>
                <MenuItem value={6}>Thirty</MenuItem>
                <MenuItem value={7}>Ten</MenuItem>
                <MenuItem value={8}>Twenty</MenuItem>
                <MenuItem value={9}>Thirty</MenuItem>
                <MenuItem value={10}>Ten</MenuItem>
                <MenuItem value={11}>Twenty</MenuItem>
                <MenuItem value={12}>Thirty</MenuItem>
                <MenuItem value={13}>Ten</MenuItem>
                <MenuItem value={14}>Twenty</MenuItem>
                <MenuItem value={15}>Thirty</MenuItem>

              */}
              </MuiSelect>



          </MuiFormControl>
        </MuiAccordionDetails>

        <MuiAccordionDetails>
          <div id="editor-menu-containetr" className="table-cell">
            {//<p onClick={menuItemClick} className={newNodeClasses}><span>&nbsp;</span>Wybór odcinków</p> 
            }
          </div>
        </MuiAccordionDetails>
      </MuiAccordion>
    </div>    
  )
  
}



