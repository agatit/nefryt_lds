import { createSlice } from '@reduxjs/toolkit'
import {Trend, TrendDef, TrendParam} from '../../store/trendApi'
import {Node} from '../../store/nodeApi'
import { enhancedApi as trendApi} from '../../store/trendApi'



export type NodeState={
   // node:Node | undefined;
    trends : Trend[];
    trenddefs : TrendDef[];
    units : any[];
    //aciveTrend : Trend | undefined;
}

const initialState: NodeState = {
  // node :undefined,
   trends : [],
   trenddefs : [],
   units : [],
   //aciveTrend :  undefined,  
}

export const nodeEditorSlice = createSlice({
    name: 'nodeEditor',
    initialState,
    reducers: {
      
    },
  
    extraReducers: (builder) => {
      builder
      .addMatcher(trendApi.endpoints.listTrends.matchFulfilled, (state, action) => {
        
        var trd : Trend[] = action.payload;
        state.trends = [];
            var idx=0;
            if (trd){
              trd.forEach((element: Trend) => {
                state.trends.push(element);
                idx++;
              });
            }

      })
      .addMatcher(trendApi.endpoints.updateTrend.matchRejected, (state, action) => {
          console.log('AAAA');
          console.log(action);
      })
      .addMatcher(trendApi.endpoints.updateTrend.matchFulfilled, (state, action) => {
        console.log('kkkkk');
        console.log(state.trends);
        console.log(action);
        for(var x=0; x<state.trends.length; x++){ 
          if (state.trends[x].ID == action.payload.ID){
            console.log(state.trends[x]);
            state.trends[x].Name = action.payload.Name? action.payload.Name : '';
            state.trends[x].TrendDefID = action.payload.TrendDefID ? action.payload.TrendDefID : '';
            state.trends[x].Unit = action.payload.Unit;
            state.trends[x].ScaledMax = action.payload.ScaledMax;
            state.trends[x].ScaledMin = action.payload.ScaledMin;
            state.trends[x].Symbol = action.payload.Symbol;
            state.trends[x].Color = action.payload.Color;
            break;
          }
        }
      })
      .addMatcher(trendApi.endpoints.listTrendDefs.matchFulfilled, (state, action) => {
        
        var trdDef : TrendDef[] = action.payload;
        state.trenddefs = [];
            var idx=0;
            if (trdDef){
              trdDef.forEach((element: TrendDef) => {
                state.trenddefs.push(element);
                idx++;
              });
            }

      })
      .addMatcher(trendApi.endpoints.listTrendParams.matchFulfilled, (state, action) => {

      })
  
    }
});

export default nodeEditorSlice.reducer