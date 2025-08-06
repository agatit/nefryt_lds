import {
  Chart,
  ChartCategoryAxis,
  ChartCategoryAxisItem,
  ChartSeries,
  ChartSeriesItem,
  ChartValueAxis,
  ChartValueAxisItem,
  ChartXAxis,
  ChartXAxisItem,
  ChartYAxis,
  ChartYAxisItem,
} from "@progress/kendo-react-charts";
import { DetailPanel } from "onyks_shared_kendo";
import React from "react";
import "../../../styles/features/lds/features/leakProbabilityMap.scss";

const LeakProbabilityPage = React.memo(function LeakProbabilityPage() {
  const data = React.useMemo(() => {
    const data = [];

    for (let i = 0; i < 100; i++) {
      for (let j = 0; j < 100; j++) {
        data.push({ x: i, y: j, value: i * j });
      }
    }

    return data;
  }, []);

  return (
    <React.Fragment>
      <main className="leak-page">
        <div className="leak-chart-container">
          <Chart
            className="leak-chart"
            transitions={false}
            pannable={true}
            zoomable={true}
            renderAs="canvas"
          >
            <ChartXAxis>
              <ChartXAxisItem labels={{ visible: false }} />
            </ChartXAxis>
            <ChartYAxis>
              <ChartYAxisItem labels={{ visible: false }} />
            </ChartYAxis>
            <ChartSeries>
              <ChartSeriesItem
                type="heatmap"
                data={data}
                xField="x"
                yField="y"
                field="value"
                labels={{ visible: false }}
                axis="valueAxis"
                categoryAxis="categoryAxis"
              />
            </ChartSeries>
          </Chart>
        </div>
        <DetailPanel flexGrow={1} extandable={false}></DetailPanel>
      </main>
    </React.Fragment>
  );
});

export default LeakProbabilityPage;
