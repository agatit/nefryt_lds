const ids = (state = [], action) => {
  switch (action.type) {
      case "ADD_ID":
        return [
          ...state, 
          {
            index: action.index,
            value: action.value
          }
        ]
      
      case "REMOVE_ID":
        return state.filter(id => id.index !== action.index)

      default:
        return state
  }
}
export default ids