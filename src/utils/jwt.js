import { STORAGE_TOKEN } from "src/constants"

export const getToken = () => {
  return localStorage.getItem(STORAGE_TOKEN);
}