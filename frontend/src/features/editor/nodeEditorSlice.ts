import { createSlice } from '@reduxjs/toolkit'
import {Trend, TrendParam} from '../../store/trendApi'
import {Node} from '../../store/nodeApi'
import { enhancedApi as trendApi} from '../../store/trendApi'

export type NodeTrend={
    trend : Trend;
    parameters : TrendParam | undefined;
}

export type NodeState={
    node:Node | undefined;
    trends : Trend[];
}

const initialState: NodeState = {
   node :undefined,
   trends : []    
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
  
    }
});

export default nodeEditorSlice.reducer