const graphData = (state = { data: null, options: null}, action) => {
  switch (action.type) {
      case "UPDATE_DATA":
        return {
            data: action.data,
            options: action.options
        }
      default:
        return state
  }
}
export default graphData
