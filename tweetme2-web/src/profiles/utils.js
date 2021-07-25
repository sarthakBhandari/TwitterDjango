import numeral from "numeral";

export const DisplayCount = (props) => {
  return (
    <span className={props.className}>
      {numeral(props.children).format("0a")}
    </span>
  );
};
