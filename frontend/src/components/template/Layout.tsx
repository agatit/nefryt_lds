import React from 'react'
import { Dispatch, ReactElement } from 'react'
import {  shallowEqual, useDispatch, useSelector } from 'react-redux'
import { AppBar,   createTheme, CssBaseline, DrawerProps,  IconButton, makeStyles, Toolbar, Typography } from '@material-ui/core'

import { Menu, SupervisedUserCircle} from '@material-ui/icons'
import {Notifications} from '@material-ui/icons'
import Link from '@material-ui/core/Link';
import { useNavigate } from 'react-router-dom'
import { RootState } from '../../app/store'  


import { Sidebar } from './Sidebar'

import { RPanel, TemplateState } from './type'

import clsx from 'clsx'
import "./styles.css"
import { RightPanel } from './RightPanel'
import { Badge } from '@mui/material'
import { toggleSidebar } from '../../features/template/templateSlice'

import { AuthData, logout, selectIsAuthenticated } from '../../features/auth/authSlice';

const drawerWidth = 240;

const useStyles  = makeStyles(theme => ({
  root:{
      display:'flex',  
    }, 
    appToolbar:{
      backgroundColor:'#0f5295',
      minHeight:50,
      maxHeight:50
    }, 
    appBar:{
      transition: theme.transitions.create(['margin', 'width'] ,{
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
      }),
    },
    appBarShift:{
      width: `calc(100%-${drawerWidth}px)`,
      marginLeft : drawerWidth,
      transition: theme.transitions.create(['margin', 'width'],{
          easing: theme.transitions.easing.easeOut,
          duration: theme.transitions.duration.enteringScreen
      })
    },
    menuButton:{
      marginRight: theme.spacing(2),
    },
    hide: {
      display:    'none',
    },
    drawer: {
      width: drawerWidth,
      flexShrink : 0,
    },
    drawerPaper: {
      width: drawerWidth,
    },
    drawerHeader:{
      display : 'flex',
      alignItems: 'center',
      padding: theme.spacing(0,1),
      ...theme.mixins.toolbar,  
    },
    sidebar:{
      backgroundColor: '#0f5295',
      minHeight:50,
      maxHeight:50,
    },
    sidebarTitle:{
      color: 'white',
      fontSize: '1rem',
      fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
      fontWeight : 400,
      lineHeight: 1.5,
      letterSpacing: '0.00938em',
      marginTop : 'auto',
      marginBottom : 'auto'
    },
    sidebarRightButton:{
      marginLeft: 'auto',
    },
    content:{
      flexGrow : 1,
      padding: theme.spacing(3),
      transition: theme.transitions.create('margin',{
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
      }),
      marginleft: -drawerWidth
    },
    contentShift:{
      transition: theme.transitions.create('margin', {
        easing : theme.transitions.easing.easeOut,
        duration : theme.transitions.duration.enteringScreen
      }),
      marginLeft : 0
    },
    label: {
      color: "#fff"
    },
    mainMenuIcon:{
      minWidth:20
    },
    linkToolbar:{
      color:'white',
      "&:hover":{
        color:'white',
      }
    }
}));


type Props={
  content: ReactElement,
  rPanel:RPanel,
  onmouseup?:React.MouseEventHandler<HTMLElement>
}  
const Layout: React.FC<Props> = (p) => {
  const navigate = useNavigate();  
  const dispatch: Dispatch<any> = useDispatch();
  const styles = useStyles()

    //const isAuthenticated = useSelector(selectIsAuthenticated);
    const isAuthenticated = true;


  const handleLogin  = (e: React.MouseEvent<HTMLElement>) => {
    if (isAuthenticated){
      dispatch(logout());
    }else{
      navigate('/login');
    }
  }

  const templateReducer: TemplateState = useSelector(
    (state: RootState) => state.template,
    shallowEqual
  )

      
  var sidebar_open = templateReducer.sidebar_open;
  var rpanel_visible = p.rPanel.visible;
  var rpanel_open = p.rPanel.open;

  var pRight = rpanel_visible ? 20 : 0;

  var appClass : string  = rpanel_visible ? "none-user-select" : "auto" ;
      
  const handleToggleDrawer  = (e: React.MouseEvent<HTMLElement>) => {
    dispatch(toggleSidebar());
  }
 
    

  return (    
    <div onMouseUp={p.onmouseup} className={styles.root}>
      <CssBaseline />
      <AppBar      
        position='fixed' className={clsx(styles.appBar, {[styles.appBarShift]:sidebar_open})}>
        <Toolbar className={styles.appToolbar}> 
          <IconButton onClick={handleToggleDrawer} id='hamburgerMenu'>
            <Menu />
          </IconButton>
          <Typography>
            NefrytLDS
          </Typography>

          <IconButton color="inherit" onClick={() => navigate('/events')} className={styles.sidebarRightButton}>
            <Badge badgeContent={4} color="secondary">
              <Notifications />
            </Badge>
          </IconButton>
            
          <Link onClick={handleLogin} className={styles.linkToolbar} >
            <SupervisedUserCircle/>
            {isAuthenticated ? 'Wyloguj' : 'Zaloguj'}
          </Link>
        </Toolbar>    
      </AppBar>    
      <Sidebar  is_open={sidebar_open} styles={styles} handleDrawer={handleToggleDrawer}/>         
    
      <div id='app-content' className={appClass} style={{paddingRight:pRight}}>
        {p.content}
        {rpanel_visible ? <RightPanel content={p.rPanel.content} styles={styles} is_open={rpanel_open} handleDrawer={undefined} children={undefined} ></RightPanel> : null} 
      </div> 
    </div>      
  )
}   

export {Layout};


