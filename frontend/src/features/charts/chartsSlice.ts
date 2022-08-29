import { createSlice } from '@reduxjs/toolkit'
import { ChartsPage } from '../../pages/Charts'
import {  ChartsState, PERIOD_EXTENSION} from './types'


const initialState: ChartsState={
    chart: {
      brush:{startIndex:0,endIndex:0},
      mode: { 
        zoom : false,
        tooltip:false,
        live : {active:false,
                timer:undefined,
                period:100
              }
      },
      is_loading_trends:true,
      grid_lines: {
        h: true,
        v: true
      },
      cfgRange: {
        from: Date.now()  - (60*60*1*1000),
        to: Date.now()
      }, 
      currRange: {
        from: Date.now() - ((PERIOD_EXTENSION)*(1*60*60*1000)+ (1*60*60*1000)),
        to: Date.now() + (PERIOD_EXTENSION*(1*60*60*1000))
      },
      refArea:{left:0,right:0},
      onlySelected : false,
      trends:[],
      data : [],
      lastUpdated:0,
      force_refresh:false,
    },
    rpanel_open:false
  };

export const chartsSlice = createSlice({
  name: 'charts',
  initialState,
  reducers: {
    setHorizontalLine : (state, action) => { 
        state.chart.grid_lines.h = action.payload;
    },
    setVerticalLine : (state, action) => { 
        state.chart.grid_lines.v = action.payload;
    },
    toggleLiveMode : (state) => {
        var currTimerange = state.chart.cfgRange.to - state.chart.cfgRange.from;
        var period = currTimerange; //Math.round(currTimerange/1000);

       if (state.chart.mode.live.active){
          var cFrom =  state.chart.cfgRange.from - (PERIOD_EXTENSION*currTimerange);

          var cTo =  state.chart.cfgRange.to + (PERIOD_EXTENSION*currTimerange);
       }else{

        cTo = Date.now();
        cFrom = Date.now()-currTimerange;

       }

       state.chart.mode.live.period = period;
       state.chart.mode.live.active = !state.chart.mode.live.active;
       state.chart.currRange.from = cFrom;
       state.chart.currRange.to = cTo;
    
    },
    toggleZoomMode : (state) => {
        state.chart.mode.zoom = state.chart.mode.live.active ? false : !state.chart.mode.zoom;
    },
    toggleTooltip : (state) => {
        state.chart.mode.tooltip = !state.chart.mode.tooltip;
    },
    toggleRightPanel: (state) => {
        state.rpanel_open = !state.rpanel_open;
    }
  },
})

export const { setHorizontalLine, setVerticalLine, toggleLiveMode, toggleZoomMode, toggleTooltip, toggleRightPanel } = chartsSlice.actions

// The function below is called a thunk and allows us to perform async logic. It
// can be dispatched like a regular action: `dispatch(incrementAsync(10))`. This
// will call the thunk with the `dispatch` function as the first argument. Async
// code can then be executed and other actions can be dispatched


// The function below is called a selector and allows us to select a value from
// the state. Selectors can also be defined inline where they're used instead of
// in the slice file. For example: `useSelector((state) => state.counter.value)`

//export const selectTemplate = (state) => state.template.value

export default chartsSlice.reducer
