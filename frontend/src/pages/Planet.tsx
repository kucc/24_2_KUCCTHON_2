import React, {useState, useEffect} from "react";
import styles from "./Planet.module.css";
import planet from '../img/Planet.svg'
import VisitorBookModal from "../components/VisitorBookModal";
import Button from "../components/Button";
import PickupModal from "../components/PickupModal";
import { useParams,useNavigate } from 'react-router-dom';
import Blackhole from '../components/Blackhole';

interface PlanetData {
  planet_name: string;
  user_id: number;
  user_name: string;
  head: number;
  pet: number;
  eye: number;
  tool: number;
  like_count: number;
}

interface PlanetProps {
  userId: number;
  setUserId: (id: number) => void;
}

const Planet: React.FC<PlanetProps> = ({userId, setUserId}) => {
  const [isVisitor, setIsVisitor] = useState(false);
  const [isPickUp, setIsPickup] = useState(false);
  const [planetData, setPlanetData] = useState<PlanetData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const navigate = useNavigate();
  const { planetUserId } = useParams<{ planetUserId: string }>(); // URL에서 planetUserId 가져오기
  const [likeResponse, setLikeResponse] = useState(null);
 
  const fetchPlanetData = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/planet/${planetUserId}`, {
        method: "GET",
      });

      if (!response.ok) {
        throw new Error("Network response was not ok " + response.statusText);
      }

      const data: PlanetData = await response.json();
      setPlanetData(data);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unknown error occurred");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPlanetData();
  }, [planetUserId]);

  const handleVisitor = () => {
    setIsVisitor(!isVisitor)
  }

  const handlePickup = () => {
    setIsPickup(!isPickUp)
  }

  const count = planetData ? planetData.like_count : 0;
  const isMine = userId === Number(planetUserId);


  const handleGiveBanana = async () => {
    if (!planetUserId || !userId) return;

    try {
      const response = await fetch(`http://127.0.0.1:8000/like/${planetUserId}?user_id=${userId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
      if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
      }
  
      const data = await response.json();
      setLikeResponse(data); // 성공 응답을 상태에 저장
      console.log("Like success:", data);
    } catch (error) {
      console.error("Error giving banana:", error);
    }
  };
  
  const handleBlackholeClick = () => {
    navigate("/gateway"); // Blackhole 클릭 시 'gateway'로 이동
  };

  return (
    <div className={styles.background}>
      <div className={isMine? styles.myPlanetPageContainer: styles.hidden}>
        <div className={styles.topBtn}>
          <Button text="방명록" onClick={handleVisitor} />
          <Button text="뽑기" onClick={handlePickup} />
          <Button text={`바나나 창고 ${count}`} />
        </div>
        <div className={styles.planetContainer}>
          <div className={styles.planetPlane} >
          <img src={planet} alt='이미지' />
          </div>
          <div className={styles.planetItem}>
            

          </div>
        </div> 
      </div>
      <div className={isMine? styles.hidden : styles.otherPlanetPageContainer}>
        <div className={styles.topBtn}>
          <Button text="방명록" onClick={handleVisitor} />
          <Button text="바나나 주기" onClick={handleGiveBanana} />
          <Button text={`바나나 창고 ${count}`}  />
        </div>
        <div className={styles.planetContainer}>
          <div className={styles.planetPlane} >
          <img src={planet} alt='이미지' />
          </div>
        </div> 
      </div>
      <div className={isVisitor? styles.visitorModal : styles.hidden}>
          <button onClick={handleVisitor} >X</button>
          <VisitorBookModal/>
      </div>
      <div className={isPickUp? styles.pickupModal: styles.hidden}>
          <button onClick={handlePickup} >X</button>
          <PickupModal/>
      </div>
      <div className={styles.BlackholeContainer} onClick={handleBlackholeClick}>
        <Blackhole/>
      </div>
    </div>
  );
};

export default Planet;
