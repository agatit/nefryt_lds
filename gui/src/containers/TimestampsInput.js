import { connect } from "react-redux"
import { updateBegin, updateEnd } from "../actions"

const TimestampsInput = ({dispatch}) => {
    return (
        <div>
            <form>
            <label htmlFor = "BeginTime" >Begin UTC Time: </label><br/>
            <input
                id="BeginTime"
                type="number"
                step="0.01"
                min="0"
                onChange={e => dispatch(updateBegin(e.target.value))}
            /><br/>
            <label htmlFor = "EndTime" >End UTC Time: </label><br/>
            <input
                id="EndTime"
                type="number"
                step="0.01"
                min="0"
                onChange={e => dispatch(updateEnd(e.target.value))}
            />
            </form>
        </div>
    )
}

export default connect() (TimestampsInput)