import React from 'react'
import PropTypes from 'prop-types'
import ID from './ID'

const IDList = ({ ids, removeID }) => (
    <ul>
        {ids.map((id) => (
            <ID key={id.index} {...id} onClick={() => removeID(id.index)} />    
        ))}
    </ul>
)

IDList.propTypes = {
    removeID: PropTypes.func.isRequired, 
    ids: PropTypes.arrayOf(
        PropTypes.shape({
            index: PropTypes.number.isRequired,
            value: PropTypes.number.isRequired
        }).isRequired
    ).isRequired
}

export default IDList