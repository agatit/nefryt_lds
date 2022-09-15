import { FormControl, FormControlLabel,  FormGroup,  FormHelperText,  FormLabel,  InputLabel,  Stack, Switch, TextField } from "@mui/material";
import { Box, Tabs, Tab, withStyles, makeStyles, createTheme, MuiThemeProvider,  Button, Select, MenuItem, IconButton, Badge, Tooltip } from "@material-ui/core"

import { Delete } from "@material-ui/icons";
import { LocalizationProvider } from "@mui/x-date-pickers";
import * as React from "react"
import { Dispatch, useEffect, useState } from "react";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { RootState } from "../../../app/store";
import { NodeDescription, NodeTypes, removeNode } from "../../../features/editor/editorSlice";
import { Node, useDeleteNodeByIdMutation, useUpdateNodeMutation } from "../../../store/nodeApi";
import { EditorState, INode, TactiveElement } from "../type";
import { PropertyEditorTab } from "./PropertyEditor"
import { NodeState } from "../../../features/editor/nodeEditorSlice";
import { useListTrendsQuery } from "../../../store/trendApi"

  type Prop ={
      activeElement : TactiveElement;
  }


 const useStyles  = makeStyles(theme => ({
   indicator:{
     backgroundColor:'#1976d2'
   },
   del_prop:{
      width:'auto'  ,
      float:"left" 
    },
    margin: {
      margin: theme.spacing(1)
    },
    inputLabelNoShrink: {
      transform: "translate(32px, 24px) scale(1)"
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
      

export const NodePropertyEditor: React.FC<Prop> = (p) => {
  const dispatch: Dispatch<any> = useDispatch()

  const classes = useStyles()

  useListTrendsQuery();

 

  const reducer: NodeState = useSelector(
    (state: RootState) => state.nodeEditor,
    shallowEqual
  )
 const activeTabIndex = 0;
      
  function a11yProps(index:number) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };  
  }

  console.log('FFFFF');
  console.log(reducer);


  const handleChange  = (e: React.ChangeEvent<{}>, value:number) => {
    //dispatch(changeTab(value));
  }

  var editFormLabel = p.activeElement.node ? 'Węzeł' : 'Odcinek';
  var nodeName = p.activeElement.node ? p.activeElement.node.Name : '';  
  var nodeType = p.activeElement.node ? p.activeElement.node.type? p.activeElement.node.type.trim() : '' : '';
  
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
    var tmpID : number = (p.activeElement.node as INode).NodeID? ((p.activeElement.node as INode).NodeID as number):0;
    delNode({nodeId:tmpID});
  }
  const saveNode = (e: React.MouseEvent<HTMLElement>) => {

    var nodeA : Node = {
      //ID: (p.state.activeElement.node as INode).NodeID,
      Name:edtNodeName,
      EditorParams: {
        PosX: (p.activeElement.node as INode).positionX,
        PosY: (p.activeElement.node as INode).positionY
      },
      Type: edtNodeType
    }

    

    updateNode({nodeId:((p.activeElement.node as INode).NodeID as number), node:nodeA});
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
        <FormLabel component="legend">{editFormLabel}</FormLabel>
        <FormControl component="fieldset" variant="standard">
          
          

            <Stack spacing={3}>
              <FormGroup style={{ marginTop:'10px'}}>
                <TextField
                    required
                    id="active_node_name"
                    label="Nazwa"
                    value={edtNodeName}
                    onChange={(e) => {
                      setEdtNodeName(e.target.value);
                    }}
                    InputLabelProps={{
                      shrink: true,
                      className: undefined
                    }}
                    
                />
                <FormControl variant='outlined' fullWidth>
       
   
              <TextField
                  variant="outlined"
                 
                  id="active_node_type"
                  value={edtNodeType}
                  label="Typ"
                  select
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
                </TextField>
                </FormControl>
                <Button style={{marginTop:'30px'}} onClick={saveNode} variant="contained">Zapisz</Button>
                
                <FormLabel style={{marginTop:30}} component="legend">Lista trendów:</FormLabel>
                <div style={{border: 'solid 1px white' , marginTop:3, maxHeight: 500, overflowY:'hidden', overflowX:'hidden'}}>
                <FormControl sx={{ m: 3 }} component="fieldset" variant="standard" >
                  
                  <FormGroup style={{ width:'410px',  }}>
                    <div style={{ maxHeight: 230, overflowY:'auto', overflowX:'hidden'}}>
                      {/*reducer.chart.trends.map((trend : ITrend, index) => (
                      
                        ((!reducer.chart.onlySelected) || ((reducer.chart.onlySelected) && (trend.selected))) ?
                        
                        <Accordion key={"Accordion_" + index} expanded={expanded === "trd_" + (trend.ID as number).toLocaleString() ?? ''} onChange={handleTrendPanelExpanded("trd_" + (trend.ID as number).toLocaleString())}>
                          <AccordionSummary key={"AccordionSummary_" + index}
                            expandIcon={trend.selected?<ExpandMore className="changeAccordionState" /> : null}
                            aria-controls={"panel_trd_" + (trend.ID as number).toLocaleString() + "-content"}
                            id={"panel_trd_" + (trend.ID as number).toLocaleString() + "-header"}
                            className={trend.selected?"changeAccordionState":""}
                          >
                            <Typography key={"Typography_" + index} sx={{flexShrink: 0 }}>
                              <FormControlLabel   key={"FormControlLabel_" + index}
                               
                                control={
                                  <Checkbox className="select-trend" key={"trd_" + (trend.ID as number).toLocaleString()} checked={trend.selected ? trend.selected : false}  onChange={handleTrendList} name={"trd_" + (trend.ID as number).toLocaleString()} />
                                }
                                label={trend.Name}
                              />
                            </Typography>   
                          </AccordionSummary>
                          <AccordionDetails key={"AccordionDetails_" + index}>
                            <Typography key={"TypographyDetails_" + index}  width="300px" marginLeft={4}>
                              <FormControlLabel key={"FormControlLabelDetails_" + index}
                                control={
                                  <Checkbox key={"trd_manual_scale_" + (trend.ID as number).toLocaleString()} className="select-trend" checked={!trend.autoscale} onChange={handleAutoscale}  name={"trd_manual_scale_" + (trend.ID as number).toLocaleString()} />
                                }
                                label="Ustaw ręcznie zakres wartości"
                              />
                              <Slider key={"trd_slider_" + (trend.ID as number).toLocaleString()}  name={"trd_slider_" + (trend.ID as number).toLocaleString()} disabled={trend.autoscale}
                                getAriaLabel={() => 'Minimum distance shift'}
                                value={[trend.scale.min, trend.scale.max]}  
                                onChange={handleTrendScale}
                                //getAriaValueText={valuetext}
                                step={trend.step}
                                min={trend.ScaledMin}
                                max={trend.ScaledMax}
                                valueLabelDisplay="auto"
                                marks={trend.marks}  
                              />
                            </Typography>
                          </AccordionDetails>  
                        </Accordion> : null 
                              ))*/}
                    </div> 
                  </FormGroup>   
                  <FormHelperText> </FormHelperText>
                </FormControl>
              </div>
           
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

