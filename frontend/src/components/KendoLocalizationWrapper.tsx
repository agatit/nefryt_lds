import * as React from "react";
import { useTranslation } from "react-i18next";
import {
  IntlProvider,
  LocalizationProvider,
  loadMessages,
  load,
} from "@progress/kendo-react-intl";
// import { i18n } from "i18next";

import likelySubtags from "cldr-core/supplemental/likelySubtags.json";
import currencyData from "cldr-core/supplemental/currencyData.json";
import weekData from "cldr-core/supplemental/weekData.json";

import numbers from "cldr-numbers-full/main/pl/numbers.json";
import caGregorian from "cldr-dates-full/main/pl/ca-gregorian.json";
import dateFields from "cldr-dates-full/main/pl/dateFields.json";
import timeZoneNames from "cldr-dates-full/main/pl/timeZoneNames.json";

export default function KendoLocalizationWrapper(
  props: React.PropsWithChildren
) {
  const { i18n } = useTranslation();
  loadMessages(i18n.getDataByLanguage(i18n.language)?.kendo, i18n.language);
  // const caGregorian = import(
  //   "cldr-dates-full/main/" + props.i18n.language + "/ca-gregorian.json"
  // );
  // const dateFields = import(
  //   "cldr-dates-full/main/" + props.i18n.language + "/dateFields.json"
  // );
  // const timeZoneNames = import(
  //   "cldr-dates-full/main/" + props.i18n.language + "/timeZoneNames.json"
  // );
  // const numbers = import(
  //   "cldr-numbers-full/main/" + props.i18n.language + "/numbers.json"
  // );

  // const likelySubtags = import("cldr-core/supplemental/likelySubtags.json");
  // const currencyData = import("cldr-core/supplemental/currencyData.json");
  // const weekData = import("cldr-core/supplemental/weekData.json");
  load(
    caGregorian,
    dateFields,
    timeZoneNames,
    numbers,
    likelySubtags,
    currencyData,
    weekData
  );

  return (
    <React.Fragment>
      <LocalizationProvider language={i18n.language}>
        <IntlProvider locale={i18n.language}>{props.children}</IntlProvider>
      </LocalizationProvider>
    </React.Fragment>
  );
}
