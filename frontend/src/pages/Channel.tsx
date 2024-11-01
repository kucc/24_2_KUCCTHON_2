import React, { useEffect, useState } from 'react';
import ReactDOM from "react-dom/client";
import styles from "./Channel.module.css";
import banana from '../img/banana.svg'
import planetImg from '../img/Planet.svg';
import { useNavigate } from 'react-router-dom';
import Planet from './Planet';

interface ChannelProps {
  userId: number;
  setUserId: (id: number) => void;
}
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
  data: Planet[];
  count: number;
}

const fetchPlanet = async (): Promise<PlanetResponse> => {
  const response = await fetch("http://127.0.0.1:8000/planet", {
    method: "GET",
  });

  if (!response.ok) {
    throw new Error("Network response was not ok " + response.statusText);
  }

  const data = await response.json();
  return data;
}

const Channel: React.FC<ChannelProps> = ({userId, setUserId}) => {
  const [planets, setPlanets] = useState<Planet[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const navigate = useNavigate();

  const handlePlanetClick = (planetUserId: number) => {
    console.log(planetUserId);
    <Planet userId={userId} setUserId={setUserId}/>
    navigate(`/planet/${planetUserId}`); // planetUserId를 URL 경로에 추가
  };
  
  useEffect(() => {
    const getPlanets = async () => {
      try {
        const data = await fetchPlanet();
        setPlanets(data.data); // planets state에 data 할당
      } catch (err) {
        // err를 Error 타입으로 단언
        if (err instanceof Error) {
          setError(err.message); // 오류 메시지 설정
        } else {
          setError("An unknown error occurred");
        }
      } finally {
        setLoading(false); // 로딩 상태 해제
      }
    };

    getPlanets();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className={styles.background}>
      <div className={styles.list}>
        {planets.map((planet) => (
          <div className={styles.planet} key={planet.user_id}>
            <div className={styles.planetText}>{planet.user_name}의 행성</div>
            <div
              className={styles.planetText}
              onClick={() => handlePlanetClick(planet.user_id)} // 클릭 시 이동
              style={{ cursor: 'pointer' }} // 커서 포인터로 변경
            >
              <img src={planetImg} className={styles.img} alt={planet.planet_name} />
              {planet.planet_name}
            </div>
            <div className={styles.planetText}>
              <img src={banana} className={styles.img} alt="likes" />
              {planet.like_count}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Channel;
