import React, {useEffect, useState} from "react";
import ReactDOM from "react-dom/client";
import styles from "./Planet.module.css";
import planet from '../img/Planet.svg'
import VisitorBookModal from "../components/VisitorBookModal";
import Button from "../components/Button";
import PickupModal from "../components/PickupModal";
import { useParams,useNavigate } from 'react-router-dom';
import Blackhole from '../components/Blackhole';
import head_tree from '../img/head_tree.svg'
import head_angel from '../img/head_angel.svg'
import eye_sunglass from '../img/eye_sunglass.svg'
import eye_shiny from '../img/eye_shiny.svg'
import pet_puppy from '../img/pet_puppy.svg'
import pet_cat from '../img/pet_cat.svg'


interface PlanetProps {
  userId: number;
  setUserId: (id: number) => void;
}

interface PlanetInfo {
  planet_name: string
  user_id: number
  user_name: string
  head: number
  pet: number
  eye: number
  tool: number
  like_count: number
}

const updateLike = async (userId: number, planetId: number) => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/like/${planetId}?user_id=${userId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`Error liking planet: ${response.status} - ${errorData.detail || 'No additional message'}`);
    }

    const data = await response.json();
    console.log("Like updated data:", data); // 업데이트된 데이터 확인
    return data;
  } catch (error) {
    console.error("Error:", error);
    throw error; // 에러를 다시 던져서 호출자에서 처리할 수 있도록 함
  }
};

const fetchPlanet = async (user_id: number): Promise<PlanetInfo> => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/planet/${user_id}`, {
      method: "GET",
    });

    if (!response.ok) {
      throw new Error(`Error fetching planet data: ${response.status}`);
    }

    const data = await response.json();
    console.log(data); // 데이터 확인
    return data;
  } catch (error) {
    console.error("Error:", error);
    throw error; // 오류 발생 시 에러 다시 던지기
  }
};



const Planet: React.FC<PlanetProps> = ({userId, setUserId}) => {
  const [planets, setPlanets] = useState<PlanetInfo | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [isVisitor, setIsVisitor] = useState(false)
  const [isPickUp, setIsPickup] = useState(false)
  const [isModalOpen, setIsModalOpen] = useState(false);
  const navigate = useNavigate();

  const { planetUserId } = useParams(); // URL에서 planetUserId 가져오기

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
  const isMine = userId === Number(planetUserId);
  console.log(isMine)

  const giveBanana= async () => {
    if (!planets) return; // items가 null인 경우 처리

    try {
      await updateLike(userId, planets.user_id); // userId와 items.id를 사용하여 좋아요 요청
      // 필요시 추가적인 상태 업데이트나 로직 실행
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message); // 오류 메시지 설정
      } else {
        setError("An unknown error occurred");
      }
    }
  }
  
  useEffect(() => {
    const getPlanets = async () => {
      try {
        const data = await fetchPlanet(Number(planetUserId));
        setPlanets(data); // planets state에 data 할당
        console.log(data);
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

  // const inMine = () => {
  //   if (userId === planetId) {
  //     return true
  //   }
  // }
  

  const handleBlackholeClick = () => {
    navigate("/gateway"); // Blackhole 클릭 시 'gateway'로 이동
  };

  return (
    <div className={styles.background}>
      <div className={isMine? styles.myPlanetPageContainer: styles.hidden}>
        <div className={styles.topBtn}>
          <Button text="방명록" onClick={handleVisitor} />
          <Button text="뽑기" onClick={handlePickup} />
          <Button text={`바나나 창고 ${planets?.like_count}`} onClick={dkarjteh} />
        </div>
        <div className={styles.planetContainer}>
          <div className={styles.planetPlane} >
          <img src={planet} alt='이미지' />
          </div>
          <div className={styles.planetItem}>
            <div className={planets?.head === 1 || planets?.head === 2 ? styles.head : styles.hidden}>
              {planets?.head === 1 && <img src={head_tree} alt="Head Type 1" />}
              {planets?.head === 2 && <img src={head_angel} alt="Head Type 2" />}
            </div>
            <div className={planets?.eye === 3 || planets?.eye === 4 ? styles.eye : styles.hidden}>
              {planets?.eye === 3 && <img src={eye_sunglass} alt="Head Type 1" />}
              {planets?.eye === 4 && <img src={eye_shiny} alt="Head Type 2" />}
            </div>
            <div className={planets?.pet === 5 || planets?.pet === 6 ? styles.pet : styles.hidden}>
              {planets?.pet === 5 && <img src={pet_puppy} alt="Head Type 1" />}
              {planets?.pet === 6 && <img src={pet_cat} alt="Head Type 2" />}
            </div>
          </div>
        </div> 
      </div>
      <div className={isMine? styles.hidden : styles.otherPlanetPageContainer}>
        <div className={styles.topBtn}>
          <Button text="방명록" onClick={handleVisitor} />
          <Button text="바나나 주기" onClick={giveBanana} />
          <Button text={`바나나 창고 ${planets?.like_count}`} onClick={dkarjteh} />
        </div>
        <div className={styles.planetContainer}>
          <div className={styles.planetPlane} >
          <img src={planet} alt='이미지' />
          </div>
          <div className={styles.planetItem}>
            <div className={planets?.head === 1 || planets?.head === 2 ? styles.head : styles.hidden}>
              {planets?.head === 1 && <img src={head_tree} alt="Head Type 1" />}
              {planets?.head === 2 && <img src={head_angel} alt="Head Type 2" />}
            </div>
            <div className={planets?.eye === 3 || planets?.eye === 4 ? styles.eye : styles.hidden}>
              {planets?.eye === 3 && <img src={eye_sunglass} alt="Head Type 1" />}
              {planets?.eye === 4 && <img src={eye_shiny} alt="Head Type 2" />}
            </div>
            <div className={planets?.pet === 5 || planets?.pet === 6 ? styles.pet : styles.hidden}>
              {planets?.pet === 5 && <img src={pet_puppy} alt="Head Type 1" />}
              {planets?.pet === 6 && <img src={pet_cat} alt="Head Type 2" />}
            </div>
          </div>
        </div> 
      </div>
      <div className={isVisitor? styles.visitorModal : styles.hidden}>
          <button onClick={handleVisitor} >X</button>
          <VisitorBookModal userId={userId} setUserId={setUserId} otherId={Number(planetUserId)}/>
      </div>
      <div className={isPickUp? styles.pickupModal: styles.hidden}>
          <button onClick={handlePickup} >X</button>

          <PickupModal 
            userId={userId} 
            setUserId={setUserId} 
            closeModal={() => setIsPickup(false)} // 모달 닫기 함수 전달
          />
      </div>
      <div className={styles.BlackholeContainer} onClick={handleBlackholeClick}>
        <Blackhole/>

      </div>
    </div>
  );
};

export default Planet;
