import React, { useEffect, useState } from "react";

import { apiTweetList } from "./lookup";

import { Tweet } from "./detail";
import { apiTweetDelete } from "./lookup";

export function TweetsList(props) {
  const { fixingRetweet, fixingDelete } = props;
  const [newTweets, setNewTweets] = useState(
    props.newTweets ? props.newTweets : []
  );
  const [tweetsInit, setTweetsInit] = useState([]);
  const [tweets, setTweets] = useState([]);
  const [tweetsDidSet, setTweetsDidSet] = useState(false);
  const [nextUrl, setNextUrl] = useState(null);

  useEffect(() => {
    if (newTweets.length < props.newTweets.length) {
      setNewTweets(props.newTweets);
    }
    const final = [...newTweets].concat(tweetsInit);
    if (final.length !== tweets.length) {
      setTweets(final);
    }
  }, [newTweets, props.newTweets, tweets, tweetsInit]);

  useEffect(() => {
    if (tweetsDidSet === false) {
      const handleTweetListLookup = (response, status) => {
        if (status === 200) {
          setTweetsInit(response.results);
          setNextUrl(response.next);
          setTweetsDidSet(true);
        }
      };
      apiTweetList(props.username, handleTweetListLookup);
    }
  }, [tweetsInit, tweetsDidSet, setTweetsDidSet, props.username]);

  const handleDidRetweet = (newTweet) => {
    let tempNewTweets = [...newTweets];
    tempNewTweets.unshift(newTweet);
    setNewTweets(tempNewTweets);
    fixingRetweet(newTweet);
  };

  const handleDelete = (props) => {
    if (props) {
      apiTweetDelete(props, (response, status) => {
        if (status === 204) {
          fixingDelete(props);
          let tempTweetsInit = tweetsInit.filter((tweet) => tweet.id !== props);
          setTweetsInit(tempTweetsInit);
          let tempTweets = tweets.filter((tweet) => tweet.id !== props);
          setTweets(tempTweets);
        }
      });
    }
  };

  const handleLoadNext = (e) => {
    e.preventDefault();
    apiTweetList(
      props.username,
      (response, status) => {
        if (status === 200) {
          const newTweets = [...tweets].concat(response.results);
          setTweetsInit(newTweets);
          setTweets(newTweets);
          setNextUrl(response.next);
        } else {
          alert("There was an error");
        }
      },
      nextUrl
    );
  };

  return (
    <>
      {tweets.map((item, index) => {
        return (
          <Tweet
            tweet={item}
            didRetweet={handleDidRetweet}
            didDelete={handleDelete}
            className="my-5 py-5 border bg-white text-dark"
            key={`${index}-{item.id}`}
          />
        );
      })}
      {nextUrl && (
        <button
          onClick={(e) => handleLoadNext(e)}
          className="btn btn-outline-primary"
        >
          Load Next
        </button>
      )}
    </>
  );
}
