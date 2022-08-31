import React from 'react';
import { DateTimePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { FormControl, FormControlLabel,  FormGroup,  FormHelperText,  FormLabel,  Stack, Switch, TextField } from "@mui/material";
import {Accordion, AccordionDetails, AccordionSummary, Badge, Box, Button, Checkbox, IconButton, LinearProgress, makeStyles, Slider} from '@material-ui/core';
import { ExpandMore} from '@material-ui/icons'
import Typography from '@mui/material/Typography';
//import { ChartsState } from './type';
import { shallowEqual, useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../app/store';
import { ChartsState, ITrend } from '../../features/charts/types';
import { addSerie, removeSerie, setAutoscale, setDateRange, setFromDate, setHorizontalLine, setOnlySelected, setToDate, setTrendScale, setVerticalLine, toggleLiveMode, toggleTooltip, toggleZoomMode } from '../../features/charts/chartsSlice';
import { Dispatch } from '@reduxjs/toolkit';
import "./style.css";

export const ChartsRPanel: React.FC = () => {
    
    const dispatch :Dispatch = useDispatch();
    
    const reducer: ChartsState = useSelector(
        (state: RootState) => state.charts,
        shallowEqual
      )
    
    const handleSwitch = (event: { target: { name: any; checked: any; }; }) => {
        if (event.target.name=='gl_horizontal'){
          dispatch(setHorizontalLine(event.target.checked));
        }else if (event.target.name=='gl_vertical'){
          dispatch(setVerticalLine(event.target.checked));
        }else if (event.target.name=='liveMode'){
          dispatch(toggleLiveMode());
        }else if (event.target.name=='zoomMode'){
          dispatch(toggleZoomMode());
        }else if (event.target.name=='tooltipMode'){
          dispatch(toggleTooltip());
        }else{
    
      }
    };

    function changeDateFrom(this: any, newValue: number | null) {
        dispatch(setFromDate(newValue));
      }
    
      function changeDateTo(this: any, newValue: number | null) {
        dispatch(setToDate(newValue));
      }

      const handleSwitchOnlySelected = (event: any) => {
        dispatch(setOnlySelected(event.target.checked));
      }

      const handleChange2 = (event: any, newValue: number | number[]) => {
        if (!Array.isArray(newValue)) {
            return;
          }
          var trd = event.target.parentElement.querySelector('input').name.replace('trd_slider_', '');
          dispatch(setTrendScale({trendiD: trd, scale: newValue}));
        };

        const changeDataRange = (e: React.MouseEvent<HTMLElement>) => {
            dispatch(setDateRange());
        }
  
        const handleChange = (panel: string) => (event: any, isExpanded: any) => {
             if ((event.target.classList.contains("changeAccordionState")) || ((event.target.parentElement) && (event.target.parentElement.classList.contains("changeAccordionState")))){
                 setExpanded(isExpanded ? panel : 'false');
             }
           };
         
           const [expanded, setExpanded] = React.useState('false');

           const handleChangeTrend = (event: any) => {
            console.log('clicked');
            event.preventDefault();
            if (event.target.checked){
              
              dispatch(addSerie({trendName: event.target.name.replace('trd_', '')}));
            }else{
              dispatch(removeSerie({trendName: event.target.name.replace('trd_', '')}));
            }

            if (!event.target.checked){
               setExpanded('false');
            }
            
          }

          const toggleAutoscale = (event:any) => {
            dispatch(setAutoscale({trendiD : event.target.name.replace('trd_manual_scale_', ''), autoscale: !event.target.checked}));
          }
          
          function valuetext(value:any) {
            return `${value}°C`;
          }

         // console.log(reducer.chart.trends);
          
    return (
        <> 
              
               <LocalizationProvider dateAdapter={AdapterDateFns}> 
                <Stack spacing={3}>
                  <FormControlLabel
                    control={
                      <Switch checked={reducer.chart.mode.live.active} onChange={handleSwitch} name="liveMode" />
                    }
                    label="Dane bieżące"
                  />
    
                  <DateTimePicker
                    renderInput={(params) => <TextField {...params} />}
                    label="Zakres od"
                    value={reducer.chart.cfgRange.from}
                    ampm={false}
                    onChange={(newValue) => {
                      changeDateFrom(newValue);
                    }}
                    //views={['hours', 'minutes', 'seconds']} 
                    inputFormat="dd-MM-yyyy HH:mm:ss"
                    mask="__ -__-____ __:__:__"
                  />
                  <DateTimePicker
                    renderInput={(params) => <TextField {...params} />}
                    label="Zakres do"
                    value={reducer.chart.cfgRange.to}
                    ampm={false}
                    onChange={(newValue) => {
                      changeDateTo(newValue);
                    }}
                    //views={['hours', 'minutes', 'seconds']} 
                    inputFormat="dd-MM-yyyy HH:mm:ss"
                    mask="__ -__-____ __:__:__"
                  />
                   <Button disabled={reducer.chart.mode.live.active} onClick={changeDataRange} variant="contained">Ustaw zakres dat</Button>
                  
                    
                 
                   <FormControlLabel  
                              control={
                              <Checkbox checked={reducer.chart.onlySelected}  onChange={handleSwitchOnlySelected}/>
                           }
                              label="Pokaż tylko wybrane"
                              
                            />
                  <div style={{border: 'solid 1px white' , marginTop:0, maxHeight: 300, overflowY:'hidden', overflowX:'hidden'}}>
                    <FormControl sx={{ m: 3 }} component="fieldset" variant="standard" >
                      <FormLabel component="legend">Wybór trendów (Wybrano: {/*ADAMselectedTrendCount*/})
                      
                      </FormLabel>
                     
                      <FormGroup style={{ width:'410px',  }}>
                          <div style={{ maxHeight: 230, overflowY:'auto', overflowX:'hidden'}}>
                          {reducer.chart.trends.map((trend : ITrend, index) => (
                            //var aa = document.getElementById("trd_manual_scale_" + trend.iD.toLocaleString());
                           ((!reducer.chart.onlySelected) || ((reducer.chart.onlySelected) && (trend.selected))) ?
                            <Accordion key={"Accordion_" + index} expanded={expanded === "trd_" + trend.ID.toLocaleString()} onChange={handleChange("trd_" + trend.ID.toLocaleString())}>
                            <AccordionSummary key={"AccordionSummary_" + index}
                              expandIcon={trend.selected?<ExpandMore className="changeAccordionState" /> : null}
                              aria-controls={"panel_trd_" + trend.ID.toLocaleString() + "-content"}
                              id={"panel_trd_" + trend.ID.toLocaleString() + "-header"}
                              className={trend.selected?"changeAccordionState":""}
                            >
                              <Typography key={"Typography_" + index} sx={{flexShrink: 0 }}>
                              <FormControlLabel   key={"FormControlLabel_" + index}
                              control={
                              <Checkbox className="select-trend" key={"trd_" + trend.ID.toLocaleString()} checked={trend.selected ? trend.selected : false}  onChange={handleChangeTrend} name={"trd_" + trend.ID.toLocaleString()} />
                           }
                              label={trend.Name}
                              
                            />
                              </Typography>
                             
                            </AccordionSummary>
                            <AccordionDetails key={"AccordionDetails_" + index}>
                              <Typography key={"TypographyDetails_" + index}  width="300px" marginLeft={4}>
                              <FormControlLabel key={"FormControlLabelDetails_" + index}
                              control={
                               <Checkbox key={"trd_manual_scale_" + trend.ID.toLocaleString()} className="select-trend" checked={!trend.autoscale} onChange={toggleAutoscale}  name={"trd_manual_scale_" + trend.ID.toLocaleString()} />
                              }
                              label="Ustaw ręcznie zakres wartości"
                              
                            />

                      
                                <Slider key={"trd_slider_" + trend.ID.toLocaleString()}  name={"trd_slider_" + trend.ID.toLocaleString()} disabled={trend.autoscale}
                                  getAriaLabel={() => 'Minimum distance shift'}
                                  value={[trend.scale.min, trend.scale.max]}  
                                  onChange={handleChange2}
                                  getAriaValueText={valuetext}
                                  step={trend.step}
                                  min={trend.ScaledMin}
                                  max={trend.ScaledMax}
                                  valueLabelDisplay="auto"
                                  marks={trend.marks}
                                  
                                />
                              </Typography>
                            </AccordionDetails>
                            
                          </Accordion> : null
                            
                           
                          ))
                          }
                          </div> 
                      </FormGroup>
                      
                      <FormHelperText> </FormHelperText>
                    </FormControl>
                  </div>

                  <div style={{border: 'solid 1px white'}}>      
                    <FormControl component="fieldset" variant="standard">
                      <FormLabel component="legend">Parametry wykresów</FormLabel>
                      <FormGroup>
                       { /*<FormControlLabel
                          control={
                           <Switch checked={reducer.chart.mode.zoom} disabled={reducer.chart.mode.live.active? true : false}   onChange={handleSwitch} name="zoomMode" />
                          }
                          label="Tryb zoom"
                        />
                        */
                       }
                        <FormControlLabel
                          control={
                           <Switch checked={reducer.chart.mode.tooltip} onChange={handleSwitch} name="tooltipMode" />
                          }
                          label="Pokazuj wartości"
                        />
                        <FormControlLabel
                          control={
                            <Switch checked={reducer.chart.grid_lines.h} onChange={handleSwitch} name="gl_horizontal" />
                          }
                          label="Poziome linie siatki"
                        />
                        <FormControlLabel
                          control={
                            <Switch checked={reducer.chart.grid_lines.v} onChange={handleSwitch} name="gl_vertical" />
                          }
                          label="Pionowe linie siatki"
                        />
                      </FormGroup>
                      <FormHelperText></FormHelperText>
                    </FormControl>
                  </div>
                </Stack>
              </LocalizationProvider>
              </> 
    )
}