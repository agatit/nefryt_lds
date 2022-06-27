import { Dispatch } from "@reduxjs/toolkit";
import { useDispatch } from "react-redux";
import { IEventsAction } from "../../pages/Events/type";
import { GET_DATA } from "./actionType";

/*
const users=['James','Michael','Harry','Sam','Dubby']

export const getData=()=>{
    return new Promise(resolve=>setTimeout(()=>{
      const nodes = [
        {
          id: "1",
          name: "VSCode",
          deadline: new Date(2020, 1, 17),
          type: "SETUP",
          isComplete: true
        },
        {
          id: "2",
          name: "JavaScript",
          deadline: new Date(2020, 2, 28),
          type: "LEARN",
          isComplete: true
        },
        {
          id: "3",
          name: "React",
          deadline: new Date(2020, 3, 8),
          type: "LEARN",
          isComplete: false
        }
      ];
        resolve({nodes})
    },3000))
}

const dispatch :Dispatch = useDispatch();



export const getDataAction=()=>async(dispatch :Dispatch) =>{
  console.log('hhhhh');
  const data= await getData()
  dispatch({
      type:GET_DATA,
      data:data
  })
}


*/



export function getData(params:any) {
 
  const action: IEventsAction = {
    type: GET_DATA,
    data : params
  }
  console.log(params);
  return action;
}
