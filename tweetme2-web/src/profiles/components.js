import React, { useState, useEffect } from "react";
import { SearchProfile } from "./search";
import { apiProfileFeed } from "./lookup";

const UserLink = (props) => {
  const { username } = props;
  const handleUserLink = (e) => {
    e.preventDefault();
    window.location.href = `/profiles/${username}`;
  };
  return (
    <span className="pointer" onClick={(e) => handleUserLink(e)}>
      {props.children}
    </span>
  );
};

export const UserPicture = (props) => {
  const { user, hideLink } = props;
  return (
    <>
      {hideLink ? (
        <span className="mx-1 px-3 py-2 rounded-circle bg-dark text-white">
          {user.username[0]}
        </span>
      ) : (
        <UserLink username={user.username}>
          <span className="mx-1 px-3 py-2 rounded-circle bg-dark text-white">
            {user.username[0]}
          </span>
        </UserLink>
      )}
    </>
  );
};
export const UserDisplay = (props) => {
  const { user, includeFullName, hideLink } = props;
  const nameDisplay = includeFullName
    ? `${user.first_name} ${user.last_name} `
    : null;

  return (
    <>
      {nameDisplay}
      {hideLink ? (
        `@${user.username}`
      ) : (
        <UserLink username={user.username}>
          <span>@{user.username}</span>
        </UserLink>
      )}
    </>
  );
};

// export function SearchComponent(props) {
//   const [username, setUsername] = useState(null);
//   const [didSearch, setDidSearch] = useState(false);
//   const [tweetsInit, setTweetsInit] = useState([]);
//   const [tweets, setTweets] = useState([]);
//   const [nextUrl, setNextUrl] = useState(null);

//   const handleNewProfile = (name) => {
//     setUsername(name);
//     setDidSearch(true);
//   };

//   useEffect(() => {
//     if (tweetsInit.length !== tweets.length) {
//       setTweets(tweetsInit);
//     }
//   }, [tweets, tweetsInit]);

//   useEffect(() => {
//     if (didSearch) {
//       const handleTweetListLookup = (response, status) => {
//         if (status === 200) {
//           console.log(response);
//           setTweetsInit(response.results);
//           setNextUrl(response.next);
//         } else if (status === 404) {
//           console.log(response);
//         }
//       };
//       apiProfileFeed(username, handleTweetListLookup);
//     }
//   }, [username]);

//   const handleLoadNext = (e) => {
//     e.preventDefault();
//     apiProfileFeed(
//       username,
//       (response, status) => {
//         if (status === 200) {
//           const newTweets = [...tweets].concat(response.results);
//           setTweetsInit(newTweets);
//           setTweets(newTweets);
//           setNextUrl(response.next);
//         }
//       },
//       nextUrl
//     );
//   };

//   return didSearch ? (
//     <div className={props.className}>
//       <SearchProfile newProfile={handleNewProfile} className="col-12 mb-3" />
//       {username ? (
//         <>
//           <ProfileBadgeComponent username={username} />
//           {tweets !== null
//             ? tweets.map((item, index) => {
//                 return (
//                   <Tweet
//                     tweet={item}
//                     className="my-5 py-5 border bg-white text-dark"
//                     key={`${index}-{item.id}`}
//                   />
//                 );
//               })
//             : null}
//           {nextUrl && (
//             <button
//               onClick={(e) => handleLoadNext(e)}
//               className="btn btn-outline-primary"
//             >
//               Load Next
//             </button>
//           )}
//         </>
//       ) : (
//         <h1>User not found</h1>
//       )}
//     </div>
//   ) : (
//     <SearchProfile newProfile={handleNewProfile} className="col-12 mb-3" />
//   );
// }
export const SearchComponent = (props) => {
  const [username, setUsername] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleNewProfile = (name) => {
    setUsername(name);
  };
  useEffect(() => {
    if (username) {
      const handleTweetListLookup = (response, status) => {
        if (status === 200) {
          setSuccess(true);
          window.location.href = `/profiles/${username}`;
        } else if (status === 404) {
          setSuccess(false);
        }
      };
      apiProfileFeed(username, handleTweetListLookup);
    }
  }, [username]);
  return (
    <>
      <SearchProfile newProfile={handleNewProfile} />
      {success === false ? (
        <div>
          <h1 className="mx-auto text-uppercase">
            User not found, search again
          </h1>
        </div>
      ) : null}
    </>
  );
};
