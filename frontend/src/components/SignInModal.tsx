import React, { useState, ChangeEvent } from 'react';
import styles from './SignInModal.module.css';

interface SignInModalProps {
  isOpen: boolean;
  close: () => void;
}

const SignInModal: React.FC<SignInModalProps> = ({ isOpen, close }) => {
  const [loginData, setLoginData] = useState({
    login_id: '',
    password: ''
  });

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setLoginData({
      ...loginData,
      [name]: value
    });
  };

  const handleLogin = () => {
    fetch("http://your-api-url.com/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(loginData),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        close(); // 로그인 성공 후 모달 닫기
      })
      .catch((error) => {
        console.error("Login error:", error);
      });
  };

  // 모달이 열려 있지 않으면 렌더링하지 않음
  if (!isOpen) return null;

  return (
        <div className={styles["modal-overlay"]} onClick={close}>
        <div className={styles["modal-content"]} onClick={(e) => e.stopPropagation()}>
        <span className="close" onClick={close}>&times;</span>
        <h2>로그인</h2>
        <input
          type="text"
          name="login_id"
          placeholder="아이디"
          value={loginData.login_id}
          onChange={handleInputChange}
          className="input-field"
        />
        <input
          type="password"
          name="password"
          placeholder="비밀번호"
          value={loginData.password}
          onChange={handleInputChange}
          className="input-field"
        />
        <button onClick={handleLogin} className="login-button">로그인</button>
      </div>
    </div>
  );
};

export default SignInModal;
