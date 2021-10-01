import { connect } from "react-redux";
import { removeID } from "../actions";
import IDList from "../components/IDList";

const mapStateToProps = (state) => ({
        ids: state.ids
})

const mapDispatchToProps = (dispatch) => ({
        removeID: (index) => dispatch(removeID(index))
})

export default connect(mapStateToProps, mapDispatchToProps)(IDList)