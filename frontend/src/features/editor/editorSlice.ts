import { createSlice } from '@reduxjs/toolkit'
import { DRAG_NODE, EditorState, INode } from '../../pages/Editor/type';
import { enhancedApi as nodeApi, Node, ListNodesApiResponse} from '../../store/nodeApi'

const initialState: EditorState = {
  area:{
   Width : 1000,
   ScaleWidth : 10,
   Height : 400,
   ScaleHeight : 10,
   SIUnit :{ 
       SIUnitTID : 'm',
       SIUnitID : 1,
       Name : 'metry',
       Description : 'metry',
       Enabled : true,
       ValueFactor : 1,
       ValueOffset : 1,
       SIUnitGroup : {} 
     },
  },
  forceRefresh : false,
  Nodes :  [
  // {Name:'AAA', NodeID : 1, TrendDef:{}, type : 'VALVE', positionX:130,positionY:100},
  // {Name:'BBB', NodeID : 2, TrendDef:{}, type : 'TEMP',  positionX:50,positionY:50},
  // {Name:'CC', NodeID : 3, TrendDef:{}, type : 'TANK', positionX:230,positionY:200},
  // {Name:'DD', NodeID : 4, TrendDef:{}, type : 'PRESS',  positionX:150,positionY:200},
 ],
 Links : [
 //{BeginNodeID:1, EndNodeID:2, beginPointX:-1, beginPointY:-1,endPointX:-1,endPointY:-1},
 //{BeginNodeID:3, EndNodeID:4,beginPointX:-1, beginPointY:-1,endPointX:-1,endPointY:-1}
 ],
 pipelines : [],
 //action:{
 //  type:BROWSE,
 //  data : []
 //},
 //activeEditor: USE_EDITOR_NODES,  
 activeNode: {node : {}, state : ''}
}

export const editorSlice = createSlice({
  name: 'editor',
  initialState,
  reducers: {
    removeNode: (state, action) => {
      

    },
    setActiveNode: (state, action) => {
      state.activeNode.node = action.payload; 
      state.activeNode.state = '';     

    },
    dragNode: (state, action) => {
      state.activeNode.node = action.payload;      
      state.activeNode.state = DRAG_NODE;
    },
  },

  extraReducers: (builder) => {
    builder
    .addMatcher(nodeApi.endpoints.listNodes.matchPending, (state) => {
      //console.log('pending');
    })
    .addMatcher(nodeApi.endpoints.listNodes.matchFulfilled, (state, action) => {
      console.log('GGGGGGGGGGGGGGG');
      console.log(action.payload);
      var nds : Node[] = action.payload;
      var nodeList : INode [] = [];
           
          var idx=0;
          if (nds){
            nds.forEach((element: Node) => {
              var nodeElement : INode = {
                NodeID: element.ID,
                type: element.Type,
                Name: element.Name? element.Name : "",
                positionX: element.EditorParams? element.EditorParams.PosX : 100,
                positionY: element.EditorParams? element.EditorParams.PosY : 100,
                TrendDef: {}
              };
              nodeList.push(nodeElement);
              idx++;
            });
          }

          state.Nodes = nodeList;
          console.log(nodeList);
    })

    .addMatcher(nodeApi.endpoints.listNodes.matchRejected, (state, action) => {
      //console.log('rejected', action) 
    })  


  },
  
})

export const { removeNode, setActiveNode, dragNode } = editorSlice.actions

// The function below is called a thunk and allows us to perform async logic. It
// can be dispatched like a regular action: `dispatch(incrementAsync(10))`. This
// will call the thunk with the `dispatch` function as the first argument. Async
// code can then be executed and other actions can be dispatched


// The function below is called a selector and allows us to select a value from
// the state. Selectors can also be defined inline where they're used instead of
// in the slice file. For example: `useSelector((state) => state.counter.value)`

//export const selectTemplate = (state) => state.template.value

export default editorSlice.reducer
