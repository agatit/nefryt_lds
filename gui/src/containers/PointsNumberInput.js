import { connect } from "react-redux"
import { updatePoints } from "../actions"

const PointsNumberInput = ({dispatch}) => {
    return (
        <div>
            <label htmlFor = "PointsNumber" >Number of Points:</label><br/>
            <input
                id="PointsNumber"
                type="number"
                min="0"
                onChange={e => dispatch(updatePoints(e.target.value))}
            />
        </div>
    )
}

export default connect() (PointsNumberInput)