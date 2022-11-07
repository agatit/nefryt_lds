import { createSlice } from '@reduxjs/toolkit'
import {Trend, TrendDef, TrendParam} from '../../store/trendApi'
import {Node} from '../../store/nodeApi'
import { enhancedApi as trendApi} from '../../store/trendApi'



export type TrendParamsState={
   // node:Node | undefined;
    trend : Trend | undefined;
    params:TrendParam[];
}

const initialState: TrendParamsState = {
   trend : undefined,
   params : []
}

export const trendEditorSlice = createSlice({
    name: 'trendEditor',
    initialState,
    reducers: {
      
    },
  
    extraReducers: (builder) => {
      builder
      
      .addMatcher(trendApi.endpoints.listTrendParams.matchFulfilled, (state, action) => {
        var trdParams : TrendParam[] = action.payload;
        state.params = [];
            var idx=0;
            if (trdParams){
              trdParams.forEach((element: TrendParam) => {
                state.params.push(element);
                idx++;
              });
            }
      })
  
    }
});

export default trendEditorSlice.reducer