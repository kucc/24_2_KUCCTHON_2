import React from "react";
import ReactDOM from "react-dom/client";
import styles from "./Home.module.css";
import Button from "../components/Button";
import homeLogo from "../img/homeLogo.svg";

const Home: React.FC = () => {
  return (
    <div className={styles.background}>
      <div className={styles.logoContainer}>
        <img src={homeLogo}></img>
      </div>
      {/* <div className={styles.LoginContainer}>
        <Button text="로그인" />
        <Button text="회원가입" />
      </div> */}
    </div>
  );
};

export default Home;
