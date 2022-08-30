import { createSlice } from '@reduxjs/toolkit'
import { ChartsPage } from '../../pages/Charts'
import {  ChartsState, ITrend, PERIOD_EXTENSION} from './types'
import { enhancedApi as trendApi, Trend, TrendDef } from '../../store/trendApi'


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
    },
    setFromDate : (state, action) => {
      state.chart.cfgRange.from = action.payload;
    },
    setToDate : (state, action) => {
      state.chart.cfgRange.to = action.payload;
    },
    setOnlySelected : (state, action) => {
      state.chart.onlySelected = action.payload;
    },
    setTrendScale : (state, action) =>{
      var trd : ITrend[] = state.chart.trends;
         
      trd.forEach((element: ITrend) => {
        if (element.ID == action.payload.trendiD){
          if (action.payload.scale[0] != NaN){
            element.scale.min = action.payload.scale[0];
          }
          if (action.payload.scale[1] != NaN){
            element.scale.max = action.payload.scale[1];
          }
        }
      });
      state.chart.trends = trd;
    },
    setDateRange : (state) => {
        var DATA_SIZE=4000;

        var range = state.chart.cfgRange.to - state.chart.cfgRange.from;
    
        if (range==0){
          range=1;
        }

        var cFrom =  state.chart.cfgRange.from - (PERIOD_EXTENSION*range);

        var cTo =  state.chart.cfgRange.to + (PERIOD_EXTENSION*range);
        state.chart.currRange.from = cFrom;
        state.chart.currRange.to = cTo;

    },
    setAutoscale : (state, action) => {
      var trd : ITrend[] = state.chart.trends;
         
      trd.forEach((element: ITrend) => {
        if (element.ID == action.payload.trendiD){
          element.autoscale = action.payload.autoscale;
        }      
      });
    }

  },

  extraReducers: (builder) => {
    builder
      .addMatcher(trendApi.endpoints.listTrends.matchPending, (state) => {
        console.log('pending');
      })
      .addMatcher(trendApi.endpoints.listTrends.matchFulfilled, (state, action) => {
        //console.log('fulfilled', action)
        var trd : Trend[] = action.payload;
        //console.log(action.payload.entries);
        var idx=0;
        var data : ITrend[] = [];
        trd.forEach((element: Trend) => {
        
           var tmp : string =  element.Symbol? element.Symbol : element.ID.toString(); 
           tmp += element.Unit? ' [' + element.Unit + ']' : '';
           var marks = [];
           marks.push({value:element.ScaledMin, label:element.ScaledMin.toLocaleString()+element.Unit});
           marks.push({value:element.ScaledMax, label:element.ScaledMax.toLocaleString()+element.Unit});
           marks.push({value: Math.round((element.ScaledMax - element.ScaledMin) / 2), label:Math.round((element.ScaledMax - element.ScaledMin) / 2).toLocaleString()+element.Unit});

           var elm : ITrend = {
             ...element,
             selected: false,
             axislabel: tmp,
             trendname: '',
             disabled: false,
             autoscale: false,
             scale: {
               min: element.ScaledMin,
               max: element.ScaledMax
             },
             marks: marks,
             step: (element.ScaledMax - element.ScaledMin) / 100
           };

           data.push(elm);
           
           idx++;
         });
         console.log('AAAAAAAAAAAAAAAA');
         console.log(data);
         state.chart.trends = data;

      })
      .addMatcher(trendApi.endpoints.listTrends.matchRejected, (state, action) => {
        console.log('rejected', action)
        state.chart.trends = [];
      })
      
      
  },
  
})

export const { setHorizontalLine, setVerticalLine, toggleLiveMode, toggleZoomMode, toggleTooltip, toggleRightPanel, 
               setFromDate,setToDate, setOnlySelected, setTrendScale, setDateRange, setAutoscale } = chartsSlice.actions

// The function below is called a thunk and allows us to perform async logic. It
// can be dispatched like a regular action: `dispatch(incrementAsync(10))`. This
// will call the thunk with the `dispatch` function as the first argument. Async
// code can then be executed and other actions can be dispatched


// The function below is called a selector and allows us to select a value from
// the state. Selectors can also be defined inline where they're used instead of
// in the slice file. For example: `useSelector((state) => state.counter.value)`

//export const selectTemplate = (state) => state.template.value

export default chartsSlice.reducer
