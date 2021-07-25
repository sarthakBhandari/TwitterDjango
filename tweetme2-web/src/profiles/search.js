import React from "react";

export function SearchProfile(props) {
  const textAreaRef = React.createRef();
  const { newProfile } = props;

  const handleSubmit = (event) => {
    event.preventDefault();
    const newVal = textAreaRef.current.value;
    newProfile(newVal);
    textAreaRef.current.value = "";
  };
  return (
    <div className={props.className}>
      <form onSubmit={(e) => handleSubmit(e)} className="col-3 mx-auto">
        <textarea
          ref={textAreaRef}
          required={true}
          className="form-control"
          name="tweet"
          placeholder="Search user by username"
        ></textarea>
        <button type="submit" className="btn btn-primary my-3">
          Search
        </button>
      </form>
    </div>
  );
}
