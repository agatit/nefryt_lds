import { PropertyEditorState, IPropertyEditorAction } from "../pages/Editor/type"
import { CHANGE_TAB } from "../actions/editor/actionType"

const initialState: PropertyEditorState = {
    activeTab:0
  }

const propertyEditorReducer = (
    state: PropertyEditorState = initialState,
    action: IPropertyEditorAction
  ): PropertyEditorState => {
    switch (action.type) {
      
        case CHANGE_TAB:{
          return {
            ...state,
           activeTab : action.tabIndex
          }
        } 
       
       
    }
    return state
  }
  
  export default propertyEditorReducer