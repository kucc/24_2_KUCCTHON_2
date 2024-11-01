import React from "react";
import styles from "./Button.module.css";
import bananaButton from "../img/bananaButton.svg";
import bananaButton_hover from "../img/bananaButton_hover.svg";
interface ButtonProps {
  text: string; 
  onClick?: () => void; 
  className?: string;
}


const Button: React.FC<ButtonProps> = ({ text, onClick, className }) => {

  return (
    <div className={styles["button-container"]} >
      <img src={bananaButton} alt="banana" className={styles["button-image"]} />

      <img
        src={bananaButton_hover}
        alt="banana hover"
        className={styles["button-hover-image"]}
        onClick={onClick}
      />

      <span className={styles["button-text"]}>{text}</span>
    </div>
  );
};

export default Button;
