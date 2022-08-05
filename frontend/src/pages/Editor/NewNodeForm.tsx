import * as React from "react"
import { Dispatch } from "redux"
import { useDispatch } from "react-redux"
import { useSelector, shallowEqual } from "react-redux"
import { actionTypes, Field, reduxForm } from 'redux-form';
import { Button, Modal, ModalBody, ModalFooter, ModalHeader } from 'reactstrap';
import { cancelNodeAction, createNode, newNode, saveNode } from "../../actions/editor/actions";
import { RootState } from "../..";
import {NEW_NODE, NodeType as NodeType}  from "../../actions/editor/actionType";
import { INode } from "./type";



  const renderField = () => (
    <div>
      <label>Email address</label>
    <input type="email" className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email"></input>
   
    </div>
  )

  type p = {
    handleSubmit : any; 
    }
 
const NewNodeForm: React.FC<p> = (a:p) => {
  const dispatch: Dispatch<any> = useDispatch()
  const isOpen: boolean = useSelector(
    (state: RootState) => state.pipelineEditorReducer.action.type == NEW_NODE,
    shallowEqual
)


const handleCancel  = (e: React.MouseEvent<HTMLElement>) => {
  dispatch(cancelNodeAction());
}
/*
const handleSubmit  = (e: any ) => {
  e.preventDefault();
  const form = e.currentTarget;

  console.log(form);

  var node : INode = {NodeID : -1,
    type : form.elements.Type.value,
    Name : form.elements.Name.value,
    positionX:0,
    positionY:0,
    TrendDef : { } 
  }

  dispatch(createNode(node));

}*/

  return (
    <Modal isOpen={isOpen} >
      <form onSubmit={a.handleSubmit}>
        <ModalHeader>
          Nowy węzeł
        </ModalHeader>
        <ModalBody>
          
            <div>
              <label>Nazwa</label>
              <Field
                className="form-control"
                name="Name"
                component="input"
                type="text"
                placeholder="Podaj nazwę węzła"
              />
            </div>
            <div>
              <label>Typ</label>
              <Field
                name="Type"
                component="select"    
                placeholder="Wybierz typ węzła"
                className="form-control" 
                required
              >
                <option value=""  disabled>Wybierz typ węzła</option>
                {NodeType.map((element) => (
                  <option value={element.value} key={element.value} >{element.name}</option>
                ))}
                
              </Field>
            </div>
         
        </ModalBody>
        <ModalFooter>
          <Button color="primary" type="submit">
            Zapisz
          </Button>{" "}
          <Button color="secondary" onClick={handleCancel}>
            Anuluj
          </Button>
        </ModalFooter>
        </form>
    </Modal>
  )
}


export default (reduxForm({
  form: 'NewNodeForm'
})(NewNodeForm));