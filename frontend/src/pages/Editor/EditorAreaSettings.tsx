import * as React from "react"
import { Dispatch } from "redux"
import { connect, useDispatch } from "react-redux"
import { useSelector, shallowEqual } from "react-redux"
import { actionTypes, Field, reduxForm, SubmissionError, WrappedFieldProps } from 'redux-form';
import { Button, Modal, ModalBody, ModalFooter, ModalHeader } from 'reactstrap';
import {  IPipelinesArea } from "./type";
import { compose } from "@reduxjs/toolkit";
import { Area } from "recharts";
import {reset} from 'redux-form';
import { RootState } from "../../app/store";


  /*const renderField = () => (
    <div>
      <label>Email address</label>
    <input type="email" className="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email"></input>
   
    </div>
  )*/

  const renderField = (props: WrappedFieldProps ) => (
    <div>
        <input {...props.input} type={'number'}/>
        {props.meta.touched && ((props.meta.error && <span style={{color: 'red'}}>{props.meta.error}</span>) || (props.meta.warning && <span>{props.meta.warning}</span>))}
    </div>
  )
 type p = {
  handleSubmit : any; 
  }
const EditorAreaSettings: React.FC<p> = (a: p) => {
  
  const area: IPipelinesArea = useSelector(
    (state: RootState) => state.editor.area ,
    shallowEqual
  )

  const dispatch: Dispatch<any> = useDispatch()
 /* const isOpen: boolean = useSelector(
    (state: RootState) => state.editor.action.type == EDITOR_AREA_SETTINGS,
    shallowEqual
)
*/
const isOpen=false;



const handleCancel  = (e: React.MouseEvent<HTMLElement>) => {
  dispatch(reset('EditorAreaSettings'));  // requires form name
 // dispatch(cancelNodeAction());
}




const handleSubmit  = (e: any ) => {
  //e.preventDefault();
 // const form = e.currentTarget;
 //e.preventDefault();

 console.log(document.forms[0]);
console.log(e.currentTarget);

 /* var node : INode = {NodeID : -1,
    type : form.elements.Type.value,
    Name : form.elements.Name.value,
    positionX:0,
    positionY:0,
    TrendDef : { } 
  }

  dispatch(saveNode(node));
  */
}



  return (
    <Modal isOpen={isOpen} >
      <form onSubmit={a.handleSubmit}>
        <ModalHeader>
          Ustawienia obszaru edytora
        </ModalHeader>
        <ModalBody>
          
            <div>
              <label>Szerokość</label>
              <Field
                className="form-control"
                name="areaWidth"
                component={renderField} 
                type="number"
                placeholder="Podaj szerokość obszaru"
              />
            </div>
            <div>
              <label>Podziałka szerokości</label>
              <Field
                className="form-control"
                name="areaScaleWidth"
                component={renderField} 
                type="number"
                placeholder="Podaj podziałkę szerokości"
              />
            </div>
            <div>
              <label>Wysokość</label>
              <Field
                name="areaHeight"
                component={renderField}   
                placeholder="Podaj wysokość obszaru"
                type="number"
                className="form-control" 
                required
              >
               
                
              </Field>
            </div>
            <div>
              <label>Podziałka wysokości</label>
              <Field
                className="form-control"
                name="areaScaleHeight"
                component={renderField} 
                type="number"
                placeholder="Podaj podziałkę wysokości"
              />
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


const validate = (values: any) => {
  const errors :any= {}
  
  if (!values.areaWidth) {
    errors.areaWidth = 'Pole wymagane'
  } else if (values.areaWidth > 10) {
    errors.areaWidth = 'Za duża wartość'
   //throw new SubmissionError({...errors})
  }
  //console.log(errors);
  //throw new SubmissionError({...errors})
  return errors
}


const handleS  = (e: any ) => {
  //e.preventDefault();
 // const form = e.currentTarget;
 //e.preventDefault();

 //console.log(document.forms[0]);
console.log(e);


 /* var node : INode = {NodeID : -1,
    type : form.elements.Type.value,
    Name : form.elements.Name.value,
    positionX:0,
    positionY:0,
    TrendDef : { } 
  }

  dispatch(saveNode(node));
  */
}


//Example = connect(
//  (state : RootState) => ({
//    initialValues: {areaWidth: state.pipelineEditorReducer.area} // pull initial values from account reducer
//  })
//)(EditorAreaSettings)


//export default 
var Export = reduxForm({ form: 'EditorAreaSettings', validate, enableReinitialize : true})(EditorAreaSettings);
 
export default connect(
    (state : RootState) => ({
      initialValues: {
        areaWidth: state.editor.area.Width,
        areaScaleWidth: state.editor.area.ScaleWidth,
        areaHeight: state.editor.area.Height,
        areaScaleHeight: state.editor.area.ScaleHeight
      } // pull initial values from account reducer
    })
)(Export);

//export default  Export
/*
export default 
  connect( (state : RootState) => ({
    initialValues: {areaWidth: state.pipelineEditorReducer.area} // pull initial values from account reducer
  }),
   (reduxForm({
  form: 'EditorAreaSettings',
  //initialValues:{areaWidth:area.Width}
}))(EditorAreaSettings));

*/

