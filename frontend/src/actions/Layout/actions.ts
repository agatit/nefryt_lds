import { ITemplateAction } from "../../components/template/type";
import { TOGGLE_RPANEL, TOGGLE_SIDEBAR } from "./actionType";



export function toggleRPanel() {
  const action: ITemplateAction = {
    type: TOGGLE_RPANEL,
  }
  return action;
}
    
export function toggleSidebar() {
    const action: ITemplateAction = {
        type: TOGGLE_SIDEBAR,
    }
    return action;
}