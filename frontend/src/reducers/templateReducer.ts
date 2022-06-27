
import { ITemplateAction, TemplateState } from "../components/template/type"
import * as templateAction from "../actions/Layout/actions"
import {TOGGLE_RPANEL, TOGGLE_SIDEBAR } from "../actions/Layout/actionType"


const initialState: TemplateState = {
    sidebar_open : false,
}

const templateReducer = (
    state: TemplateState = initialState,
    action: ITemplateAction
  ): TemplateState => {
    switch (action.type) {
        case TOGGLE_SIDEBAR:{
            return {
              ...state,
             sidebar_open : !state.sidebar_open
            }
        }
    }
    return state
  }
  
  export default templateReducer