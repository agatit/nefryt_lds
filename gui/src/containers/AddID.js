import React from "react"
import { connect } from "react-redux"
import { addID } from '../actions'

const AddID = ({dispatch}) => {
    let input 
  
    return (
      <div>
        <span>ID List: </span>
        <form onSubmit={e =>{
            e.preventDefault()
            if (!input.value.trim()) {
              return
            }
            dispatch(addID(input.value))
            input.value = ''
          }}>
            <label htmlFor="AddButton" />
            <input id="AddButton" type="number" min="0" ref={node => input = node}  />
            <button type="submit">
              Add ID
            </button>
        </form>
      </div>
    )
}

export default connect()(AddID)