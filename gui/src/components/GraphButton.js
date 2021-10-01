import React from 'react'
import {Line} from 'react-chartjs-2'


const GraphButton = ({params, data, options, updateData}) => (
    <div>
        <button
        onClick = {() => updateData(params)}
        >Create Graph</button>
        <Line type='line' data={data} options={options} />
    </div>
)

export default GraphButton
