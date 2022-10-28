
import * as React from "react"
import { shallowEqual, useDispatch, useSelector } from "react-redux";
import { Trend, TrendDef, useListTrendDefsQuery, useUpdateTrendMutation } from "../../../store/trendApi";
import { Accordion, AccordionDetails, AccordionSummary, Button, Checkbox, FormControl, FormControlLabel,  FormGroup,  FormHelperText,  FormLabel,  InputLabel,  MenuItem,  Slider,  Stack, Switch, TextField, Typography } from "@mui/material";
import { RootState } from "../../../app/store";
import { NodeState } from "../../../features/editor/nodeEditorSlice";
import { Color, ColorPicker, createColor } from "material-ui-color";
import { CollectionsBookmarkOutlined } from "@material-ui/icons";


 type Prop ={
    activeElement: any;
    activeTrend : Trend;
}
  


export const TrendPropertyEditor: React.FC<Prop> = (p) => {
    const dispatch: React.Dispatch<any> = useDispatch()

    const nodeEditor: NodeState = useSelector(
        (state: RootState) => state.nodeEditor,
        shallowEqual
    )


    const [trendName, setTrendName] = React.useState(p.activeTrend? p.activeTrend?.Name : '');
    const [trendSymbol, setTrendSymbol] = React.useState(p.activeTrend? p.activeTrend?.Symbol : '');
    const [trendDef, setTrendDef] = React.useState(p.activeTrend ? p.activeTrend?.TrendDefID: '');
    const [trendScaledMin, setTrendScaledMin] = React.useState(p.activeTrend?.ScaledMin);
    const [trendScaledMax, setTrendScaledMax] = React.useState(p.activeTrend?.ScaledMax);
    const [unitID, setUnitID] = React.useState('');
    var tmp : string = p.activeTrend?.Color ? p.activeTrend?.Color:'#000';
    const [trendColor, setTrendColor] = React.useState(tmp);

    const [updateTrend, { isLoading, isError, error, isSuccess }] =
    useUpdateTrendMutation();

    const saveTrend = (e: React.MouseEvent<HTMLElement>) => {
      console.log('DDDD');
     
        var tmptrend : Trend = {
            TrendDefID: trendDef,
            Symbol: trendSymbol,
            Name: trendName,
            Unit:'C',
            RawMin: 0,
            RawMax: 0,
            ScaledMin: trendScaledMin,
            ScaledMax: trendScaledMax,
            NodeID:p.activeTrend.NodeID
        }
        console.log(tmptrend);
            var trendID = p.activeTrend? p.activeTrend.ID ? p.activeTrend.ID  : -1 : -1;
            if (trendID > 0){
                updateTrend({trendId:trendID, trend: tmptrend});
            }
      }
    

    return (
        <React.Fragment>
             
            <FormControl sx={{ m: 3 }} component="fieldset" variant="standard" >     
                      
                <TextField
                    required
                    id="trend_name"
                    label="Nazwa"
                    value={trendName}
                    onChange={(e) => {
                        //edtTrend.Name = e.target.value;
                        setTrendName(e.target.value);
                    }}
                    InputLabelProps={{
                        shrink: true,
                        className: undefined
                    }}
                                  
                />

                <TextField
                    variant="outlined"
                                
                    id="trend_type"
                    value={trendDef}
                    label="Typ"
                    select
                    onChange={(e) => {
                        //console.log(e);
                        //console.log(e.target.value as string);
                        //edtTrend.TrendDefID = (e.target.value as string);
                        setTrendDef((e.target.value as string));
                    }}
                >
                    {
                        nodeEditor.trenddefs.map((element:TrendDef, index:number) => (
                           
                             <MenuItem key={'trenddefs_' + element.ID}  value={element.ID}>{element.Name}</MenuItem>
                        
                        ))

                    }
                </TextField>

                <TextField
                    required
                    id="trend_symbol"
                    label="Symbol"
                    value={trendSymbol}
                    onChange={(e) => {
                        //edtTrend.Name = e.target.value;
                        setTrendSymbol(e.target.value);
                    }}
                    InputLabelProps={{
                        shrink: true,
                        className: undefined
                    }}
                                  
                />

                <TextField
                    variant="outlined"
                                
                    id="trend_unit_id"
                    value={unitID}
                    label="Jednostka"
                    select
                    onChange={(e) => {
                        //console.log(e);
                        //console.log(e.target.value as string);
                        //edtTrend.TrendDefID = (e.target.value as string);
                        setUnitID((e.target.value as string));
                    }}
                >
                    {
                        nodeEditor.units.map((element:any, index:number) => (
                            <MenuItem key={element.key} value={element.ID}>{element.Name}</MenuItem>
                        
                        ))

                    }
                </TextField>



                <ColorPicker value={trendColor} onChange={(newValue: Color) => {
                    console.log('FFFFF');
                    console.log(newValue);
                        //setTrendColor(createColor(newValue));
                        setTrendColor(`#${newValue.hex}`);
                    }} />

                <TextField
                    type='number'
                    required
                    id="trend_scaled_min"
                    label="Wartość minimalna"
                    value={trendScaledMin}
                    onChange={(e) => {
                        //edtTrend.Name = e.target.value;
                        setTrendScaledMin(parseInt(e.target.value, 0));
                    }}
                    InputLabelProps={{
                        shrink: true,
                        className: undefined
                    }}
                                  
                />
                <TextField
                    type='number'
                    required
                    id="trend_scaled_max"
                    label="Wartość maksymalna"
                    value={trendScaledMax}
                    onChange={(e) => {
                        //edtTrend.Name = e.target.value;
                        setTrendScaledMax(parseInt(e.target.value, 0));
                    }}
                    InputLabelProps={{
                        shrink: true,
                        className: undefined
                    }}
                                  
                />

                <Button style={{marginTop:'30px', width:'300px'}} onClick={saveTrend} variant="contained">Zapisz zmiany</Button>
                
      </FormControl>
           
        </React.Fragment>

    )
}