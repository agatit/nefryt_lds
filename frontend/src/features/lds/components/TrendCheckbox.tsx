import { Typography } from "@progress/kendo-react-common";
import "../../../styles/features/lds/components/trendCheckbox.scss";
import { Checkbox, CheckboxProps } from "@progress/kendo-react-inputs";

export interface TrendCheckboxProps extends CheckboxProps {
  trendName?: string | null;
}

export default function TrendCheckbox(props: TrendCheckboxProps) {
  const { trendName, ...checkboxProps } = props;
  return (
    <div className="lds-trend-checkbox">
      {trendName && (
        <Typography.p margin={{ bottom: 0 }}>{trendName}</Typography.p>
      )}
      <Checkbox {...checkboxProps} />
    </div>
  );
}
