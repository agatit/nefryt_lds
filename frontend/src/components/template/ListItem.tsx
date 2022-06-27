import React, { Dispatch } from 'react'
import {useDispatch} from 'react-redux'
import {useNavigate } from "react-router-dom";
import List from '@material-ui/core/List'
import * as icons from '@material-ui/icons'
import {makeStyles} from '@material-ui/core'
import ListItem from '@material-ui/core/ListItem'
import ListItemIcon from '@material-ui/core/ListItemIcon'
import ListItemText from '@material-ui/core/ListItemText'

import {toggleRPanel, toggleSidebar } from '../../actions/Layout/actions'

const useStyles = makeStyles(theme => ({
    root:{
        width:'100%',
        maxWidth:360,
        backgroundColor: theme.palette.background.paper
    },
    subitem:{
        paddingLeft:14
    }
    
}));

export const NestedList: React.FC = () => {
    const styles = useStyles();
    const navigate = useNavigate();
    const dispatch: Dispatch<any> = useDispatch()
    
    const handleDashboard  = (e: React.MouseEvent<HTMLElement>) => {
        navigate('/');
        dispatch(toggleSidebar());
    }
       
    const handleEditor  = (e: React.MouseEvent<HTMLElement>) => {
        navigate('/editor');
        dispatch(toggleSidebar());
    }
      
    const handleEvents  = (e: React.MouseEvent<HTMLElement>) => {
        navigate('/events');
        dispatch(toggleSidebar());
    }
      
    const handleCharts  = (e: React.MouseEvent<HTMLElement>) => {
        navigate('/charts');
        //dispatch(toggleRPanel());
        dispatch(toggleSidebar());
    }


    return (
       <List component='nav' arria-aria-labelledby='nested-list-subheader' className={styles.root}>
            <ListItem button onClick={handleDashboard}>
                <ListItemIcon>
                    <icons.Dashboard/>
                </ListItemIcon>
                <ListItemText primary='Detekcja'/>
            </ListItem>
            <ListItem button onClick={handleEditor}>
                <ListItemIcon>
                    <icons.Edit/>
                </ListItemIcon>
                <ListItemText primary='Edytor'/>
            </ListItem>
          
            <ListItem button onClick={handleEvents}>
                <ListItemIcon>
                    <icons.ListAlt/>
                </ListItemIcon>
                <ListItemText primary='Lista Alarmów'/>
            </ListItem>

            <ListItem button onClick={handleCharts}>
                <ListItemIcon>
                    <icons.ShowChart/>
                </ListItemIcon>
                <ListItemText primary='Wykresy'/>
            </ListItem>
       </List>
    )
}



