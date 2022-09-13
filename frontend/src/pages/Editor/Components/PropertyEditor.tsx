import * as React from "react"
import { Box, Typography } from "@material-ui/core";



type Prop={
    index:number
    activeTabIndex:number
}
   
export const PropertyEditorTab: React.FC<Prop> = (p) => {
    return (
        
      <div style={{backgroundColor:'white' , height:'91%'}}
        role="tabpanel"
        hidden={p.activeTabIndex !== p.index}
        id={`simple-tabpanel-${p.index}`}
        aria-labelledby={`simple-tab-${p.index}`}
      >
        {p.activeTabIndex === p.index && (
          <Box sx={{ p: 3 }}>
            <Typography>{p.index}</Typography>
          </Box>
        )}
      </div>
    );
  }
 