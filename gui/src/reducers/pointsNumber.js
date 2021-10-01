const pointsNumber = (state = {}, action) => {
    switch (action.type) {
        case "UPDATE_POINTS":
            return {
                value: action.value
            }
        default:
            return state
    }
}

export default pointsNumber