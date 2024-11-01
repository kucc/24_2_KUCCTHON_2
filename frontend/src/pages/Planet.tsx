import React, {useState} from "react";
import ReactDOM from "react-dom/client";
import styles from "./Planet.module.css";
import planet from '../img/Planet.svg'
import VisitorBookModal from "../components/VisitorBookModal";
import Button from "../components/Button";
import PickupModal from "../components/PickupModal";
import { useParams,useNavigate } from 'react-router-dom';
import Blackhole from '../components/Blackhole';


interface PlanetProps {
  userId: number;
  setUserId: (id: number) => void;
}

const Planet: React.FC<PlanetProps> = ({userId, setUserId}) => {

  const [isVisitor, setIsVisitor] = useState(false)
  const [isPickUp, setIsPickup] = useState(false)
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

  const giveBanana= () => {
  }

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
          <Button text={`바나나 창고 ${count}`} onClick={dkarjteh} />
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
          <Button text="바나나 주기" onClick={giveBanana} />
          <Button text={`바나나 창고 ${count}`} onClick={dkarjteh} />
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
