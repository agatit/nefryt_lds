const initialState = {
    begin: null, 
    end: null, 
}

const timestamps = (state = initialState, action) => {
    switch (action.type) {
        case "UPDATE_BEGIN":
            return {
                begin: action.value, 
                end: state.end
            }
        case "UPDATE_END":
            return {
                begin: state.begin,
                end: action.value
            }

        default:
            return state
    }
}

export default timestamps