import React, { useState } from 'react';
import ReactDOM from "react-dom/client";
import styles from "./Home.module.css";
import Button from "../components/Button";
import SignInModal from "../components/SignInModal";
import homeLogo from "../img/homeLogo.svg";
import { Sign } from "crypto";

const Home: React.FC = () => {

  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => {
    console.log('openModal');
    setIsModalOpen(true);}
  const closeModal = () => {setIsModalOpen(false);
    console.log('closeModal')
  }

  return (
    <div className={styles.background}>
      <div className={styles.logoContainer}>
        <img src={homeLogo}></img>
      </div>
      <div className={styles.LoginContainer}>
        <Button  onClick={openModal} text="로그인" />
        <SignInModal isOpen={isModalOpen} close={closeModal} />
        {/* <Button text="회원가입" /> */}
      </div>
    </div>
  );
};

export default Home;
