import React, { useState } from 'react';
import ReactDOM from "react-dom/client";
import styles from "./Home.module.css";
import Button from "../components/Button";
import SignInModal from "../components/SignInModal";
import SignUpModal from '../components/SignUpModal'; 
import homeLogo from "../img/homeLogo.svg";

interface Planet {
  planet_name: string
  user_id: number
  user_name: string
  head: number
  pet: number
  eye: number
  tool: number
  like_count: number
}

interface PlanetResponse {
  success: boolean
  message: string
  data: Planet[]
}

// useQuery 훅을 사용하여 내가 쓴 질문 데이터 가져오기
function usePlanet() {
  return useQuery<PlanetResponse, Error>(
    ['myQuestions', arrange],
    async () => {
      const res = await axios.get(`${process.env.REACT_APP_HOST}/user/mypage/questionhistory/${arrange}`, {
        withCredentials: true,
      })
      return res.data
    },
    {
      retry: false,
      onError: (error) => {
        console.error('내가 쓴 질문 가져오기 에러:', error)
      },
    },
  )
}

const Channel: React.FC = () => {
  const { isLoading: isLoadingPlanet, error: planetError, data: planetData } = usePlanet()
  const [isVisitor, setIsVisitor] = useState(false)
  const [isPickUp, setIsPickup] = useState(false)

  const handleVisitor = () => {
    setIsVisitor(!isVisitor)
  }

  const handlePickup = () => {
    setIsPickup(!isPickUp)
  }

  const dkarjteh = () => {
    console.log('바나나 거지 ㅋㅋ')
  }

  const count = 8
  const isMine = true

  const giveBanana= () => {

  }

  // const inMine = () => {
  //   if (userId === planetId) {
  //     return true
  //   }
  // }

  return (
    <div className={styles.background}>
      <div className={styles.planetList}>
        
      </div>

      <div className={styles.LoginContainer}>
      
      </div>
         
    </div>
  );
};

export default Channel;
function useQuery<T, U>(arg0: any[], arg1: () => Promise<any>, arg2: { retry: boolean; onError: (error: any) => void; }) {
  throw new Error('Function not implemented.');
}

