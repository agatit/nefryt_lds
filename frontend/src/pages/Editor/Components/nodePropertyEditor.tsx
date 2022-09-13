import { Box, Tabs, Tab, withStyles, makeStyles, createTheme, MuiThemeProvider, FormLabel, FormControl, FormGroup, TextField, FormControlLabel, Button, Select, MenuItem, IconButton, Badge, Tooltip } from "@material-ui/core"
import { Delete } from "@material-ui/icons";
import { Stack } from "@mui/material";
import { LocalizationProvider } from "@mui/x-date-pickers";
import * as React from "react"
import { Dispatch, useEffect, useState } from "react";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { RootState } from "../../../app/store";
import { NodeDescription, NodeTypes, removeNode } from "../../../features/editor/editorSlice";
import { Node, useDeleteNodeByIdMutation, useUpdateNodeMutation } from "../../../store/nodeApi";
import { EditorState, INode } from "../type";
import { PropertyEditorTab } from "./PropertyEditor"

  type Prop ={
      handleSubmit : any;
  }


 const useStyles  = makeStyles(theme => ({
   indicator:{
     backgroundColor:'#1976d2'
   },
   del_prop:{
      width:'auto'   
    }
 }));


const MuiTabs = withStyles((theme) =>({
  root:{
    borderTop: '1px solid',
    borderColor:  '#0f5295', //'rgba(0, 0, 0, 0.12)',
    backgroundColor:'#969696',
    minHeight:'36px',
  },
}))(Tabs);

const MuiTab = withStyles((theme) =>({
  root:{
      minHeight:'36px',
      fontSize:'11px',
      "&:hover":{
        backgroundColor: 'silver',   //'rgba(106, 154, 160, 1)',
      },
      "&.Mui-selected":{
        backgroundColor:'white',
        color:'#111',
      }
  }, 
  }))(Tab);

  

const theme = createTheme({
  palette: {
    secondary: {
      main: '#1976d2'      
    }
  }
});
      

export const NodePropertyEditor: React.FC = () => {
  const dispatch: Dispatch<any> = useDispatch()

  const classes = useStyles()


  const reducer: EditorState = useSelector(
    (state: RootState) => state.editor,
    shallowEqual
  )
 const activeTabIndex = 0;
      
  function a11yProps(index:number) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };  
  }



  const handleChange  = (e: React.ChangeEvent<{}>, value:number) => {
    //dispatch(changeTab(value));
  }

  var editFormLabel = reducer.activeElement.node ? 'Węzeł' : 'Odcinek';
  var nodeName = reducer.activeElement.node ? reducer.activeElement.node.Name : '';  
  var nodeType = reducer.activeElement.node ? reducer.activeElement.node.type? reducer.activeElement.node.type.trim() : '' : '';
  
  const [edtNodeName, setEdtNodeName] = useState(nodeName);
  const [edtNodeType, setEdtNodeType] = useState(nodeType);


  useEffect(() => {
    setEdtNodeName(nodeName);
    setEdtNodeType(nodeType);

  },[nodeName, nodeType]);


  const [updateNode, { isLoading, isError, error, isSuccess }] =
  useUpdateNodeMutation();

  const [delNode, {}] = useDeleteNodeByIdMutation();
  
  const handleSubmit  = (e: any ) => {
    
    
  }

  
  const removeNode = (e: React.MouseEvent<HTMLElement>) => {
    var tmpID : number = (reducer.activeElement.node as INode).NodeID? ((reducer.activeElement.node as INode).NodeID as number):0;
    delNode({nodeId:tmpID});
  }
  const saveNode = (e: React.MouseEvent<HTMLElement>) => {

    var nodeA : Node = {
      //ID: (p.state.activeElement.node as INode).NodeID,
      Name:edtNodeName,
      EditorParams: {
        PosX: (reducer.activeElement.node as INode).positionX,
        PosY: (reducer.activeElement.node as INode).positionY
      },
      Type: edtNodeType
    }

    updateNode({nodeId:((reducer.activeElement.node as INode).NodeID as number), node:nodeA});
       console.log(nodeA);    
    //dispatch(setDateRange());
    //console.log(e);
    //var name = document.getElementById('new_node_name'); 
    //alert(name);

  }

  return (
    <React.Fragment>
      <MuiThemeProvider theme={theme}>
        <Tooltip title="Usuń węzeł">
          <IconButton color="inherit" onClick={e => removeNode(e)} className={classes.del_prop}>          
              <Delete />
          </IconButton>
        </Tooltip>
        <FormControl component="fieldset" variant="standard">
          <FormLabel component="legend">{editFormLabel}</FormLabel>
          

            <Stack spacing={3}>
              <FormGroup style={{ width:'410px', marginTop:'10px'}}>
                <TextField
                    required
                    id="active_node_name"
                    label="Nazwa węzła"
                    value={edtNodeName}
                    onChange={(e) => {
                      setEdtNodeName(e.target.value);
                    }}
                    
                />

              <Select
                  labelId="active_node_label"
                  id="active_node_type"
                  value={edtNodeType}
                  label="Typ węzła"
                  onChange={(e) => {
                    //console.log(e);
                    console.log(e.target.value as string);
                    setEdtNodeType((e.target.value as string));
                  }}
                >
                 {
                  NodeTypes.map((element:string, index:number) => (
                    <MenuItem  value={element}>{NodeDescription[index]}</MenuItem>
                  ))

                 }
                </Select>
                <Button style={{marginTop:'30px'}} onClick={saveNode} variant="contained">Zapisz</Button>
                
           
          </FormGroup>

          </Stack>
        </FormControl>  
        {/*<Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <MuiTabs TabIndicatorProps={{style: {top:0,}}} textColor="secondary" indicatorColor="secondary"  value={activeTabIndex} onChange={handleChange } >
            <MuiTab label="Węzeł" {...a11yProps(0)} />
            <MuiTab label="Odcinki" {...a11yProps(1)}  />
          </MuiTabs>
        </Box>
        <PropertyEditorTab activeTabIndex={activeTabIndex} index={0} /> 
        <PropertyEditorTab activeTabIndex={activeTabIndex} index={1} />   
        */} 
      </MuiThemeProvider>
    </React.Fragment>
  
  )
}

