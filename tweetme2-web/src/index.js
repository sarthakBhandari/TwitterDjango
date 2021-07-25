import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import { TweetsComponent, TweetDetailComponent, FeedComponent } from "./tweets";
import { ProfileBadgeComponent } from "./profiles";
import * as serviceWorker from "./serviceWorker";

const e = React.createElement;

const rootEl = document.getElementById("root");
if (rootEl) {
  ReactDOM.render(e(TweetsComponent, rootEl.dataset), rootEl);
}

const tweetDetailElements = document.querySelectorAll(".tweetme-2-detail");

tweetDetailElements.forEach((container) => {
  ReactDOM.render(e(TweetDetailComponent, container.dataset), container);
});

const feedEl = document.getElementById("tweetme-2-feed");
if (feedEl) {
  ReactDOM.render(e(FeedComponent, feedEl.dataset), feedEl);
}

const profileBadgeElements = document.querySelectorAll(
  ".tweetme-2-profile-badge"
);

profileBadgeElements.forEach((container) => {
  ReactDOM.render(e(ProfileBadgeComponent, container.dataset), container);
});

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
