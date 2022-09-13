import { createSlice } from '@reduxjs/toolkit'
import { DRAG_NODE, EditorState, ILink, INode, NEW_NODE, SELECTED } from '../../pages/Editor/type';
import { enhancedApi as nodeApi, Node, ListNodesApiResponse} from '../../store/nodeApi'
import { enhancedApi as linkApi, Link} from '../../store/linkApi'
import { Simulate } from 'react-dom/test-utils';
import { SettingsEthernet } from '@material-ui/icons';
import { object } from 'zod';


export const NodeTypes = [ 'TANK','VALVE', 'PRESS'];
export const NodeDescription = ['Zbiornik', 'Zawór', 'Prztwornik ciśnienia'];

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
  activeElement: {node : undefined, LinkID:-1, state : ''}
}

export const editorSlice = createSlice({
  name: 'editor',
  initialState,
  reducers: {
    removeNode: (state, action) => {
      

    },
    setActiveNode: (state, action) => {
      state.activeElement.node = action.payload;
      state.activeElement.LinkID = -1; 
      state.activeElement.state = SELECTED;     

    },
    setActiveLink: (state, action) => {
      console.log('aaaaa');
      console.log(action.payload);
      state.activeElement.node = undefined;
      state.activeElement.LinkID = action.payload; 
      state.activeElement.state = SELECTED;     

    },
    dragNode: (state, action) => {
      state.activeElement.node = action.payload;  
      state.activeElement.LinkID = -1;    
      state.activeElement.state = DRAG_NODE;
    },
    newNode:(state, action) => {
      state.activeElement.node = action.payload;
      state.activeElement.LinkID = -1;
      state.activeElement.state = NEW_NODE;
    }
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
    .addMatcher(nodeApi.endpoints.createNode.matchFulfilled, (state, action) => {
      console.log('dddd');
      console.log(action.payload);
      var tmpNode : INode = {
        NodeID : action.payload.ID,
        type: action.payload.Type,
        Name: '',
        positionX: action.payload.EditorParams?.PosX? action.payload.EditorParams?.PosX : 0,
        positionY: action.payload.EditorParams?.PosY? action.payload.EditorParams?.PosY : 0,
        TrendDef: {}
      }
      state.Nodes.push(tmpNode);
      state.activeElement.node = tmpNode;
      state.activeElement.LinkID=-1;
      state.activeElement.state = SELECTED;
    })
    .addMatcher(nodeApi.endpoints.updateNode.matchFulfilled, (state, action) => {
      //console.log('dddd');
      //console.log(action.payload);
      for(var x=0; x<state.Nodes.length; x++){ 
        if (state.Nodes[x].NodeID == action.payload.ID){
          state.Nodes[x].Name = action.payload.Name? action.payload.Name : '';
          state.Nodes[x].TrendDef = action.payload.TrendID ? action.payload.TrendID : '';
          state.Nodes[x].positionX = action.payload.EditorParams?.PosX? action.payload.EditorParams?.PosX : 0;
          state.Nodes[x].positionY = action.payload.EditorParams?.PosY? action.payload.EditorParams?.PosY : 0;
          state.Nodes[x].type = action.payload.Type;

          for(var y=0; y<state.Links.length; y++){ 
            if ((state.Links[y].BeginNodeID == action.payload.ID) || (state.Links[y].EndNodeID == action.payload.ID)){
              var beginPosX : number = 0;
              var beginPosY : number = 0; 
              var endPosX : number = 0;
              var endPosY : number = 0; 
              var lengthX : number = 0;
              var lengthY : number = 0;

              var BeginNode : INode = state.Nodes.find((x: { NodeID?: number }) => x.NodeID === state.Links[y].BeginNodeID) as INode;
              var EndNode : INode = state.Nodes.find((x: { NodeID?: number }) => x.NodeID === state.Links[y].EndNodeID) as INode;
                if (BeginNode && EndNode && (BeginNode.positionX) && (BeginNode.positionY)){
                  beginPosX  = (BeginNode.positionX % state.area.ScaleWidth) == 0 ?  Math.floor(BeginNode.positionX / state.area.ScaleWidth) : Math.floor(BeginNode.positionX / state.area.ScaleWidth) + 1;
                  beginPosY = (BeginNode.positionY % state.area.ScaleHeight) == 0 ?  Math.floor(BeginNode.positionY / state.area.ScaleHeight) : Math.floor(BeginNode.positionY / state.area.ScaleHeight) + 1;
                
                  endPosX  = (EndNode.positionX % state.area.ScaleWidth) == 0 ?  Math.floor(EndNode.positionX / state.area.ScaleWidth) : Math.floor(EndNode.positionX / state.area.ScaleWidth) + 1;
                  endPosY = (EndNode.positionY % state.area.ScaleHeight) == 0 ?  Math.floor(EndNode.positionY / state.area.ScaleHeight) : Math.floor(EndNode.positionY / state.area.ScaleHeight) + 1;              
                 
                  lengthX  = endPosX - beginPosX;
                  lengthY  = endPosY - beginPosY;
        
                  
                  
                  state.Links[y].beginPointX = beginPosX;
                  state.Links[y].beginPointY = beginPosY;
        
                  state.Links[y].endPointX = endPosX;
                  state.Links[y].endPointY = endPosY;
                }
            }
          }

          state.activeElement.state=SELECTED;
          break;
        }
      }
  
      //console.log(action);
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
    .addMatcher(nodeApi.endpoints.deleteNodeById.matchFulfilled, (state, action) => {
      console.log('dddd');
      console.log(action.payload);

      for(var x=0; x<state.Nodes.length; x++){ 
        if (state.Nodes[x].NodeID == state.activeElement.node?.NodeID){
          state.Nodes.splice(x, 1);

          for(var y=state.Links.length-1; y>0; y--){ 
            if ((state.Links[y].BeginNodeID == state.activeElement.node?.NodeID) || (state.Links[y].EndNodeID == state.activeElement.node?.NodeID)){
              state.Links.splice(y, 1);
            }
          }

          state.activeElement.state=SELECTED;
          state.activeElement.node=undefined;
          state.activeElement.LinkID=-1;
          break;
        }
      }
    })

    

  },
  
})

export const { removeNode, setActiveNode, dragNode, setActiveLink, newNode } = editorSlice.actions

// The function below is called a thunk and allows us to perform async logic. It
// can be dispatched like a regular action: `dispatch(incrementAsync(10))`. This
// will call the thunk with the `dispatch` function as the first argument. Async
// code can then be executed and other actions can be dispatched


// The function below is called a selector and allows us to select a value from
// the state. Selectors can also be defined inline where they're used instead of
// in the slice file. For example: `useSelector((state) => state.counter.value)`

//export const selectTemplate = (state) => state.template.value

export default editorSlice.reducer
