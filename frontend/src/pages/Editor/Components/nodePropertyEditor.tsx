import { Accordion, AccordionDetails, AccordionSummary, Checkbox, FormControl, FormControlLabel,  FormGroup,  FormHelperText,  FormLabel,  InputLabel,  Slider,  Stack, Switch, TextField, Typography } from "@mui/material";
import { Box, Tabs, Tab, withStyles, makeStyles, createTheme, MuiThemeProvider,  Button, Select, MenuItem, IconButton, Badge, Tooltip } from "@material-ui/core"

import { Delete, ExpandMore } from "@material-ui/icons";
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
import { Trend, TrendDef, useListTrendDefsQuery, useListTrendsQuery } from "../../../store/trendApi"
import { Label } from "recharts";
import { TabPanel } from "@mui/lab";
import PropTypes from 'prop-types';
import { TrendPropertyEditor } from "./trendPropertyEditor";

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
  


  function TabPanel(props: { [x: string]: any; children: any; value: any; index: any; }) {
    const { children, value, index, ...other } = props;
  
    return (
      <div
        role="tabpanel"
        hidden={value !== index}
        id={`simple-tabpanel-${index}`}
        aria-labelledby={`simple-tab-${index}`}
        {...other}
      >
        {value === index && (
          <Box sx={{ p: 3 }}>
            <Typography component="span">{children}</Typography>
          </Box>
        )}
      </div>
    );
  }
  
  TabPanel.propTypes = {
    children: PropTypes.node,
    index: PropTypes.number.isRequired,
    value: PropTypes.number.isRequired,
  };


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

 


  const handleChange  = (e: React.ChangeEvent<{}>, value:number) => {
    //dispatch(changeTab(value));
  }

  var editFormLabel = p.activeElement.node ? 'Węzeł' : 'Odcinek';
  var nodeName = p? p.activeElement.node ? p.activeElement.node.Name : '' : '';  
  var nodeType = p? p.activeElement.node ? p.activeElement.node.type? p.activeElement.node.type.trim() : '' : '':'';
  

  const [edtNodeName, setEdtNodeName] = useState(nodeName);
  const [edtNodeType, setEdtNodeType] = useState(nodeType);

 

  var node_id : string ='0';
  useEffect(() => {
    setEdtNodeName(nodeName);
    setEdtNodeType(nodeType);
  },[nodeName, nodeType]);

  //useEffect(() => {
    if ((p.activeElement.node ) && ((p.activeElement.node as INode).NodeID)){
      node_id = (((p.activeElement.node as INode).NodeID) as number).toString();
    }
  //},[p]);

 

  var filter_txt : string = 'NodeID eq ' + node_id; 
  var filter={$filter:filter_txt};

   useListTrendsQuery(filter, {refetchOnMountOrArgChange : true});

   var filterTrdDef={};
   useListTrendDefsQuery(filterTrdDef, {refetchOnMountOrArgChange : true});
  
  
  const [updateNode, { isLoading, isError, error, isSuccess }] =
  useUpdateNodeMutation();

  const [delNode, {}] = useDeleteNodeByIdMutation();
  
  const handleSubmit  = (e: any ) => {
    
    
  }

  

  
  const removeNode = (e: React.MouseEvent<HTMLElement>) => {
    var tmpID : number = (p.activeElement.node as INode).NodeID? ((p.activeElement.node as INode).NodeID as number):0;
    delNode({nodeId:tmpID});
  }

  const saveTrendData = (e: React.MouseEvent<HTMLElement>) => {


  }

  const saveParameters = (e: React.MouseEvent<HTMLElement>) => {


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

  const [expanded, setExpanded] = React.useState('false');
  
  const handleTrendPanelExpanded = (panel: string) => (event: any, isExpanded: any) => {
    if ((event.target.classList.contains("changeAccordionState")) || ((event.target.parentElement) && (event.target.parentElement.classList.contains("changeAccordionState")))){
      setExpanded(isExpanded ? panel : 'false');
    }
  };
     
  const [trdTabIndex, setTrdTabIndex] = React.useState(0);

  const handleChangeTabIndex = (event: any, newValue: React.SetStateAction<number>) => {
    setTrdTabIndex(newValue);
  };


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
                    <MenuItem key={'menuItemNodeType' + element}  value={element}>{NodeDescription[index]}</MenuItem>
                  ))

                 }
                </TextField>
                </FormControl>
                <Button style={{marginTop:'30px'}} onClick={saveNode} variant="contained">Zapisz</Button>
                
                <FormLabel style={{marginTop:30}} component="legend">Lista trendów:</FormLabel>
                <div style={{border: 'solid 1px white' , marginTop:3, maxHeight: 500, overflowY:'hidden', overflowX:'hidden'}}>
                <FormControl sx={{ m: 3 }} component="fieldset" variant="standard" >
                  
                  <FormGroup style={{ width:'410px',  }}>
                    <div style={{ maxHeight: 530, overflowY:'auto', overflowX:'hidden', maxWidth:'410px'}}>
                      {reducer.trends.map((trend : Trend, index) => (
                      
                        <Accordion key={"Accordion_" + index} expanded={expanded === "trd_" + (trend.ID as number).toLocaleString() ?? ''} onChange={handleTrendPanelExpanded("trd_" + (trend.ID as number).toLocaleString())}>
                          <AccordionSummary key={"AccordionSummary_" + index}
                            expandIcon={<ExpandMore className="changeAccordionState" />}
                            aria-controls={"panel_trd_" + (trend.ID as number).toLocaleString() + "-content"}
                            id={"panel_trd_" + (trend.ID as number).toLocaleString() + "-header"}
                            className={"changeAccordionState"}
                          >
                            {trend.Name}
                          </AccordionSummary>
                          <AccordionDetails key={"AccordionDetails_" + index}>
                            <Typography component="span" key={"TypographyDetails_" + index}  width="100%" marginLeft={4}>
                            <Box  key={'BoxTrend' + trend.ID} sx={{ borderBottom: 1, borderColor: 'divider' }}>
                              <Tabs key={'tabsTrend_' + trend.ID} value={trdTabIndex} onChange={handleChangeTabIndex} aria-label="basic tabs example">
                                <Tab key={'tabTrend0_' + trend.ID} label="Dane" {...a11yProps(0)} />
                                <Tab  key={'tabTrend1_' + trend.ID} label="Parametry" {...a11yProps(1)} />

                              </Tabs>
                            </Box>
                            <TabPanel key={'TabPanel0Trend' + trend.ID} value={trdTabIndex} index={0}>
                              <TrendPropertyEditor key={'terndEditor' + trend.ID} activeTrend={trend} activeElement={undefined}></TrendPropertyEditor>
                             
                            </TabPanel>
                            <TabPanel  key={'TabPanel1Trend' + trend.ID} value={trdTabIndex} index={1}>
                              <FormControl sx={{ m: 3 }} component="fieldset" variant="standard" >
                              
                                 <Button  key={'TabPanel0TrendButton' + trend.ID} style={{marginTop:'30px', width:'300px'}} onClick={saveParameters} variant="contained">Zapisz parametry</Button>
                              </FormControl>
                            </TabPanel>
                                                  
                              
                            </Typography>
                          </AccordionDetails>  
                        </Accordion> 
                      ))}
                    </div> 
                  </FormGroup>   
                  <FormHelperText> </FormHelperText>
                </FormControl>
              </div>
           
          </FormGroup>

          </Stack>
        </FormControl>  
        
      </MuiThemeProvider>
    </React.Fragment>
  
  )
}

