import { Configuration } from "../services/api";
import axios from "axios";

export const config = new Configuration();
export const host =
  (import.meta.env.VITE_API_USE_HTTPS == "true" ? "https://" : "http://") +
  import.meta.env.VITE_API_HOST +
  ":" +
  import.meta.env.VITE_API_PORT;
export const axiosInstance = axios.create();
