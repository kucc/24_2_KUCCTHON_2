import React, { useState, ChangeEvent } from 'react';
import styles from './SignUpModal.module.css';

interface SignUpModalProps {
  isOpen: boolean;
  close: () => void;
}

const SignUpModal: React.FC<SignUpModalProps> = ({ isOpen, close }) => {
  const [signupData, setSignupData] = useState({
    login_id: '',
    password: '',
    confirmPassword: '',
    user_name: '',
    planet_name: ''
  });

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setSignupData({
      ...signupData,
      [name]: value
    });
  };

  const handleSignUp = () => {
    if (signupData.password !== signupData.confirmPassword) {
      alert("비밀번호가 일치하지 않습니다.");
      setSignupData({
        login_id: '',
        password: '',
        confirmPassword: '',
        user_name: '',
        planet_name: ''
      });
      return;
    }

    fetch("http://127.0.0.1:8000/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        login_id: signupData.login_id,
        password: signupData.password,
        user_name: signupData.user_name,
        planet_name: signupData.planet_name
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        close(); // 회원가입 성공 후 모달 닫기
      })
      .catch((error) => {
        console.error("Sign Up error:", error);
      });
  };

  if (!isOpen) return null;

  return (
    <div className={styles.modal_overlay} onClick={close}>
      <div className={styles.modal_content} onClick={(e) => e.stopPropagation()}>
        <span className={styles.close} onClick={close}>&times;</span>
        <h2>회원가입</h2>
        <input
          type="text"
          name="login_id"
          placeholder="아이디"
          value={signupData.login_id}
          onChange={handleInputChange}
          className={styles.input_field}
        />
        <input
          type="password"
          name="password"
          placeholder="비밀번호"
          value={signupData.password}
          onChange={handleInputChange}
          className={styles.input_field}
        />
        <input
          type="password"
          name="confirmPassword"
          placeholder="비밀번호 확인"
          value={signupData.confirmPassword}
          onChange={handleInputChange}
          className={styles.input_field}
        />
        <input
          type="text"
          name="user_name"
          placeholder="사용자 이름"
          value={signupData.user_name}
          onChange={handleInputChange}
          className={styles.input_field}
        />
        <input
          type="text"
          name="planet_name"
          placeholder="행성 이름"
          value={signupData.planet_name}
          onChange={handleInputChange}
          className={styles.input_field}
        />
        <button onClick={handleSignUp} className={styles.signup_button}>회원가입</button>
      </div>
    </div>
  );
};

export default SignUpModal;
