import React, { useState } from 'react';
import paper from '../img/paper.svg';
import Button from "../components/Button";
import styles from "./PickupModal.module.css";
import axios from "axios";

interface ItemResponse {
    id: number;
    place: string;
    name: string;
}

interface PickupProps {
    userId: number;
    setUserId: (id: number) => void;
  }

const fetchPlanet = async (user_id:number): Promise<ItemResponse> => {
  const response = await fetch("http://127.0.0.1:8000/item/random_item/${user_id}", {
    method: "GET",
  });

  if (!response.ok) {
    throw new Error("Network response was not ok " + response.statusText);
  }

  const data = await response.json();
  return data;
}

const PickupModal: React.FC<PickupProps> = ({userId,setUserId}) => {

    const [items, setItems] = useState<ItemResponse | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(false); // 초기 로딩 상태를 false로 설정

    const getRandomItem = async () => {
      setLoading(true); // 새로운 요청 시 로딩 상태 활성화
      try {
        const data = await fetchPlanet(userId);
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

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
      <div className={styles.pickUpContainer}>
        <div className={styles.paper}>
          <img src={paper} alt='이미지' />
        </div>
        <div>
          {items && (
            <div>
              <p>아이템 이름: {items.name}</p>
              <p>아이템 위치: {items.place}</p>
            </div>
          )}
        </div>
        <div className={styles.Btn}>
            <Button text='바나나 사용하기' onClick={getRandomItem} />
        </div>
      </div>
    );
};

export default PickupModal;
