import { connect } from "react-redux";
import GraphButton from "../components/GraphButton";
import {updateData} from "../actions"

const mapStateToProps = (state) => ({
    params: {
        ids: state.ids.map(function(id) {
            return id.value
        }), 
        begin: state.timestamps.begin,
        end: state.timestamps.end, 
        number: state.pointsNumber.value
    },
    data: state.graphData.data,
    options: state.graphData.options
})

const mapDispatchToProps = (dispatch) => ({
    updateData: ( params) => updateData(dispatch, params)
})


export default connect(mapStateToProps, mapDispatchToProps)(GraphButton)