import React, { useState } from 'react';
import ReactDOM from "react-dom/client";
import styles from "./Home.module.css";
import Button from "../components/Button";
import SignInModal from "../components/SignInModal";
import SignUpModal from '../components/SignUpModal'; 
import homeLogo from "../img/homeLogo.svg";

const Home: React.FC = () => {
  const [currentModal, setCurrentModal] = useState<'signIn' | 'signUp' | null>(null);

  const openSignInModal = () => {
    console.log('Open Sign-In Modal');
    setCurrentModal('signIn');
  };

  const openSignUpModal = () => {
    console.log('Open Sign-Up Modal');
    setCurrentModal('signUp');
  };

  const closeModal = () => {
    setCurrentModal(null);
    console.log('Close Modal');
  };


  return (
    <div className={styles.background}>
      <div className={styles.logoContainer}>
        <img src={homeLogo} alt="Home Logo" />
      </div>

      <div className={styles.LoginContainer}>
      <Button onClick={openSignInModal} text="로그인" />
      <Button onClick={openSignUpModal} text="회원가입" />
      </div>
         {/* 로그인 모달 */}
         {currentModal === 'signIn' && <SignInModal isOpen={currentModal === 'signIn'} close={closeModal} />}

         {/* 회원가입 모달 */}
         {currentModal === 'signUp' && <SignUpModal isOpen={currentModal === 'signUp'} close={closeModal} />}
    </div>
  );
};

export default Home;
