import React from 'react'
import AddID from '../containers/AddID'
import GetIDList from '../containers/GetIDList'
import PointsNumberInput from '../containers/PointsNumberInput'
import TimestampsInput from '../containers/TimestampsInput'
import GraphButton from '../containers/GraphButtonContainer'


const App = () => (
    <div>
        <AddID />
        <GetIDList />
        <TimestampsInput/>
        <PointsNumberInput />
        <GraphButton />  
    </div>
)

export default App