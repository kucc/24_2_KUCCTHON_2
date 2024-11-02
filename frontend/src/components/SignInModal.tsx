import React, { useState, ChangeEvent } from 'react';
import styles from './SignInModal.module.css';
import { useNavigate } from 'react-router-dom';


interface SignInModalProps {
  isOpen: boolean;
  close: () => void;
  userId: number;
  setUserId: (id: number) => void;
}

  const SignInModal: React.FC<SignInModalProps> = ({ isOpen, close, userId, setUserId }) => {
  const [loginData, setLoginData] = useState({
    login_id: '',
    password: ''
  });

  const navigate = useNavigate();

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setLoginData({
      ...loginData,
      [name]: value
    });
  };

  const handleLogin = () => {
    fetch("http://127.0.0.1:8000/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(loginData),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error('Network response was not ok'); // 응답 오류 처리
        }
        return res.json(); // JSON 응답 반환
      })
      .then((data) => {
        console.log(data); // 로그인 응답 데이터 로깅
        close(); // 로그인 성공 후 모달 닫기
        navigate("/gateway");
        setUserId(data.user.id); // 사용자 ID 설정
        localStorage.setItem("accessToken", data.token.access_token); // 토큰을 로컬 스토리지에 저장
      })
      .catch((error) => {
        console.error("Login error:", error);
      });
  };
  

  // 모달이 열려 있지 않으면 렌더링하지 않음
  if (!isOpen) return null;

  return (
        <div className={styles.modal_overlay} onClick={close}>
        <div className={styles.modal_content} onClick={(e) => e.stopPropagation()}>
        <span className={styles.close} onClick={close}>&times;</span>
        <h2>로그인</h2>
        <input
          type="text"
          name="login_id"
          placeholder="아이디"
          value={loginData.login_id}
          onChange={handleInputChange}
          className={styles.input_field}
        />
        <input
          type="password"
          name="password"
          placeholder="비밀번호"
          value={loginData.password}
          onChange={handleInputChange}
          className={styles.input_field}
        />
        <button onClick={handleLogin} className={styles.login_button}>로그인</button>
      </div>
    </div>
  );
};

export default SignInModal;
