import {combineReducers} from "redux"
import ids from "./ids"
import pointsNumber from "./pointsNumber"
import timestamps from "./timestamps"
import graphData from "./graphData"

export default combineReducers({
    ids, pointsNumber, timestamps, graphData
})