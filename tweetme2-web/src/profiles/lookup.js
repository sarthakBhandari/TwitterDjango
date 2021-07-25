import { backendLookup } from "../lookup";

export function apiProfileDetail(username, callback) {
  let endpoint = `/profiles/${username}/`;
  backendLookup("GET", endpoint, callback);
}

export const apiProfileFollowToggle = (username, action, callback) => {
  let endpoint = `/profiles/${username}/follow`;
  const data = { action: `${action && action}`.toLowerCase() };
  backendLookup("POST", endpoint, callback, data);
};

export function apiProfileFeed(username, callback, nextUrl) {
  let endpoint = `/profiles/${username}/feed/`;
  if (nextUrl !== undefined && nextUrl !== null) {
    endpoint = nextUrl.replace("http://localhost:8000/api", "");
  }
  backendLookup("GET", endpoint, callback);
}
