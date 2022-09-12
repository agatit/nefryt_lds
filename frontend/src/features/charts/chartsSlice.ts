import { createSlice } from '@reduxjs/toolkit'
import { ChartsPage } from '../../pages/Charts'
import {  ChartsState, ITrend, ITrendData, PERIOD_EXTENSION} from './types'
import { enhancedApi as trendApi, Trend, TrendData, TrendDef } from '../../store/trendApi'
import { CollectionsOutlined } from '@material-ui/icons';

var colorList:string[] = ["#ff0000", "#00ff00", '#0000ff', '#000000'];

var x = new Date();
var currentTimeZoneOffsetInSeconds = x.getTimezoneOffset();


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
     //  state.chart.currRange.from = cFrom;
     //  state.chart.currRange.to = cTo;
    
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
      state.chart.cfgRange.from =  Date.parse(action.payload);
    },
    setToDate : (state, action) => {
      state.chart.cfgRange.to =  Date.parse(action.payload);
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
    },
    addSerie : (state, action) => {
      //console.log('add');
      var trd : ITrend[] = state.chart.trends.map((obj: ITrend) => ({...obj}));

      var idx=0; 
      const selectedTrends: ITrend[] =trd.filter((obj: ITrend) => obj.selected);

      idx = selectedTrends.length;
      trd.forEach(element => {
         if (element.ID == action.payload.trendName)
         {
           element.selected = true; 
           element.disabled = false; 
           element.autoscale = true;
           //element.scaledMax = 
           //if (element.color==undefined){
             if (selectedTrends.length < colorList.length){
               var selectedColorList: ITrend[] =trd.filter((obj: ITrend) => obj.Color==colorList[idx%colorList.length]);
               if (selectedColorList.length>0){
                 try{
                   colorList.forEach(color => {
                     selectedColorList =selectedTrends.filter((obj: ITrend) => obj.Color==color);
                     if (selectedColorList.length==0){
                       element.Color =color;
                     }
                   });

                 }catch{

                 }


               }else{
                 element.Color =colorList[idx%colorList.length];
               }
             }else{
               var count = selectedTrends.length;
               var mincolor = colorList[idx%colorList.length];
               colorList.forEach(color => {
                 selectedColorList =selectedTrends.filter((obj: ITrend) => obj.Color==color);
                 if (count > selectedColorList.length){
                   count = selectedColorList.length;
                   element.Color =color;
                 }
               });
               
             }
           //}
         }
       });
       state.chart.trends = trd;

    },
    removeSerie : (state, action) => {
      //console.log('remove');
      var data : any[] = [];
          var trds : ITrend[] = state.chart.trends.map((obj: ITrend) => ({...obj})); 
          if ((state.chart.data) && (state.chart.data.length>0)){
           data = state.chart.data.map((obj: any) => ({...obj}));
          }
         
         trds.forEach(element => {
            if (element.ID == action.payload.trendName)
            {
              element.selected = false;
              element.Color = undefined;
              
            }
          });
          state.chart.data=data;
          state.chart.trends = trds;
    },
    setBrushRange: (state, action) => {
      var range = action.payload.to - action.payload.from;
      
      if (range==0){
        range=1;
      }
      var cFrom;
      var cTo;
      if (state.chart.mode.live.active){
        cFrom = action.payload.from 
        cTo = action.payload.to
      }else{
        cFrom = action.payload.from - (PERIOD_EXTENSION*range);
        cTo =  action.payload.to + (PERIOD_EXTENSION*range);
      }  
      state.chart.brush.startIndex = action.payload.from;
      state.chart.brush.endIndex = action.payload.to;
      state.chart.currRange.from = cFrom;
      state.chart.currRange.to = cTo;
      state.chart.cfgRange.from = action.payload.from;
      state.chart.cfgRange.to = action.payload.to;

    },
    setTimer : (state, action) => {
      state.chart.mode.live.active = action.payload ? true : false;
      state.chart.mode.live.timer = action.payload;
    },
    setTimestampRange: (state, action) => {
      var range = action.payload.to - action.payload.from;
      
      if (range==0){
        range=1;
      }
      var cFrom;
      var cTo;
      if (state.chart.mode.live.active){
        cFrom = action.payload.from 
        cTo = action.payload.to
      }else{
        cFrom = action.payload.from - (PERIOD_EXTENSION*range);
        cTo =  action.payload.to + (PERIOD_EXTENSION*range);
      }  
      state.chart.currRange.from = cFrom;
      state.chart.currRange.to = cTo;
      state.chart.cfgRange.from = action.payload.from;
      state.chart.cfgRange.to = action.payload.to;

    },
    disableTrend : (state, action) => {
      var trd : ITrend[] = state.chart.trends;
         
      trd.forEach((element: ITrend) => {
        if (element.ID == action.payload){
         element.disabled = true;
        }
      });
    },
    enableTrend: (state, action) => {
      var trd : ITrend[] = state.chart.trends;
      trd.forEach((element: ITrend) => {
        if (element.ID == action.payload){
          element.disabled = false;
        }
      });

    }

  },

  extraReducers: (builder) => {
    builder
      .addMatcher(trendApi.endpoints.listTrends.matchPending, (state) => {
        //console.log('pending');
      })
      .addMatcher(trendApi.endpoints.listTrends.matchFulfilled, (state, action) => {
        var trd : Trend[] = action.payload;
        var idx=0;
        trd.forEach((element: Trend) => {
        
           var tmp : string =  element.Symbol? element.Symbol : element.ID? element.ID.toString():''; 
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

           state.chart.trends.push(elm);
           
           idx++;
         });

      })

      .addMatcher(trendApi.endpoints.listTrends.matchRejected, (state, action) => {
       // console.log('rejected', action);
      //  console.log(action);
        
      })  

      .addMatcher(trendApi.endpoints.getTrendData.matchPending, (state) => {
        //console.log('pending');
        state.chart.is_loading_trends = true;
      })

      .addMatcher(trendApi.endpoints.getTrendData.matchFulfilled, (state, action) => {
        console.log('TrendData match');
        console.log(action);
        var dat : ITrendData[]=[];
        var mltp = 1; //1000;

        var brushStartIndex=0;
        var brushEndIndex=0;
        var timeTo=state.chart.cfgRange.to;
        var timeFrom=state.chart.cfgRange.from;
        if ((action.payload) &&  (action.payload.length > 0)){ 
          
          timeTo = action.payload[action.payload.length-1].Timestamp * mltp + action.payload[action.payload.length-1].TimestampMs;
          timeFrom = timeTo - state.chart.mode.live.period;
          //console.log(timeFrom);
          //console.log(timeTo);
          console.log(currentTimeZoneOffsetInSeconds);
          action.payload.forEach((el:TrendData)=>{
            var ut = el.Timestamp *mltp + el.TimestampMs + currentTimeZoneOffsetInSeconds*1000;
            //console.log(ut);
            dat.push({...el, unixtime:ut});
            
            if (el.Timestamp *mltp + el.TimestampMs  < state.chart.cfgRange.from - currentTimeZoneOffsetInSeconds*1000){
              brushStartIndex = brushStartIndex+1;
            }
            if (el.Timestamp *mltp + el.TimestampMs  < state.chart.cfgRange.to - currentTimeZoneOffsetInSeconds*1000){
              brushEndIndex = brushEndIndex+1;
            }          
            //console.log(state.chart.data);
           });
           state.chart.brush.startIndex = brushStartIndex;
           state.chart.brush.endIndex = brushEndIndex;
           state.chart.data = dat;
           console.log(state.chart.data);
        }
        state.chart.is_loading_trends = false;

      })

      .addMatcher(trendApi.endpoints.getTrendData.matchRejected, (state, action) => {
        console.log('rejected TrendData', action);
        state.chart.is_loading_trends = false;
      })  
  },
  
})

export const { setHorizontalLine, setVerticalLine, toggleLiveMode, toggleZoomMode, toggleTooltip, toggleRightPanel, 
               setFromDate,setToDate, setOnlySelected, setTrendScale, setDateRange, setAutoscale,
               addSerie, removeSerie, setBrushRange, setTimer, setTimestampRange,
               enableTrend, disableTrend } = chartsSlice.actions

// The function below is called a thunk and allows us to perform async logic. It
// can be dispatched like a regular action: `dispatch(incrementAsync(10))`. This
// will call the thunk with the `dispatch` function as the first argument. Async
// code can then be executed and other actions can be dispatched


// The function below is called a selector and allows us to select a value from
// the state. Selectors can also be defined inline where they're used instead of
// in the slice file. For example: `useSelector((state) => state.counter.value)`

//export const selectTemplate = (state) => state.template.value

export default chartsSlice.reducer
