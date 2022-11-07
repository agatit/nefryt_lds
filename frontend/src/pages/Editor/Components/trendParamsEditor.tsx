
import * as React from "react"
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { Trend, TrendDef, TrendParam, useListTrendDefsQuery, useListTrendParamsQuery, useUpdateTrendMutation } from "../../../store/trendApi";
import { Accordion, AccordionDetails, AccordionSummary, Button, Checkbox, FormControl, FormControlLabel,  FormGroup,  FormHelperText,  FormLabel,  InputLabel,  MenuItem,  Slider,  Stack, Switch, TextField, Typography } from "@mui/material";
import { RootState } from "../../../app/store";
import { NodeState } from "../../../features/editor/nodeEditorSlice";
import { Color, ColorPicker, createColor } from "material-ui-color";
import { CollectionsBookmarkOutlined } from "@material-ui/icons";
import { TrendParamsState } from "../../../features/editor/trendEditorSlice";


 type Prop ={
    activeTrend : Trend;
}
  


export const TrendParamsEditor: React.FC<Prop> = (p) => {
    const dispatch: React.Dispatch<any> = useDispatch()

    const trendEditor: TrendParamsState = useSelector(
        (state: RootState) => state.trendEditor,
        shallowEqual
    )

    const saveParams = (e: React.MouseEvent<HTMLElement>) => {

    }

    var trendID = p.activeTrend? p.activeTrend.ID ? p.activeTrend.ID  : -1 : -1;
    //var filter_txt : string = 'TrendID eq ' + trendID; 
    //var filter={$filter:filter_txt};
     useListTrendParamsQuery({trendId : trendID}, {refetchOnMountOrArgChange : true});
   
    return (
        <React.Fragment>
             
            <FormControl sx={{ m: 3 }} component="fieldset" variant="standard" >     
            {trendEditor.params.map((trend : TrendParam, index) => (      
                <TextField
                    required
                    id="trend_name"
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