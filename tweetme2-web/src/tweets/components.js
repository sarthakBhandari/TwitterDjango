import React, { useEffect, useState } from "react";

import { TweetCreate } from "./create";
import { Tweet } from "./detail";
import { apiTweetDetail } from "./lookup";
import { TweetsList } from "./list";
import { FeedList } from "./feed";
import { SearchComponent } from "../profiles";

export function FeedComponent(props) {
  const [newTweets, setNewTweets] = useState([]);
  const canTweet = props.canTweet === "false" ? false : true;
  const handleNewTweet = (newTweet) => {
    let tempNewTweets = [...newTweets];
    tempNewTweets.unshift(newTweet);
    setNewTweets(tempNewTweets);
    // console.log(newTweet, newTweets);
  };
  const fixingRetweet = (retweet) => {
    let tempNewTweets = [...newTweets];
    tempNewTweets.unshift(retweet);
    setNewTweets(tempNewTweets);
  };
  const fixingDelete = (id) => {
    let tempNewTweets = newTweets.filter((tweet) => tweet.id !== id);
    setNewTweets(tempNewTweets);
  };
  return (
    <div className={props.className}>
      <SearchComponent {...props} />
      {canTweet === true && (
        <TweetCreate didTweet={handleNewTweet} className="col-12 mb-3" />
      )}
      <FeedList
        newTweets={newTweets}
        fixingRetweet={fixingRetweet}
        fixingDelete={fixingDelete}
        {...props}
      />
    </div>
  );
}

export function TweetsComponent(props) {
  const [newTweets, setNewTweets] = useState([]);
  const canTweet = props.canTweet === "false" ? false : true;
  const handleNewTweet = (newTweet) => {
    let tempNewTweets = [...newTweets];
    tempNewTweets.unshift(newTweet);
    setNewTweets(tempNewTweets);
  };
  const fixingRetweet = (retweet) => {
    let tempNewTweets = [...newTweets];
    tempNewTweets.unshift(retweet);
    setNewTweets(tempNewTweets);
  };
  const fixingDelete = (id) => {
    let tempNewTweets = newTweets.filter((tweet) => tweet.id !== id);
    setNewTweets(tempNewTweets);
  };
  return (
    <div className={props.className}>
      <SearchComponent {...props} />
      {canTweet === true && (
        <TweetCreate didTweet={handleNewTweet} className="col-12 mb-3" />
      )}
      <TweetsList
        fixingRetweet={fixingRetweet}
        fixingDelete={fixingDelete}
        newTweets={newTweets}
        {...props}
      />
    </div>
  );
}

export function TweetDetailComponent(props) {
  const { tweetId } = props;
  const [didLookup, setDidLookup] = useState(false);
  const [tweet, setTweet] = useState(null);

  const handleBackendLookup = (response, status) => {
    if (status === 200) {
      setTweet(response);
    } else {
      alert("There was an error finding your tweet.");
    }
  };
  useEffect(() => {
    if (didLookup === false) {
      apiTweetDetail(tweetId, handleBackendLookup);
      setDidLookup(true);
    }
  }, [tweetId, didLookup, setDidLookup]);

  return tweet === null ? null : (
    <Tweet tweet={tweet} className={props.className} />
  );
}
