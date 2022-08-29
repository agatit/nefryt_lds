

export type TemplateState = {
  sidebar_open : boolean,
}


export interface ITemplateAction {
  type: string
}

export type SidebarParams={
  is_open : boolean,
  styles : ClassNameMap,
  handleDrawer:  MouseEventHandler<T>, 
}

export type RPanelParams = {
  styles: ClassNameMap,
  is_open: boolean,
  handleDrawer:  MouseEventHandler<T>,  
  content: ReactElement
  children: ReactElement
}
    
export type RPanel ={
  enable: boolean,
  open: boolean,
  content : ReactElement,
  handleDrawer:  MouseEventHandler<T>,  
}

