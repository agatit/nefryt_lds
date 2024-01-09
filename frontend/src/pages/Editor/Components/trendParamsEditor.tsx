
import * as React from "react"
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { Trend, TrendDef, TrendParam, useListTrendDefsQuery, useListTrendParamsQuery, useUpdateTrendMutation } from "../../../store/trendApi";
import { Accordion, AccordionDetails, AccordionSummary, Button, Checkbox, FormControl, FormControlLabel,  FormGroup,  FormHelperText,  FormLabel,  InputLabel,  MenuItem,  Slider,  Stack, Switch, TextField, Typography } from "@mui/material";
import { RootState } from "../../../app/store";
import { NodeState } from "../../../features/editor/nodeEditorSlice";
import { Color, ColorPicker, createColor } from "material-ui-color";
import { CollectionsBookmarkOutlined } from "@material-ui/icons";
import { setNodeTrendParams, TrendParamsState } from "../../../features/editor/trendEditorSlice";
import { useState } from "react";


 type Prop ={
    trendID : number;
}
  


export const TrendParamsEditor: React.FC<Prop> = (p) => {
    const dispatch: React.Dispatch<any> = useDispatch()
    const [param, setParam] = useState<TrendParam[]>([])

    const trendEditor: TrendParamsState = useSelector(
        (state: RootState) => state.trendEditor,
        shallowEqual
    )

    const saveParams = (e: React.MouseEvent<HTMLElement>) => {

    }

    //var filter_txt : string = 'TrendID eq ' + trendID; 
    //var filter={$filter:filter_txt};
    const useListTrendParamsresponse = useListTrendParamsQuery({trendId : p.trendID}, {refetchOnMountOrArgChange : true});
   

    React.useEffect(() => {
        setParam(useListTrendParamsresponse.data as TrendParam[])  
        //params = (useListTrendParamsresponse.data as TrendParam[])
        //console.log(params);
        //dispatch(setNodeTrendParams(useListTrendParamsresponse.data));
      },[useListTrendParamsresponse.data]);

     console.log(param);
    return (
        <React.Fragment>
             
            <FormControl sx={{ m: 3 }} component="fieldset" variant="standard" >     
            {param?.map((trend : TrendParam, index) => ( 
                     
                <TextField
                    required
                    key={trend.TrendParamDefID}
                    id="param_name"
                    label="Nazwa"
                    value={''}
                    onChange={(e) => {
                        //edtTrend.Name = e.target.value;
                        //setTrendName(e.target.value);
                    }}
                    InputLabelProps={{
                        shrink: true,
                        className: undefined
                    }}
                                  
                />
            ))}

                <Button style={{marginTop:'30px', width:'300px'}} onClick={saveParams} variant="contained">Zapisz zmiany</Button>
                
      </FormControl>
           
        </React.Fragment>

    )
}