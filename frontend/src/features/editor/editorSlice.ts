import { createSlice } from '@reduxjs/toolkit'
import { DRAG_NODE, EditorState, ILink, INode } from '../../pages/Editor/type';
import { enhancedApi as nodeApi, Node, ListNodesApiResponse} from '../../store/nodeApi'
import { enhancedApi as linkApi, Link} from '../../store/linkApi'
import { Simulate } from 'react-dom/test-utils';
import { SettingsEthernet } from '@material-ui/icons';

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
  Nodes :  [],
  Links : [],
  pipelines : [],
  activeElement: {node : {}, link:-1, state : ''}
}

export const editorSlice = createSlice({
  name: 'editor',
  initialState,
  reducers: {
    removeNode: (state, action) => {
      

    },
    setActiveNode: (state, action) => {
      state.activeElement.node = action.payload;
      state.activeElement.link = -1; 
      state.activeElement.state = '';     

    },
    setActiveLink: (state, action) => {
      console.log('aaaaa');
      console.log(action.payload);
      state.activeElement.node = {};
      state.activeElement.link = action.payload; 
      state.activeElement.state = '';     

    },
    dragNode: (state, action) => {
      state.activeElement.node = action.payload;  
      state.activeElement.link = -1;    
      state.activeElement.state = DRAG_NODE;
    },
  },

  extraReducers: (builder) => {
    builder
    .addMatcher(nodeApi.endpoints.listNodes.matchPending, (state) => {
      //console.log('pending');
    })
    .addMatcher(nodeApi.endpoints.listNodes.matchFulfilled, (state, action) => {
      //console.log('GGGGGGGGGGGGGGG');
      //console.log(action.payload);
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
      console.log('rejected', action);
        console.log(action);
    })  


    .addMatcher(linkApi.endpoints.listLinks.matchPending, (state) => {
      //console.log('pending');
    })
    .addMatcher(linkApi.endpoints.listLinks.matchFulfilled, (state, action) => {
      console.log(state);
      var nds : Link[] = action.payload;
      var linkList : ILink [] = [];
           
          var idx=0;
          if (nds){
            nds.forEach((element: Link) => {
              var linkElement : ILink = {
                ID : element.ID,
                BeginNodeID: element.BeginNodeID ? element.BeginNodeID : -1,
                EndNodeID: element.EndNodeID ? element.EndNodeID : -1 ,
                beginPointX: 0,
                beginPointY: 0,
                endPointX: 0,
                endPointY: 0,
                length : element.Length
              };
              
 
              var beginPosX : number = 0;
              var beginPosY : number = 0; 
              var endPosX : number = 0;
              var endPosY : number = 0; 
              var lengthX : number = 0;
              var lengthY : number = 0;

              var BeginNode : INode = state.Nodes.find((x: { NodeID?: number }) => x.NodeID === linkElement.BeginNodeID) as INode;
              var EndNode : INode = state.Nodes.find((x: { NodeID?: number }) => x.NodeID === linkElement.EndNodeID) as INode;
                if (BeginNode && EndNode && (BeginNode.positionX) && (BeginNode.positionY)){
                  beginPosX  = (BeginNode.positionX % state.area.ScaleWidth) == 0 ?  Math.floor(BeginNode.positionX / state.area.ScaleWidth) : Math.floor(BeginNode.positionX / state.area.ScaleWidth) + 1;
                  beginPosY = (BeginNode.positionY % state.area.ScaleHeight) == 0 ?  Math.floor(BeginNode.positionY / state.area.ScaleHeight) : Math.floor(BeginNode.positionY / state.area.ScaleHeight) + 1;
                
                  endPosX  = (EndNode.positionX % state.area.ScaleWidth) == 0 ?  Math.floor(EndNode.positionX / state.area.ScaleWidth) : Math.floor(EndNode.positionX / state.area.ScaleWidth) + 1;
                  endPosY = (EndNode.positionY % state.area.ScaleHeight) == 0 ?  Math.floor(EndNode.positionY / state.area.ScaleHeight) : Math.floor(EndNode.positionY / state.area.ScaleHeight) + 1;              
                 
                  lengthX  = endPosX - beginPosX;
                  lengthY  = endPosY - beginPosY;
        
                  
                  
                  linkElement.beginPointX = beginPosX;
                  linkElement.beginPointY = beginPosY;
        
                  linkElement.endPointX = endPosX;
                  linkElement.endPointY = endPosY;
                }

                linkList.push(linkElement);
                idx++;
            });
          }

          state.Links = linkList;

      
    })

    .addMatcher(linkApi.endpoints.listLinks.matchRejected, (state, action) => {
      //console.log('rejected', action) 
    })  
    .addMatcher(nodeApi.endpoints.updateNode.matchFulfilled, (state, action) => {
      console.log('FFFFFFFFFFF');
      console.log(action);
      //state.user = action.payload.username
      //state.token = action.payload.token
      //state.refreshToken = action.payload.refreshToken
      //localStorage.setItem('token', action.payload.token);
      //localStorage.setItem('refreshToken', action.payload.token);
      //localStorage.setItem('user', action.payload.token);
      //state.isAuthenticated = true
    })
    .addMatcher(nodeApi.endpoints.updateNode.matchRejected, (state, action) => {
      console.log('rejected', action);
      console.log(action);
    })


  },
  
})

export const { removeNode, setActiveNode, dragNode, setActiveLink } = editorSlice.actions

// The function below is called a thunk and allows us to perform async logic. It
// can be dispatched like a regular action: `dispatch(incrementAsync(10))`. This
// will call the thunk with the `dispatch` function as the first argument. Async
// code can then be executed and other actions can be dispatched


// The function below is called a selector and allows us to select a value from
// the state. Selectors can also be defined inline where they're used instead of
// in the slice file. For example: `useSelector((state) => state.counter.value)`

//export const selectTemplate = (state) => state.template.value

export default editorSlice.reducer
