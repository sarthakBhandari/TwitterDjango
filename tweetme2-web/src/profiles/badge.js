import React from "react";
import { useEffect, useState } from "react";
import { apiProfileDetail } from "./lookup";
import { UserDisplay, UserPicture } from "./components";
import { apiProfileFollowToggle } from "./lookup";
import { DisplayCount } from "./utils";

const ProfileBadge = (props) => {
  const { user, didFollowToggle, profileLoading } = props;
  let currentVerb = user && user.is_following ? "Unfollow" : "Follow";
  currentVerb = profileLoading ? "Loading..." : currentVerb;

  const handleFollowToggle = (e) => {
    e.preventDefault();
    if (didFollowToggle && !profileLoading) {
      didFollowToggle(currentVerb);
    }
  };
  return user ? (
    <div className="p-2">
      <div className="mb-2">
        <UserPicture user={user} hideLink={true} />
      </div>
      <p>
        <UserDisplay user={user} includeFullName={true} hideLink={true} />
      </p>
      <p>
        <DisplayCount>{user.followers_count}</DisplayCount>
        {user.followers_count === 1 ? " follower" : " followers"}
      </p>
      <p>
        <DisplayCount>{user.following_count}</DisplayCount> following
      </p>
      <p>{user.location}</p>
      <p>{user.bio}</p>

      <button
        onClick={(e) => handleFollowToggle(e)}
        className="btn btn-primary"
      >
        {currentVerb}
      </button>
    </div>
  ) : null;
};

export function ProfileBadgeComponent(props) {
  const { username } = props;
  const [didLookup, setDidLookup] = useState(false);
  const [profile, setProfile] = useState(null);
  const [profileLoading, setProfileLoading] = useState(false);

  const handleBackendLookup = (response, status) => {
    if (status === 200) {
      setProfile(response);
    } else {
      alert("There was an error finding your tweet.");
    }
  };
  useEffect(() => {
    if (didLookup === false) {
      apiProfileDetail(username, handleBackendLookup);
      setDidLookup(true);
    }
  }, [username, didLookup, setDidLookup]);

  const handleNewFollow = (actionVerb) => {
    setProfileLoading(true);
    apiProfileFollowToggle(username, actionVerb, (response, status) => {
      // console.log(response, status);
      if (status === 200) {
        setProfile(response);
        // apiProfileDetail(username, handleBackendLookup) // does the same thing but two lookups
      }
      setProfileLoading(false);
    });
  };

  return profile === null ? null : (
    <ProfileBadge
      user={profile}
      didFollowToggle={handleNewFollow}
      profileLoading={profileLoading}
    />
  );
}
