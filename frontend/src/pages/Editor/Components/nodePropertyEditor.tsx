import { Box, Tabs, Tab, withStyles, makeStyles, createTheme, MuiThemeProvider } from "@material-ui/core"
import * as React from "react"
import { Dispatch } from "react";
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { RootState } from "../../../app/store";
import { PropertyEditorTab } from "./PropertyEditor"

  type Prop ={
      activeTab : number;
  }


 const useStyles  = makeStyles(theme => ({
   indicator:{
     backgroundColor:'#1976d2'
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

 // const activeTabIndex: number = useSelector(
 //   (state: RootState) => state.editor.activeTab,
 //   shallowEqual
 // )
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
          
  return (
    <React.Fragment>
      <MuiThemeProvider theme={theme}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <MuiTabs TabIndicatorProps={{style: {top:0,}}} textColor="secondary" indicatorColor="secondary"  value={activeTabIndex} onChange={handleChange } >
            <MuiTab label="Węzeł" {...a11yProps(0)} />
            <MuiTab label="Odcinki" {...a11yProps(1)}  />
          </MuiTabs>
        </Box>
        <PropertyEditorTab activeTabIndex={activeTabIndex} index={0} /> 
        <PropertyEditorTab activeTabIndex={activeTabIndex} index={1} />    
      </MuiThemeProvider>
    </React.Fragment>
  
  )
}

