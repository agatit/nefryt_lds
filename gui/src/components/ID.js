import React from 'react'
import PropTypes from 'prop-types'

const ID = ({onClick, value}) => (
    <li onClick={onClick}>
        ID Plot: {value}
    </li>
)

ID.propTypes = {
    onClick: PropTypes.func.isRequired,
    value: PropTypes.number.isRequired
}

export default ID