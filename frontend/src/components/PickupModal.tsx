import React, { useEffect, useState } from 'react';
import paper from '../img/paper.svg';
import Button from "../components/Button";
import styles from "./PickupModal.module.css";
import axios from "axios";
import head_tree from '../img/head_tree.svg'
import head_angel from '../img/head_angel.svg'
import eye_sunglass from '../img/eye_sunglass.svg'
import eye_shiny from '../img/eye_shiny.svg'
import pet_puppy from '../img/pet_puppy.svg'
import pet_cat from '../img/pet_cat.svg'

interface ItemResponse {
    id: number;
    place: string;
    name: string;
}

interface PickupProps {
    userId: number;
    setUserId: (id: number) => void;
  }

  const fetchRandomItem = async (user_id: number) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/item/random_item?user_id=${user_id}`, {
        method: "GET",
      });
  
      if (!response.ok) {
        throw new Error(`Error fetching random item: ${response.status}`);
      }
  
      const data = await response.json();
      console.log("Random item data:", data); // 데이터 확인
      return data;
    } catch (error) {
      console.error("Error:", error);
      throw error; // 에러를 다시 던져서 호출자에서 처리할 수 있도록 함
    }
  };
  
  const PickupModal: React.FC<PickupProps> = ({ userId, setUserId }) => {
    const [items, setItems] = useState<ItemResponse | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(false); // 초기 로딩 상태를 false로 설정
  
    const getRandomItem = async () => {
      setLoading(true); // 새로운 요청 시 로딩 상태 활성화
      try {
        const data = await fetchRandomItem(userId); // userId를 전달하여 랜덤 아이템 가져오기
        setItems(data); // items state에 data 할당
        setError(null); // 이전 오류 상태 초기화
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message); // 오류 메시지 설정
        } else {
          setError("An unknown error occurred");
        }
      } finally {
        setLoading(false); // 로딩 상태 해제
      }
    };
  
    // 컴포넌트가 처음 마운트될 때 랜덤 아이템을 가져옵니다.
    useEffect(() => {
      getRandomItem();
    }, []); // userId가 변경될 때마다 호출
  
    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;
  
    return (
      <div className={styles.pickUpContainer}>
        <div className={styles.paper}>
          <img src={paper} alt="이미지" />
        </div>
        <div>
          <div className={items?.id === 1 || items?.id === 2 ? styles.item : styles.hidden}>
            {items?.id === 1 && <img src={head_tree} alt="Head Type 1" />}
            {items?.id === 2 && <img src={head_angel} alt="Head Type 2" />}
          </div>
          <div className={items?.id === 3 || items?.id === 4 ? styles.item : styles.hidden}>
            {items?.id === 3 && <img src={eye_sunglass} alt="Eye Type 1" />}
            {items?.id === 4 && <img src={eye_shiny} alt="Eye Type 2" />}
          </div>
          <div className={items?.id === 5 || items?.id === 6 ? styles.item : styles.hidden}>
            {items?.id === 5 && <img src={pet_puppy} alt="Pet Type 1" />}
            {items?.id === 6 && <img src={pet_cat} alt="Pet Type 2" />}
          </div>
        </div>
        <div className={styles.Btn}>
          <Button text="바나나 사용하기" onClick={getRandomItem} /> {/* 버튼 클릭 시 랜덤 아이템 가져오기 */}
        </div>
      </div>
    );
  };

export default PickupModal;
