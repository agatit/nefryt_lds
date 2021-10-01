let nextIDIndex = 0

export const addID = (value) => ({
  type: "ADD_ID",
  index: nextIDIndex++,
  value: parseInt(value)
})

export const removeID = (index) => ({
  type: "REMOVE_ID",
  index: index
})

export const updatePoints = (value) => ({
  type: "UPDATE_POINTS",
  value: parseInt(value)
})

export const updateBegin= (value) => ({
  type: "UPDATE_BEGIN",
  value: parseFloat(value)
})

export const updateEnd = (value) => ({
  type: "UPDATE_END",
  value: parseFloat(value)
})

const getString = (items) => {
    const keyValuePairs = []
    for (const key in items) {
      keyValuePairs.push(encodeURIComponent(key) + '=' + encodeURIComponent(items[key]))
    }
    return `http://localhost:5000/?${keyValuePairs.join('&')}`
}

const randomNum = () => Math.floor(Math.random() * (235 - 52 + 1) + 52)

const randomColor = () => `rgb(${randomNum()}, ${randomNum()}, ${randomNum()})`

const getData = async (params) => {
    const {ids, begin, end, number} = params
    const data = {
        labels: [],
        datasets: []
    }
    const options = {
      elements: {
        point: {
            radius: 0
        },
        line: {
            borderWidth: 1
        },
      },
      scales: {
        yAxes: []
      }
    
    }
    for (const id of ids) {
        await fetch(getString({id, begin, end, number}))
        .then(res => res.json())
        .then(
            (res) => {
                let color = randomColor()
                data.labels = res.labels
                data.datasets=[...data.datasets, 
                {
                    label: `Controller no. ${id}`,
                    data: res.data, 
                    borderColor: color,
                    yAxisID: `${id}`
                }]
                options.scales.yAxes = [...options.scales.yAxes,
                  {
                    type: 'linear',
                    id: `${id}`
                  }
                ]
            }
        )
    }
    
    return [data, options]
}


export const updateData = async (dispatch, params) => {
  const [data, options] = await getData(params)
  return dispatch({
    type: "UPDATE_DATA",
    data: data, 
    options: options
  })
}
