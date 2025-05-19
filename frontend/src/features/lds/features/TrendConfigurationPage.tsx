import ScaleScrollBar from "../../../components/ScaleScrollBar";

export default function TrendConfigurationPage() {
  return (
    <ScaleScrollBar
      value={{ start: 20, end: 50 }}
      min={0}
      max={100}
      vertical={true}
    />
  );
}
